# Bench Criteria — aiox_research vs 4 players

> Fixture for Story RA-F.1 AC-1 / AC-2 / AC-3 — emitted because `comparison_pattern=multi_player` AND `dimensions_count=5`.

```yaml
schema_version: "bench-criteria.v1"
slug: "2026-05-19-research-bench-multi-player-fixture"
date: "2026-05-19"
profile: gold_absorption
anchor: aiox_research
players: ["aiox_research", "openhands", "claude_code", "aider", "cline"]
players_count: 5
macro_dimensions_count: 5
microdimensions_count: 15
weights_file: "bench-weights.yaml"
```

```yaml
scoring_calibration:
  type: hybrid
  scale: "1-5"
  scale_description: "1=absent, 3=present-partial, 5=present-strong-with-evidence"
  baseline: "Deep Research Bench v1.2 reference scores + GitHub API snapshot 2026-05-19"
  calibrated_by: "@aiox-dev single-pass"
  disclaimer: |
    Scores are hybrid — analytical anchored to one empirical baseline per
    dimension. Inter-rater agreement NOT measured.
  reproducibility: high
```

Framework-agnosticism pledge applied — NO `aiox_fit`, NO anchor-only-satisfiable axes.

## Macro Dimensions

(5 universal dimensions; see `comparison-matrix.json` for cell scores.)

| id | label | weight |
|---|---|---|
| agentic_planning_control | Agentic planning + control loop | 18 |
| tool_runtime_integration | MCP/browser/scholarly native | 18 |
| research_depth_synthesis | Source coverage + deep-read | 14 |
| multi_agent_orchestration | Spawn + parallel + roles | 12 |
| evidence_fidelity_evaluation | Citation gate + verified_ratio | 10 |
