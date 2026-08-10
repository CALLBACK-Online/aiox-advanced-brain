# Bench Criteria — tech-research-multi-player-status fixture

> Fixture stub anchoring AC-1 (F.1) trigger when matrices.yaml has multi_player + ≥5 dims.

```yaml
schema_version: "research-criteria.v1"
slug: "fixture-tech-research-multi-player-status"
date: "2026-05-19"
profile: "standard"
anchor: "claude_code"
players: ["claude_code", "aider", "cline", "openhands", "cursor"]
players_count: 5
macro_dimensions_count: 5
microdimensions_count: 15

scoring_calibration:
  type: hybrid
  scale: "0-2"
  baseline: "Status code helper canonical map (coverage_matrix_helper.py)"
  calibrated_by: "@aiox-dev fixture stub"
  disclaimer: "Hybrid scores derived from 4-level enum via helper."
  reproducibility: high
```

## Macro Dimensions

| Group | Operational Definition | Weight |
|---|---|---|
| `agentic_planning` | Sub-agent spawn + role specialization | 0.30 |
| `tool_runtime` | MCP/browser/runtime native support | 0.25 |
| `multi_agent` | Parallel team orchestration | 0.20 |
| `evidence_fidelity` | Citation + source verification | 0.15 |
| `ux_control` | Operator-control surface | 0.10 |

## Rejected Dimensions

| Axis | Excluded Because |
|---|---|
| `sinkra_fit` | Framework-agnostic mandate per `.claude/rules/bench-weight-calibration.md` |

## Caps & Field-Name Conventions

| Field | Cap |
|---|---|
| N/A — fixture | this is a stub for F.2 validator exercising |

---

*Fixture criteria.md stub — F.1 trigger anchor for F.2 fixture.*
