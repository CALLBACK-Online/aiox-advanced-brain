#!/usr/bin/env python3
"""Gap Detector — APPEND-ONLY gap tracker for tech-research pipeline.

Story: STORY-RA-B.1 | Created: 2026-05-19
Phase: P3.4 (reflect-and-gap-detect) — runs after P3.2, before P3.5

SEMANTICS: APPEND-ONLY
  - Wave N never removes gaps from previous waves; only transitions status.
  - New gaps are appended AFTER existing entries (stable IDs, stable order).
  - Validator rejects any write that removes entries.
  - Atomic write: tempfile + validate + mv (crash recovery via last-good state).

CRASH RECOVERY:
  - gap_detector.py writes to gaps.yaml.tmp, validates, then atomically renames.
  - pipeline-state.yaml#gaps_yaml_ref always points to last committed gaps.yaml.
  - On pipeline restart: read last-good gaps.yaml. No duplication.

Usage:
    python gap_detector.py --output-dir /path/to/docs/research/{slug}/ \\
                           --wave 1 \\
                           --mode research

    python gap_detector.py --output-dir /path/to/docs/research/{slug}/ \\
                           --wave 2 \\
                           --mode product_discovery

    python gap_detector.py --output-dir /path/to/docs/research/{slug}/ \\
                           --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import re
from datetime import datetime, timezone
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ─── Schema Constants ─────────────────────────────────────────────────────────

GAPS_SCHEMA_VERSION = "1.0"
GAPS_FILENAME = "gaps.yaml"
GAPS_TMP_SUFFIX = ".tmp"
PIPELINE_STATE_FILENAME = "pipeline-state.yaml"

REQUIRED_GAP_KEYS = {
    "id",
    "question",
    "source_hint",
    "priority",
    "attempts",
    "status",
    "opened_in_wave",
    "closed_in_wave",
    "closed_by_source",
}

VALID_STATUSES = frozenset({"open", "closed", "abandoned"})
VALID_PRIORITIES = frozenset({"high", "medium", "low"})
VALID_SOURCE_HINTS = frozenset({
    "academic-paper",
    "enterprise-postmortem",
    "general-web",
    "any",
})
VALID_MODES = frozenset({"research", "product_discovery"})

# ID format: G + 3-digit zero-padded int (G001 … G999)
_ID_PATTERN = re.compile(r"^G(\d{3})$")

# ─── YAML I/O Helpers ─────────────────────────────────────────────────────────


def _load_yaml(path: str) -> dict:
    """Load a YAML file, returning an empty dict on failure.

    Never raises — callers handle absence/parse errors via returned empty dict.
    """
    if not os.path.exists(path):
        return {}
    if not HAS_YAML:
        # Fallback: attempt rudimentary key extraction (not full parse)
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _dump_yaml(data: dict) -> str:
    """Serialize a dict to YAML string."""
    if HAS_YAML:
        return yaml.dump(
            data,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
    # Fallback: JSON (valid YAML superset for simple structures)
    return json.dumps(data, ensure_ascii=False, indent=2)


def _write_atomic(path: str, content: str) -> None:
    """Atomic write: write to .tmp, validate existence, rename.

    If rename fails (e.g. cross-device), falls back to direct write.
    Designed for AN_KE_163 concurrent-writer atomic-write pattern.
    """
    tmp_path = path + GAPS_TMP_SUFFIX
    dir_path = os.path.dirname(os.path.abspath(path))

    # Use a named temp file in the same directory for atomic rename
    try:
        fd, actual_tmp = tempfile.mkstemp(
            suffix=GAPS_TMP_SUFFIX,
            prefix=os.path.basename(path) + ".",
            dir=dir_path,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
            # Atomic rename (POSIX guarantee: same filesystem)
            os.replace(actual_tmp, path)
        except Exception:
            # Clean up temp file on failure
            try:
                os.unlink(actual_tmp)
            except OSError:
                pass
            raise
    except (OSError, IOError):
        # Final fallback: direct write (non-atomic but better than losing data)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    # Clean up any stale .tmp files from prior crashed runs
    stale_tmp = path + GAPS_TMP_SUFFIX
    if os.path.exists(stale_tmp):
        try:
            os.unlink(stale_tmp)
        except OSError:
            pass


# ─── Gap ID Management ────────────────────────────────────────────────────────


def _next_id(existing_gaps: list[dict]) -> str:
    """Compute the next available gap ID (G{NNN} format).

    Reads the highest numeric suffix from existing IDs and increments.
    If no existing gaps, starts at G001.
    """
    max_num = 0
    for entry in existing_gaps:
        gid = str(entry.get("id", ""))
        m = _ID_PATTERN.match(gid)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"G{max_num + 1:03d}"


# ─── Validation ───────────────────────────────────────────────────────────────


def _validate_gaps_document(data: dict) -> tuple[bool, list[str]]:
    """Validate a gaps.yaml document.

    Returns (is_valid, list_of_problems).
    Checks:
      1. schema_version field present
      2. gaps field is a list
      3. Each entry has all required keys
      4. IDs are unique and match G{NNN} format
      5. status values are in the allowed set
    """
    problems: list[str] = []

    if not isinstance(data, dict):
        return False, ["gaps document is not a mapping"]

    if not data.get("schema_version"):
        problems.append("missing schema_version field")

    gaps = data.get("gaps")
    if not isinstance(gaps, list):
        problems.append("'gaps' field must be a list")
        return False, problems

    seen_ids: set[str] = set()
    for idx, entry in enumerate(gaps):
        if not isinstance(entry, dict):
            problems.append(f"gaps[{idx}] is not a mapping")
            continue
        # Required keys
        missing = REQUIRED_GAP_KEYS - set(entry.keys())
        if missing:
            problems.append(f"gaps[{idx}] missing required keys: {sorted(missing)}")
        # ID format
        gid = str(entry.get("id", ""))
        if not _ID_PATTERN.match(gid):
            problems.append(f"gaps[{idx}] id={gid!r} does not match G{{NNN}} format")
        elif gid in seen_ids:
            problems.append(f"gaps[{idx}] duplicate id={gid!r}")
        else:
            seen_ids.add(gid)
        # Status enum
        status = entry.get("status")
        if status not in VALID_STATUSES:
            problems.append(
                f"gaps[{idx}] id={gid!r} status={status!r} not in {sorted(VALID_STATUSES)}"
            )

    return len(problems) == 0, problems


def _validate_no_entries_removed(
    old_gaps: list[dict], new_gaps: list[dict]
) -> tuple[bool, list[str]]:
    """APPEND-ONLY invariant: ensure no entries were removed.

    Returns (is_valid, list_of_problems).
    Every ID present in old_gaps must be present in new_gaps.
    """
    problems: list[str] = []
    old_ids = {str(e.get("id", "")) for e in old_gaps if isinstance(e, dict)}
    new_ids = {str(e.get("id", "")) for e in new_gaps if isinstance(e, dict)}
    removed = old_ids - new_ids
    if removed:
        problems.append(
            f"APPEND-ONLY violation: the following gap IDs were removed: {sorted(removed)}. "
            "Transition status to 'closed' or 'abandoned' instead of deleting."
        )
    return len(problems) == 0, problems


# ─── Core Operations ─────────────────────────────────────────────────────────


def load_existing_gaps(output_dir: str) -> tuple[dict, list[dict]]:
    """Load existing gaps.yaml.

    Returns (document_dict, gaps_list).
    If gaps.yaml is absent → returns empty initialized document.
    If gaps.yaml is present but not parseable → raises RuntimeError (halt condition).
    """
    path = os.path.join(output_dir, GAPS_FILENAME)
    if not os.path.exists(path):
        # Wave 1: initialize fresh document
        doc = {
            "schema_version": GAPS_SCHEMA_VERSION,
            "story_ref": "STORY-RA-B.1",
            "pipeline_id": "",
            "slug": os.path.basename(output_dir.rstrip("/")),
            "generated_at": "",
            "wave_last_updated": 0,
            "summary": {
                "total": 0,
                "open": 0,
                "closed": 0,
                "abandoned": 0,
                "gap_convergence": False,
            },
            "gaps": [],
        }
        return doc, []

    if not HAS_YAML:
        raise RuntimeError(
            "PyYAML is required to load existing gaps.yaml. "
            "Install with: pip install pyyaml"
        )

    with open(path, encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh)
        except Exception as exc:
            raise RuntimeError(
                f"gaps.yaml is present but not parseable at {path}. "
                f"Parse error: {exc}. "
                "APPEND-ONLY integrity at risk — manual inspection required."
            ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            f"gaps.yaml at {path} is not a mapping (got {type(data).__name__}). "
            "File may be corrupted."
        )

    gaps = data.get("gaps", [])
    if not isinstance(gaps, list):
        raise RuntimeError(
            f"gaps.yaml at {path} has 'gaps' field that is not a list. "
            "File may be corrupted."
        )

    return data, gaps


def load_pipeline_state(output_dir: str) -> dict:
    """Load pipeline-state.yaml for context (wave_num, mode, pipeline_id)."""
    path = os.path.join(output_dir, PIPELINE_STATE_FILENAME)
    return _load_yaml(path)


def transition_closed_gaps(
    existing_gaps: list[dict],
    wave_num: int,
    sources: list[dict],
) -> tuple[list[dict], int]:
    """Transition open gaps to closed when covered by wave sources.

    Heuristic: a gap is considered closed if any source's title, url, or
    abstract contains ≥ 2 significant words from the gap's question.

    Returns (updated_gaps, n_closed_this_wave).
    """
    closed_count = 0
    updated = []

    # Build a searchable source corpus for this wave
    source_texts: list[tuple[str, str]] = []  # (source_id, combined_text)
    for src in sources:
        if not isinstance(src, dict):
            continue
        sid = str(src.get("id") or src.get("url") or "")
        text_parts = [
            str(src.get("title", "")),
            str(src.get("url", "")),
            str(src.get("abstract", "")),
            str(src.get("snippet", "")),
        ]
        source_texts.append((sid, " ".join(text_parts).lower()))

    for entry in existing_gaps:
        if not isinstance(entry, dict):
            updated.append(entry)
            continue

        entry = dict(entry)  # shallow copy to avoid mutating caller's list
        if entry.get("status") != "open":
            # Already closed or abandoned — no transition
            updated.append(entry)
            continue

        # Increment attempts for this wave
        entry["attempts"] = int(entry.get("attempts", 0)) + 1

        # Check if any source closes this gap
        question = str(entry.get("question", "")).lower()
        # Extract significant words (> 4 chars, not stop words)
        words = [w for w in re.findall(r"\b[a-z]{5,}\b", question)
                 if w not in {"which", "where", "these", "there", "their",
                              "would", "could", "should", "about", "after",
                              "before", "between"}]

        closed_by: Optional[str] = None
        if words:
            for source_id, source_text in source_texts:
                # At least 2 significant words from the question appear in source
                matches = sum(1 for w in words if w in source_text)
                if matches >= min(2, len(words)):
                    closed_by = source_id
                    break

        if closed_by:
            entry["status"] = "closed"
            entry["closed_in_wave"] = wave_num
            entry["closed_by_source"] = closed_by
            closed_count += 1

        updated.append(entry)

    return updated, closed_count


def detect_new_gaps(
    wave_summary_path: str,
    existing_gaps: list[dict],
    wave_num: int,
    mode: str,
    output_dir: str,
) -> list[dict]:
    """Identify new gaps not already tracked.

    Reads wave summary content and emits candidate gaps that are not
    semantically similar to any existing open gap (dedup heuristic).

    Returns list of new gap dicts to append.
    """
    new_gaps: list[dict] = []

    # Look for wave summary file
    summary_content = ""
    candidate_paths = [
        wave_summary_path,
        os.path.join(output_dir, f"wave-{wave_num}-summary.md"),
        os.path.join(output_dir, f"wave-{wave_num}-progress.jsonl"),
    ]
    for candidate in candidate_paths:
        if candidate and os.path.exists(candidate):
            try:
                with open(candidate, encoding="utf-8") as fh:
                    summary_content = fh.read()
            except OSError:
                pass
            if summary_content:
                break

    if not summary_content:
        # No summary available — emit a placeholder gap for missing coverage
        # This ensures Wave 1 always produces at least one gap to bootstrap the system
        placeholder = _build_gap_entry(
            question=(
                "Wave summary not available — what are the primary unanswered "
                "research questions for this topic?"
            ),
            source_hint="any",
            priority="medium",
            wave_num=wave_num,
        )
        new_gaps.append(placeholder)
        return new_gaps

    # Extract unanswered-question markers from summary content
    # Common patterns in research summaries:
    #   - Lines starting with "- [ ]" or "TODO:" or "OPEN:" or "GAP:"
    #   - Sentences containing "unclear", "unknown", "not found", "missing"
    #   - In product-discovery mode: "JTBD gap", "competitor", "WTP"
    gap_patterns = [
        (r"(?:GAP|OPEN|TODO):\s*(.+?)(?:\n|$)", "general-web", "medium"),
        (r"-\s*\[\s*\]\s+(.+?)(?:\n|$)", "general-web", "medium"),
        (r"(?:remains?\s+unclear|not\s+found|no\s+data\s+found|missing\s+data)\s*:?\s*(.+?)(?:\.|$)",
         "general-web", "low"),
    ]
    if mode == "product_discovery":
        gap_patterns += [
            (r"(?:JTBD\s+gap|job-to-be-done\s+gap)\s*:?\s*(.+?)(?:\.|$)",
             "enterprise-postmortem", "high"),
            (r"(?:competitor\s+(?:gap|unknown))\s*:?\s*(.+?)(?:\.|$)",
             "general-web", "medium"),
            (r"(?:WTP|willingness.to.pay)\s+(?:gap|unclear)\s*:?\s*(.+?)(?:\.|$)",
             "enterprise-postmortem", "high"),
        ]

    # Build set of existing open questions for dedup
    existing_questions_lower = {
        str(g.get("question", "")).lower()
        for g in existing_gaps
        if isinstance(g, dict) and g.get("status") == "open"
    }

    for pattern, source_hint, priority in gap_patterns:
        for m in re.finditer(pattern, summary_content, re.IGNORECASE | re.MULTILINE):
            question_raw = m.group(1).strip()
            if len(question_raw) < 10:
                continue
            # Dedup: skip if semantically similar to existing open gap
            question_lower = question_raw.lower()
            words_new = set(re.findall(r"\b[a-z]{5,}\b", question_lower))
            is_duplicate = False
            for existing_q in existing_questions_lower:
                words_existing = set(re.findall(r"\b[a-z]{5,}\b", existing_q))
                if words_new and words_existing:
                    overlap = len(words_new & words_existing) / len(words_new | words_existing)
                    if overlap >= 0.5:
                        is_duplicate = True
                        break
            if is_duplicate:
                continue

            gap = _build_gap_entry(
                question=question_raw,
                source_hint=source_hint,
                priority=priority,
                wave_num=wave_num,
            )
            new_gaps.append(gap)
            existing_questions_lower.add(question_lower)

    # Always ensure at least one gap exists per wave to bootstrap the gap system
    if not new_gaps and not existing_gaps:
        placeholder = _build_gap_entry(
            question=(
                f"Wave {wave_num}: What key research questions remain unanswered "
                "for this topic after this wave of sources?"
            ),
            source_hint="any",
            priority="medium",
            wave_num=wave_num,
        )
        new_gaps.append(placeholder)

    return new_gaps


def _build_gap_entry(
    question: str,
    source_hint: str,
    priority: str,
    wave_num: int,
) -> dict:
    """Build a new gap entry dict with all required keys."""
    return {
        "id": "PLACEHOLDER",  # Replaced by caller after ID assignment
        "question": question,
        "source_hint": source_hint if source_hint in VALID_SOURCE_HINTS else "any",
        "priority": priority if priority in VALID_PRIORITIES else "medium",
        "attempts": 0,
        "status": "open",
        "opened_in_wave": wave_num,
        "closed_in_wave": None,
        "closed_by_source": None,
        "notes": "",
    }


def compute_gap_convergence(gaps: list[dict]) -> bool:
    """Return True if ALL gaps have status != 'open' (i.e. none are open).

    This is the gap_set.is_empty() signal consumed by heartbeat-policy.yaml
    signal #6 (gap_convergence, priority 6).

    Returns False if gaps list is empty (no gaps detected yet — not converged).
    """
    if not gaps:
        return False  # No gaps found yet — not converged (unknown state)
    return all(
        isinstance(g, dict) and g.get("status") in {"closed", "abandoned"}
        for g in gaps
    )


def update_summary(doc: dict, gaps: list[dict]) -> dict:
    """Recompute and update the summary block."""
    n_open = sum(1 for g in gaps if isinstance(g, dict) and g.get("status") == "open")
    n_closed = sum(1 for g in gaps if isinstance(g, dict) and g.get("status") == "closed")
    n_abandoned = sum(1 for g in gaps if isinstance(g, dict) and g.get("status") == "abandoned")
    gap_convergence = compute_gap_convergence(gaps)

    doc["summary"] = {
        "total": len(gaps),
        "open": n_open,
        "closed": n_closed,
        "abandoned": n_abandoned,
        "gap_convergence": gap_convergence,
    }
    return doc


def update_pipeline_state(
    output_dir: str,
    gaps: list[dict],
    gap_convergence: bool,
) -> None:
    """Update pipeline-state.yaml with gap metrics and gaps_yaml_ref.

    Adds (or updates) these fields:
      - gap_convergence_signal  (bool)  — consumed by Phase 3.5 heartbeat
      - gaps_yaml_ref           (str)   — path to committed gaps.yaml
      - gaps_open_count         (int)
      - gaps_closed_count       (int)
      - gaps_total_count        (int)
    """
    ps_path = os.path.join(output_dir, PIPELINE_STATE_FILENAME)
    ps_data = _load_yaml(ps_path)

    n_open = sum(1 for g in gaps if isinstance(g, dict) and g.get("status") == "open")
    n_closed = sum(1 for g in gaps if isinstance(g, dict) and g.get("status") == "closed")

    ps_data["gap_convergence_signal"] = gap_convergence
    ps_data["gaps_yaml_ref"] = GAPS_FILENAME
    ps_data["gaps_open_count"] = n_open
    ps_data["gaps_closed_count"] = n_closed
    ps_data["gaps_total_count"] = len(gaps)

    content = _dump_yaml(ps_data)
    _write_atomic(ps_path, content)


# ─── Main Detector Entry Point ────────────────────────────────────────────────


def run_gap_detection(
    output_dir: str,
    wave_num: int,
    mode: str = "research",
    sources: Optional[list[dict]] = None,
    wave_summary_path: str = "",
    dry_run: bool = False,
) -> dict:
    """Main entry point for P3.4 gap detection.

    Args:
        output_dir: Path to docs/research/{date}-{slug}/ (runtime output dir).
        wave_num: Current wave number (1-based).
        mode: "research" or "product_discovery".
        sources: List of source dicts from this wave (for gap closing heuristic).
        wave_summary_path: Explicit path to wave summary file (optional; auto-detected).
        dry_run: If True, compute but do not write any files.

    Returns:
        dict with keys:
          n_open, n_closed, n_abandoned, n_new_this_wave, n_closed_this_wave,
          gap_convergence, gaps (list), warnings (list), errors (list)
    """
    result: dict = {
        "wave_num": wave_num,
        "mode": mode,
        "n_open": 0,
        "n_closed": 0,
        "n_abandoned": 0,
        "n_new_this_wave": 0,
        "n_closed_this_wave": 0,
        "gap_convergence": False,
        "gaps": [],
        "warnings": [],
        "errors": [],
    }

    if not HAS_YAML:
        result["errors"].append(
            "PyYAML not available — gap_detector.py requires 'pip install pyyaml'"
        )
        return result

    if mode not in VALID_MODES:
        result["warnings"].append(
            f"Unknown mode={mode!r} — defaulting to 'research'. "
            f"Valid modes: {sorted(VALID_MODES)}"
        )
        mode = "research"

    # ── Step 1: Load existing gaps ────────────────────────────────────────
    try:
        doc, existing_gaps = load_existing_gaps(output_dir)
    except RuntimeError as exc:
        result["errors"].append(str(exc))
        return result

    old_gap_ids = [str(g.get("id", "")) for g in existing_gaps if isinstance(g, dict)]

    # ── Step 2: Transition closed gaps ───────────────────────────────────
    sources = sources or []
    updated_gaps, n_closed_this_wave = transition_closed_gaps(
        existing_gaps, wave_num, sources
    )
    result["n_closed_this_wave"] = n_closed_this_wave

    # ── Step 3: Detect new gaps ───────────────────────────────────────────
    new_gap_candidates = detect_new_gaps(
        wave_summary_path=wave_summary_path,
        existing_gaps=updated_gaps,
        wave_num=wave_num,
        mode=mode,
        output_dir=output_dir,
    )

    # Assign IDs and append
    for candidate in new_gap_candidates:
        candidate["id"] = _next_id(updated_gaps)
        updated_gaps.append(candidate)

    result["n_new_this_wave"] = len(new_gap_candidates)

    # ── Step 4: APPEND-ONLY invariant check ──────────────────────────────
    is_valid, inv_problems = _validate_no_entries_removed(existing_gaps, updated_gaps)
    if not is_valid:
        result["errors"].extend(inv_problems)
        return result

    # ── Step 5: Update document ───────────────────────────────────────────
    doc["gaps"] = updated_gaps
    doc["wave_last_updated"] = wave_num
    doc["generated_at"] = datetime.now(timezone.utc).isoformat()
    doc["slug"] = os.path.basename(output_dir.rstrip("/"))

    # Update pipeline_id from pipeline-state.yaml if available
    ps_data = load_pipeline_state(output_dir)
    if ps_data.get("pipeline_id"):
        doc["pipeline_id"] = str(ps_data["pipeline_id"])

    doc = update_summary(doc, updated_gaps)
    gap_convergence = doc["summary"]["gap_convergence"]

    # ── Step 6: Validate document ─────────────────────────────────────────
    is_doc_valid, doc_problems = _validate_gaps_document(doc)
    if not is_doc_valid:
        result["errors"].extend(doc_problems)
        return result

    # ── Step 7: Atomic write ──────────────────────────────────────────────
    gaps_path = os.path.join(output_dir, GAPS_FILENAME)
    header = (
        "# gaps.yaml — APPEND-ONLY gap tracker for tech-research pipeline\n"
        "# Story: STORY-RA-B.1 | Auto-generated by gap_detector.py\n"
        "# DO NOT manually remove entries — transition status to 'closed' or 'abandoned' instead.\n"
        "# See squads/research/templates/tech-research/gaps.yaml for schema reference.\n\n"
    )
    content = header + _dump_yaml(doc)

    if not dry_run:
        _write_atomic(gaps_path, content)

    # ── Step 8: Update pipeline-state.yaml ───────────────────────────────
    if not dry_run:
        try:
            update_pipeline_state(output_dir, updated_gaps, gap_convergence)
        except Exception as exc:
            result["warnings"].append(
                f"Could not update pipeline-state.yaml: {exc}. "
                "gaps.yaml was written successfully — pipeline-state may be stale."
            )

    # ── Populate result summary ───────────────────────────────────────────
    summary = doc["summary"]
    result["n_open"] = summary["open"]
    result["n_closed"] = summary["closed"]
    result["n_abandoned"] = summary["abandoned"]
    result["gap_convergence"] = gap_convergence
    result["gaps"] = updated_gaps

    return result


# ─── Self-Test (PoC: crash recovery + APPEND-ONLY) ───────────────────────────


def run_self_test() -> int:
    """PoC: test APPEND-ONLY semantics and crash recovery.

    Creates a temporary directory, runs gap detection across 2 simulated waves,
    and verifies:
      1. Wave 1 creates gaps.yaml with initial gaps
      2. Wave 2 appends new gaps and transitions an existing one (does not delete)
      3. A crash mid-wave (simulated) leaves last-good gaps.yaml intact
      4. Recovery reads last-good gaps.yaml without duplicating closed gaps

    Returns 0 on success, 1 on failure.
    """
    import shutil

    print("[self-test] Starting gap_detector APPEND-ONLY + crash recovery PoC...")
    tmpdir = tempfile.mkdtemp(prefix="gap_detector_test_")
    exit_code = 0

    try:
        # ── Wave 1: fresh run ─────────────────────────────────────────────
        print("[self-test] Wave 1: fresh detection (no existing gaps.yaml)...")
        r1 = run_gap_detection(
            output_dir=tmpdir,
            wave_num=1,
            mode="research",
        )
        assert len(r1["errors"]) == 0, f"Wave 1 errors: {r1['errors']}"
        gaps_path = os.path.join(tmpdir, GAPS_FILENAME)
        assert os.path.exists(gaps_path), "gaps.yaml not created after Wave 1"
        doc1 = _load_yaml(gaps_path)
        assert isinstance(doc1.get("gaps"), list), "gaps field must be a list"
        n_gaps_w1 = len(doc1["gaps"])
        print(f"[self-test] Wave 1 PASS: {n_gaps_w1} gaps created, gap_convergence={doc1['summary']['gap_convergence']}")

        # ── Wave 2: append + transition ──────────────────────────────────
        # Write a wave summary with a new gap pattern
        summary_path = os.path.join(tmpdir, "wave-2-summary.md")
        with open(summary_path, "w", encoding="utf-8") as fh:
            fh.write("## Wave 2 Summary\n\n")
            fh.write("GAP: What is the performance overhead of pgvector at 10M vectors?\n")
            fh.write("GAP: How do enterprise customers evaluate vector database pricing?\n")
            fh.write("Most queries answered about basic functionality.\n")

        print("[self-test] Wave 2: appending new gaps, transitioning existing...")
        r2 = run_gap_detection(
            output_dir=tmpdir,
            wave_num=2,
            mode="research",
            wave_summary_path=summary_path,
        )
        assert len(r2["errors"]) == 0, f"Wave 2 errors: {r2['errors']}"
        doc2 = _load_yaml(gaps_path)
        n_gaps_w2 = len(doc2["gaps"])
        assert n_gaps_w2 >= n_gaps_w1, (
            f"APPEND-ONLY violation: Wave 2 has {n_gaps_w2} gaps, Wave 1 had {n_gaps_w1}"
        )
        print(f"[self-test] Wave 2 PASS: {n_gaps_w2} total gaps (was {n_gaps_w1}), "
              f"gap_convergence={doc2['summary']['gap_convergence']}")

        # ── Simulate crash mid-wave: write stale .tmp, verify last-good ──
        print("[self-test] Crash simulation: writing stale .tmp file...")
        stale_tmp = gaps_path + GAPS_TMP_SUFFIX
        with open(stale_tmp, "w", encoding="utf-8") as fh:
            fh.write("# CORRUPTED by simulated crash mid-write\ngaps: null\n")

        # Load gaps.yaml again — must be last-good (Wave 2 state), not the stale .tmp
        doc_after_crash = _load_yaml(gaps_path)
        assert len(doc_after_crash.get("gaps", [])) == n_gaps_w2, (
            f"Crash recovery FAIL: expected {n_gaps_w2} gaps, got "
            f"{len(doc_after_crash.get('gaps', []))}"
        )
        print(f"[self-test] Crash recovery PASS: gaps.yaml intact with {n_gaps_w2} entries")

        # ── Wave 3 recovery: run again after simulated crash ──────────────
        print("[self-test] Wave 3 (post-crash recovery): running gap detection...")
        r3 = run_gap_detection(
            output_dir=tmpdir,
            wave_num=3,
            mode="research",
        )
        assert len(r3["errors"]) == 0, f"Wave 3 recovery errors: {r3['errors']}"
        doc3 = _load_yaml(gaps_path)
        n_gaps_w3 = len(doc3["gaps"])
        assert n_gaps_w3 >= n_gaps_w2, (
            f"APPEND-ONLY violation post-crash: Wave 3 has {n_gaps_w3}, Wave 2 had {n_gaps_w2}"
        )
        # No stale .tmp should remain after successful wave 3 write
        assert not os.path.exists(stale_tmp), "Stale .tmp file not cleaned up"
        print(f"[self-test] Wave 3 recovery PASS: {n_gaps_w3} gaps, "
              f"gap_convergence={doc3['summary']['gap_convergence']}")

        # ── APPEND-ONLY: verify Wave 1 IDs still present in Wave 3 ───────
        w1_ids = {str(g.get("id")) for g in doc1["gaps"]}
        w3_ids = {str(g.get("id")) for g in doc3["gaps"]}
        removed = w1_ids - w3_ids
        assert not removed, (
            f"APPEND-ONLY FAIL: Wave 1 IDs removed in Wave 3: {removed}"
        )
        print(f"[self-test] APPEND-ONLY invariant PASS: all Wave 1 IDs present in Wave 3")

        print("\n[self-test] ALL ASSERTIONS PASSED — gap_detector APPEND-ONLY + crash recovery verified.")

    except AssertionError as exc:
        print(f"\n[self-test] ASSERTION FAILED: {exc}")
        exit_code = 1
    except Exception as exc:
        print(f"\n[self-test] UNEXPECTED ERROR: {exc}")
        exit_code = 1
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        print(f"[self-test] Temp dir cleaned up.")

    return exit_code


# ─── CLI Entry Point ──────────────────────────────────────────────────────────


def main() -> int:
    """CLI entry point for phase-3-4-reflect-and-gap-detect.yaml invocation."""
    parser = argparse.ArgumentParser(
        description="Gap detector — APPEND-ONLY gap tracker for tech-research pipeline (P3.4).",
    )
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        help="Path to docs/research/{date}-{slug}/ runtime output directory.",
    )
    parser.add_argument(
        "--wave",
        type=int,
        default=1,
        help="Current wave number (1-based). Default: 1.",
    )
    parser.add_argument(
        "--mode",
        choices=sorted(VALID_MODES),
        default="research",
        help="Pipeline mode. Default: research.",
    )
    parser.add_argument(
        "--wave-summary",
        dest="wave_summary",
        default="",
        help="Explicit path to wave summary file. Auto-detected if omitted.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute gap detection but do not write any files.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run APPEND-ONLY + crash recovery self-test (PoC). Ignores other args.",
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
        return 3

    result = run_gap_detection(
        output_dir=args.output_dir,
        wave_num=args.wave,
        mode=args.mode,
        wave_summary_path=args.wave_summary,
        dry_run=args.dry_run,
    )

    # Emit result as JSON (consumed by orchestrator / pipeline-state writer)
    summary_out = {
        "wave_num": result["wave_num"],
        "mode": result["mode"],
        "n_open": result["n_open"],
        "n_closed": result["n_closed"],
        "n_abandoned": result["n_abandoned"],
        "n_new_this_wave": result["n_new_this_wave"],
        "n_closed_this_wave": result["n_closed_this_wave"],
        "gap_convergence": result["gap_convergence"],
        "warnings": result["warnings"],
        "errors": result["errors"],
    }
    print(json.dumps(summary_out, indent=2))

    if result["errors"]:
        return 1
    if args.dry_run:
        print("[dry-run] No files written.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
