# Fixture 03 — Wave Max + Low Coverage Hard Stop + Source Contradiction Replan

## Purpose

Synthetic fixture exercising the `wave_max_with_low_coverage` stop signal (priority 1)
AND the `source_contradiction_detected` replan signal.
Wave 3, coverage still only 38%. Hard stop — highest priority signal.
Expected decision: STOP with matched_signal=wave_max_with_low_coverage.

## Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `wave_max_with_low_coverage` | wave_num == 3 AND coverage < 50 | **STOP** (priority 1) |
| `new_information_ratio` | < 0.05 | also fires (priority 7) but wave_max wins |

## Replan Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `source_contradiction_detected` | true | **REPLAN** |

Note: Both wave_max_with_low_coverage (stop priority 1) AND new_information_ratio (priority 7)
fire. Priority 1 is the matched_signal reported. new_information_ratio is logged as
also_fired but not the matched_signal.

This fixture demonstrates:
- Stop signal priority ordering (lower number = higher priority)
- Multiple stop signals firing simultaneously
- Replan signals coexisting with stop (logged, not acted upon)
- VETO caveat should be emitted in the final report when this stop fires

## Fixture State

```yaml
wave_num: 3
coverage_score: 38
token_budget_used: 0.78       # < 0.85, budget not exhausted
cost_usd_used: 1.45
cost_max: 5.00
wallclock_used: 650
timeout_sec: 900
new_information_ratio: 0.03   # < 0.05, also fires (priority 7)
gap_set_is_empty: false
source_contradiction_detected: true
wave_returned_low_signal: false
unsupported_claim_top_tier_ratio: 0.11
```

## Expected Output

```json
{
  "decision": "STOP",
  "matched_signal": "wave_max_with_low_coverage",
  "stop_reason": "Wave 3 exhausted with coverage below acceptable threshold.",
  "stop_reason_category": "max_waves",
  "also_fired": ["new_information_ratio"],
  "replan_actions": ["inject_contradiction_resolution_subquery"]
}
```
