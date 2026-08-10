#!/usr/bin/env python3
"""
Phase 2: Rule Extraction & Classification
Agent: ronald-ross (classification) + michael-feathers (extraction)

Outputs → outputs/decoded/{slug}/extraction/
  - raw-rules.yaml
  - classified-rules.yaml
  - fact-model.yaml
  - dedup-matrix.md  (E7: mandatory file even if empty)
  - shadow-rules.yaml  (if documentation-only rules found)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


FEATHERS_AGENT = "squads/domain-decoder/agents/michael-feathers.md"
ROSS_AGENT = "squads/domain-decoder/agents/ronald-ross.md"
TASK_FILE = "squads/domain-decoder/tasks/extract-rules.md"

EXPECTED_OUTPUTS = [
    "classified-rules.yaml",
    "fact-model.yaml",
    "dedup-matrix.md",
]


def build_prompt(
    item_id: str,
    metadata: Dict[str, Any],
    discovery_output: str,
    characterization_output: str,
) -> str:
    system_name = metadata.get("system_name", item_id)
    source_location = metadata.get("source_location", "")

    return f"""You are executing Phase 2 (Extraction & Classification) of the Domain Decoder pipeline.

Read task file at {TASK_FILE}.
Read agent files: {FEATHERS_AGENT} (extraction) and {ROSS_AGENT} (classification).

## System Under Analysis
- **System Name:** {system_name}
- **Source Location:** {source_location}

## Prior Phase Outputs
**Phase 0 (Discovery):** {discovery_output}
**Phase 1 (Characterization):** {characterization_output}

Read full outputs from:
- outputs/decoded/{item_id}/discovery/ (context map, glossary, source mapping)
- outputs/decoded/{item_id}/characterization/ (seam map, rule location index, tests)

## Your Deliverables (save ALL to outputs/decoded/{item_id}/extraction/)

1. **raw-rules.yaml** — Raw rules extracted from seams with source traceability
2. **classified-rules.yaml** — Rules classified with Ross taxonomy (CONSTRAINT, COMPUTATION, INFERENCE, ACTION_ENABLER, BEHAVIORAL)
3. **fact-model.yaml** — Fact model per bounded context (terms → facts → rules)
4. **dedup-matrix.md** — Deduplication matrix for multi-layer rules (E7: file MUST exist)
5. **shadow-rules.yaml** — Rules found only in documentation (if any)

## ID Format
- Rule IDs: RE-{{DOMAIN}}-{{NNN}} (e.g., RE-SALES-001)
- Domain = bounded context in UPPERCASE

## Enforcement Rules
- E1: Spawn dedicated agent per sub-task
- E2: Save ALL outputs BEFORE completion
- E3: Only business rules (PO test: "would a PO care if this changed?")
- E6: Cover ALL bounded contexts equally
- E7: dedup-matrix.md MUST exist (even if empty)
- E8: Output path MUST be outputs/decoded/{item_id}/extraction/

## Veto Conditions
- Do NOT begin without passing characterization tests from Phase 1
- Do NOT classify without the glossary from Phase 0
- Do NOT assign RE-{{DOMAIN}}-{{NNN}} to non-business rules
- Do NOT skip dedup matrix

Report: total rules extracted, breakdown by Ross category, bounded contexts covered."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    if output_base:
        return output_base / "extraction"
    return Path(f"outputs/decoded/{item_id}/extraction")


def check_cache(item_id: str, output_base: Optional[Path] = None) -> bool:
    out_dir = get_output_dir(item_id, output_base)
    if not out_dir.exists():
        return False
    existing = [f.name for f in out_dir.iterdir() if f.is_file()]
    return all(name in existing for name in EXPECTED_OUTPUTS)


async def handle_extraction(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """Phase 2: Rule Extraction & Classification."""
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files in extraction directory.",
            output_dir=str(out_dir),
        )

    # E7: Verify dedup-matrix exists
    dedup_file = out_dir / "dedup-matrix.md"
    if not dedup_file.exists():
        return PhaseResult(
            success=False,
            error="E7 violation: dedup-matrix.md not found. File MUST exist even if no duplicates.",
            output_dir=str(out_dir),
        )

    # Count rules from classified-rules
    rules_count = 0
    classified_file = out_dir / "classified-rules.yaml"
    if classified_file.exists():
        content = classified_file.read_text(encoding="utf-8", errors="replace")
        rules_count = content.count("id: ")

    # Detect contexts covered
    contexts: List[str] = []
    if classified_file.exists():
        content = classified_file.read_text(encoding="utf-8", errors="replace")
        for line in content.split("\n"):
            if "bounded_context:" in line:
                ctx = line.split("bounded_context:")[-1].strip().strip('"').strip("'")
                if ctx and ctx not in contexts:
                    contexts.append(ctx)

    return PhaseResult(
        success=True,
        output=f"Extraction complete: {rules_count} rules across {len(contexts)} contexts",
        output_dir=str(out_dir),
        rules_extracted=rules_count,
        contexts_covered=contexts,
        metadata={
            "rules_extracted": rules_count,
            "contexts": contexts,
            "dedup_matrix_exists": True,
            "files_produced": [f.name for f in existing_files],
        },
    )
