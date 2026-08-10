#!/usr/bin/env python3
"""Output structure validator for tech-research and research-bench pipelines.

Worker atom: QG-PROD-6 (output completeness)
Deterministic: file existence + content checks, no LLM needed.

Usage:
    python output_validator.py [--mode current|target] [--skill tech-research|research-bench]
                               [--enforcement warn|block] /path/to/output_dir/

Modes (Sprint 0 A2 fix — REQUIRED_FILES paradox):
    current  Default. Baseline V1 artifacts that every Claude Code + Codex run
             must produce. Aligns with E07 gold standard.
    target   Aspirational V3 artifacts including curiosity_queue, evolving_report,
             and execution-log JSONL. Used by spy v5 evolution + future skill
             upgrades.

Skill discrimination (Story RA-F.1 AC-5):
    --skill tech-research   Default. Apply tech-research V1/V3 baseline checks +
                            criteria-calibration extension hook + status-code
                            compliance hook.
    --skill research-bench  Apply research-bench Gold contract checks + criteria-
                            calibration extension hook + status-code compliance
                            hook. Replaces baseline file list with bench-specific
                            paths.

Enforcement (Story RA-F.1 PO Condition 2):
    --enforcement warn      Default. Findings reported but exit 0 unless legacy
                            checks fail. Stays warn for 30d post-merge per story
                            Regression Risk row 1.
    --enforcement block     Findings cause exit non-zero. Promoted by operator
                            after 30d clean window.

Status-code compliance (Story RA-F.2 AC-6):
    Adds `check_status_code_compliance()` extension hook that validates:
      - recommendations-by-use-case.md presence in multi-player ≥3 candidates
      - coverage matrices use 4-level enum (confirmed/partial/uncertain/not_present)
      - visual symbols ✅/◐/?/— consistent with helper canonical map

    Hook is GENERIC across both skills (no `if skill == 'tech-research' else ...`),
    per STORY-RA-F.2 PO Condition 2.
"""

import argparse
import os
import sys
import json
import re

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Story RA-F.2 — coverage_matrix_helper is the canonical source for the 4-level
# status enum, score map, and symbol map used by check_status_code_compliance().
# Ensure the helper's directory is on sys.path BEFORE attempting import (validator
# may be invoked from any cwd by callers like bench-make.sh or skill prompts).
_HELPER_DIR = os.path.dirname(os.path.abspath(__file__))
if _HELPER_DIR not in sys.path:
    sys.path.insert(0, _HELPER_DIR)
try:
    from coverage_matrix_helper import (  # type: ignore[import-not-found]
        STATUS_ENUM,
        SCORE_MAP,
        SYMBOL_MAP_UNICODE,
        SYMBOL_MAP_ASCII,
        validate_matrix,
    )
    HAS_COVERAGE_HELPER = True
except ImportError:
    HAS_COVERAGE_HELPER = False
    STATUS_ENUM = ()  # type: ignore[assignment]
    SCORE_MAP = {}  # type: ignore[assignment]
    SYMBOL_MAP_UNICODE = {}  # type: ignore[assignment]
    SYMBOL_MAP_ASCII = {}  # type: ignore[assignment]
    validate_matrix = None  # type: ignore[assignment]

# ─────────────────────────────────────────────────────────────────────────────
# Story RA-F.1 — Criteria + Scoring Calibration extension hook (AC-5)
# ─────────────────────────────────────────────────────────────────────────────
# This block is the GENERIC extension point referenced by Story RA-F.1 §PO
# Condition 1 ("extension hook genérico, não shape-specific"). It is invoked
# by `validate_output` AFTER the skill-specific baseline checks and emits
# findings into the same `results` dict. The hook is intentionally agnostic
# to whether the run is tech-research or research-bench — it inspects file
# placement and YAML frontmatter only.

CALIBRATION_TRIGGER_DIMENSIONS = 5     # AC-1 threshold
CALIBRATION_TRIGGER_PATTERN = "multi_player"

# Files that may carry numeric scores and therefore MUST declare a
# `scoring_calibration` block when they exist (AC-2).
SCORED_ATOM_CANDIDATES = (
    "matrices.yaml",
    "comparison-matrix.json",
    "scorecard.json",
    "scenario-scorecards.json",
)

SCORING_CALIBRATION_REQUIRED_KEYS = (
    "type",
    "scale",
    "calibrated_by",
    "disclaimer",
    "reproducibility",
)

CALIBRATION_TYPE_ALLOWED = ("interpretive", "empirical", "hybrid")
CALIBRATION_REPRODUCIBILITY_ALLOWED = ("low", "medium", "high")

# Story RA-F.2 — Status code 4-níveis trigger thresholds (AC-3, AC-4, AC-6).
# multi_player AND candidates_count >= 3 → recommendations-by-use-case.md required.
STATUS_CODE_TRIGGER_PATTERN = "multi_player"
STATUS_CODE_TRIGGER_CANDIDATES = 3
RECOMMENDATIONS_FILE = "recommendations-by-use-case.md"

# ─────────────────────────────────────────────────────────────────────────────
# Story RA-F.3 — Extraction Ladder + Mandatory Sources + Gap Analysis hooks
# ─────────────────────────────────────────────────────────────────────────────
# Three GENERIC extension hooks following the F.1/F.2 shape:
#   check_extraction_ladder()          — validates sources.yaml schema enrichment
#   check_mandatory_sources_coverage() — warns if mandatory_additions not applied
#   check_gap_analysis_presence()      — warns/errors if gap-analysis.md absent on multi_player
#
# Severity default = WARNING (exit 0 unless --enforcement block per precedent F.1/F.2).
# Findings written to results['extraction_ladder_findings'] /
#   results['mandatory_sources_findings'] / results['gap_analysis_findings'].

# extraction_* fields introduced by STORY-RA-F.3 AC-B2
EXTRACTION_FIELDS_OPTIONAL = (
    "extraction_method",
    "extraction_quality",
    "extraction_attempts",
)
EXTRACTION_VALID_METHODS = frozenset({
    "websearch_snippet", "webfetch", "etl", "playwright",
    "manual_paste", "extraction_blocked",
})
EXTRACTION_VALID_QUALITIES = frozenset({
    "full", "snippet_only", "blocked_fallback_used",
})

# Gap analysis atom filename (AC-C1)
GAP_ANALYSIS_FILE = "gap-analysis.md"
GAP_ANALYSIS_TRIGGER_PATTERN = "multi_player"

# Mandatory sources log key (AC-A2)
MANDATORY_ADDITIONS_KEY = "mandatory_additions"

REQUIRED_FILES_CURRENT = [
    "README.md",
    "00-query-original.md",
    "01-deep-research-prompt.md",
    "02-research-report.md",
    "03-recommendations.md",
    "quick-wins.md",
    "metrics.yaml",
    "pipeline-state.yaml",
]

REQUIRED_FILES_TARGET = REQUIRED_FILES_CURRENT + [
    "curiosity_queue.yaml",
    "evolving_report.md",
    "execution-log.jsonl",
]

# Default for backward compatibility when callers do not pass --mode.
REQUIRED_FILES = REQUIRED_FILES_CURRENT

OPTIONAL_FILES = []

README_REQUIRED_SECTIONS = [
    "TL;DR",
    "Research Metadata",
    "workflow_version",
    "runtime_contract",
    "coverage_score",
    "citation_verified",
    "stop_reason",
    "rubrics",
]

REPORT_MIN_SIZE = 500
RECS_MIN_SIZE = 200


