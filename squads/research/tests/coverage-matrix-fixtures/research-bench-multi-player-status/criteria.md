# Bench Criteria — research-bench-multi-player-status fixture

> F.1 anchor stub for research-bench AC-1 trigger.

```yaml
schema_version: "bench-criteria.v1"
slug: "fixture-research-bench-multi-player-status"
date: "2026-05-19"
profile: "standard"
anchor: "claude_code"
players: ["claude_code", "aider", "cline", "openhands", "cursor"]
players_count: 5
macro_dimensions_count: 5

scoring_calibration:
  type: hybrid
  scale: "0-2"
  baseline: "coverage_matrix_helper.py canonical 4-level map"
  calibrated_by: "@aiox-dev fixture stub"
  disclaimer: "Hybrid scores; status→score via helper"
  reproducibility: high
```

## Macro Dimensions

| Group | Weight |
|---|---|
| `agentic_planning_control` | 0.18 |
| `tool_runtime_integration` | 0.18 |
| `research_depth_synthesis` | 0.15 |
| `multi_agent_orchestration` | 0.12 |
| `evidence_fidelity_evaluation` | 0.12 |

## Rejected Dimensions

| Axis | Excluded Because |
|---|---|
| `aiox_fit` | Framework-agnostic mandate |

---

*Fixture criteria.md research-bench stub.*
