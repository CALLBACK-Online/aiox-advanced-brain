#!/usr/bin/env python3
"""Specialist dispatcher for the research pipeline.

Story: RA-C.1 | 2026-05-19
SPIKE-RA-C.0 verdict: GO — Task tool parallel spawn confirmed viable.

Consults squads/research/data/specialist-contracts.yaml, evaluates each
specialist's `invoked_when` expression against the pipeline_state, and returns
the list of specialists to invoke with their serialized inputs.

Failure isolation: specialist evaluation errors are caught individually.
A failing specialist does NOT propagate to others (error_propagation=false).

Usage:
    python specialist_dispatcher.py \\
        --phase-id P4.5 \\
        --pipeline-state '{"evidence_grading_required": true, "mode": "tech-research"}'

    python specialist_dispatcher.py \\
        --phase-id P4 \\
        --pipeline-state path/to/pipeline-state.yaml \\
        [--contracts path/to/specialist-contracts.yaml] \\
        [--force-dormant]

Output (JSON to stdout):
    {
      "phase_id": "P4.5",
      "specialists_to_invoke": [
        {
          "id": "sackett",
          "agent_file": "squads/research/agents/sackett.md",
          "triggers_in_phase": "P4.5",
          "failure_mode": "warn_and_continue",
          "serialized_input": {"claims": []},
          "available_tools": []
        }
      ],
      "skipped": [...],
      "errors": [...]
    }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# ─────────────────────────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────────────────────────

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, "..", "..", "..", ".."))
_DEFAULT_CONTRACTS = os.path.join(
    _REPO_ROOT, "squads", "research", "data", "specialist-contracts.yaml"
)


# ─────────────────────────────────────────────────────────────────────────────
# Minimal expression DSL (D3 from story Decision Log)
#
# Grammar supported (case-insensitive keywords):
#   field == value
#   field in [val1, val2, ...]
#   field contains 'substring'
#   expr AND expr
#   expr OR expr
#
# NO Python eval — expressions are parsed with regex, not executed. This keeps
# the DSL safe against injection from untrusted contract YAML edits.
# ─────────────────────────────────────────────────────────────────────────────

_EQ_PATTERN = re.compile(
    r"^(\w+)\s*==\s*(['\"]?)(.+?)\2$",
)
_IN_PATTERN = re.compile(
    r"^(\w+)\s+in\s+\[([^\]]*)\]$",
)
_CONTAINS_PATTERN = re.compile(
    r"^(\w+)\s+contains\s+['\"]([^'\"]+)['\"]$",
)
_GT_PATTERN = re.compile(
    r"^(\w+)\s*>\s*(\d+(?:\.\d+)?)$",
)
_LT_PATTERN = re.compile(
    r"^(\w+)\s*<\s*(\d+(?:\.\d+)?)$",
)


def _coerce(value: Any, expected: str) -> Any:
    """Coerce pipeline state value for comparison with contract expression value."""
    if isinstance(value, bool):
        if expected.lower() in ("true", "false"):
            return str(value).lower()
        return str(value)
    return value


def _eval_atom(expr: str, state: dict) -> bool:
    """Evaluate a single (non-conjunctive) expression atom."""
    expr = expr.strip()

    # field == value
    m = _EQ_PATTERN.match(expr)
    if m:
        field, _, expected = m.groups()
        actual = state.get(field)
        if actual is None:
            return False
        return str(_coerce(actual, expected)).lower() == expected.lower()

    # field in [val1, val2]
    m = _IN_PATTERN.match(expr)
    if m:
        field, values_str = m.groups()
        actual = state.get(field)
        if actual is None:
            return False
        allowed = [v.strip().strip("'\"") for v in values_str.split(",")]
        return str(actual) in allowed

    # field contains 'substring'
    m = _CONTAINS_PATTERN.match(expr)
    if m:
        field, substring = m.groups()
        actual = state.get(field)
        if actual is None:
            return False
        return substring in str(actual)

    # field > numeric
    m = _GT_PATTERN.match(expr)
    if m:
        field, threshold = m.groups()
        actual = state.get(field)
        if actual is None:
            return False
        try:
            return float(actual) > float(threshold)
        except (TypeError, ValueError):
            return False

    # field < numeric  (wave_num == 0 uses == so this is extra safety)
    m = _LT_PATTERN.match(expr)
    if m:
        field, threshold = m.groups()
        actual = state.get(field)
        if actual is None:
            return False
        try:
            return float(actual) < float(threshold)
        except (TypeError, ValueError):
            return False

    # Unrecognised atom — conservative fail
    return False


def _eval_expression(expr: str, state: dict) -> bool:
    """Evaluate an invoked_when expression against pipeline_state.

    Handles AND / OR conjunctions (left-to-right, AND before OR per natural
    precedence). Atoms are evaluated by _eval_atom.
    """
    # Normalise whitespace
    expr = expr.strip()
    if not expr:
        return False

    # OR split (lowest precedence)
    or_parts = re.split(r"\s+OR\s+", expr, flags=re.IGNORECASE)
    if len(or_parts) > 1:
        return any(_eval_expression(part, state) for part in or_parts)

    # AND split
    and_parts = re.split(r"\s+AND\s+", expr, flags=re.IGNORECASE)
    if len(and_parts) > 1:
        return all(_eval_atom(part.strip(), state) for part in and_parts)

    return _eval_atom(expr, state)


# ─────────────────────────────────────────────────────────────────────────────
# Contract loader
# ─────────────────────────────────────────────────────────────────────────────

def _load_contracts(path: str) -> dict:
    """Load specialist-contracts.yaml."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"specialist-contracts.yaml not found: {path}")
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if HAS_YAML:
        data = yaml.safe_load(raw)
    else:
        raise ImportError(
            "PyYAML is required. Install with: pip install pyyaml"
        )
    if not isinstance(data, dict) or "specialists" not in data:
        raise ValueError("specialist-contracts.yaml must contain a 'specialists' mapping")
    return data


