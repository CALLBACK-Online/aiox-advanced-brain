#!/usr/bin/env python3
"""Claims confidence aggregator — Story RA-D.2 AC-2.

Reads claims.yaml from a research output directory and emits a
``confidence_distribution`` aggregate block at the top of the file
(Decision D3: top placement for fast scan by Observatory adapter).

Also mirrors the visual summary into ``metrics.yaml`` (Gold Rule 9 — YAML
sidecars are audit artifacts; visible values must live in JSON/MD/metrics).

Usage (standalone smoke test):
    python claims_aggregator.py /path/to/docs/research/{date}-{slug}/

Usage (from Phase 5 Document workflow — step 8.5):
    python3 squads/research/scripts/tech-research/claims_aggregator.py {output_dir}

Exit codes:
    0  — PASS (aggregate written or no claims.yaml to aggregate)
    1  — claims.yaml present but not parseable / write failed
    2  — no claims.yaml found (advisory — not all runs produce one)
"""

from __future__ import annotations

import json
import os
import sys

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

CLAIMS_FILE = "claims.yaml"
METRICS_FILE = "metrics.yaml"

# Allowed confidence values per RA-D.2 AC-1 schema.
VALID_CONFIDENCE = frozenset({"high", "medium", "low", "none"})

# Allowed status values per RA-D.2 AC-1 schema.
VALID_STATUS = frozenset({"supported", "unsupported", "unknown", "ambiguous"})

# Sackett evidence grades accepted in evidence_grade field.
VALID_GRADES = frozenset({"1a", "1b", "2a", "2b", "3", "4", "5"})


# ─────────────────────────────────────────────────────────────────────────────
# Core aggregation logic
# ─────────────────────────────────────────────────────────────────────────────

def _pct(count: int, total: int) -> str:
    """Format count as 'N (X%)' string."""
    if total == 0:
        return "0 (0%)"
    pct = round(count / total * 100)
    return f"{count} ({pct}%)"


def compute_confidence_distribution(claims: list) -> dict:
    """Compute the confidence_distribution aggregate block from a list of claim dicts.

    Args:
        claims: List of claim mapping objects from claims.yaml#claims.

    Returns:
        confidence_distribution dict matching RA-D.2 AC-2 schema.
    """
    total = len(claims)
    counts: dict[str, int] = {
        "supported": 0,
        "unsupported": 0,
        "unknown": 0,
        "ambiguous": 0,
        "rewritten": 0,
    }
    by_grade: dict[str, int] = {g: 0 for g in sorted(VALID_GRADES)}
    sackett_any = False

    for claim in claims:
        if not isinstance(claim, dict):
            continue

        status = claim.get("status", "unknown")
        if status in counts:
            counts[status] += 1

        if claim.get("rewritten") is True:
            counts["rewritten"] += 1

        grade = claim.get("evidence_grade")
        if grade in VALID_GRADES:
            by_grade[str(grade)] += 1
            sackett_any = True

    dist: dict = {
        "total": total,
        "supported": _pct(counts["supported"], total),
        "unsupported": _pct(counts["unsupported"], total),
        "unknown": _pct(counts["unknown"], total),
        "ambiguous": _pct(counts["ambiguous"], total),
        "rewritten": _pct(counts["rewritten"], total),
    }

    # by_grade only populated when Sackett ran (Decision D2 / RA-D.2 AC-2)
    if sackett_any:
        dist["by_grade"] = by_grade

    return dist


# ─────────────────────────────────────────────────────────────────────────────
# I/O helpers
# ─────────────────────────────────────────────────────────────────────────────

def _load_yaml(path: str) -> dict | None:
    """Load a YAML file.  Returns None on parse error or missing PyYAML."""
    if not HAS_YAML:
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _load_yaml_raw(path: str) -> str:
    """Return raw file content as a string."""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _inject_distribution(raw: str, dist: dict) -> str:
    """Inject / update the confidence_distribution block in raw YAML text.

    Strategy: replace the existing ``confidence_distribution:`` block (if any)
    with the newly computed one.  Uses line-level manipulation to avoid
    round-tripping through a YAML serialiser (which would reorder keys and
    strip comments).

    If no existing block is found, the distribution is prepended after the
    top-of-file comment header.
    """
    dist_lines = ["confidence_distribution:"]
    dist_lines.append(f"  total: {dist['total']}")
    for key in ("supported", "unsupported", "unknown", "ambiguous", "rewritten"):
        dist_lines.append(f"  {key}: \"{dist[key]}\"")
    if "by_grade" in dist:
        dist_lines.append("  by_grade:")
        for grade, count in sorted(dist["by_grade"].items()):
            dist_lines.append(f"    {grade}: {count}")
    dist_block = "\n".join(dist_lines)

    lines = raw.splitlines()

    # Find existing block start
    start_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.rstrip() == "confidence_distribution:":
            start_idx = idx
            break

    if start_idx is not None:
        # Find end of existing block (next top-level key or EOF)
        end_idx = start_idx + 1
        while end_idx < len(lines):
            l = lines[end_idx]
            if l and not l.startswith(" ") and not l.startswith("#") and l.rstrip() != "":
                break
            end_idx += 1
        # Replace block
        new_lines = lines[:start_idx] + dist_block.splitlines() + lines[end_idx:]
        return "\n".join(new_lines) + "\n"

    # Prepend after header comments / top keys
    # Insert before the first non-comment, non-schema_version content line
    insert_at = 0
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") or stripped == "":
            insert_at = idx + 1
        elif stripped.startswith("schema_version") or stripped.startswith("story") or stripped.startswith("produced_by"):
            insert_at = idx + 1
        else:
            break

    new_lines = (
        lines[:insert_at]
        + [""]
        + ["# --- confidence_distribution aggregate (RA-D.2 AC-2) ---"]
        + dist_block.splitlines()
        + [""]
        + lines[insert_at:]
    )
    return "\n".join(new_lines) + "\n"


