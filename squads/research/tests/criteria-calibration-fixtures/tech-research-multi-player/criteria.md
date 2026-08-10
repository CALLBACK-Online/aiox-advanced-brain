# Criteria — 5 Open-Source Research Stacks

> Fixture for Story RA-F.1 AC-1 — emitted because `comparison_pattern=multi_player` AND `dimensions_count=5`.

```yaml
schema_version: "research-criteria.v1"
slug: "tech-research-multi-player-fixture"
date: "2026-05-19"
comparison_pattern: "multi_player"
players_count: 5
dimensions_count: 5
emitted_by: "/tech-research"
phase: "M7/P5 — Document Final Artifacts"
paired_artifacts:
  matrix: "matrices.yaml"
  scoring_script: "scripts/scoring-tech-research-multi-player-fixture.py"
```

```yaml
scoring_calibration:
  type: hybrid
  scale: "1-5"
  scale_description: "1=absent, 3=present-partial, 5=present-strong-with-evidence"
  baseline: "GitHub API snapshot 2026-05-19 + maintainer docs review"
  calibrated_by: "@aiox-dev single-pass"
  disclaimer: |
    Scores are hybrid — interpretive judgment anchored to one empirical
    baseline per dimension. Inter-rater agreement was NOT measured.
  reproducibility: high
```

## Dimensions

### Dimension 1 — agentic_planning

```yaml
id: agentic_planning
label: "Agentic Planning & Control"
operational_definition: |
  Degree to which the stack plans multi-step actions, supports
  long-horizon goals, and exposes plan as a first-class object.
evidence_signals:
  - "presence of explicit plan/replan API"
  - "documented loop-control primitives"
  - "real-run traces showing >3 reasoning hops"
scale_anchors:
  1: "chat-style one-shot, no planning"
  3: "tool-call loop with implicit planning"
  5: "explicit plan object + replan + audit trace"
weight: 0.30
weight_rationale: "Critical for absorption — differentiates research stacks from chat wrappers."
justification: "02-research-report.md §1"
```

### Dimension 2 — tool_runtime

```yaml
id: tool_runtime
label: "Tool Runtime Integration"
operational_definition: "MCP/browser/arXiv/PubMed native support."
evidence_signals:
  - "MCP server documented"
  - "browser tool native"
  - "scholarly DB adapters"
scale_anchors:
  1: "no external tools"
  3: "1-2 tool integrations"
  5: "MCP-native + multi-source"
weight: 0.25
weight_rationale: "Surface scrapers vs real research stacks."
justification: "02-research-report.md §2"
```

### Dimension 3 — multi_agent

```yaml
id: multi_agent
label: "Multi-Agent Orchestration"
operational_definition: "Spawned sub-agents, role specialization, parallel exec."
evidence_signals:
  - "Agent tool / sub-agent spawn API"
  - "parallel execution evidence"
  - "role specialization in docs"
scale_anchors:
  1: "single agent loop"
  3: "static role split"
  5: "dynamic spawn + parallel"
weight: 0.20
weight_rationale: "Differentiates monolithic loops from teams."
justification: "02-research-report.md §3"
```

### Dimension 4 — evidence_fidelity

```yaml
id: evidence_fidelity
label: "Evidence Fidelity & Citation Verification"
operational_definition: "Citation gates, source dating, confidence tagging."
evidence_signals:
  - "verified_ratio gate documented"
  - "source date enforcement"
  - "confidence tag schema"
scale_anchors:
  1: "no citation discipline"
  3: "citations present, no gate"
  5: "verified_ratio>=0.85 gate"
weight: 0.15
weight_rationale: "Anti-hallucination floor."
justification: "02-research-report.md §4"
```

### Dimension 5 — ux_control

```yaml
id: ux_control
label: "UX Operator Control"
operational_definition: "Pause/resume, intermediate review, replan from operator."
evidence_signals:
  - "interrupt API"
  - "operator-in-the-loop UX"
  - "documented control primitives"
scale_anchors:
  1: "no operator control during run"
  3: "pause only"
  5: "pause + replan + audit"
weight: 0.10
weight_rationale: "Recovers cost when agent goes off-script."
justification: "02-research-report.md §5"
```

## Caps & Field-Name Conventions

| Raw Field | Cap | Source |
|---|---|---|
| `stargazers_count_snapshot_at_2026-05-19` | snapshot — frozen at date | github.com |
| `contributors_api_capped_100` | GitHub API cap | github.com contributors endpoint |
