#!/usr/bin/env python3
"""
Phase 1: Legacy Code Characterization
Agent: michael-feathers (+ martin-fowler for architecture)

Outputs → outputs/decoded/{slug}/characterization/
  - architecture-classification.md
  - characterization-tests.md
  - seam-map.yaml
  - smell-to-rule-mapping.yaml
  - rule-location-index.yaml
  - tests/  (characterization test files, enforcement E5)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


AGENT_FILE = "squads/code-anatomist/agents/michael-feathers.md"
TASK_FILE = "squads/code-anatomist/tasks/characterize-legacy.md"
FOWLER_AGENT = "squads/code-anatomist/agents/martin-fowler.md"

EXPECTED_OUTPUTS = [
    "architecture-classification.md",
    "characterization-tests.md",
    "seam-map.yaml",
    "rule-location-index.yaml",
]


def build_prompt(
    item_id: str,
    metadata: Dict[str, Any],
    discovery_output: str,
) -> str:
    """Build the agent prompt for Phase 1 Characterization."""
    system_name = metadata.get("system_name", item_id)
    source_location = metadata.get("source_location", "")

    return f"""You are executing Phase 1 (Characterization) of the Domain Decoder pipeline.

Read your agent file at {AGENT_FILE} and task file at {TASK_FILE}.
Also read {FOWLER_AGENT} for Martin Fowler's architecture analysis.

## System Under Analysis
- **System Name:** {system_name}
- **Source Location:** {source_location}

## Phase 0 Output (Discovery)
{discovery_output}

Read the full discovery outputs from outputs/decoded/{item_id}/discovery/ for context map, glossary, and source mapping.

## Your Deliverables (save ALL to outputs/decoded/{item_id}/characterization/)

1. **architecture-classification.md** — Architecture pattern (Transaction Script, Domain Model, etc.) with code evidence
2. **characterization-tests.md** — Characterization tests documenting CURRENT behavior (min 5 per major context, 3 per minor)
3. **seam-map.yaml** — Seam map: SM-{{CONTEXT}}-{{NNN}} with type, location, accessible rules
4. **smell-to-rule-mapping.yaml** — Code smells mapped to rule candidates
5. **rule-location-index.yaml** — Master index: file → methods → estimated rules → risk level
6. **tests/** — Directory with actual characterization test files (E5)

## Enforcement Rules
- E1: Spawn dedicated agent, do NOT synthesize from memory
- E2: Save ALL outputs BEFORE reporting completion
- E5: Characterization tests MUST be written to tests/ subdirectory
- E6: Cover ALL bounded contexts equally
- E8: Output path MUST be outputs/decoded/{item_id}/characterization/

## Critical Veto Conditions
- Do NOT extract rules — only LOCATE and CHARACTERIZE
- Do NOT modify the legacy code — READ-ONLY
- Characterization tests assert ACTUAL behavior, not DESIRED behavior

Report: architecture pattern, number of characterization tests, number of seams found."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    if output_base:
        return output_base / "characterization"
    return Path(f"outputs/decoded/{item_id}/characterization")


def check_cache(item_id: str, output_base: Optional[Path] = None) -> bool:
    out_dir = get_output_dir(item_id, output_base)
    if not out_dir.exists():
        return False
    existing = [f.name for f in out_dir.iterdir() if f.is_file()]
    return all(name in existing for name in EXPECTED_OUTPUTS)


async def handle_characterization(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """
    Phase 1: Legacy Code Characterization.

    Verifies that michael-feathers agent produced required outputs.
    """
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files in characterization directory.",
            output_dir=str(out_dir),
        )

    # E5: Verify characterization tests exist
    tests_dir = out_dir / "tests"
    test_count = 0
    if tests_dir.exists():
        test_files = list(tests_dir.glob("*"))
        test_count = len(test_files)

    # Count seams from seam-map
    seam_count = 0
    seam_file = out_dir / "seam-map.yaml"
    if seam_file.exists():
        content = seam_file.read_text(encoding="utf-8", errors="replace")
        seam_count = content.count("id: ")

    # Extract architecture pattern
    arch_pattern = "unknown"
    arch_file = out_dir / "architecture-classification.md"
    if arch_file.exists():
        content = arch_file.read_text(encoding="utf-8", errors="replace")
        for pattern in ["Transaction Script", "Domain Model", "Table Module", "Service Layer", "Active Record"]:
            if pattern.lower() in content.lower():
                arch_pattern = pattern
                break

    return PhaseResult(
        success=True,
        output=f"Characterization complete: {arch_pattern} pattern, {test_count} tests, {seam_count} seams",
        output_dir=str(out_dir),
        metadata={
            "architecture_pattern": arch_pattern,
            "characterization_tests": test_count,
            "seams_found": seam_count,
            "files_produced": [f.name for f in existing_files],
        },
    )