def _mirror_to_metrics(metrics_path: str, dist: dict) -> None:
    """Mirror claims confidence_distribution into metrics.yaml (Gold Rule 9).

    The mirror is additive: only the claims_confidence key is updated.
    If metrics.yaml is not parseable, we skip silently (advisory).
    """
    if not os.path.exists(metrics_path):
        return
    if not HAS_YAML:
        return

    try:
        with open(metrics_path, encoding="utf-8") as fh:
            raw = fh.read()
            data = yaml.safe_load(raw) or {}
    except Exception:
        return

    if not isinstance(data, dict):
        return

    data["claims_confidence"] = {
        "total": dist["total"],
        "supported": dist.get("supported", "0 (0%)"),
        "unsupported": dist.get("unsupported", "0 (0%)"),
        "rewritten": dist.get("rewritten", "0 (0%)"),
    }

    try:
        with open(metrics_path, "w", encoding="utf-8") as fh:
            yaml.dump(data, fh, allow_unicode=True, default_flow_style=False, sort_keys=False)
    except Exception:
        pass  # advisory — metrics mirror failure does not block


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def aggregate(output_dir: str) -> int:
    """Run aggregation for the given output directory.

    Returns exit code: 0 PASS, 1 ERROR, 2 NO-OP (advisory).
    """
    claims_path = os.path.join(output_dir, CLAIMS_FILE)

    if not os.path.exists(claims_path):
        print(
            f"[claims_aggregator] {CLAIMS_FILE} not found in {output_dir} — "
            "skipping (advisory, not all runs invoke citation_verifier)",
            file=sys.stderr,
        )
        return 2

    if not HAS_YAML:
        print(
            "[claims_aggregator] PyYAML not available — cannot parse claims.yaml. "
            "Install with: pip install pyyaml",
            file=sys.stderr,
        )
        return 1

    data = _load_yaml(claims_path)
    if data is None:
        print(
            f"[claims_aggregator] {claims_path} is not parseable. "
            "Check for YAML syntax errors.",
            file=sys.stderr,
        )
        return 1

    claims_list = data.get("claims", [])
    if not isinstance(claims_list, list):
        print(
            f"[claims_aggregator] {claims_path} 'claims' field is not a list.",
            file=sys.stderr,
        )
        return 1

    dist = compute_confidence_distribution(claims_list)

    # Read raw text and inject distribution block
    try:
        raw = _load_yaml_raw(claims_path)
    except OSError as exc:
        print(f"[claims_aggregator] Cannot read {claims_path}: {exc}", file=sys.stderr)
        return 1

    updated = _inject_distribution(raw, dist)

    try:
        with open(claims_path, "w", encoding="utf-8") as fh:
            fh.write(updated)
    except OSError as exc:
        print(f"[claims_aggregator] Cannot write {claims_path}: {exc}", file=sys.stderr)
        return 1

    # Mirror to metrics.yaml (Gold Rule 9 — advisory)
    metrics_path = os.path.join(output_dir, METRICS_FILE)
    _mirror_to_metrics(metrics_path, dist)

    total = dist["total"]
    rewritten = dist.get("rewritten", "0 (0%)")
    print(
        f"[claims_aggregator] PASS — {total} claims aggregated. "
        f"Supported: {dist.get('supported')}, "
        f"Rewritten: {rewritten}. "
        f"confidence_distribution written to top of {CLAIMS_FILE}."
    )
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print(
            f"Usage: python {os.path.basename(__file__)} /path/to/research/output/",
            file=sys.stderr,
        )
        sys.exit(3)

    output_dir = sys.argv[1]
    if not os.path.isdir(output_dir):
        print(f"[claims_aggregator] Not a directory: {output_dir}", file=sys.stderr)
        sys.exit(3)

    sys.exit(aggregate(output_dir))


if __name__ == "__main__":
    main()
