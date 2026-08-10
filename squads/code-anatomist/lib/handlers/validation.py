#!/usr/bin/env python3
"""
Phase 5: Validation & Delivery
Agent: decoder-chief

Outputs → outputs/decoded/{slug}/validation/
  - sbvr-validation.md  (45-item checklist with PASS/FAIL per item)
  - extraction-quality.md  (54-item checklist with PASS/FAIL per item)
  - rule-catalog.md  (final deliverable from template)
  - traceability-matrix.yaml  (Rule ID → Source → Line → Module → SME → Policy)
  - delivery-manifest.yaml  (package listing all deliverables)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


AGENT_FILE = "squads/code-anatomist/agents/decoder-chief.md"
SBVR_CHECKLIST = "squads/code-anatomist/checklists/sbvr-validation.md"
QUALITY_CHECKLIST = "squads/code-anatomist/checklists/extraction-quality.md"
CATALOG_TEMPLATE = "squads/code-anatomist/templates/rule-catalog-tmpl.md"

EXPECTED_OUTPUTS = [
    "sbvr-validation.md",
    "extraction-quality.md",
    "rule-catalog.md",
    "traceability-matrix.yaml",
]

# Minimum passing thresholds (from workflow definition)
MIN_SBVR_SCORE = 85  # percent
MIN_QUALITY_SCORE = 85  # percent
SBVR_CRITICAL_COUNT = 5  # all 5 criticals must pass


def build_prompt(
    item_id: str,
    metadata: Dict[str, Any],
    expression_output: str,
) -> str:
    system_name = metadata.get("system_name", item_id)

    return f"""You are executing Phase 5 (Validation & Delivery) of the Domain Decoder pipeline.

Read your agent file at {AGENT_FILE}.
Read checklists: {SBVR_CHECKLIST} and {QUALITY_CHECKLIST}.
Read template: {CATALOG_TEMPLATE}.

## System Under Analysis
- **System Name:** {system_name}

## Phase 4 Output (Expression)
{expression_output}

Read ALL prior phase outputs from outputs/decoded/{item_id}/:
- discovery/ (context map, glossary, source mapping)
- characterization/ (architecture, seam map, tests)
- extraction/ (classified rules, fact model, dedup matrix)
- modeling/ (decision model, decision tables, DRDs)
- expression/ (rules expressed, ambiguity log, consistency review)

## Your Deliverables (save ALL to outputs/decoded/{item_id}/validation/)

1. **sbvr-validation.md** — Run SBVR checklist (45 items), item-by-item PASS/FAIL. Score >= {MIN_SBVR_SCORE}%. All {SBVR_CRITICAL_COUNT} criticals MUST pass.
2. **extraction-quality.md** — Run quality checklist (54 items), item-by-item PASS/FAIL. Score >= {MIN_QUALITY_SCORE}%. No auto-fail conditions.
3. **rule-catalog.md** — Final rule catalog from template. ALL sections filled. No empty tables.
4. **traceability-matrix.yaml** — Every rule: ID → source file → line → module → SME → policy
5. **delivery-manifest.yaml** — Package listing all deliverables across all phases

## Enforcement Rules (CRITICAL)
- E4: Apply SBVR checklist ITEM BY ITEM (45 items with individual PASS/FAIL). Do NOT invent scores.
- E4: Apply quality checklist ITEM BY ITEM (54 items with individual PASS/FAIL). Do NOT invent scores.
- E9: Phase Gate MUST verify with actual commands:
  1. ls outputs/decoded/{item_id}/{{phase_dir}}/ for each phase
  2. Each output file > 500 bytes
  3. No VETO/BLOCKED/FAILED markers in outputs
- E2: Save ALL outputs BEFORE reporting completion
- E8: Output path MUST be outputs/decoded/{item_id}/validation/

## SBVR Score Calculation
score = (items_passed / total_items) * 100
If score < {MIN_SBVR_SCORE}% OR any critical fails → return to responsible agent with feedback.

Report: SBVR score, quality score, total rules in catalog, traceability coverage."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    if output_base:
        return output_base / "validation"
    return Path(f"outputs/decoded/{item_id}/validation")


async def handle_validation(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """
    Phase 5: Validation & Delivery.
    Runs SBVR + quality checklists, generates final catalog, traceability matrix.
    """
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files in validation directory.",
            output_dir=str(out_dir),
        )

    # Parse SBVR score
    sbvr_score = 0.0
    sbvr_file = out_dir / "sbvr-validation.md"
    if sbvr_file.exists():
        content = sbvr_file.read_text(encoding="utf-8", errors="replace")
        pass_count = content.lower().count("pass")
        fail_count = content.lower().count("fail")
        total = pass_count + fail_count
        if total > 0:
            sbvr_score = (pass_count / total) * 100

    # Parse quality score
    quality_score = 0.0
    quality_file = out_dir / "extraction-quality.md"
    if quality_file.exists():
        content = quality_file.read_text(encoding="utf-8", errors="replace")
        pass_count = content.lower().count("pass")
        fail_count = content.lower().count("fail")
        total = pass_count + fail_count
        if total > 0:
            quality_score = (pass_count / total) * 100

    # Count rules in final catalog
    catalog_rules = 0
    catalog_file = out_dir / "rule-catalog.md"
    if catalog_file.exists():
        content = catalog_file.read_text(encoding="utf-8", errors="replace")
        catalog_rules = content.count("RE-")

    # E9: Validate all prior phase outputs exist
    base = output_base or Path(f"outputs/decoded/{item_id}")
    phase_dirs = ["discovery", "characterization", "extraction", "modeling", "expression", "validation"]
    missing_phases = []
    for pd in phase_dirs:
        phase_path = base / pd
        if not phase_path.exists() or not any(phase_path.iterdir()):
            missing_phases.append(pd)

    # Check minimum scores
    scores_pass = sbvr_score >= MIN_SBVR_SCORE and quality_score >= MIN_QUALITY_SCORE
    if not scores_pass and (sbvr_score > 0 or quality_score > 0):
        return PhaseResult(
            success=False,
            error=f"Validation scores below threshold: SBVR={sbvr_score:.1f}% (min {MIN_SBVR_SCORE}%), Quality={quality_score:.1f}% (min {MIN_QUALITY_SCORE}%)",
            output_dir=str(out_dir),
            metadata={
                "sbvr_score": sbvr_score,
                "quality_score": quality_score,
            },
        )

    return PhaseResult(
        success=True,
        output=f"Validation complete: SBVR={sbvr_score:.1f}%, Quality={quality_score:.1f}%, {catalog_rules} rules in catalog",
        output_dir=str(out_dir),
        rules_extracted=catalog_rules,
        metadata={
            "sbvr_score": sbvr_score,
            "quality_score": quality_score,
            "catalog_rules": catalog_rules,
            "missing_phases": missing_phases,
            "files_produced": [f.name for f in existing_files],
        },
    )