def _load_pipeline_state(source: str) -> dict:
    """Load pipeline state from JSON string or YAML file path."""
    source = source.strip()
    # JSON inline string
    if source.startswith("{"):
        try:
            return json.loads(source)
        except json.JSONDecodeError as e:
            raise ValueError(f"pipeline_state JSON parse error: {e}") from e
    # File path
    if not os.path.exists(source):
        raise FileNotFoundError(f"pipeline-state file not found: {source}")
    with open(source, encoding="utf-8") as f:
        raw = f.read()
    if HAS_YAML and (source.endswith(".yaml") or source.endswith(".yml")):
        data = yaml.safe_load(raw)
    else:
        data = json.loads(raw)
    return data if isinstance(data, dict) else {}


# ─────────────────────────────────────────────────────────────────────────────
# Input serializer
# ─────────────────────────────────────────────────────────────────────────────

def _serialize_input(specialist_id: str, contract: dict, pipeline_state: dict) -> dict:
    """Build a minimal serialized input for the specialist from pipeline_state.

    Only includes fields declared in input_schema that are present in
    pipeline_state. Missing fields are kept as empty stubs (typed neutral
    values) so the specialist can proceed gracefully.
    """
    schema = contract.get("input_schema", {})
    serialized: dict = {}
    for field, field_def in schema.items():
        if field in pipeline_state:
            serialized[field] = pipeline_state[field]
        elif isinstance(field_def, dict) and field_def.get("type") == "list":
            serialized[field] = []  # empty list stub
        elif field_def == "string" or (isinstance(field_def, dict) and field_def.get("type") == "string"):
            serialized[field] = ""  # empty string stub
        else:
            serialized[field] = None
    return serialized


# ─────────────────────────────────────────────────────────────────────────────
# Core dispatch logic
# ─────────────────────────────────────────────────────────────────────────────

