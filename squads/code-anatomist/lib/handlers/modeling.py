#!/usr/bin/env python3
"""
Phase 3: Decision Modeling
Agent: barbara-von-halle (Decision Model) + james-taylor (DMN tables, DRDs)

Outputs → outputs/decoded/{slug}/modeling/
  - decision-inventory.yaml
  - decision-model.yaml
  - decision-tables/  (one .yaml per decision table)
  - drds/  (one .md per bounded context with Mermaid diagrams)
  - validation-report.yaml
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


VON_HALLE_AGENT = "squads/code-anatomist/agents/barbara-von-halle.md"
TAYLOR_AGENT = "squads/code-anatomist/agents/james-taylor.md"
TASK_FILE = "squads/code-anatomist/tasks/model-decisions.md"

EXPECTED_OUTPUTS = [
    "decision-inventory.yaml",
    "decision-model.yaml",
    "validation-report.yaml",
]


def build_prompt(
    item_id: str,
    metadata: Dict[str, Any],
    extraction_output: str,
) -> str:
    system_name = metadata.get("system_name", item_id)

    return f"""You are executing Phase 3 (Decision Modeling) of the Domain Decoder pipeline.

Read task file at {TASK_FILE}.
Read agent files: {VON_HALLE_AGENT} (Decision Model) and {TAYLOR_AGENT} (DMN tables).

## System Under Analysis
- **System Name:** {system_name}

## Phase 2 Output (Extraction)
{extraction_output}

Read full outputs from:
- outputs/decoded/{item_id}/discovery/glossary.yaml (ubiquitous language)
- outputs/decoded/{item_id}/discovery/context-map.md (bounded contexts)
- outputs/decoded/{item_id}/extraction/classified-rules.yaml (classified rules)
- outputs/decoded/{item_id}/extraction/fact-model.yaml (fact model)

## Your Deliverables (save ALL to outputs/decoded/{item_id}/modeling/)

1. **decision-inventory.yaml** — All business decisions: DEC-{{CONTEXT}}-{{NNN}}
2. **decision-model.yaml** — Decisions → rule families → rules (von Halle structure)
3. **decision-tables/** — DMN decision tables with hit policies (one .yaml per table: DT-{{CONTEXT}}-{{NNN}})
4. **drds/** — Decision Requirements Diagrams in Mermaid (one .md per context)
5. **validation-report.yaml** — Gaps, contradictions, orphaned rules, circular deps

## Process
1. Identify business decisions from classified rules (barbara-von-halle)
2. Group rules into rule families per decision (barbara-von-halle)
3. Build DMN decision tables with correct hit policies (james-taylor)
4. Create DRDs showing decision dependencies (james-taylor)
5. Validate completeness: no orphaned rules, no contradictions (barbara-von-halle)

## Hit Policy Guide
- U (Unique): exactly one row matches
- F (First): first matching row wins
- P (Priority): highest priority output
- A (Any): all matches must agree
- C (Collect): collect all matching outputs

## Enforcement Rules
- E1: Spawn dedicated agent
- E2: Save ALL outputs BEFORE completion
- E6: Cover ALL bounded contexts
- E8: Output path MUST be outputs/decoded/{item_id}/modeling/

Report: decisions found, decision tables created, orphaned rules (should be 0)."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    if output_base:
        return output_base / "modeling"
    return Path(f"outputs/decoded/{item_id}/modeling")


def check_cache(item_id: str, output_base: Optional[Path] = None) -> bool:
    out_dir = get_output_dir(item_id, output_base)
    if not out_dir.exists():
        return False
    existing = [f.name for f in out_dir.iterdir() if f.is_file()]
    return all(name in existing for name in EXPECTED_OUTPUTS)


async def handle_modeling(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """Phase 3: Decision Modeling."""
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files in modeling directory.",
            output_dir=str(out_dir),
        )

    # Count decisions
    decision_count = 0
    inventory_file = out_dir / "decision-inventory.yaml"
    if inventory_file.exists():
        content = inventory_file.read_text(encoding="utf-8", errors="replace")
        decision_count = content.count("id: ")

    # Count decision tables
    dt_dir = out_dir / "decision-tables"
    dt_count = 0
    if dt_dir.exists():
        dt_count = len(list(dt_dir.glob("*.yaml")))

    # Check validation report for issues
    orphaned_rules = 0
    contradictions = 0
    val_file = out_dir / "validation-report.yaml"
    if val_file.exists():
        content = val_file.read_text(encoding="utf-8", errors="replace")
        orphaned_rules = content.count("orphaned")
        contradictions = content.count("contradiction")

    # Count DRDs
    drd_dir = out_dir / "drds"
    drd_count = 0
    if drd_dir.exists():
        drd_count = len(list(drd_dir.glob("*.md")))

    return PhaseResult(
        success=True,
        output=f"Modeling complete: {decision_count} decisions, {dt_count} tables, {drd_count} DRDs",
        output_dir=str(out_dir),
        metadata={
            "decisions": decision_count,
            "decision_tables": dt_count,
            "drds": drd_count,
            "orphaned_rules": orphaned_rules,
            "contradictions": contradictions,
            "files_produced": [f.name for f in existing_files],
        },
    )
