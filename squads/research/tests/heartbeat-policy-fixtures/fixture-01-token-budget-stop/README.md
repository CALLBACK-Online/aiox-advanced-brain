# Fixture 01 — Token Budget Hard Stop

## Purpose

Synthetic fixture exercising the `token_budget` stop signal (priority 2).
At wave 1, token budget is already 91% consumed — above the 0.85 threshold.
Expected decision: STOP with matched_signal=token_budget.

## Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `token_budget` | token_budget_used > 0.85 | **STOP** |
| `wave_max_with_low_coverage` | wave_num == 3 AND coverage_score < 50 | no (wave_num=1) |
| `coverage_score` | coverage_score >= 70 | no (coverage=42) |
| `new_information_ratio` | new_information_ratio < 0.05 | no (ratio=0.42) |

## Replan Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `unsupported_claim_top_tier` | > 20% | **REPLAN** (24% in this fixture) |

## Fixture State

```yaml
wave_num: 1
coverage_score: 42
token_budget_used: 0.91      # > 0.85 → fires token_budget stop
cost_usd_used: 0.18
cost_max: 5.00
wallclock_used: 180
timeout_sec: 900
new_information_ratio: 0.42
gap_set_is_empty: false
source_contradiction_detected: false
wave_returned_low_signal: false
unsupported_claim_top_tier_ratio: 0.24
```

## Expected Output

```json
{
  "decision": "STOP",
  "matched_signal": "token_budget",
  "stop_reason": "Token budget 85% consumed. Reserving 15% headroom for synthesis, citation verification, and documentation phases.",
  "stop_reason_category": "budget_limit",
  "replan_actions": ["inject_citation_recovery_subquery"]
}
```

Note: Even though a replan signal fired, STOP takes precedence. Replan actions are logged
but not acted upon — the run is halting, not continuing to the next wave.