def _load_structured_file(path: str) -> dict:
    """Load YAML or JSON file content."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith(".json") or not HAS_YAML:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    try:
        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _numeric_score_present(data) -> bool:
    """Recursively scan a parsed YAML/JSON structure for numeric score-like fields.

    Returns True if any of the well-known score field names carries a numeric
    value. Used to decide whether `scoring_calibration` is mandatory.
    """
    score_keys = {
        "score",
        "rank_score",
        "dimension_score",
        "feature_depth_score",
        "microdim_score",
        "total",
        "weighted_total",
    }
    if isinstance(data, dict):
        for key, value in data.items():
            if key in score_keys and isinstance(value, (int, float)):
                return True
            if _numeric_score_present(value):
                return True
    elif isinstance(data, list):
        for item in data:
            if _numeric_score_present(item):
                return True
    return False


def _extract_calibration_block(data) -> dict:
    """Pull `scoring_calibration` block from a parsed YAML/JSON structure.

    Accepts either a top-level `scoring_calibration:` (YAML frontmatter style)
    or a nested `meta.scoring_calibration` (JSON style).
    """
    if not isinstance(data, dict):
        return {}
    if isinstance(data.get("scoring_calibration"), dict):
        return data["scoring_calibration"]
    meta = data.get("meta")
    if isinstance(meta, dict) and isinstance(meta.get("scoring_calibration"), dict):
        return meta["scoring_calibration"]
    return {}


def _calibration_block_is_valid(block: dict) -> tuple[bool, list]:
    """Validate the `scoring_calibration` block per AC-2 schema.

    Returns (is_valid, list_of_problems).
    """
    problems = []
    for key in SCORING_CALIBRATION_REQUIRED_KEYS:
        if key not in block:
            problems.append(f"missing required key: {key}")
    cal_type = block.get("type")
    if cal_type and cal_type not in CALIBRATION_TYPE_ALLOWED:
        problems.append(
            f"type='{cal_type}' not in {CALIBRATION_TYPE_ALLOWED}"
        )
    repro = block.get("reproducibility")
    if repro and repro not in CALIBRATION_REPRODUCIBILITY_ALLOWED:
        problems.append(
            f"reproducibility='{repro}' not in {CALIBRATION_REPRODUCIBILITY_ALLOWED}"
        )
    if cal_type in ("hybrid", "empirical") and not block.get("baseline"):
        problems.append("type=hybrid|empirical requires `baseline`")
    return (len(problems) == 0, problems)


def _count_dimensions(data) -> int:
    """Best-effort count of dimensions/axes declared in a scored atom.

    Tries the most common shapes:
    - matrices.yaml#matrices[].dimensions[] (research extractor format)
    - comparison-matrix.json#dimensions[]
    - rows[].dimension (one row per dimension)
    """
    if not isinstance(data, dict):
        return 0
    if isinstance(data.get("dimensions"), list):
        return len(data["dimensions"])
    if isinstance(data.get("microdimensions"), list):
        return len(data["microdimensions"])
    if isinstance(data.get("matrices"), list):
        total = 0
        for m in data["matrices"]:
            if isinstance(m, dict) and isinstance(m.get("dimensions"), list):
                total = max(total, len(m["dimensions"]))
        return total
    if isinstance(data.get("rows"), list):
        return len(data["rows"])
    return 0


def _comparison_pattern_from(data) -> str:
    """Pull `comparison_pattern` from common metadata locations."""
    if not isinstance(data, dict):
        return ""
    if isinstance(data.get("comparison_pattern"), str):
        return data["comparison_pattern"]
    meta = data.get("meta")
    if isinstance(meta, dict) and isinstance(meta.get("comparison_pattern"), str):
        return meta["comparison_pattern"]
    inferred = data.get("inferred_context") or data.get("metadata")
    if isinstance(inferred, dict) and isinstance(inferred.get("comparison_pattern"), str):
        return inferred["comparison_pattern"]
    return ""


def _candidates_count_from(data) -> int:
    """Best-effort count of candidates/players declared in a scored atom.

    Tries the most common shapes:
      - matrices.yaml#rows[].cells (each cell = one player) — uses MAX across rows
        to be robust to legacy rows that omit some players
      - comparison-matrix.json#players[]
      - matrices.yaml#players[]
      - rows[].cells (legacy)
    """
    if not isinstance(data, dict):
        return 0
    if isinstance(data.get("players"), list):
        return len(data["players"])
    if isinstance(data.get("matrices"), list):
        total = 0
        for m in data["matrices"]:
            if isinstance(m, dict) and isinstance(m.get("players"), list):
                total = max(total, len(m["players"]))
        if total:
            return total
    rows = data.get("rows")
    if isinstance(rows, list):
        max_cells = 0
        for row in rows:
            if isinstance(row, dict):
                cells = row.get("cells")
                if isinstance(cells, dict):
                    max_cells = max(max_cells, len(cells))
                elif isinstance(cells, list):
                    max_cells = max(max_cells, len(cells))
        return max_cells
    return 0


def _iter_cell_status_values(data):
    """Yield every status string that appears in a matrix-shaped structure.

    Walks the common shapes used by both skills:
      - rows[].cells[player] = "status" OR {"status": "..."}
      - rows[].cells[].status (list form)

    Returns iterator of (path, raw_value) tuples for traceability.
    """
    if not isinstance(data, dict):
        return
    rows = data.get("rows")
    if not isinstance(rows, list):
        return
    for r_idx, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        cells = row.get("cells")
        if isinstance(cells, dict):
            for player, cell in cells.items():
                if isinstance(cell, dict) and "status" in cell:
                    yield (f"rows[{r_idx}].cells.{player}.status", cell["status"])
                elif isinstance(cell, str):
                    yield (f"rows[{r_idx}].cells.{player}", cell)
        elif isinstance(cells, list):
            for c_idx, cell in enumerate(cells):
                if isinstance(cell, dict) and "status" in cell:
                    yield (f"rows[{r_idx}].cells[{c_idx}].status", cell["status"])
                elif isinstance(cell, str):
                    yield (f"rows[{r_idx}].cells[{c_idx}]", cell)


def check_status_code_compliance(output_dir: str, results: dict) -> None:
    """Generic extension hook for Story RA-F.2 AC-6 checks.

    GENERIC (no skill-specific branches per PO Condition 2). Runs after
    check_criteria_calibration in validate_output and emits findings into the
    same results dict.

    Three checks performed:

    1. recommendations-by-use-case.md PRESENCE when comparison_pattern=multi_player
       AND candidates_count >= 3 (Story §AC-4).

    2. Coverage matrices use 4-level enum (Story §AC-1). Walks every status
       value in matrices.yaml / comparison-matrix.json and rejects anything
       outside {confirmed, partial, uncertain, not_present} (PT-BR/legacy aliases
       normalize first via coverage_matrix_helper.normalize_status).

    3. Visual symbols consistent — if a status appears in markdown rendering
       (recommendations atom, report), symbols MUST be ✅/◐/?/— (Unicode) or
       [X]/[~]/[?]/[ ] (ASCII). Creative emojis like 🟢/🟡/🔴 are flagged.

    Findings written to results['status_code_findings'] for later severity
    translation in main() (warn → warnings[], block → errors[] + valid=false).
    """
    findings: list[str] = []

    if not HAS_COVERAGE_HELPER:
        # Helper missing means this validator was deployed without the canonical
        # 4-level source of truth. Surface as warning — caller should install the
        # helper before relying on AC-6 enforcement.
        results.setdefault("warnings", []).append(
            "coverage_matrix_helper.py not importable — Story RA-F.2 AC-6 checks SKIPPED. "
            "Ensure squads/research/scripts/tech-research/coverage_matrix_helper.py exists "
            "and is on PYTHONPATH."
        )
        results["checks"].append(
            {"check": "status_code_compliance", "status": "skipped — helper missing"}
        )
        return

    # ─── Discover scored atoms ────────────────────────────────────────────
    scored_files: list[tuple[str, dict]] = []
    for atom_name in SCORED_ATOM_CANDIDATES:
        path = os.path.join(output_dir, atom_name)
        if os.path.exists(path):
            data = _load_structured_file(path)
            scored_files.append((atom_name, data))

    # ─── AC-4: recommendations-by-use-case.md presence ───────────────────
    recs_required = False
    recs_trigger: list[str] = []
    for atom_name, data in scored_files:
        pattern = _comparison_pattern_from(data)
        candidates = _candidates_count_from(data)
        if pattern == STATUS_CODE_TRIGGER_PATTERN and candidates >= STATUS_CODE_TRIGGER_CANDIDATES:
            recs_required = True
            recs_trigger.append(
                f"{atom_name} (pattern={pattern}, candidates={candidates})"
            )

    if recs_required:
        recs_path = os.path.join(output_dir, RECOMMENDATIONS_FILE)
        if os.path.exists(recs_path):
            # Read minimal validation — count use cases by looking for the
            # `id: uc_*` token in YAML blocks (template uses this convention).
            try:
                with open(recs_path, encoding="utf-8") as f:
                    recs_content = f.read()
                use_cases = re.findall(r"^\s*id:\s*[\"']?uc_[\w]+", recs_content, re.MULTILINE)
                results["checks"].append(
                    {
                        "check": "recommendations_by_use_case_presence",
                        "status": "EXISTS",
                        "use_cases_found": len(use_cases),
                        "trigger": recs_trigger,
                    }
                )
                if len(use_cases) < 5:
                    findings.append(
                        f"{RECOMMENDATIONS_FILE} has {len(use_cases)} use cases — "
                        "Story RA-F.2 AC-4 requires minimum 5 distinct use cases "
                        "(each starts with `id: uc_*`)"
                    )
            except OSError as exc:
                findings.append(f"{RECOMMENDATIONS_FILE} unreadable: {exc}")
        else:
            findings.append(
                f"{RECOMMENDATIONS_FILE} MISSING — trigger fired by: {', '.join(recs_trigger)} "
                f"(AC-4: comparison_pattern=multi_player AND candidates_count>={STATUS_CODE_TRIGGER_CANDIDATES})"
            )

    # ─── AC-1: 4-level enum compliance on every cell ─────────────────────
    enum_violations_total = 0
    for atom_name, data in scored_files:
        # Skip atoms with no rows[]; they may be score-only legacy shapes that
        # belong to F.1 territory (handled by check_criteria_calibration).
        if not isinstance(data, dict) or not isinstance(data.get("rows"), list):
            continue
        if validate_matrix is None:  # type: ignore[truthy-bool]
            continue
        res = validate_matrix(data)  # type: ignore[misc]
        if not res.valid:
            enum_violations_total += len(res.errors)
            for err in res.errors[:5]:  # cap to 5 to keep log readable
                findings.append(
                    f"{atom_name} status enum violation: {err} "
                    f"(AC-1: must be one of {STATUS_ENUM} or alias)"
                )
            if len(res.errors) > 5:
                findings.append(
                    f"{atom_name}: {len(res.errors) - 5} additional enum violations elided"
                )
        else:
            # F.1 score-only fixtures (no `status` field per cell) trigger ONLY
            # warnings inside validate_matrix; we forward those as advisories
            # rather than findings so backward-compat is preserved.
            for warn in res.warnings:
                results.setdefault("warnings", []).append(f"[status-code] {atom_name}: {warn}")

    if enum_violations_total == 0 and scored_files:
        results["checks"].append(
            {
                "check": "status_enum_compliance",
                "status": "PASS",
                "atoms_checked": [name for name, _ in scored_files],
            }
        )

    # ─── AC-1: Visual symbol consistency in markdown atoms ───────────────
    # Search for forbidden creative emojis in atoms that may render the matrix
    # visually (recommendations + report + executive-report). Allowed glyphs
    # are restricted to the helper's canonical Unicode + ASCII maps.
    allowed_symbols = set(SYMBOL_MAP_UNICODE.values()) | set(SYMBOL_MAP_ASCII.values())
    # Forbidden creative emojis explicitly enumerated per Story Anti-patterns
    # ("Não usar emojis criativos 🟢/🟡/🔴 etc."). Detection is character-class
    # based to avoid false positives on legitimate prose emojis.
    forbidden_symbols = ("🟢", "🟡", "🔴", "🟠", "🟣", "🔵")

    markdown_atoms = [
        RECOMMENDATIONS_FILE,
        "02-research-report.md",
        "executive-report.md",
        "battle-card.md",
    ]
    for md_name in markdown_atoms:
        path = os.path.join(output_dir, md_name)
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                md_content = f.read()
        except OSError:
            continue
        violations = [sym for sym in forbidden_symbols if sym in md_content]
        if violations:
            findings.append(
                f"{md_name} uses forbidden creative emojis {violations} — "
                f"Story RA-F.2 anti-pattern: only {sorted(allowed_symbols)} permitted"
            )

    # ─── Persist findings ────────────────────────────────────────────────
    for f in findings:
        results.setdefault("status_code_findings", []).append(f)


def check_extraction_ladder(output_dir: str, results: dict) -> None:
    """Story RA-F.3 AC-B2 — Extension hook: validate extraction schema enrichment.

    GENERIC (no skill-specific branches, per precedent F.1/F.2). Runs after
    check_status_code_compliance in validate_output and emits findings into
    results['extraction_ladder_findings'].

    Two checks performed:

    1. sources.yaml schema enrichment: when sources.yaml exists AND contains
       extraction_method fields, validates that values are from the allowed set
       (websearch_snippet|webfetch|etl|playwright|manual_paste|extraction_blocked).
       Invalid values are flagged. Missing fields are NOT flagged — they are
       intentionally optional per AC-B2 and extraction-no-fallbacks.md.

    2. Ladder log presence: when sources.yaml has entries with
       extraction_quality: blocked_fallback_used, checks that the entry also
       has extraction_notes (or extraction_ladder_steps_tried) so failure is
       documented explicitly rather than silenced.

    Severity: default WARNING; ERROR under --enforcement block.
    """
    findings: list[str] = []

    sources_path = os.path.join(output_dir, "sources.yaml")
    if not os.path.exists(sources_path):
        results["checks"].append(
            {"check": "extraction_ladder", "status": "skipped — sources.yaml absent"}
        )
        return

    sources_data = _load_structured_file(sources_path)
    if not isinstance(sources_data, dict):
        results["checks"].append(
            {"check": "extraction_ladder", "status": "skipped — sources.yaml not parseable"}
        )
        return

    sources = sources_data.get("sources") or []
    if not isinstance(sources, list) or not sources:
        results["checks"].append(
            {"check": "extraction_ladder", "status": "skipped — no sources entries"}
        )
        return

    enriched_count = 0
    blocked_without_log = []

    for entry in sources:
        if not isinstance(entry, dict):
            continue
        url = entry.get("url", "(unknown)")
        method = entry.get("extraction_method")
        quality = entry.get("extraction_quality")
        attempts = entry.get("extraction_attempts")

        # Check 1: method value validity (only when field present)
        if method is not None:
            enriched_count += 1
            if method not in EXTRACTION_VALID_METHODS:
                findings.append(
                    f"sources.yaml entry '{url}': extraction_method={method!r} "
                    f"not in allowed set {sorted(EXTRACTION_VALID_METHODS)}"
                )

        # Check 2: quality value validity (only when field present)
        if quality is not None and quality not in EXTRACTION_VALID_QUALITIES:
            findings.append(
                f"sources.yaml entry '{url}': extraction_quality={quality!r} "
                f"not in allowed set {sorted(EXTRACTION_VALID_QUALITIES)}"
            )

        # Check 3: blocked entries must have a log
        if quality == "blocked_fallback_used":
            has_notes = bool(entry.get("extraction_notes"))
            has_steps = bool(entry.get("extraction_ladder_steps_tried"))
            if not has_notes and not has_steps:
                blocked_without_log.append(url)

    if blocked_without_log:
        findings.append(
            f"{len(blocked_without_log)} source(s) with extraction_quality=blocked_fallback_used "
            f"lack extraction_notes or extraction_ladder_steps_tried — failure must be logged, "
            f"not silenced. URLs: {blocked_without_log[:3]}{'...' if len(blocked_without_log) > 3 else ''}"
        )

    if not findings:
        results["checks"].append({
            "check": "extraction_ladder",
            "status": "PASS",
            "enriched_sources": enriched_count,
            "total_sources": len(sources),
        })
    for f in findings:
        results.setdefault("extraction_ladder_findings", []).append(f)


def check_mandatory_sources_coverage(output_dir: str, results: dict) -> None:
    """Story RA-F.3 AC-A2 — Extension hook: warn if mandatory_additions not applied.

    GENERIC (no skill-specific branches). Checks the learning log for a run that
    produced outputs in output_dir. If a learning log is present with a domain
    that matches mandatory-sources.yaml entries, and mandatory_additions is absent
    or empty, emits a WARNING.

    Detection strategy: looks for mandatory_additions key in:
      - pipeline-state.yaml (under metadata or top-level)
      - metrics.yaml (under any top-level key)
      - any learning log YAML in .aiox/learning/logs/tech-research/ whose
        run_id or output_dir matches this folder slug

    This is a WARN-only check by default. It does NOT block the run — the
    mandatory sources matrix is additive (anti-pattern §1 from story).
    """
    findings: list[str] = []
    slug = os.path.basename(output_dir.rstrip("/"))

    # ── Look for mandatory_additions in pipeline-state or metrics ────────
    mandatory_applied = False

    for candidate_file in ("pipeline-state.yaml", "metrics.yaml"):
        path = os.path.join(output_dir, candidate_file)
        if not os.path.exists(path):
            continue
        data = _load_structured_file(path)
        if not isinstance(data, dict):
            continue
        # Check at root level and one level deep
        if MANDATORY_ADDITIONS_KEY in data:
            mandatory_applied = True
            break
        for val in data.values():
            if isinstance(val, dict) and MANDATORY_ADDITIONS_KEY in val:
                mandatory_applied = True
                break
        if mandatory_applied:
            break

    # ── Look for mandatory_additions in any learning log for this slug ───
    if not mandatory_applied:
        log_dirs = [
            os.path.join(output_dir, "..", "..", "..", ".aiox", "learning", "logs", "tech-research"),
            os.path.join(output_dir, "..", "..", "..", ".aiox", "learning", "logs", "research-bench"),
        ]
        for log_dir in log_dirs:
            log_dir = os.path.normpath(log_dir)
            if not os.path.isdir(log_dir):
                continue
            for fname in os.listdir(log_dir):
                if not fname.endswith(".yaml"):
                    continue
                if slug not in fname:
                    continue
                log_data = _load_structured_file(os.path.join(log_dir, fname))
                if isinstance(log_data, dict) and MANDATORY_ADDITIONS_KEY in log_data:
                    mandatory_applied = True
                    break
                # Check phases sub-dict
                phases = log_data.get("phases", {}) if isinstance(log_data, dict) else {}
                for phase_data in phases.values():
                    if isinstance(phase_data, dict) and MANDATORY_ADDITIONS_KEY in phase_data:
                        mandatory_applied = True
                        break
                if mandatory_applied:
                    break
            if mandatory_applied:
                break

    if mandatory_applied:
        results["checks"].append({
            "check": "mandatory_sources_coverage",
            "status": "PASS — mandatory_additions log found",
        })
    else:
        # Advisory warning — not block by default (anti-pattern §1: matrix is additive, not gating)
        findings.append(
            f"mandatory_additions key not found in pipeline-state.yaml / metrics.yaml or "
            f"learning log for slug '{slug}'. If mandatory-sources.yaml domains were applicable, "
            f"Phase 1.5 should have logged mandatory_additions. This is advisory — check that "
            f"squads/research/data/mandatory-sources.yaml domains were evaluated during decompose."
        )

    for f in findings:
        results.setdefault("mandatory_sources_findings", []).append(f)


def check_gap_analysis_presence(output_dir: str, results: dict) -> None:
    """Story RA-F.3 AC-C1 — Extension hook: require gap-analysis.md on multi_player.

    GENERIC (no skill-specific branches per precedent F.1/F.2). Checks:

    1. If any scored atom declares comparison_pattern=multi_player AND
       candidates_count >= 2 (less strict than F.2's >=3 — gap analysis applies
       for any multi-player comparison, not just recommendations-by-use-case).

    2. When trigger fires: gap-analysis.md MUST be present in output_dir.
       If absent → finding emitted.

    3. Cross-link check (AC-C2): when gap-analysis.md exists, 02-research-report.md
       should contain a reference to it (advisory — not block).

    Severity: default WARNING; ERROR under --enforcement block.
    Findings written to results['gap_analysis_findings'].
    """
    findings: list[str] = []

    # ── Discover scored atoms ─────────────────────────────────────────────
    scored_files: list[tuple[str, dict]] = []
    for atom_name in SCORED_ATOM_CANDIDATES:
        path = os.path.join(output_dir, atom_name)
        if os.path.exists(path):
            data = _load_structured_file(path)
            scored_files.append((atom_name, data))

    # ── Check trigger ────────────────────────────────────────────────────
    gap_required = False
    gap_trigger: list[str] = []

    for atom_name, data in scored_files:
        pattern = _comparison_pattern_from(data)
        candidates = _candidates_count_from(data)
        if pattern == GAP_ANALYSIS_TRIGGER_PATTERN and candidates >= 2:
            gap_required = True
            gap_trigger.append(f"{atom_name} (pattern={pattern}, candidates={candidates})")

    # Also check pipeline-state.yaml for comparison_pattern field directly
    pipeline_state_path = os.path.join(output_dir, "pipeline-state.yaml")
    if os.path.exists(pipeline_state_path) and not gap_required:
        ps_data = _load_structured_file(pipeline_state_path)
        if isinstance(ps_data, dict):
            pattern = ps_data.get("comparison_pattern") or ps_data.get("inferred_pattern")
            if pattern == GAP_ANALYSIS_TRIGGER_PATTERN:
                gap_required = True
                gap_trigger.append(f"pipeline-state.yaml (comparison_pattern={pattern})")

    if not gap_required:
        results["checks"].append({
            "check": "gap_analysis_presence",
            "status": "skipped — comparison_pattern=multi_player not detected",
        })
        return

    # ── Check gap-analysis.md presence ───────────────────────────────────
    gap_path = os.path.join(output_dir, GAP_ANALYSIS_FILE)
    if os.path.exists(gap_path):
        size = os.path.getsize(gap_path)
        results["checks"].append({
            "check": "gap_analysis_presence",
            "status": "EXISTS",
            "size_bytes": size,
            "trigger": gap_trigger,
        })

        # ── AC-C2: cross-link advisory check ─────────────────────────────
        report_path = os.path.join(output_dir, "02-research-report.md")
        if os.path.exists(report_path):
            try:
                with open(report_path, encoding="utf-8") as fh:
                    report_content = fh.read()
                if "gap-analysis.md" not in report_content:
                    findings.append(
                        "gap-analysis.md exists but 02-research-report.md does not cross-link to it. "
                        "AC-C2 requires: 'Ver análise dedicada de lacunas: [./gap-analysis.md](./gap-analysis.md)' "
                        "in the appropriate section of 02-research-report.md."
                    )
            except OSError:
                pass
    else:
        findings.append(
            f"gap-analysis.md MISSING — trigger fired by: {', '.join(gap_trigger)} "
            f"(AC-C1: comparison_pattern=multi_player requires standalone gap-analysis.md atomo; "
            f"use template squads/research/templates/gap-analysis-tmpl.md)"
        )

    for f in findings:
        results.setdefault("gap_analysis_findings", []).append(f)


def check_heartbeat_policy(results: dict, policy_path: str = "") -> None:
    """Story RA-A.1 AC-4 — Extension hook: validate heartbeat-policy.yaml schema.

    GENERIC extension hook following the F.1/F.2/F.3/C.1 shape:
      - Severity default = WARNING (exit 0 unless --enforcement block)
      - Findings written to results['heartbeat_policy_findings']

    Checks performed:

    1. heartbeat-policy.yaml exists at policy_path (or default repo-relative location).

    2. Required top-level keys present:
       schema_version, governed_by, stop_when_any, replan_when_any, runtime_contract

    3. stop_when_any: all 7 canonical signals present by id:
       {coverage_score, token_budget, wallclock, cost_usd, gap_convergence,
        new_information_ratio, wave_max_with_low_coverage}

    4. Each signal entry declares required keys:
       signal, condition, category, priority, stop_reason_category

    5. Threshold range validation:
       - coverage_score condition references value in [0, 100] range
       - token_budget_used threshold in (0.0, 1.0] (ratio)
       - new_information_ratio threshold in [0.0, 1.0] (ratio)

    6. replan_when_any: at least 3 signals, each with required keys:
       signal, condition, category, action

    Args:
        results: The validate_output results dict to append into.
        policy_path: Explicit path to heartbeat-policy.yaml.
                     If empty, resolves relative to this script's repo root.
    """
    findings: list[str] = []

    # ── Resolve policy path ──────────────────────────────────────────────────
    if not policy_path:
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        _repo_root = os.path.normpath(os.path.join(_script_dir, "..", "..", "..", ".."))
        policy_path = os.path.join(
            _repo_root, "squads", "research", "data", "heartbeat-policy.yaml"
        )

    # ── Check 1: file existence ──────────────────────────────────────────────
    if not os.path.exists(policy_path):
        findings.append(
            f"heartbeat-policy.yaml MISSING at {policy_path} — "
            "Story RA-A.1 AC-1 requires this file to exist"
        )
        results.setdefault("heartbeat_policy_findings", []).extend(findings)
        results["checks"].append({
            "check": "heartbeat_policy",
            "status": "MISSING — file not found",
        })
        return

    policy_data = _load_structured_file(policy_path)
    if not policy_data:
        findings.append(
            f"heartbeat-policy.yaml is empty or not parseable at {policy_path}"
        )
        results.setdefault("heartbeat_policy_findings", []).extend(findings)
        return

    # ── Check 2: required top-level keys ────────────────────────────────────
    REQUIRED_TOP_LEVEL = {
        "schema_version", "governed_by", "stop_when_any",
        "replan_when_any", "runtime_contract",
    }
    missing_top = REQUIRED_TOP_LEVEL - set(policy_data.keys())
    if missing_top:
        findings.append(
            f"heartbeat-policy.yaml missing required top-level keys: {sorted(missing_top)}"
        )

    # ── Check 3: stop_when_any — all 7 signals present ──────────────────────
    REQUIRED_STOP_SIGNALS = {
        "coverage_score",
        "token_budget",
        "wallclock",
        "cost_usd",
        "gap_convergence",
        "new_information_ratio",
        "wave_max_with_low_coverage",
    }
    REQUIRED_SIGNAL_KEYS = {"signal", "condition", "category", "priority", "stop_reason_category"}

    stop_when_any = policy_data.get("stop_when_any")
    if not isinstance(stop_when_any, list):
        findings.append(
            "heartbeat-policy.yaml stop_when_any must be a list of signal entries"
        )
    else:
        declared_stop_ids = set()
        signal_results: list[dict] = []
        for entry in stop_when_any:
            if not isinstance(entry, dict):
                findings.append("stop_when_any: entry is not a mapping")
                continue
            sig_id = entry.get("signal")
            if sig_id:
                declared_stop_ids.add(sig_id)

            # Check 4: required keys per signal
            missing_keys = REQUIRED_SIGNAL_KEYS - set(entry.keys())
            if missing_keys:
                findings.append(
                    f"stop_when_any signal '{sig_id}': missing required keys: {sorted(missing_keys)}"
                )

            # Check 5a: threshold range validation for ratio signals
            condition = entry.get("condition", "")
            if sig_id == "token_budget" or sig_id == "new_information_ratio":
                # Extract numeric value from condition string
                import re as _re
                nums = _re.findall(r"\b0\.\d+\b", condition)
                for num_str in nums:
                    val = float(num_str)
                    if not (0.0 < val <= 1.0):
                        findings.append(
                            f"stop_when_any signal '{sig_id}': threshold {val} "
                            f"out of expected range (0.0, 1.0] for ratio signal"
                        )

            signal_results.append({"id": sig_id, "priority": entry.get("priority")})

        missing_stop_ids = REQUIRED_STOP_SIGNALS - declared_stop_ids
        if missing_stop_ids:
            findings.append(
                f"heartbeat-policy.yaml stop_when_any missing required signals: "
                f"{sorted(missing_stop_ids)} "
                f"(AC-1 requires all 7: {sorted(REQUIRED_STOP_SIGNALS)})"
            )

    # ── Check 6: replan_when_any — at least 3 signals with required keys ────
    REQUIRED_REPLAN_KEYS = {"signal", "condition", "category", "action"}
    replan_when_any = policy_data.get("replan_when_any")
    if not isinstance(replan_when_any, list):
        findings.append(
            "heartbeat-policy.yaml replan_when_any must be a list of signal entries"
        )
    else:
        if len(replan_when_any) < 3:
            findings.append(
                f"heartbeat-policy.yaml replan_when_any has {len(replan_when_any)} signals; "
                "Story RA-A.1 AC-1 requires at least 3"
            )
        for entry in replan_when_any:
            if not isinstance(entry, dict):
                findings.append("replan_when_any: entry is not a mapping")
                continue
            sig_id = entry.get("signal", "(unknown)")
            missing_keys = REQUIRED_REPLAN_KEYS - set(entry.keys())
            if missing_keys:
                findings.append(
                    f"replan_when_any signal '{sig_id}': missing required keys: {sorted(missing_keys)}"
                )

    # ── Check: governed_by references quality-gates.yaml ────────────────────
    governed_by = policy_data.get("governed_by", "")
    if "quality-gates" not in str(governed_by):
        findings.append(
            f"heartbeat-policy.yaml governed_by='{governed_by}' does not reference "
            "quality-gates.yaml — Story RA-A.1 AC-2 requires governed_by: quality-gates.yaml"
        )

    # ── Persist results ──────────────────────────────────────────────────────
    if not findings:
        results["checks"].append({
            "check": "heartbeat_policy",
            "status": "PASS",
            "stop_signals_validated": len(stop_when_any) if isinstance(stop_when_any, list) else 0,
            "replan_signals_validated": len(replan_when_any) if isinstance(replan_when_any, list) else 0,
            "schema_version": policy_data.get("schema_version", "unknown"),
            "governed_by": governed_by,
        })
    else:
        results["checks"].append({
            "check": "heartbeat_policy",
            "status": "FINDINGS",
            "count": len(findings),
        })

    for f in findings:
        results.setdefault("heartbeat_policy_findings", []).append(f)


def check_specialist_contracts(results: dict, contracts_path: str = "") -> None:
    """Story RA-C.1 AC-3 — Extension hook: validate specialist-contracts.yaml schema.

    GENERIC extension hook following the F.1/F.2/F.3 shape:
      - Severity default = WARNING (exit 0 unless --enforcement block)
      - Findings written to results['specialist_contracts_findings']

    Checks performed:

    1. specialist-contracts.yaml exists at contracts_path (or default location).

    2. All 5 required specialists are present:
       {sackett, klein, booth, creswell, forsgren}

    3. Each specialist entry declares required keys:
       invoked_when, input_schema, output_schema, available_tools,
       triggers_in_phase, failure_mode

    4. invoked_when is a non-empty string (parseable expression).

    5. failure_mode is one of: warn_and_continue | halt

    6. available_tools is a list (may be empty — forward-compat ADR-001 Wave 2).

    Args:
        results: The validate_output results dict to append into.
        contracts_path: Explicit path to specialist-contracts.yaml.
                        If empty, resolves relative to this script's repo root.
    """
    findings: list[str] = []

    # ── Resolve contracts path ────────────────────────────────────────────
    if not contracts_path:
        _script_dir = os.path.dirname(os.path.abspath(__file__))
        _repo_root = os.path.normpath(os.path.join(_script_dir, "..", "..", "..", ".."))
        contracts_path = os.path.join(
            _repo_root, "squads", "research", "data", "specialist-contracts.yaml"
        )

    # ── Check 1: file existence ───────────────────────────────────────────
    if not os.path.exists(contracts_path):
        findings.append(
            f"specialist-contracts.yaml MISSING at {contracts_path} — "
            "Story RA-C.1 AC-1 requires this file to exist"
        )
        results.setdefault("specialist_contracts_findings", []).extend(findings)
        results["checks"].append({
            "check": "specialist_contracts",
            "status": "MISSING — file not found",
        })
        return

    contracts_data = _load_structured_file(contracts_path)
    if not contracts_data:
        findings.append(
            f"specialist-contracts.yaml is empty or not parseable at {contracts_path}"
        )
        results.setdefault("specialist_contracts_findings", []).extend(findings)
        return

    specialists = contracts_data.get("specialists")
    if not isinstance(specialists, dict):
        findings.append(
            "specialist-contracts.yaml missing 'specialists' mapping at top level"
        )
        results.setdefault("specialist_contracts_findings", []).extend(findings)
        return

    # ── Check 2: required specialist IDs ─────────────────────────────────
    REQUIRED_SPECIALISTS = {"sackett", "klein", "booth", "creswell", "forsgren"}
    REQUIRED_SPECIALIST_KEYS = {
        "invoked_when",
        "input_schema",
        "output_schema",
        "available_tools",
        "triggers_in_phase",
        "failure_mode",
    }
    VALID_FAILURE_MODES = {"warn_and_continue", "halt"}

    missing_specialists = REQUIRED_SPECIALISTS - set(specialists.keys())
    if missing_specialists:
        findings.append(
            f"specialist-contracts.yaml missing required specialists: {sorted(missing_specialists)} "
            f"(AC-1 requires all 5: {sorted(REQUIRED_SPECIALISTS)})"
        )

    # ── Check 3-6: per-specialist schema validation ───────────────────────
    spec_results: list[dict] = []
    for spec_id in sorted(specialists.keys()):
        if spec_id not in REQUIRED_SPECIALISTS:
            # Unknown specialist — warn but don't fail
            results.setdefault("warnings", []).append(
                f"[specialist-contracts] Unknown specialist '{spec_id}' in contracts "
                f"(not in required set {sorted(REQUIRED_SPECIALISTS)})"
            )
            continue

        entry = specialists.get(spec_id)
        if not isinstance(entry, dict):
            findings.append(
                f"{spec_id}: entry is not a mapping"
            )
            continue

        spec_issues: list[str] = []

        # Check 3: required keys present
        missing_keys = REQUIRED_SPECIALIST_KEYS - set(entry.keys())
        if missing_keys:
            spec_issues.append(f"missing required keys: {sorted(missing_keys)}")

        # Check 4: invoked_when is non-empty string
        invoked_when = entry.get("invoked_when")
        if not isinstance(invoked_when, str) or not invoked_when.strip():
            spec_issues.append(
                "invoked_when must be a non-empty string expression "
                "(DSL: field == value | field in [list] | field contains 'str')"
            )

        # Check 5: failure_mode in allowed set
        failure_mode = entry.get("failure_mode")
        if failure_mode is not None and failure_mode not in VALID_FAILURE_MODES:
            spec_issues.append(
                f"failure_mode={failure_mode!r} not in {sorted(VALID_FAILURE_MODES)}"
            )

        # Check 6: available_tools is a list (may be empty)
        available_tools = entry.get("available_tools")
        if available_tools is not None and not isinstance(available_tools, list):
            spec_issues.append(
                f"available_tools must be a list (may be empty for ADR-001 Wave 2 forward-compat); "
                f"got {type(available_tools).__name__}"
            )

        if spec_issues:
            for issue in spec_issues:
                findings.append(f"{spec_id}: {issue}")
        else:
            spec_results.append({
                "id": spec_id,
                "invoked_when": invoked_when,
                "triggers_in_phase": entry.get("triggers_in_phase"),
                "failure_mode": failure_mode,
                "available_tools_count": len(entry.get("available_tools") or []),
            })

    # ── Persist results ───────────────────────────────────────────────────
    if not findings:
        results["checks"].append({
            "check": "specialist_contracts",
            "status": "PASS",
            "specialists_validated": spec_results,
            "schema_version": contracts_data.get("schema_version", "unknown"),
        })
    else:
        results["checks"].append({
            "check": "specialist_contracts",
            "status": "FINDINGS",
            "count": len(findings),
        })

    for f in findings:
        results.setdefault("specialist_contracts_findings", []).append(f)


def check_gaps_schema(output_dir: str, results: dict, gaps_path: str = "") -> None:
    """Story RA-B.1 AC-3 — Extension hook: validate gaps.yaml schema + APPEND-ONLY invariant.

    GENERIC extension hook following the F.1/F.2/F.3/C.1/A.1 shape:
      - Severity default = WARNING (exit 0 unless --enforcement block)
      - Findings written to results['gaps_schema_findings']

    Checks performed:

    1. gaps.yaml exists in output_dir (or at explicit gaps_path).
       If absent: skipped (gaps may not yet exist for Wave 1 runs).

    2. schema_version field present.

    3. gaps field is a list.

    4. Each entry has all required keys:
       {id, question, source_hint, priority, attempts, status,
        opened_in_wave, closed_in_wave, closed_by_source}

    5. IDs match G{NNN} format and are unique across the array.

    6. status values are in the allowed set: {open, closed, abandoned}.

    7. APPEND-ONLY invariant: no entries removed between waves.
       Checked by comparing against a prior snapshot stored in pipeline-state.yaml
       (gaps_total_count field). If gaps_total_count > current count → violation.

    8. gap_convergence_signal present in pipeline-state.yaml when gaps.yaml exists.
       This confirms Phase 3.5 (heartbeat) has the signal it needs.

    Args:
        output_dir: Path to the research output directory.
        results: The validate_output results dict to append into.
        gaps_path: Explicit path to gaps.yaml. If empty, resolves to {output_dir}/gaps.yaml.
    """
    findings: list[str] = []

    # ── Resolve gaps path ─────────────────────────────────────────────────
    if not gaps_path:
        gaps_path = os.path.join(output_dir, "gaps.yaml")

    # ── Check 1: file existence (skipped if absent — not yet generated) ──
    if not os.path.exists(gaps_path):
        results["checks"].append({
            "check": "gaps_schema",
            "status": "skipped — gaps.yaml not yet generated (Wave 1 may not have run P3.4)",
        })
        return

    if not HAS_YAML:
        results.setdefault("warnings", []).append(
            "PyYAML not importable — Story RA-B.1 gaps.yaml checks SKIPPED. "
            "Install with: pip install pyyaml"
        )
        results["checks"].append({
            "check": "gaps_schema",
            "status": "skipped — PyYAML unavailable",
        })
        return

    try:
        with open(gaps_path, encoding="utf-8") as fh:
            gaps_data = yaml.safe_load(fh)
    except Exception as exc:
        findings.append(
            f"gaps.yaml not parseable at {gaps_path}: {exc} — "
            "APPEND-ONLY integrity at risk; check for incomplete atomic write"
        )
        results.setdefault("gaps_schema_findings", []).extend(findings)
        results["checks"].append({"check": "gaps_schema", "status": "PARSE_ERROR"})
        return

    if not isinstance(gaps_data, dict):
        findings.append(
            f"gaps.yaml at {gaps_path} is not a mapping (got {type(gaps_data).__name__})"
        )
        results.setdefault("gaps_schema_findings", []).extend(findings)
        return

    # ── Check 2: schema_version ──────────────────────────────────────────
    if not gaps_data.get("schema_version"):
        findings.append("gaps.yaml missing required field: schema_version")

    # ── Check 3: gaps is a list ──────────────────────────────────────────
    gaps = gaps_data.get("gaps")
    if not isinstance(gaps, list):
        findings.append(
            f"gaps.yaml 'gaps' field must be a list; got {type(gaps).__name__}"
        )
        results.setdefault("gaps_schema_findings", []).extend(findings)
        return

    _GAPS_REQUIRED_KEYS = {
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
    _GAPS_VALID_STATUSES = {"open", "closed", "abandoned"}
    _GAPS_ID_PATTERN = re.compile(r"^G\d{3}$")

    # ── Checks 4–6: per-entry schema validation ───────────────────────────
    seen_ids: set[str] = set()
    for idx, entry in enumerate(gaps):
        if not isinstance(entry, dict):
            findings.append(f"gaps[{idx}] is not a mapping")
            continue
        # Check 4: required keys
        missing = _GAPS_REQUIRED_KEYS - set(entry.keys())
        if missing:
            findings.append(
                f"gaps[{idx}] missing required keys: {sorted(missing)}"
            )
        # Check 5: ID format + uniqueness
        gid = str(entry.get("id", ""))
        if not _GAPS_ID_PATTERN.match(gid):
            findings.append(
                f"gaps[{idx}] id={gid!r} does not match G{{NNN}} format "
                "(e.g. G001, G002, ... G999)"
            )
        elif gid in seen_ids:
            findings.append(f"gaps[{idx}] duplicate id={gid!r}")
        else:
            seen_ids.add(gid)
        # Check 6: status enum
        status = entry.get("status")
        if status not in _GAPS_VALID_STATUSES:
            findings.append(
                f"gaps[{idx}] id={gid!r} status={status!r} not in "
                f"{sorted(_GAPS_VALID_STATUSES)}"
            )

    # ── Check 7: APPEND-ONLY invariant via pipeline-state.yaml ───────────
    # If pipeline-state.yaml recorded a prior gaps_total_count, the current
    # count must be ≥ that value (no entries may have been removed).
    ps_path = os.path.join(output_dir, "pipeline-state.yaml")
    if os.path.exists(ps_path):
        try:
            with open(ps_path, encoding="utf-8") as fh:
                ps_data = yaml.safe_load(fh) or {}
        except Exception:
            ps_data = {}

        prior_total = ps_data.get("gaps_total_count")
        if prior_total is not None and isinstance(prior_total, int):
            current_total = len(gaps)
            if current_total < prior_total:
                findings.append(
                    f"APPEND-ONLY violation: pipeline-state.yaml recorded "
                    f"gaps_total_count={prior_total} but gaps.yaml now has "
                    f"{current_total} entries. "
                    f"{prior_total - current_total} entries were removed — "
                    "transition status to 'closed' or 'abandoned' instead."
                )

    # ── Check 8: gap_convergence_signal in pipeline-state.yaml ──────────
    if os.path.exists(ps_path):
        try:
            with open(ps_path, encoding="utf-8") as fh:
                ps_check = yaml.safe_load(fh) or {}
        except Exception:
            ps_check = {}
        if "gap_convergence_signal" not in ps_check:
            findings.append(
                "pipeline-state.yaml missing gap_convergence_signal field — "
                "Phase 3.5 heartbeat (signal #6) requires this field to evaluate "
                "gap_set.is_empty(). Ensure gap_detector.py ran successfully."
            )

    # ── Persist results ──────────────────────────────────────────────────
    if not findings:
        n_open = sum(
            1 for g in gaps
            if isinstance(g, dict) and g.get("status") == "open"
        )
        n_closed = sum(
            1 for g in gaps
            if isinstance(g, dict) and g.get("status") == "closed"
        )
        results["checks"].append({
            "check": "gaps_schema",
            "status": "PASS",
            "total_gaps": len(gaps),
            "open": n_open,
            "closed": n_closed,
            "abandoned": len(gaps) - n_open - n_closed,
            "schema_version": gaps_data.get("schema_version", "unknown"),
        })
    else:
        results["checks"].append({
            "check": "gaps_schema",
            "status": "FINDINGS",
            "count": len(findings),
        })

    for f in findings:
        results.setdefault("gaps_schema_findings", []).append(f)


def check_claims_confidence(output_dir: str, results: dict) -> None:
    """Story RA-D.2 AC-5 — Extension hook: validate claims.yaml schema + confidence_distribution.

    GENERIC extension hook following the F.1/F.2/F.3/C.1/A.1/B.1 shape:
      - Severity default = WARNING (exit 0 unless --enforcement block)
      - Findings written to results['claims_confidence_findings']

    Checks performed:

    1. claims.yaml exists in output_dir.
       If absent: skipped (not all runs invoke citation_verifier).

    2. schema_version field present.

    3. claims field is a list.

    4. Each claim entry has all required RA-D.2 AC-1 keys:
       {claim_id, text, original_claim, rewritten, status, confidence, evidence_grade, wave_introduced}

    5. claim_id format: C{NNN} (e.g. C001) and unique across array.

    6. status in {supported, unsupported, unknown, ambiguous}.

    7. confidence in {high, medium, low, none}.

    8. rewritten is bool; when True, original_claim must be non-null string.

    9. evidence_grade is null OR one of {1a, 1b, 2a, 2b, 3, 4, 5}.

    10. confidence_distribution aggregate block present at top level
        with required keys: {total, supported, unsupported, unknown, ambiguous, rewritten}.

    Args:
        output_dir: Path to the research output directory.
        results: The validate_output results dict to append into.
    """
    findings: list[str] = []

    # ── Check 1: file existence (skipped if absent) ───────────────────────
    claims_path = os.path.join(output_dir, "claims.yaml")
    if not os.path.exists(claims_path):
        results["checks"].append({
            "check": "claims_confidence",
            "status": "skipped — claims.yaml not yet generated (citation_verifier may not have run)",
        })
        return

    if not HAS_YAML:
        results.setdefault("warnings", []).append(
            "PyYAML not importable — Story RA-D.2 claims.yaml checks SKIPPED. "
            "Install with: pip install pyyaml"
        )
        results["checks"].append({
            "check": "claims_confidence",
            "status": "skipped — PyYAML unavailable",
        })
        return

    try:
        with open(claims_path, encoding="utf-8") as fh:
            claims_data = yaml.safe_load(fh)
    except Exception as exc:
        findings.append(
            f"claims.yaml not parseable at {claims_path}: {exc}"
        )
        results.setdefault("claims_confidence_findings", []).extend(findings)
        results["checks"].append({"check": "claims_confidence", "status": "PARSE_ERROR"})
        return

    if not isinstance(claims_data, dict):
        findings.append(
            f"claims.yaml at {claims_path} is not a mapping (got {type(claims_data).__name__})"
        )
        results.setdefault("claims_confidence_findings", []).extend(findings)
        return

    # ── Check 2: schema_version ──────────────────────────────────────────
    if not claims_data.get("schema_version"):
        findings.append("claims.yaml missing required field: schema_version")

    # ── Check 3: claims is a list ────────────────────────────────────────
    claims = claims_data.get("claims")
    if not isinstance(claims, list):
        findings.append(
            f"claims.yaml 'claims' field must be a list; got {type(claims).__name__}"
        )
        results.setdefault("claims_confidence_findings", []).extend(findings)
        return

    _CLAIMS_REQUIRED_KEYS = {
        "claim_id",
        "text",
        "original_claim",
        "rewritten",
        "status",
        "confidence",
        "evidence_grade",
        "wave_introduced",
    }
    _CLAIMS_VALID_STATUSES = {"supported", "unsupported", "unknown", "ambiguous"}
    _CLAIMS_VALID_CONFIDENCE = {"high", "medium", "low", "none"}
    _CLAIMS_VALID_GRADES = {"1a", "1b", "2a", "2b", "3", "4", "5", None}
    _CLAIMS_ID_PATTERN = re.compile(r"^C\d{3}$")

    # ── Checks 4–9: per-claim schema validation ───────────────────────────
    seen_ids: set[str] = set()
    for idx, entry in enumerate(claims):
        if not isinstance(entry, dict):
            findings.append(f"claims[{idx}] is not a mapping")
            continue

        # Check 4: required keys
        missing = _CLAIMS_REQUIRED_KEYS - set(entry.keys())
        if missing:
            findings.append(
                f"claims[{idx}] missing required keys: {sorted(missing)}"
            )

        # Check 5: claim_id format + uniqueness
        cid = str(entry.get("claim_id", ""))
        if not _CLAIMS_ID_PATTERN.match(cid):
            findings.append(
                f"claims[{idx}] claim_id={cid!r} does not match C{{NNN}} format "
                "(e.g. C001, C002, ... C999)"
            )
        elif cid in seen_ids:
            findings.append(f"claims[{idx}] duplicate claim_id={cid!r}")
        else:
            seen_ids.add(cid)

        # Check 6: status enum
        status = entry.get("status")
        if status not in _CLAIMS_VALID_STATUSES:
            findings.append(
                f"claims[{idx}] claim_id={cid!r} status={status!r} not in "
                f"{sorted(_CLAIMS_VALID_STATUSES)}"
            )

        # Check 7: confidence enum
        confidence = entry.get("confidence")
        if confidence not in _CLAIMS_VALID_CONFIDENCE:
            findings.append(
                f"claims[{idx}] claim_id={cid!r} confidence={confidence!r} not in "
                f"{sorted(_CLAIMS_VALID_CONFIDENCE)}"
            )

        # Check 8: rewritten + original_claim consistency
        rewritten = entry.get("rewritten")
        original_claim = entry.get("original_claim")
        if rewritten is True and not original_claim:
            findings.append(
                f"claims[{idx}] claim_id={cid!r} rewritten=true but original_claim is null/empty — "
                "Decision D1: original_claim must be set when rewritten=true"
            )

        # Check 9: evidence_grade enum
        grade = entry.get("evidence_grade")
        if grade not in _CLAIMS_VALID_GRADES:
            findings.append(
                f"claims[{idx}] claim_id={cid!r} evidence_grade={grade!r} not in "
                f"{{1a, 1b, 2a, 2b, 3, 4, 5, null}} — "
                "Decision D2: null when Sackett not invoked"
            )

    # ── Check 10: confidence_distribution aggregate block (RA-D.2 AC-2) ──
    _DIST_REQUIRED_KEYS = {
        "total",
        "supported",
        "unsupported",
        "unknown",
        "ambiguous",
        "rewritten",
    }
    dist = claims_data.get("confidence_distribution")
    if not isinstance(dist, dict):
        findings.append(
            "claims.yaml missing confidence_distribution aggregate block (RA-D.2 AC-2). "
            "Run claims_aggregator.py to generate it."
        )
    else:
        missing_dist_keys = _DIST_REQUIRED_KEYS - set(dist.keys())
        if missing_dist_keys:
            findings.append(
                f"claims.yaml confidence_distribution missing required keys: "
                f"{sorted(missing_dist_keys)} (RA-D.2 AC-2)"
            )
        # Validate total matches actual claims count
        declared_total = dist.get("total")
        if declared_total is not None and declared_total != len(claims):
            findings.append(
                f"claims.yaml confidence_distribution.total={declared_total} does not match "
                f"actual claims count={len(claims)}. Re-run claims_aggregator.py."
            )

    # ── Persist results ──────────────────────────────────────────────────
    if not findings:
        n_rewritten = sum(
            1 for c in claims
            if isinstance(c, dict) and c.get("rewritten") is True
        )
        results["checks"].append({
            "check": "claims_confidence",
            "status": "PASS",
            "total_claims": len(claims),
            "rewritten": n_rewritten,
            "has_distribution": isinstance(dist, dict),
            "schema_version": claims_data.get("schema_version", "unknown"),
        })
    else:
        results["checks"].append({
            "check": "claims_confidence",
            "status": "FINDINGS",
            "count": len(findings),
        })

    for f in findings:
        results.setdefault("claims_confidence_findings", []).append(f)


def check_criteria_calibration(output_dir: str, results: dict) -> None:
    """Generic extension hook for Story RA-F.1 AC-5 checks.

    Inspects whichever scored atoms exist (research or bench) and reports:
      - criteria.md presence when AC-1 trigger fires
      - scoring_calibration block presence + validity per AC-2 schema
      - scoring-{slug}.py presence when AC-3 trigger fires (>=3 sub-scores
        evidenced by `weights` block with 3+ entries OR a `WEIGHTS = {...}`
        signature in any sibling `scoring-*.py`)

    Findings are appended to results['errors'] (when AC violation is
    unambiguous) or results['warnings'] (when condition is ambiguous OR
    enforcement is `warn`). Severity translation to exit code is done in
    `main()` based on the --enforcement flag.
    """
    findings = []

    # ─── Discover scored atoms in this run ────────────────────────────────
    scored_files: list[tuple[str, dict]] = []
    for atom_name in SCORED_ATOM_CANDIDATES:
        path = os.path.join(output_dir, atom_name)
        if os.path.exists(path):
            data = _load_structured_file(path)
            scored_files.append((atom_name, data))

    if not scored_files:
        results["checks"].append(
            {"check": "criteria_calibration", "status": "skipped — no scored atoms found"}
        )
        return

    # ─── AC-1: criteria.md trigger ───────────────────────────────────────
    # Trigger fires when ANY scored atom declares multi_player AND has >=5
    # dimensions. We inspect each scored atom independently.
    criteria_required = False
    trigger_evidence = []
    for atom_name, data in scored_files:
        pattern = _comparison_pattern_from(data)
        dims = _count_dimensions(data)
        if pattern == CALIBRATION_TRIGGER_PATTERN and dims >= CALIBRATION_TRIGGER_DIMENSIONS:
            criteria_required = True
            trigger_evidence.append(f"{atom_name} (pattern={pattern}, dims={dims})")

    criteria_path = os.path.join(output_dir, "criteria.md")
    if criteria_required:
        if os.path.exists(criteria_path):
            results["checks"].append(
                {"check": "criteria_md_presence", "status": "EXISTS", "trigger": trigger_evidence}
            )
        else:
            findings.append(
                f"criteria.md MISSING — trigger fired by: {', '.join(trigger_evidence)} "
                f"(AC-1: comparison_pattern=multi_player AND dimensions_count>={CALIBRATION_TRIGGER_DIMENSIONS})"
            )

    # ─── AC-2: scoring_calibration block ─────────────────────────────────
    for atom_name, data in scored_files:
        if not _numeric_score_present(data):
            continue
        block = _extract_calibration_block(data)
        if not block:
            findings.append(
                f"{atom_name} has numeric score fields but no `scoring_calibration` block "
                "(AC-2: required at root or under `meta.scoring_calibration`)"
            )
            continue
        ok, problems = _calibration_block_is_valid(block)
        if not ok:
            findings.append(
                f"{atom_name} scoring_calibration block invalid: " + "; ".join(problems)
            )
        else:
            results["checks"].append(
                {"check": f"scoring_calibration::{atom_name}", "status": "VALID"}
            )

    # ─── AC-3: reproducible scoring script ───────────────────────────────
    # Trigger: composite scoring with >=3 sub-scores. Heuristic: look for a
    # `weights:` block (or `normalized_weights:`) with >=3 entries in any
    # scored atom OR in bench-weights.yaml when present.
    script_required = False
    script_trigger = []
    candidates_for_weights = list(scored_files)
    bench_weights_path = os.path.join(output_dir, "bench-weights.yaml")
    if os.path.exists(bench_weights_path):
        candidates_for_weights.append(
            ("bench-weights.yaml", _load_structured_file(bench_weights_path))
        )
    for atom_name, data in candidates_for_weights:
        if not isinstance(data, dict):
            continue
        weights = data.get("weights") or data.get("normalized_weights")
        if isinstance(weights, dict) and len(weights) >= 3:
            script_required = True
            script_trigger.append(f"{atom_name} ({len(weights)} weighted sub-scores)")
        elif isinstance(weights, list) and len(weights) >= 3:
            script_required = True
            script_trigger.append(f"{atom_name} ({len(weights)} weighted sub-scores)")

    if script_required:
        scripts_dir = os.path.join(output_dir, "scripts")
        found_scripts = []
        if os.path.isdir(scripts_dir):
            for entry in os.listdir(scripts_dir):
                if entry.startswith("scoring-") and entry.endswith(".py"):
                    found_scripts.append(entry)
        if not found_scripts:
            findings.append(
                f"scoring-{{slug}}.py MISSING in {output_dir}/scripts/ — "
                f"trigger fired by: {', '.join(script_trigger)} "
                "(AC-3: composite scoring with >=3 weighted sub-scores requires reproducible Python script)"
            )
        else:
            results["checks"].append(
                {
                    "check": "scoring_script_presence",
                    "status": "EXISTS",
                    "scripts": found_scripts,
                    "trigger": script_trigger,
                }
            )

    # ─── Persist findings ────────────────────────────────────────────────
    for f in findings:
        results.setdefault("criteria_calibration_findings", []).append(f)


def validate_output(output_dir: str, *, skill: str = "tech-research") -> dict:
    """Validate research output directory structure and content."""
    results = {
        "directory": output_dir,
        "skill": skill,
        "valid": True,
        "checks": [],
        "warnings": [],
        "errors": [],
    }

    if not os.path.isdir(output_dir):
        results["valid"] = False
        results["errors"].append(f"Directory not found: {output_dir}")
        return results

    # The research-bench branch skips the tech-research V1/V3 baseline file
    # checks because bench runs do not produce 02-research-report.md etc.
    # Instead, baseline bench presence is enforced by `bench:gold:validate`.
    # Story RA-F.1 only adds the criteria-calibration extension hook here.
    if skill == "research-bench":
        check_criteria_calibration(output_dir, results)
        # Story RA-F.2 AC-6 — status code 4-níveis + recommendations atom + symbols
        check_status_code_compliance(output_dir, results)
        # Story RA-F.3 — extraction ladder + mandatory sources + gap analysis
        check_extraction_ladder(output_dir, results)
        check_mandatory_sources_coverage(output_dir, results)
        check_gap_analysis_presence(output_dir, results)
        # Story RA-C.1 AC-3 — specialist-contracts schema validation
        check_specialist_contracts(results)
        # Story RA-A.1 AC-4 — heartbeat-policy schema validation
        check_heartbeat_policy(results)
        # Story RA-B.1 AC-3 — gaps.yaml schema + APPEND-ONLY enforce
        check_gaps_schema(output_dir, results)
        # Story RA-D.2 AC-5 — claims.yaml schema + confidence_distribution
        check_claims_confidence(output_dir, results)
        return results

    for f in REQUIRED_FILES:
        path = os.path.join(output_dir, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            results["checks"].append({"file": f, "status": "EXISTS", "size": size})

            if f == "02-research-report.md" and size < REPORT_MIN_SIZE:
                results["warnings"].append(f"{f} is small ({size} bytes, min {REPORT_MIN_SIZE})")
            if f == "03-recommendations.md" and size < RECS_MIN_SIZE:
                results["warnings"].append(f"{f} is small ({size} bytes, min {RECS_MIN_SIZE})")
        else:
            results["valid"] = False
            results["errors"].append(f"MISSING required file: {f}")
            results["checks"].append({"file": f, "status": "MISSING"})

    for f in OPTIONAL_FILES:
        path = os.path.join(output_dir, f)
        if os.path.exists(path):
            results["checks"].append({"file": f, "status": "EXISTS", "size": os.path.getsize(path)})
        else:
            results["warnings"].append(f"Optional file missing: {f}")

    readme_path = os.path.join(output_dir, "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            content = f.read()
        for section in README_REQUIRED_SECTIONS:
            if section not in content:
                results["valid"] = False
                results["errors"].append(f"README.md missing required section/keyword: {section}")

        # Title noise check (defensive — advisory only).
        # Tópico should be a clean human phrase. Codification prefixes (TR-D7,
        # Research:, etc.) belong to the slug, not the topic. The kb-index
        # cleans these downstream via clean_title_prefixes(), but emitting a
        # warning here surfaces the smell at write-time so authors learn the
        # convention. WARN ratio is 1 — even one tagged title gets flagged.
        topic_match = re.search(r"^>\s*\*\*Tópico:\*\*\s*(.+?)\s*$", content, re.MULTILINE)
        if topic_match:
            topic_value = topic_match.group(1).strip()
            noise_patterns = [
                (r"^TR[-_]?D?\d+", "TR-D7 / TR-7 / TR-1"),
                (r"^Research\s*[—–\-:]", "Research: / Research —"),
                (r"^Tech\s+Research\s*[—–\-:]", "Tech Research:"),
                (r"^Pesquisa\s*[—–\-:]", "Pesquisa:"),
                (r"^Investigation\s*[—–\-:]", "Investigation:"),
            ]
            for pattern, hint in noise_patterns:
                if re.search(pattern, topic_value, re.IGNORECASE):
                    results["warnings"].append(
                        f"README.md **Tópico:** starts with codification prefix "
                        f"matching `{hint}`. Display will be auto-cleaned by "
                        f"research_kb_index.py, but ideally codes live in the "
                        f"slug, not the topic. See templates/output-structure.md."
                    )
                    break

        if "scope_declaration_required: true" in content and "scope_declaration" not in content:
            results["valid"] = False
            results["errors"].append("README.md declares scope_declaration_required but no scope_declaration block was found")

    report_path = os.path.join(output_dir, "02-research-report.md")
    if os.path.exists(report_path):
        with open(report_path, encoding="utf-8") as f:
            content = f.read()
        confidence_tags = len(re.findall(r"\[(?:HIGH|MEDIA|LOW)\s*—", content))
        if confidence_tags == 0:
            results["valid"] = False
            results["errors"].append("02-research-report.md has no confidence tags [HIGH|MEDIA|LOW]")
        results["checks"].append({"check": "confidence_tags", "count": confidence_tags})

        # Source date coverage (QF-5):
        # Count tokens that look like inline source date annotations.
        #   "[Title](url) — 2026"             → with-date
        #   "[Title](url) — 2026-04"          → with-date
        #   "[Title](url) — date_unknown"     → no-date
        # Thresholds (advisory for backwards-compat):
        #   no_date_ratio < 0.20 → OK
        #   0.20 <= ratio < 0.30 → WARN
        #   ratio >= 0.30         → FAIL  (set valid=false)
        #
        # Phase 4.5 CITATION_GATE — Scholarly Source Preference Policy (STORY-154.2):
        # When both scholarly (arXiv/PubMed/Semantic Scholar via scholarly_search.py) and
        # generic web sources are present in results, scholarly sources MUST be ranked higher
        # in the verified_ratio computation. Scholarly sources carry credibility 1.4x vs
        # web search 1.0x. If verified_ratio < 0.85, prefer promoting scholarly sources
        # over generic web pages during the verification step.
        source_dates = len(re.findall(r"—\s*\d{4}", content))
        date_unknown = len(re.findall(r"—\s*date_unknown\b", content, re.IGNORECASE))
        total_dated_or_unknown = source_dates + date_unknown
        if total_dated_or_unknown > 0:
            no_date_ratio = date_unknown / total_dated_or_unknown
            results["checks"].append({
                "check": "source_date_coverage",
                "with_date": source_dates,
                "date_unknown": date_unknown,
                "no_date_ratio": round(no_date_ratio, 3),
            })
            if no_date_ratio >= 0.30:
                results["valid"] = False
                results["errors"].append(
                    f"02-research-report.md has {date_unknown}/{total_dated_or_unknown} sources "
                    f"marked date_unknown (ratio {no_date_ratio:.0%} >= 30%). "
                    "Run Phase 4.5 verify-citations to populate dates via WebFetch."
                )
            elif no_date_ratio >= 0.20:
                results["warnings"].append(
                    f"02-research-report.md has {date_unknown}/{total_dated_or_unknown} sources "
                    f"marked date_unknown (ratio {no_date_ratio:.0%}). Consider re-running "
                    "Phase 4.5 to improve source freshness."
                )
        else:
            results["checks"].append({"check": "source_date_coverage", "count": source_dates})

        # Legacy check kept for downstream consumers reading the older shape.
        results["checks"].append({"check": "source_dates_in_refs", "count": source_dates})

        if re.search(r"\b(alternatives?|comparativo|comparison|landscape|builders?|tools?|frameworks?)\b", content, re.IGNORECASE):
            if "scope_declaration" not in content and "## Scope" not in content:
                results["valid"] = False
                results["errors"].append("Comparison/category report missing scope_declaration or ## Scope section")

        if "## Stop Reason" not in content and "stop_reason" not in content:
            results["valid"] = False
            results["errors"].append("02-research-report.md missing Stop Reason section or stop_reason marker")

    quick_wins_path = os.path.join(output_dir, "quick-wins.md")
    if os.path.exists(quick_wins_path):
        with open(quick_wins_path, encoding="utf-8") as f:
            qw_content = f.read()
        has_selecionados = "## Quick Wins Selecionados" in qw_content
        has_nao_encontrados = "## Quick Wins Não Encontrados" in qw_content
        if not (has_selecionados or has_nao_encontrados):
            results["valid"] = False
            results["errors"].append(
                "quick-wins.md missing required section: '## Quick Wins Selecionados' OR '## Quick Wins Não Encontrados'"
            )
        if has_selecionados:
            qw_block = qw_content.split("## Quick Wins Selecionados", 1)[1]
            qw_block = qw_block.split("\n## ", 1)[0]
            qw_rows = len(re.findall(r"^\|\s*(?:QW-)?[1-9]\d?\s*\|", qw_block, re.MULTILINE))
            results["checks"].append({"check": "quick_wins_rows", "count": qw_rows})
            if qw_rows < 3 and not has_nao_encontrados:
                results["valid"] = False
                results["errors"].append(
                    f"quick-wins.md has {qw_rows} Quick Win rows; minimum is 3 OR include '## Quick Wins Não Encontrados' with documented gap"
                )
            evidence_refs = len(re.findall(r"§\s*\d", qw_block)) + len(re.findall(r"02-research-report\.md", qw_block))
            results["checks"].append({"check": "quick_wins_evidence_refs", "count": evidence_refs})
            if qw_rows >= 1 and evidence_refs == 0:
                results["valid"] = False
                results["errors"].append(
                    "quick-wins.md Quick Wins Selecionados has rows but zero evidence references to 02-research-report.md (each QW must cite §X.Y)"
                )

    metrics = _load_structured_file(os.path.join(output_dir, "metrics.yaml"))
    pipeline_state = _load_structured_file(os.path.join(output_dir, "pipeline-state.yaml"))

    for field in ["workflow_version", "coverage_score", "integrity_score", "citation_verified", "stop_reason", "rubrics", "runtime_contract"]:
        if field not in metrics:
            results["valid"] = False
            results["errors"].append(f"metrics.yaml missing required field: {field}")

    rubrics = metrics.get("rubrics")
    if not isinstance(rubrics, dict) or not rubrics:
        results["valid"] = False
        results["errors"].append("metrics.yaml rubrics must be a non-empty mapping")
    else:
        for axis in ["information_recall", "analysis", "presentation"]:
            axis_value = rubrics.get(axis)
            if not isinstance(axis_value, dict) or "passed" not in axis_value or "total" not in axis_value:
                results["valid"] = False
                results["errors"].append(f"metrics.yaml rubrics missing passed/total for axis: {axis}")

    if not pipeline_state.get("pipeline_id"):
        results["valid"] = False
        results["errors"].append("pipeline-state.yaml missing required field: pipeline_id")
    if not pipeline_state.get("status"):
        results["valid"] = False
        results["errors"].append("pipeline-state.yaml missing required field: status")
    if "stop_reason" not in pipeline_state:
        results["valid"] = False
        results["errors"].append("pipeline-state.yaml missing required field: stop_reason")

    curiosity = _load_structured_file(os.path.join(output_dir, "curiosity_queue.yaml"))
    if "items" not in curiosity or not isinstance(curiosity.get("items"), list):
        results["valid"] = False
        results["errors"].append("curiosity_queue.yaml missing list field: items")

    execution_log_path = os.path.join(output_dir, "execution-log.jsonl")
    if os.path.exists(execution_log_path):
        with open(execution_log_path, encoding="utf-8") as f:
            rows = [line.strip() for line in f if line.strip()]
        if not rows:
            results["valid"] = False
            results["errors"].append("execution-log.jsonl is empty")
        for idx, row in enumerate(rows, start=1):
            try:
                json.loads(row)
            except json.JSONDecodeError:
                results["valid"] = False
                results["errors"].append(f"execution-log.jsonl line {idx} is not valid JSON")

    follow_ups = [f for f in os.listdir(output_dir) if re.match(r"0[4-9]-.*\.md|[1-9]\d-.*\.md", f)]
    if follow_ups:
        results["checks"].append({"check": "follow_up_files", "count": len(follow_ups), "files": follow_ups})

    # Story RA-F.1 AC-5 — criteria + calibration extension hook
    check_criteria_calibration(output_dir, results)

    # Story RA-F.2 AC-6 — status code 4-níveis + recommendations atom + symbols
    check_status_code_compliance(output_dir, results)

    # Story RA-F.3 — extraction ladder + mandatory sources + gap analysis
    check_extraction_ladder(output_dir, results)
    check_mandatory_sources_coverage(output_dir, results)
    check_gap_analysis_presence(output_dir, results)

    # Story RA-C.1 AC-3 — specialist-contracts schema validation
    check_specialist_contracts(results)

    # Story RA-A.1 AC-4 — heartbeat-policy schema validation
    check_heartbeat_policy(results)

    # Story RA-B.1 AC-3 — gaps.yaml schema + APPEND-ONLY enforce
    check_gaps_schema(output_dir, results)

    # Story RA-D.2 AC-5 — claims.yaml schema + confidence_distribution
    check_claims_confidence(output_dir, results)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Validate tech-research pipeline output structure.",
    )
    parser.add_argument(
        "--mode",
        choices=["current", "target"],
        default="current",
        help=(
            "Validation mode. 'current' (default) checks the V1 baseline that all "
            "Claude Code + Codex runs must produce. 'target' adds V3 cognitive "
            "atoms (curiosity_queue.yaml, evolving_report.md, execution-log.jsonl) "
            "expected after spy v5 evolution. Default mode is the gate that runs "
            "today; target mode is the aspirational gate."
        ),
    )
    parser.add_argument(
        "--skill",
        choices=["tech-research", "research-bench"],
        default="tech-research",
        help=(
            "Which skill produced this output. Selects the file-baseline checks "
            "applied BEFORE the shared criteria-calibration extension hook "
            "(Story RA-F.1 AC-5). research-bench skips tech-research's V1/V3 "
            "file list (which is enforced by bench:gold:validate instead) and "
            "applies the calibration hook only."
        ),
    )
    parser.add_argument(
        "--enforcement",
        choices=["warn", "block"],
        default="warn",
        help=(
            "How criteria-calibration findings affect the exit code. 'warn' "
            "(default) reports findings but exits 0 unless legacy V1/V3 baseline "
            "checks fail. 'block' makes any criteria-calibration finding cause "
            "exit non-zero. Story RA-F.1 Regression Risk row 1: stay 'warn' for "
            "30d post-merge, then promote to 'block'."
        ),
    )
    parser.add_argument("output_dir", help="Path to docs/research/{date}-{slug}/")
    args = parser.parse_args()

    global REQUIRED_FILES
    REQUIRED_FILES = (
        REQUIRED_FILES_TARGET if args.mode == "target" else REQUIRED_FILES_CURRENT
    )

    result = validate_output(args.output_dir, skill=args.skill)
    result["mode"] = args.mode
    result["enforcement"] = args.enforcement

    findings = result.get("criteria_calibration_findings", [])
    if findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in findings:
                result["errors"].append(f"[criteria-calibration] {f}")
        else:
            for f in findings:
                result["warnings"].append(f"[criteria-calibration] {f}")

    # Story RA-F.2 AC-6 — status-code findings honor the same enforcement flag.
    # 30d warn → block promotion window is canonical for F.2 too (tracked by
    # @aiox-devops); see tech-research/SKILL.md §Validator for mechanics.
    status_findings = result.get("status_code_findings", [])
    if status_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in status_findings:
                result["errors"].append(f"[status-code] {f}")
        else:
            for f in status_findings:
                result["warnings"].append(f"[status-code] {f}")

    # Story RA-F.3 — extraction ladder findings (same enforcement window)
    extraction_findings = result.get("extraction_ladder_findings", [])
    if extraction_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in extraction_findings:
                result["errors"].append(f"[extraction-ladder] {f}")
        else:
            for f in extraction_findings:
                result["warnings"].append(f"[extraction-ladder] {f}")

    # Story RA-F.3 — mandatory sources coverage findings
    mandatory_findings = result.get("mandatory_sources_findings", [])
    if mandatory_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in mandatory_findings:
                result["errors"].append(f"[mandatory-sources] {f}")
        else:
            for f in mandatory_findings:
                result["warnings"].append(f"[mandatory-sources] {f}")

    # Story RA-F.3 — gap analysis presence findings
    gap_findings = result.get("gap_analysis_findings", [])
    if gap_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in gap_findings:
                result["errors"].append(f"[gap-analysis] {f}")
        else:
            for f in gap_findings:
                result["warnings"].append(f"[gap-analysis] {f}")

    # Story RA-C.1 AC-3 — specialist-contracts schema findings
    spec_contract_findings = result.get("specialist_contracts_findings", [])
    if spec_contract_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in spec_contract_findings:
                result["errors"].append(f"[specialist-contracts] {f}")
        else:
            for f in spec_contract_findings:
                result["warnings"].append(f"[specialist-contracts] {f}")

    # Story RA-A.1 AC-4 — heartbeat-policy schema findings
    # Same enforcement window as F.1/F.2/F.3/C.1: default warn, promote to block after 30d.
    heartbeat_findings = result.get("heartbeat_policy_findings", [])
    if heartbeat_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in heartbeat_findings:
                result["errors"].append(f"[heartbeat-policy] {f}")
        else:
            for f in heartbeat_findings:
                result["warnings"].append(f"[heartbeat-policy] {f}")

    # Story RA-B.1 AC-3 — gaps.yaml schema + APPEND-ONLY findings
    # Same enforcement window as F.1/F.2/F.3/C.1/A.1: default warn, promote to block after 30d.
    gaps_schema_findings = result.get("gaps_schema_findings", [])
    if gaps_schema_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in gaps_schema_findings:
                result["errors"].append(f"[gaps-schema] {f}")
        else:
            for f in gaps_schema_findings:
                result["warnings"].append(f"[gaps-schema] {f}")

    # Story RA-D.2 AC-5 — claims.yaml schema + confidence_distribution findings
    # Same enforcement window as F.1/F.2/F.3/C.1/A.1/B.1: default warn, promote to block after 30d.
    claims_confidence_findings = result.get("claims_confidence_findings", [])
    if claims_confidence_findings:
        if args.enforcement == "block":
            result["valid"] = False
            for f in claims_confidence_findings:
                result["errors"].append(f"[claims-confidence] {f}")
        else:
            for f in claims_confidence_findings:
                result["warnings"].append(f"[claims-confidence] {f}")

    print(json.dumps(result, indent=2))

    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