def dispatch(
    phase_id: str,
    pipeline_state: dict,
    contracts: dict,
    *,
    force_dormant: bool = False,
) -> dict:
    """Evaluate specialists and return dispatch result.

    Failure isolation: each specialist is evaluated independently. An
    evaluation exception is caught, logged to errors[], and processing
    continues for the remaining specialists (error_propagation=false).

    Args:
        phase_id: Current pipeline phase (e.g. "P4.5", "P4", "P2")
        pipeline_state: Current pipeline state dict
        contracts: Loaded specialist-contracts.yaml data
        force_dormant: When True, include specialists with status=dormant

    Returns:
        Dict with keys: phase_id, specialists_to_invoke, skipped, errors
    """
    result: dict = {
        "phase_id": phase_id,
        "specialists_to_invoke": [],
        "skipped": [],
        "errors": [],
    }

    specialists_section = contracts.get("specialists", {})
    if not isinstance(specialists_section, dict):
        result["errors"].append("'specialists' section is not a mapping in contracts")
        return result

    for spec_id, contract in specialists_section.items():
        if not isinstance(contract, dict):
            result["errors"].append(f"{spec_id}: contract entry is not a mapping — skipped")
            continue

        # ── Dormant gate ────────────────────────────────────────────────────
        # Specialists in agent files carry status: dormant. The contract does
        # not replicate status — dispatcher skips when phase mismatch makes it
        # irrelevant or force_dormant is False (default).
        triggers_in_phase = contract.get("triggers_in_phase", "")
        if not force_dormant and triggers_in_phase and triggers_in_phase != phase_id:
            result["skipped"].append({
                "id": spec_id,
                "reason": f"triggers_in_phase={triggers_in_phase} does not match current phase_id={phase_id}",
            })
            continue

        # ── Evaluate invoked_when expression ───────────────────────────────
        invoked_when = contract.get("invoked_when", "")
        try:
            should_invoke = _eval_expression(invoked_when, pipeline_state)
        except Exception as exc:  # noqa: BLE001
            # Failure isolation: catch ALL exceptions per AC-5
            result["errors"].append(
                f"{spec_id}: expression evaluation error ({exc!r}) — skipped safely"
            )
            continue

        if not should_invoke:
            result["skipped"].append({
                "id": spec_id,
                "reason": f"invoked_when='{invoked_when}' evaluated False for current pipeline_state",
            })
            continue

        # ── Build invocation entry ──────────────────────────────────────────
        try:
            serialized_input = _serialize_input(spec_id, contract, pipeline_state)
        except Exception as exc:  # noqa: BLE001
            result["errors"].append(
                f"{spec_id}: input serialization error ({exc!r}) — skipped safely"
            )
            continue

        result["specialists_to_invoke"].append({
            "id": spec_id,
            "agent_file": contract.get("agent_file", f"squads/research/agents/{spec_id}.md"),
            "triggers_in_phase": triggers_in_phase,
            "failure_mode": contract.get("failure_mode", "warn_and_continue"),
            "serialized_input": serialized_input,
            "available_tools": contract.get("available_tools", []),
        })

    return result


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate specialist invocation conditions for a given pipeline phase.",
    )
    parser.add_argument(
        "--phase-id",
        required=True,
        help="Current pipeline phase identifier (e.g. P4.5, P4, P2, P1.5)",
    )
    parser.add_argument(
        "--pipeline-state",
        required=True,
        help=(
            "Pipeline state as JSON string '{...}' OR path to pipeline-state.yaml"
        ),
    )
    parser.add_argument(
        "--contracts",
        default=_DEFAULT_CONTRACTS,
        help=(
            f"Path to specialist-contracts.yaml "
            f"(default: {os.path.relpath(_DEFAULT_CONTRACTS)})"
        ),
    )
    parser.add_argument(
        "--force-dormant",
        action="store_true",
        default=False,
        help=(
            "Include specialists regardless of triggers_in_phase mismatch. "
            "Useful for testing individual specialists."
        ),
    )
    args = parser.parse_args()

    try:
        contracts = _load_contracts(args.contracts)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(json.dumps({"error": str(exc), "exit_code": 3}), file=sys.stderr)
        sys.exit(3)

    try:
        pipeline_state = _load_pipeline_state(args.pipeline_state)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "exit_code": 3}), file=sys.stderr)
        sys.exit(3)

    result = dispatch(
        phase_id=args.phase_id,
        pipeline_state=pipeline_state,
        contracts=contracts,
        force_dormant=args.force_dormant,
    )

    print(json.dumps(result, indent=2))

    # Exit non-zero if there were evaluation errors so callers can detect issues
    if result["errors"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
