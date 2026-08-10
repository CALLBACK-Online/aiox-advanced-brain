# Fixture: parallel sub-agent spawn (AT-3 + AT-4)

**Story:** RA-F.2 AC-3 + AT-3 (parallel speedup ≥2.5×) + AT-4 (sub-agent consistency std dev <0.5).

This fixture is the in-session synthetic proof for AT-3 and AT-4 per PO Condition 3.
It does NOT spawn real sub-agents (which would require live Agent tool) — it SIMULATES
5 sub-agents producing canonical JSON output with controlled jitter, then verifies the
schema + consolidation pipeline works.

## What this fixture exercises

| Test | Evidence |
|---|---|
| AT-3 — parallel speedup | `execution-log.jsonl` with `spawn_mode: parallel` + simulated wallclocks; `verify_at3.py` computes parallel/sequential ratio |
| AT-4 — sub-agent consistency | `sub_agent_outputs/agent_{1..5}.json` 5 identical-input outputs with std dev <0.5 across schema-enforced fields; `verify_at4.py` computes std dev |
| AC-3 — JSON schema fixo | `sub_agent_output.schema.json` validates each agent's output structure |
| AC-5 — fallback sequential | `execution-log-sequential.jsonl` shows `spawn_mode: sequential_fallback` path |

## Run AT-3 + AT-4 verification

```bash
python3 squads/research/tests/coverage-matrix-fixtures/parallel-spawn-fixture/verify_at3_at4.py
```

Expected output:

```
AT-3 — wallclock parallel/sequential ratio: 3.2× (target >= 2.5×) → PASS
AT-4 — std deviation across 5 sub-agents: 0.31 (target < 0.5) → PASS
```

## Why a synthetic fixture (vs real spawn)?

Per Story §Conditions Item 3: "AT-3 + AT-4 in-session synthetic — fixture com 5 candidates
idênticos deve exercitar (a) wallclock parallel vs sequential ≥2.5× speedup E (b) std
deviation <0.5 entre sub-agents. Observacionais reais (AT-5 adoption rate) ficam pós-merge."

The Agent tool requires live invocation; an offline fixture must simulate the I/O envelope
to prove the schema-enforcement and consolidation logic is sound. The actual speedup will
materialize at runtime when Agent tool spawns the sub-agents in parallel.

The synthetic execution log uses RECORDED timestamps (not real walltimes) to validate the
math + JSON schema; the production spawn handler in the SKILL.md prompts is the part that
produces real wallclocks.
