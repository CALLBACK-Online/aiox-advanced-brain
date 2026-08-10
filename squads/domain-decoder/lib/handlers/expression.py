#!/usr/bin/env python3
"""
Phase 4: Rule Expression & Standardization
Agent: graham-witt (RuleSpeak) + ronald-ross (consistency)

Outputs → outputs/decoded/{slug}/expression/
  - rules-expressed.md  (all rules with RuleSpeak final statements)
  - ambiguity-log.yaml
  - consistency-review.yaml
  - glossary-crossref.yaml
  - stakeholder-review.yaml  (if available)
  - updated-glossary.yaml  (glossary with new terms found)
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..phase_runner import PhaseResult
except ImportError:
    from phase_runner import PhaseResult


WITT_AGENT = "squads/domain-decoder/agents/graham-witt.md"
ROSS_AGENT = "squads/domain-decoder/agents/ronald-ross.md"
TASK_FILE = "squads/domain-decoder/tasks/express-rules.md"

EXPECTED_OUTPUTS = [
    "rules-expressed.md",
    "ambiguity-log.yaml",
    "consistency-review.yaml",
    "glossary-crossref.yaml",
]

# Banned words from the task (ambiguity signals)
BANNED_WORDS = [
    "appropriate", "reasonable", "sufficient", "timely", "significant",
    "adequate", "proper", "applicable", "current", "recent",
    "usually", "generally", "normally", "often", "sometimes",
    "may impact", "could affect", "etc.", "and/or", "as needed", "up to",
]


def build_prompt(
    item_id: str,
    metadata: Dict[str, Any],
    modeling_output: str,
) -> str:
    system_name = metadata.get("system_name", item_id)
    language = metadata.get("language", "English")

    return f"""You are executing Phase 4 (Expression) of the Domain Decoder pipeline.

Read task file at {TASK_FILE}.
Read agent files: {WITT_AGENT} (RuleSpeak) and {ROSS_AGENT} (consistency).

## System Under Analysis
- **System Name:** {system_name}
- **Language:** {language}

## Phase 3 Output (Modeling)
{modeling_output}

Read full outputs from:
- outputs/decoded/{item_id}/discovery/glossary.yaml (ubiquitous language)
- outputs/decoded/{item_id}/extraction/classified-rules.yaml (classified rules)
- outputs/decoded/{item_id}/modeling/decision-model.yaml (decision model)
- outputs/decoded/{item_id}/modeling/decision-tables/ (DMN tables)

## Your Deliverables (save ALL to outputs/decoded/{item_id}/expression/)

1. **rules-expressed.md** — Every rule with final RuleSpeak statement
2. **ambiguity-log.yaml** — Each ambiguous term found and its replacement
3. **consistency-review.yaml** — Pattern consistency audit
4. **glossary-crossref.yaml** — Cross-reference: all terms in rules vs glossary
5. **updated-glossary.yaml** — Glossary with any new terms discovered
6. **stakeholder-review.yaml** — Review results (if stakeholders available)

## RuleSpeak Patterns
- OBLIGATION: "[Subject] MUST [verb phrase]."
- PROHIBITION: "[Subject] MUST NOT [verb phrase]."
- PERMISSION: "[Subject] MAY [verb phrase]."
- CONDITION: "It is [required/prohibited/permitted] that [condition]."
- DERIVATION: "[Term] is [derived as] [expression]."
- FACT: "[Subject] [verb] [object/complement]."
- CONDITIONAL OBLIGATION: "If [condition], then [subject] MUST [verb phrase]."
- CONDITIONAL DERIVATION: "If [condition], then [term] is [expression]."

## Banned Words (replace with precise terms)
{', '.join(BANNED_WORDS)}

## Enforcement Rules
- E1: Spawn dedicated agent
- E2: Save ALL outputs BEFORE completion
- E6: Cover ALL bounded contexts
- E8: Output path MUST be outputs/decoded/{item_id}/expression/

## Veto Conditions
- ONE rule = ONE sentence (no 'and' connecting obligations)
- MUST/MUST NOT/MAY only (never 'should', 'shall', 'will')
- Active voice for obligations
- All terms must be in glossary

Report: rules expressed, ambiguities resolved, consistency issues found."""


def get_output_dir(item_id: str, output_base: Optional[Path] = None) -> Path:
    if output_base:
        return output_base / "expression"
    return Path(f"outputs/decoded/{item_id}/expression")


def check_cache(item_id: str, output_base: Optional[Path] = None) -> bool:
    out_dir = get_output_dir(item_id, output_base)
    if not out_dir.exists():
        return False
    existing = [f.name for f in out_dir.iterdir() if f.is_file()]
    return all(name in existing for name in EXPECTED_OUTPUTS)


def lint_rules(rules_file: Path) -> Dict[str, Any]:
    """
    Quick lint: check for banned words in the final rules-expressed.md.
    Mirrors the function of squads/domain-decoder/scripts/rule-lint.js.
    """
    if not rules_file.exists():
        return {"passed": False, "error": "rules-expressed.md not found"}

    content = rules_file.read_text(encoding="utf-8", errors="replace").lower()
    violations = []
    for word in BANNED_WORDS:
        if word.lower() in content:
            violations.append(word)

    return {
        "passed": len(violations) == 0,
        "violations": violations,
        "violation_count": len(violations),
    }


async def handle_expression(
    item_id: str,
    metadata: Dict[str, Any],
    previous_outputs: Dict[int, str],
    output_base: Optional[Path] = None,
    **kwargs,
) -> PhaseResult:
    """Phase 4: Rule Expression & Standardization."""
    out_dir = get_output_dir(item_id, output_base)
    out_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(out_dir.glob("*.md")) + list(out_dir.glob("*.yaml"))
    if not existing_files:
        return PhaseResult(
            success=False,
            error="No output files in expression directory.",
            output_dir=str(out_dir),
        )

    # Count expressed rules
    rules_expressed = 0
    rules_file = out_dir / "rules-expressed.md"
    if rules_file.exists():
        content = rules_file.read_text(encoding="utf-8", errors="replace")
        # Count RE- IDs as proxy for expressed rules
        rules_expressed = content.count("RE-")

    # Lint check
    lint_result = lint_rules(rules_file)

    # Count ambiguities resolved
    ambiguities = 0
    amb_file = out_dir / "ambiguity-log.yaml"
    if amb_file.exists():
        content = amb_file.read_text(encoding="utf-8", errors="replace")
        ambiguities = content.count("ambiguous_term:")

    return PhaseResult(
        success=True,
        output=f"Expression complete: {rules_expressed} rules expressed, {ambiguities} ambiguities resolved",
        output_dir=str(out_dir),
        rules_extracted=rules_expressed,
        metadata={
            "rules_expressed": rules_expressed,
            "ambiguities_resolved": ambiguities,
            "lint_passed": lint_result["passed"],
            "lint_violations": lint_result.get("violations", []),
            "files_produced": [f.name for f in existing_files],
        },
    )
