# Specialist Dispatch Fixture — PoC Mini (Story RA-C.1)

**Purpose:** Validate `specialist_dispatcher.py` failure isolation guarantee.

SPIKE-RA-C.0 confirmed: Task tool parallel spawn is viable. This fixture is
the PoC required by Story RA-C.1 AC-4 before the full dispatcher implementation
was committed. It demonstrates:

1. **Happy path:** Sackett dispatched correctly when `evidence_grading_required == true`
2. **Failure isolation:** A malformed expression in a fixture specialist causes
   that specialist to be skipped with an error entry — other specialists are
   unaffected (`error_propagation=false`)

## Running the PoC

```bash
# From repo root
cd squads/research/tests/specialist-dispatch-fixture

# Run the Python PoC directly
python poc_dispatch.py

# Or run via pytest
cd squads/research/scripts/tech-research/tests
python -m pytest ../../../tests/specialist-dispatch-fixture/test_poc_dispatch.py -v
```

## Expected output

```
=== Specialist Dispatch PoC — RA-C.1 ===

Test 1: Sackett dispatched on P4.5 evidence_grading_required=true
  specialists_to_invoke: ['sackett']
  skipped: 4 specialists (phase mismatch)
  errors: []
  PASS

Test 2: Failure isolation — malformed specialist does NOT block sackett
  specialists_to_invoke: ['sackett']
  errors: ['bad_specialist: expression evaluation error ...']
  isolation confirmed: error_propagation=false
  PASS
```

## PoC Evidence (AC-4)

- Sackett invoked via Task-tool-style contract: input_schema serialized correctly
- Execution: synchronous (no Task tool in PoC; contract serialization validated)
- Output schema validated: graded_claims structure matches sackett output_schema
- Isolation: error in bad_specialist does NOT prevent sackett dispatch
- Timing: < 50ms (Python dict evaluation, no I/O except file load)

## Result

GO — dispatcher design is viable. Failure isolation confirmed.
See story RA-C.1 Dev Agent Record for full evidence log.
