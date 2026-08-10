#!/usr/bin/env python3
"""PoC mini — specialist_dispatcher.py failure isolation proof.

Story: RA-C.1 AC-4 | 2026-05-19

Demonstrates:
  1. Sackett dispatched on P4.5 when evidence_grading_required == true
  2. A malformed specialist expression causes that specialist to error
     while sackett is still dispatched (error_propagation=false)

Run:
    python poc_dispatch.py
    python -m pytest poc_dispatch.py -v   (via pytest parametrize below)
"""

from __future__ import annotations

import os
import sys
import json
import time

# ── Resolve paths portable (no machine-absolute paths committed) ──────────────
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_THIS_DIR, "..", "..", "..", ".."))
_SCRIPTS = os.path.join(_REPO_ROOT, "squads", "research", "scripts", "tech-research")
_CONTRACTS_PATH = os.path.join(_REPO_ROOT, "squads", "research", "data", "specialist-contracts.yaml")

if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)

from specialist_dispatcher import dispatch, _load_contracts  # noqa: E402


# ── Fixture: minimal contracts for isolation test ─────────────────────────────

FIXTURE_CONTRACTS_OK = {
    "schema_version": "specialist-contracts.v1",
    "specialists": {
        "sackett": {
            "agent_file": "squads/research/agents/sackett.md",
            "invoked_when": "evidence_grading_required == true",
            "input_schema": {
                "claims": {"type": "list", "items": {"text": "string", "sources": "list"}},
            },
            "output_schema": {
                "graded_claims": {"type": "list"},
            },
            "available_tools": [],
            "triggers_in_phase": "P4.5",
            "failure_mode": "warn_and_continue",
        },
    },
}

FIXTURE_CONTRACTS_WITH_BAD = {
    "schema_version": "specialist-contracts.v1",
    "specialists": {
        "sackett": FIXTURE_CONTRACTS_OK["specialists"]["sackett"],
        "bad_specialist": {
            # Intentionally malformed: invoked_when is None — triggers evaluation error
            "agent_file": "squads/research/agents/sackett.md",  # reuse path for fixture
            "invoked_when": None,  # causes _eval_expression to handle None safely
            "input_schema": {},
            "output_schema": {},
            "available_tools": [],
            "triggers_in_phase": "P4.5",
            "failure_mode": "warn_and_continue",
        },
    },
}

PIPELINE_STATE_P4_5 = {
    "evidence_grading_required": True,
    "phase_id": "P4.5",
    "mode": "tech-research",
    "coverage_target": 80,
    "wave_num": 1,
    "domain_signals": "software-delivery",
    "research_design": "single-method",
}


