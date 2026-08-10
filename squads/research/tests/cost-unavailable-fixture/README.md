# Fixture — cost_confidence: unavailable (AC-5)

## Story

STORY-RA-A.2 — AC-5: Mock unavailable cost signal tested.

## Purpose

Verify the heartbeat policy correctly ignores the `cost_usd_used > cost_max` signal
when `cost_confidence` is `unavailable` (SDK failure + tiktoken failure).

Without this guard, a false-positive stop would halt the pipeline when the cost
meter is simply broken — not when the budget is actually exhausted.

## Scenario

```
cost_usd_used = 3.00   >   cost_max = 2.50   → would normally fire cost_usd stop
cost_confidence = unavailable               → signal IGNORED
```

Other signals do not fire (wave=1, coverage=42, token=30%). Decision: **CONTINUE**.

## Expected Output from `phase-summary` command

```json
{
  "coverage": 0.42,
  "token_used_pct": 0.30,
  "wallclock_sec": 180.0,
  "cost_usd": null,
  "cost_confidence": "unavailable",
  "cost_signal_ignored": true,
  "gaps_open": 2,
  "new_info_ratio": 0.35,
  "decision": "CONTINUE",
  "rationale": "Coverage 42.0% below threshold, wave 1",
  "stop_rule": "CONTINUE",
  "wave": 1,
  "high_sources": 2
}
```

Key assertions:
- `cost_usd` is `null` (not a false positive 3.00)
- `cost_confidence` is `"unavailable"`
- `cost_signal_ignored` is `true`
- `decision` is `"CONTINUE"` (not STOP from cost_usd)

## How to Run

```bash
echo '{
  "coverage": 0.42,
  "token_used_pct": 0.30,
  "wallclock_sec": 180,
  "cost_usd": 3.00,
  "cost_confidence": "unavailable",
  "gaps_open": 2,
  "new_info_ratio": 0.35,
  "wave": 1,
  "high_sources": 2
}' | python squads/research/scripts/tech-research/coverage_calculator.py phase-summary
```

Assert: `cost_signal_ignored == true` AND `decision == "CONTINUE"`.
