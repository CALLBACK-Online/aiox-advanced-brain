# Research Report — 5 Open-Source Research Stacks Compared

## Scope

```yaml
scope_declaration: |
  Comparing 5 stacks for absorption analysis across 5 universal dimensions.
  Framework-agnostic per .claude/rules/bench-weight-calibration.md.
```

## Findings

The five stacks differ materially on agentic planning, tool runtime, and
multi-agent orchestration. See `criteria.md` for the framework and
`matrices.yaml` for per-cell scores. [HIGH — verified across 5 GitHub repos
2026-05-19](https://github.com/anthropics/claude-code) — 2026

[HIGH — Aider docs 2026-05-19](https://aider.chat/docs) — 2026 — confirms
single-agent loop with no parallelism.

[HIGH — Cline architecture 2026-05-19](https://github.com/cline/cline) — 2026
— evidence of MCP runtime integration but no spawned sub-agents.

[MEDIA — OpenHands paper 2026](https://arxiv.org/abs/2407.16741) — 2026 —
multi-agent orchestration claimed but evidence partial in benchmark runs.

[HIGH — Cursor changelog 2026-05](https://cursor.sh/changelog) — 2026 —
agentic planning limited to chat orchestration.

## Stop Reason

coverage_gate_passed at 88% overall, all rubrics above threshold.
