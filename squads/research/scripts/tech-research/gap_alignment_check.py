#!/usr/bin/env python3
"""Gap Alignment Check — validates that Wave 2+ sub-queries target open gaps.

Story: STORY-RA-B.2 | Created: 2026-05-19
Phase: post-Wave-2 finalize — runs after gap_detector.py, before next wave or close.

PURPOSE:
  Measures alignment_ratio = sub_queries_that_target_gap / total_sub_queries.
  Wave 2+ sub-queries MUST carry metadata `targets_gaps: [G001, G003, ...]`.
  Ratio >= 0.60 → PASS. Ratio < 0.60 → FAIL (warning, not veto — first iteration heuristic).

SEMANTICS:
  - READ-ONLY from gaps.yaml (RA-B.1 artifact). Never mutates it.
  - READ from sub-queries metadata (inline JSON/YAML or file).
  - Emits JSON result to stdout (consumed by orchestrator).
  - Exit 0 = check ran (PASS or FAIL — caller decides on FAIL action).
  - Exit 1 = errors (missing required args, parse failure, gaps.yaml corrupt).
  - Exit 2 = no sub-queries provided (nothing to check).

PRODUCT-DISCOVERY MODE:
  Same algorithm — only the sub-query decomposition framing changes (JTBD/Villain/WTP
  instead of scope angles). The alignment mechanism and threshold are universal.

Usage:
    python gap_alignment_check.py \\
        --output-dir /path/to/docs/research/{slug}/ \\
        --wave 2 \\
        --sub-queries '[{"id":"sq1","query":"...","targets_gaps":["G001"]}]'

    python gap_alignment_check.py \\
        --output-dir /path/to/docs/research/{slug}/ \\
        --wave 2 \\
        --sub-queries-file /path/to/sub-queries-wave2.json

    python gap_alignment_check.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import re
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ─── Constants ────────────────────────────────────────────────────────────────

ALIGNMENT_THRESHOLD = 0.60
GAPS_FILENAME = "gaps.yaml"
SCHEMA_VERSION = "1.0"

# ID format: G + 3-digit zero-padded int (G001 … G999)
_GAP_ID_PATTERN = re.compile(r"^G(\d{3})$")


# ─── YAML/JSON I/O ────────────────────────────────────────────────────────────


def _load_yaml(path: str) -> dict:
    """Load a YAML file. Returns empty dict on absence or parse failure."""
    if not os.path.exists(path):
        return {}
    if not HAS_YAML:
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _load_gaps(output_dir: str) -> tuple[list[dict], list[str]]:
    """Load gaps.yaml from output_dir.

    Returns (gaps_list, errors).
    errors is non-empty on parse failure or schema violation.
    """
    errors: list[str] = []
    gaps_path = os.path.join(output_dir, GAPS_FILENAME)

    if not os.path.exists(gaps_path):
        errors.append(
            f"gaps.yaml not found at {gaps_path}. "
            "Run gap_detector.py (RA-B.1) before gap_alignment_check.py."
        )
        return [], errors

    if not HAS_YAML:
        errors.append(
            "PyYAML is required to load gaps.yaml. "
            "Install with: pip install pyyaml"
        )
        return [], errors

    try:
        with open(gaps_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception as exc:
        errors.append(f"gaps.yaml parse error: {exc}")
        return [], errors

    if not isinstance(data, dict):
        errors.append("gaps.yaml is not a YAML mapping.")
        return [], errors

    gaps = data.get("gaps", [])
    if not isinstance(gaps, list):
        errors.append("gaps.yaml: 'gaps' field is not a list.")
        return [], errors

    return gaps, errors


def _parse_sub_queries(raw: str) -> tuple[list[dict], list[str]]:
    """Parse sub-queries from a JSON string.

    Returns (sub_queries, errors).
    Accepts:
      - JSON array: [{"id":"sq1","query":"...","targets_gaps":["G001"]}, ...]
      - JSON object: {"sub_queries": [...]}
    """
    errors: list[str] = []
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"sub-queries JSON parse error: {exc}")
        return [], errors

    if isinstance(parsed, list):
        return parsed, errors
    if isinstance(parsed, dict):
        sq = parsed.get("sub_queries") or parsed.get("subqueries") or parsed.get("queries")
        if isinstance(sq, list):
            return sq, errors
        errors.append(
            "sub-queries JSON object must contain 'sub_queries', 'subqueries', or 'queries' array key."
        )
        return [], errors

    errors.append(
        "sub-queries must be a JSON array or an object with a 'sub_queries' key."
    )
    return [], errors


# ─── Alignment Logic ─────────────────────────────────────────────────────────


def _extract_gap_ids(sub_query: dict) -> list[str]:
    """Extract valid gap IDs from a sub-query dict.

    Accepts:
      - targets_gaps: ["G001", "G002"]  (canonical field — AC-1 / AC-2)
      - gap_ids: ["G001"]               (alias)
    """
    candidates: list[str] = []

    for field in ("targets_gaps", "gap_ids"):
        val = sub_query.get(field)
        if val is None:
            continue
        if isinstance(val, list):
            candidates = [str(v) for v in val]
            break
        if isinstance(val, str) and val.strip():
            candidates = [v.strip() for v in val.split(",") if v.strip()]
            break

    # Filter: only accept canonical G{NNN} IDs
    valid = [gid for gid in candidates if _GAP_ID_PATTERN.match(gid)]
    return valid


def compute_alignment(
    sub_queries: list[dict],
    open_gap_ids: set[str],
    wave_num: int,
) -> dict:
    """Compute alignment_ratio and classify each sub-query.

    Rules (STORY-RA-B.2 D2):
    - Wave 1: targets_gaps is optional (no gaps exist yet). All queries auto-exempt.
    - Wave 2+: targets_gaps is EXPECTED. Queries without it are counted as unaligned.

    Args:
        sub_queries: list of sub-query dicts with optional targets_gaps field.
        open_gap_ids: set of currently open gap IDs from gaps.yaml.
        wave_num: current wave number (1-based).

    Returns:
        dict with alignment_ratio, threshold, status, breakdown.
    """
    total = len(sub_queries)

    if total == 0:
        return {
            "alignment_ratio": 0.0,
            "threshold": ALIGNMENT_THRESHOLD,
            "status": "SKIP",
            "note": "No sub-queries provided — nothing to check.",
            "total_sub_queries": 0,
            "aligned_count": 0,
            "unaligned_count": 0,
            "unaligned_queries": [],
            "wave": wave_num,
        }

    # Wave 1: gap-driven decompose not required (no gaps exist yet)
    if wave_num <= 1:
        return {
            "alignment_ratio": 1.0,
            "threshold": ALIGNMENT_THRESHOLD,
            "status": "EXEMPT",
            "note": "Wave 1: targets_gaps not required (gaps.yaml populated by P3.4 after Wave 1).",
            "total_sub_queries": total,
            "aligned_count": total,
            "unaligned_count": 0,
            "unaligned_queries": [],
            "wave": wave_num,
        }

    # Wave 2+: check alignment
    aligned: list[dict] = []
    unaligned: list[dict] = []

    for sq in sub_queries:
        sq_id = sq.get("id") or sq.get("query", "")[:60]
        gap_ids = _extract_gap_ids(sq)

        # A sub-query is aligned if it references at least one OPEN gap
        # (open_gap_ids may be empty if all gaps closed — query still counts if it references any valid G-ID)
        has_valid_gap_ref = bool(gap_ids)
        # Bonus: if we have open gaps, check the referenced IDs are in the open set
        # If open_gap_ids is empty (all closed), any gap reference is acceptable
        if has_valid_gap_ref and open_gap_ids:
            hit = any(gid in open_gap_ids for gid in gap_ids)
            has_valid_gap_ref = hit

        if has_valid_gap_ref:
            aligned.append({"id": sq_id, "targets_gaps": gap_ids})
        else:
            unaligned.append({
                "id": sq_id,
                "targets_gaps_declared": gap_ids,
                "reason": "no_gap_ref" if not gap_ids else "no_open_gap_match",
            })

    aligned_count = len(aligned)
    alignment_ratio = aligned_count / total if total > 0 else 0.0
    passed = alignment_ratio >= ALIGNMENT_THRESHOLD

    return {
        "alignment_ratio": round(alignment_ratio, 4),
        "threshold": ALIGNMENT_THRESHOLD,
        "status": "PASS" if passed else "FAIL",
        "total_sub_queries": total,
        "aligned_count": aligned_count,
        "unaligned_count": len(unaligned),
        "unaligned_queries": unaligned,
        "wave": wave_num,
    }


# ─── Main Check Entry Point ───────────────────────────────────────────────────


def run_alignment_check(
    output_dir: str,
    wave_num: int,
    sub_queries: list[dict],
    mode: str = "research",
) -> dict:
    """Main entry point for gap alignment check (AC-2).

    Args:
        output_dir: path to docs/research/{date}-{slug}/ runtime output directory.
        wave_num: current wave number (1-based).
        sub_queries: list of sub-query dicts (with optional targets_gaps field).
        mode: "research" or "product_discovery" — universal threshold (AC-5).

    Returns:
        dict with:
          alignment_ratio (float), threshold (float), status (PASS|FAIL|EXEMPT|SKIP),
          total_sub_queries (int), aligned_count (int), unaligned_count (int),
          unaligned_queries (list), wave (int), open_gaps_count (int),
          warnings (list[str]), errors (list[str])
    """
    result: dict = {
        "schema_version": SCHEMA_VERSION,
        "story_ref": "STORY-RA-B.2",
        "mode": mode,
        "wave": wave_num,
        "alignment_ratio": 0.0,
        "threshold": ALIGNMENT_THRESHOLD,
        "status": "FAIL",
        "total_sub_queries": 0,
        "aligned_count": 0,
        "unaligned_count": 0,
        "unaligned_queries": [],
        "open_gaps_count": 0,
        "warnings": [],
        "errors": [],
    }

    # Load gaps (read-only from RA-B.1 artifact)
    gaps, load_errors = _load_gaps(output_dir)
    if load_errors:
        result["errors"].extend(load_errors)
        return result

    # Extract open gap IDs
    open_gap_ids = {
        str(g.get("id", ""))
        for g in gaps
        if isinstance(g, dict) and g.get("status") == "open"
    }
    result["open_gaps_count"] = len(open_gap_ids)

    # Product-discovery mode: same algorithm, JTBD/WTP decomposition handled upstream
    # The alignment check is universal per AC-5 / D3
    if mode == "product_discovery":
        result["warnings"].append(
            "product_discovery mode: decompose targets JTBD/Villain/WTP instead of scope angles. "
            "alignment_ratio threshold is identical (0.60)."
        )

    # Compute alignment
    check = compute_alignment(sub_queries, open_gap_ids, wave_num)
    result.update(check)

    # Emit advisory warning on FAIL (not veto — D1: first-iteration heuristic)
    if result["status"] == "FAIL":
        result["warnings"].append(
            f"alignment_ratio={result['alignment_ratio']:.2%} < threshold={ALIGNMENT_THRESHOLD:.0%}. "
            "Wave 2+ sub-queries should target open gaps (targets_gaps metadata). "
            "WARNING — not a veto in first iteration. Threshold may become BLOCKING after 10 runs."
        )

    return result


# ─── Self-Test ────────────────────────────────────────────────────────────────


def run_self_test() -> int:
    """Self-test: verify alignment_ratio logic and PASS/FAIL/EXEMPT semantics.

    Test cases:
      T1: Wave 1 → EXEMPT (targets_gaps optional)
      T2: Wave 2, 4/5 queries aligned → PASS (ratio 0.80 >= 0.60)
      T3: Wave 2, 2/5 queries aligned → FAIL (ratio 0.40 < 0.60)
      T4: Wave 2, exactly 3/5 aligned → PASS (ratio 0.60 == threshold)
      T5: Wave 2, 0 sub-queries → SKIP
      T6: product-discovery mode, same threshold
    """
    import tempfile
    import shutil

    print("[self-test] Starting gap_alignment_check self-test...")
    tmpdir = tempfile.mkdtemp(prefix="gap_alignment_test_")
    exit_code = 0

    try:
        # Write a minimal gaps.yaml with 3 open gaps
        gaps_content = (
            "schema_version: '1.0'\n"
            "story_ref: STORY-RA-B.1\n"
            "pipeline_id: test\n"
            "slug: test\n"
            "generated_at: '2026-05-19T00:00:00Z'\n"
            "wave_last_updated: 1\n"
            "summary:\n"
            "  total: 3\n"
            "  open: 3\n"
            "  closed: 0\n"
            "  abandoned: 0\n"
            "  gap_convergence: false\n"
            "gaps:\n"
            "  - id: G001\n"
            "    question: 'What is the performance of pgvector?'\n"
            "    source_hint: academic-paper\n"
            "    priority: high\n"
            "    attempts: 0\n"
            "    status: open\n"
            "    opened_in_wave: 1\n"
            "    closed_in_wave: null\n"
            "    closed_by_source: null\n"
            "  - id: G002\n"
            "    question: 'What are enterprise adoption patterns?'\n"
            "    source_hint: enterprise-postmortem\n"
            "    priority: medium\n"
            "    attempts: 0\n"
            "    status: open\n"
            "    opened_in_wave: 1\n"
            "    closed_in_wave: null\n"
            "    closed_by_source: null\n"
            "  - id: G003\n"
            "    question: 'What is the cost model for cloud vector DBs?'\n"
            "    source_hint: general-web\n"
            "    priority: low\n"
            "    attempts: 0\n"
            "    status: open\n"
            "    opened_in_wave: 1\n"
            "    closed_in_wave: null\n"
            "    closed_by_source: null\n"
        )
        gaps_path = os.path.join(tmpdir, "gaps.yaml")
        with open(gaps_path, "w", encoding="utf-8") as fh:
            fh.write(gaps_content)

        # T1: Wave 1 → EXEMPT
        r = run_alignment_check(tmpdir, wave_num=1, sub_queries=[
            {"id": "sq1", "query": "how does pgvector work"},
            {"id": "sq2", "query": "vector DB comparison"},
        ])
        assert r["status"] == "EXEMPT", f"T1 FAIL: expected EXEMPT, got {r['status']}"
        print(f"[self-test] T1 PASS: Wave 1 → EXEMPT ({r['alignment_ratio']})")

        # T2: Wave 2, 4/5 aligned → PASS (ratio 0.80)
        sqs_4of5 = [
            {"id": "sq1", "query": "pgvector performance", "targets_gaps": ["G001"]},
            {"id": "sq2", "query": "enterprise vector db", "targets_gaps": ["G002"]},
            {"id": "sq3", "query": "cost model cloud", "targets_gaps": ["G003"]},
            {"id": "sq4", "query": "latency benchmarks", "targets_gaps": ["G001", "G003"]},
            {"id": "sq5", "query": "unrelated topic"},  # no gap ref
        ]
        r = run_alignment_check(tmpdir, wave_num=2, sub_queries=sqs_4of5)
        assert r["status"] == "PASS", f"T2 FAIL: expected PASS, got {r['status']} ({r['alignment_ratio']})"
        assert r["aligned_count"] == 4, f"T2 FAIL: aligned_count={r['aligned_count']}"
        assert r["unaligned_count"] == 1, f"T2 FAIL: unaligned_count={r['unaligned_count']}"
        print(f"[self-test] T2 PASS: 4/5 → ratio={r['alignment_ratio']:.2%} → PASS")

        # T3: Wave 2, 2/5 aligned → FAIL (ratio 0.40)
        sqs_2of5 = [
            {"id": "sq1", "query": "pgvector perf", "targets_gaps": ["G001"]},
            {"id": "sq2", "query": "enterprise", "targets_gaps": ["G002"]},
            {"id": "sq3", "query": "unrelated a"},
            {"id": "sq4", "query": "unrelated b"},
            {"id": "sq5", "query": "unrelated c"},
        ]
        r = run_alignment_check(tmpdir, wave_num=2, sub_queries=sqs_2of5)
        assert r["status"] == "FAIL", f"T3 FAIL: expected FAIL, got {r['status']}"
        assert r["aligned_count"] == 2, f"T3 FAIL: aligned_count={r['aligned_count']}"
        assert len(r["warnings"]) > 0, "T3 FAIL: expected FAIL warning"
        print(f"[self-test] T3 PASS: 2/5 → ratio={r['alignment_ratio']:.2%} → FAIL (warning issued)")

        # T4: Wave 2, exactly 3/5 = 0.60 → PASS (threshold is inclusive)
        sqs_3of5 = [
            {"id": "sq1", "query": "pgvector perf", "targets_gaps": ["G001"]},
            {"id": "sq2", "query": "enterprise", "targets_gaps": ["G002"]},
            {"id": "sq3", "query": "cost model", "targets_gaps": ["G003"]},
            {"id": "sq4", "query": "unrelated a"},
            {"id": "sq5", "query": "unrelated b"},
        ]
        r = run_alignment_check(tmpdir, wave_num=2, sub_queries=sqs_3of5)
        assert r["status"] == "PASS", f"T4 FAIL: expected PASS at 3/5=0.60, got {r['status']}"
        print(f"[self-test] T4 PASS: 3/5 = 0.60 exactly → PASS (threshold inclusive)")

        # T5: Wave 2, 0 sub-queries → SKIP
        r = run_alignment_check(tmpdir, wave_num=2, sub_queries=[])
        assert r["status"] == "SKIP", f"T5 FAIL: expected SKIP, got {r['status']}"
        print("[self-test] T5 PASS: 0 sub-queries → SKIP")

        # T6: product-discovery mode, same threshold
        r = run_alignment_check(
            tmpdir, wave_num=2,
            sub_queries=sqs_4of5,
            mode="product_discovery",
        )
        assert r["status"] == "PASS", f"T6 FAIL: expected PASS in product_discovery, got {r['status']}"
        assert r["threshold"] == ALIGNMENT_THRESHOLD, "T6 FAIL: threshold changed in product_discovery"
        print(f"[self-test] T6 PASS: product_discovery → same threshold ({r['threshold']})")

        print("\n[self-test] ALL ASSERTIONS PASSED — gap_alignment_check verified.")

    except AssertionError as exc:
        print(f"\n[self-test] ASSERTION FAILED: {exc}")
        exit_code = 1
    except Exception as exc:
        print(f"\n[self-test] UNEXPECTED ERROR: {exc}")
        exit_code = 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        print("[self-test] Temp dir cleaned up.")

    return exit_code


# ─── CLI Entry Point ──────────────────────────────────────────────────────────


def main() -> int:
    """CLI entry point — invoked from phase finalize or orchestrator."""
    parser = argparse.ArgumentParser(
        description=(
            "Gap Alignment Check — validates Wave 2+ sub-queries target open gaps "
            "(STORY-RA-B.2). Emits JSON to stdout."
        ),
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        help="Path to docs/research/{date}-{slug}/ runtime output directory.",
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=2,
        help="Current wave number (1-based). Default: 2.",
    )
    parser.add_argument(
        "--sub-queries",
        dest="sub_queries_json",
        default=None,
        help="JSON array of sub-query dicts (with optional targets_gaps field).",
    )
    parser.add_argument(
        "--sub-queries-file",
        dest="sub_queries_file",
        default=None,
        help="Path to JSON file with sub-query dicts.",
    )
    parser.add_argument(
        "--mode",
        choices=["research", "product_discovery"],
        default="research",
        help="Pipeline mode. Default: research.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run self-test and exit.",
    )

    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    if not args.output_dir:
        parser.error("--output-dir is required unless --self-test is specified.")

    if not os.path.isdir(args.output_dir):
        print(
            f"ERROR: output directory not found: {args.output_dir}",
            file=sys.stderr,
        )
        return 1

    # Load sub-queries
    sub_queries_raw: Optional[str] = None
    if args.sub_queries_json:
        sub_queries_raw = args.sub_queries_json
    elif args.sub_queries_file:
        if not os.path.exists(args.sub_queries_file):
            print(
                f"ERROR: sub-queries file not found: {args.sub_queries_file}",
                file=sys.stderr,
            )
            return 1
        try:
            with open(args.sub_queries_file, encoding="utf-8") as fh:
                sub_queries_raw = fh.read()
        except OSError as exc:
            print(f"ERROR: cannot read sub-queries file: {exc}", file=sys.stderr)
            return 1

    if sub_queries_raw is None:
        print(
            "ERROR: --sub-queries or --sub-queries-file is required.",
            file=sys.stderr,
        )
        return 2

    sub_queries, parse_errors = _parse_sub_queries(sub_queries_raw)
    if parse_errors:
        for err in parse_errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    if not sub_queries:
        # Empty list provided — exit 2 (no-op)
        result = {
            "status": "SKIP",
            "alignment_ratio": 0.0,
            "threshold": ALIGNMENT_THRESHOLD,
            "total_sub_queries": 0,
            "aligned_count": 0,
            "unaligned_count": 0,
            "unaligned_queries": [],
            "wave": args.wave,
            "warnings": ["No sub-queries provided."],
            "errors": [],
        }
        print(json.dumps(result, indent=2))
        return 2

    result = run_alignment_check(
        output_dir=args.output_dir,
        wave_num=args.wave,
        sub_queries=sub_queries,
        mode=args.mode,
    )

    print(json.dumps(result, indent=2))

    if result.get("errors"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
