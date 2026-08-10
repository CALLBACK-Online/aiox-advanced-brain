# Fixture 02 — Coverage Score Stop + Wave Low Signal Replan

## Purpose

Synthetic fixture exercising the `coverage_score` stop signal (priority 5)
AND the `wave_returned_low_signal` replan signal.
Wave 2, coverage reached 74%. Budget healthy, no economic signals fire.
Expected decision: STOP with matched_signal=coverage_score.

## Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `wave_max_with_low_coverage` | wave_num == 3 AND coverage < 50 | no (wave_num=2) |
| `token_budget` | token_budget_used > 0.85 | no (0.52) |
| `cost_usd` | cost_usd_used > cost_max | no (0.82 < 5.00) |
| `wallclock` | wallclock_used > timeout_sec | no (340 < 900) |
| `coverage_score` | coverage_score >= 70 | **STOP** (74 >= 70) |
| `gap_convergence` | gap_set.is_empty() | no (always false until RA-B.1) |
| `new_information_ratio` | < 0.05 | no (0.18) |

## Replan Signals Expected to Fire

| Signal | Condition | Expected |
|---|---|---|
| `source_contradiction_detected` | true | no |
| `wave_returned_low_signal` | true | **REPLAN** |
| `unsupported_claim_top_tier` | > 20% | no (8%) |

Note: Replan fires alongside coverage_score STOP. Since STOP wins, replan is logged but
the run does not continue to wave 3. Demonstrates coexistence of STOP + REPLAN signals.

## Fixture State

```yaml
wave_num: 2
coverage_score: 74
token_budget_used: 0.52
cost_usd_used: 0.82
cost_max: 5.00
wallclock_used: 340
timeout_sec: 900
new_information_ratio: 0.18
gap_set_is_empty: false
source_contradiction_detected: false
wave_returned_low_signal: true
unsupported_claim_top_tier_ratio: 0.08
```

## Expected Output

```json
{
  "decision": "STOP",
  "matched_signal": "coverage_score",
  "stop_reason": "Coverage threshold reached.",
  "stop_reason_category": "decision_sufficiency",
  "replan_actions": ["pivot_query_phrasing"]
}
```