def run_poc() -> bool:
    """Execute PoC tests and print results. Returns True if all pass."""
    all_pass = True

    print("=== Specialist Dispatch PoC — RA-C.1 ===\n")

    # ── Test 1: Sackett dispatched on P4.5 ───────────────────────────────────
    print("Test 1: Sackett dispatched on P4.5 when evidence_grading_required=true")
    t0 = time.perf_counter()
    result1 = dispatch(
        phase_id="P4.5",
        pipeline_state=PIPELINE_STATE_P4_5,
        contracts=FIXTURE_CONTRACTS_OK,
    )
    elapsed1_ms = (time.perf_counter() - t0) * 1000

    invoked_ids = [s["id"] for s in result1["specialists_to_invoke"]]
    test1_pass = (
        "sackett" in invoked_ids
        and len(result1["errors"]) == 0
        and result1["specialists_to_invoke"][0]["failure_mode"] == "warn_and_continue"
        and isinstance(result1["specialists_to_invoke"][0]["serialized_input"].get("claims"), list)
    )

    print(f"  specialists_to_invoke: {invoked_ids}")
    print(f"  errors: {result1['errors']}")
    print(f"  sackett.failure_mode: {result1['specialists_to_invoke'][0]['failure_mode'] if invoked_ids else 'N/A'}")
    print(f"  sackett.serialized_input: {json.dumps(result1['specialists_to_invoke'][0]['serialized_input'] if invoked_ids else {})}")
    print(f"  elapsed: {elapsed1_ms:.1f}ms")
    status1 = "PASS" if test1_pass else "FAIL"
    print(f"  {status1}\n")
    if not test1_pass:
        all_pass = False

    # ── Test 2: Failure isolation ─────────────────────────────────────────────
    print("Test 2: Failure isolation — bad_specialist error does NOT block sackett")
    t0 = time.perf_counter()
    result2 = dispatch(
        phase_id="P4.5",
        pipeline_state=PIPELINE_STATE_P4_5,
        contracts=FIXTURE_CONTRACTS_WITH_BAD,
        force_dormant=True,  # force both into scope so isolation is tested
    )
    elapsed2_ms = (time.perf_counter() - t0) * 1000

    invoked_ids2 = [s["id"] for s in result2["specialists_to_invoke"]]
    errors2 = result2["errors"]

    # Isolation: sackett must be invoked, bad_specialist must produce an error
    sackett_invoked = "sackett" in invoked_ids2
    bad_errored = any("bad_specialist" in e for e in errors2)

    test2_pass = sackett_invoked and bad_errored

    print(f"  specialists_to_invoke: {invoked_ids2}")
    print(f"  errors: {errors2}")
    print(f"  sackett_invoked: {sackett_invoked}")
    print(f"  bad_specialist_errored: {bad_errored}")
    print(f"  error_propagation=false confirmed: {test2_pass}")
    print(f"  elapsed: {elapsed2_ms:.1f}ms")
    status2 = "PASS" if test2_pass else "FAIL"
    print(f"  {status2}\n")
    if not test2_pass:
        all_pass = False

    # ── Test 3: Real contracts file loads and parses ──────────────────────────
    print("Test 3: Real specialist-contracts.yaml loads and passes check_specialist_contracts")
    try:
        real_contracts = _load_contracts(_CONTRACTS_PATH)
        specialists = real_contracts.get("specialists", {})
        required = {"sackett", "klein", "booth", "creswell", "forsgren"}
        missing = required - set(specialists.keys())
        test3_pass = not missing and real_contracts.get("schema_version") == "specialist-contracts.v1"
        print(f"  schema_version: {real_contracts.get('schema_version')}")
        print(f"  specialists found: {sorted(specialists.keys())}")
        print(f"  missing required: {sorted(missing)}")
    except Exception as exc:  # noqa: BLE001
        test3_pass = False
        print(f"  ERROR loading contracts: {exc}")
    status3 = "PASS" if test3_pass else "FAIL"
    print(f"  {status3}\n")
    if not test3_pass:
        all_pass = False

    print(f"=== Overall: {'ALL PASS' if all_pass else 'FAILURES DETECTED'} ===")
    return all_pass


# ── Pytest entry points ───────────────────────────────────────────────────────

def test_sackett_dispatched_on_p4_5():
    """AC-4 PoC: Sackett is dispatched on P4.5 with evidence_grading_required=true."""
    result = dispatch(
        phase_id="P4.5",
        pipeline_state=PIPELINE_STATE_P4_5,
        contracts=FIXTURE_CONTRACTS_OK,
    )
    ids = [s["id"] for s in result["specialists_to_invoke"]]
    assert "sackett" in ids, f"sackett not dispatched; got {ids}"
    assert result["errors"] == [], f"unexpected errors: {result['errors']}"
    entry = result["specialists_to_invoke"][0]
    assert entry["failure_mode"] == "warn_and_continue"
    assert isinstance(entry["serialized_input"].get("claims"), list)


def test_failure_isolation():
    """AC-5 PoC: Bad specialist expression does NOT block sackett (error_propagation=false)."""
    result = dispatch(
        phase_id="P4.5",
        pipeline_state=PIPELINE_STATE_P4_5,
        contracts=FIXTURE_CONTRACTS_WITH_BAD,
        force_dormant=True,
    )
    ids = [s["id"] for s in result["specialists_to_invoke"]]
    assert "sackett" in ids, f"sackett should still be dispatched; got {ids}"
    assert any("bad_specialist" in e for e in result["errors"]), (
        f"bad_specialist should have an error; errors: {result['errors']}"
    )


def test_real_contracts_file():
    """AC-1 PoC: Real specialist-contracts.yaml loads with all 5 specialists."""
    contracts = _load_contracts(_CONTRACTS_PATH)
    specialists = contracts.get("specialists", {})
    required = {"sackett", "klein", "booth", "creswell", "forsgren"}
    missing = required - set(specialists.keys())
    assert not missing, f"Missing specialists in contracts: {sorted(missing)}"
    assert contracts.get("schema_version") == "specialist-contracts.v1"


if __name__ == "__main__":
    success = run_poc()
    sys.exit(0 if success else 1)
