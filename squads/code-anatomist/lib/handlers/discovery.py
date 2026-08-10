#!/usr/bin/env python3
"""
Phase 0: Discovery & Domain Mapping
Agent: eric-evans (+ ronald-ross for classify-rules)

Outputs → outputs/decoded/{slug}/discovery/
  - context-map.md
  - glossary.yaml
  - source-mapping.yaml
  - rule-type-inventory.yaml
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


AGENT_FILE = "squads/code-anatomist/agents/eric-evans.md"
TASK_FILE = "squads/code-anatomist/tasks/map-domain.md"
CLASSIFY_TASK = "squads/code-anatomist/tasks/classify-rules.md"

EXPECTED_OUTPUTS = [
    "context-map.md",
    "glossary.yaml",
    "source-mapping.yaml",
    "rule-type-inventory.yaml",
]


def build_prompt(item_id: str, metadata: Dict[str, Any]) -> str:
    """Build the agent prompt for Phase 0 Discovery."""
    system_name = metadata.get("system_name", item_id)
    source_location = metadata.get("source_location", "")
    primary_domain = metadata.get("primary_domain", "")
    known_rule_areas = metadata.get("known_rule_areas", [])
    existing_docs = metadata.get("existing_docs", "")

    return f"""You are executing Phase 0 (Discovery) of the Domain Decoder pipeline.

Read your agent file at {AGENT_FILE} and task file at {TASK_FILE}.
Also read {CLASSIFY_TASK} for the rule classification sub-task.

## System Under Analysis
- **System Name:** {system_name}
- **Source Location:** {source_location}
- **Primary Domain:** {primary_domain}
- **Known Rule Areas:** {', '.join(known_rule_areas) if known_rule_areas else 'Not specified'}
- **Existing Docs:** {existing_docs or 'None provided'}

## Your Deliverables (save ALL to outputs/decoded/{item_id}/discovery/)

1. **context-map.md** — Bounded contexts with relationships (Evans relationship types)
2. **glossary.yaml** — Ubiquitous language glossary (min 15 terms per major context)
3. **source-mapping.yaml** — Source files/modules mapped to bounded contexts
4. **rule-type-inventory.yaml** — Ross taxonomy classification of expected rule types

## Process
1. Read the codebase at {source_location} (if accessible)
2. Identify bounded contexts from module structure, database schemas, team boundaries
3. Build glossary from code identifiers, comments, docs
4. Map source files to contexts
5. Sample 10-20 files and classify expected rule types (Ross taxonomy)
6. Save all outputs before completing

## Enforcement Rules
- E2: Save ALL outputs BEFORE reporting completion
- E3: Only tag actual business rules, not UI/config details
- E8: Output path MUST be outputs/decoded/{item_id}/discovery/
- E6: Cover ALL bounded contexts equally

Report the number of bounded contexts found and glossary terms defined."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    """Get the output directory for this phase."""
    if output_base:
        return output_base / "discovery"
    return Path(f"outputs/decoded/{item_id}/discovery")


def check_cache(item_id: str, output_base: Optional[Path] = None) -> bool:
    """Check if discovery outputs already exist."""
    out_dir = get_output_dir(item_id, output_base)
    if not out_dir.exists():
        return False
    existing = [f.name for f in out_dir.iterdir() if f.is_file()]
    return all(name in existing for name in EXPECTED_OUTPUTS)


async def handle_discovery(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """
    Phase 0: Discovery & Domain Mapping.

    This handler builds the prompt and context for the eric-evans agent.
    In production, the PhaseRunner caller spawns the agent with this prompt.
    The handler returns a PhaseResult based on what the agent produces.

    For CLI/orchestrator integration:
      1. Caller spawns the Discovery agent (persona: squads/code-anatomist/agents/eric-evans.md)
         with prompt=build_prompt(...)
      2. Agent saves outputs to outputs/decoded/{slug}/discovery/
      3. This handler verifies outputs exist and returns PhaseResult
    """
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Verify outputs were saved (E2, E9)
    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files found in discovery directory. Agent must save outputs before phase completes.",
            output_dir=str(out_dir),
        )

    # Count bounded contexts from context-map if available
    context_map = out_dir / "context-map.md"
    contexts_found: List[str] = []
    if context_map.exists():
        content = context_map.read_text(encoding="utf-8", errors="replace")
        # Simple heuristic: count ## headers as contexts
        contexts_found = [
            line.strip("# ").strip()
            for line in content.split("\n")
            if line.startswith("## ") and not line.startswith("## Context Map")
        ]

    # Count glossary terms
    glossary_file = out_dir / "glossary.yaml"
    glossary_terms = 0
    if glossary_file.exists():
        content = glossary_file.read_text(encoding="utf-8", errors="replace")
        glossary_terms = content.count("term:")

    return PhaseResult(
        success=True,
        output=f"Discovery complete: {len(contexts_found)} bounded contexts, {glossary_terms} glossary terms",
        output_dir=str(out_dir),
        contexts_covered=contexts_found if contexts_found else ["unknown"],
        metadata={
            "bounded_contexts": len(contexts_found),
            "glossary_terms": glossary_terms,
            "files_produced": [f.name for f in existing_files],
        },
    )
