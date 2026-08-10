# Changelog

## 2026-07-06 — skills/tech-research/SKILL.md

Movido para fora do contexto carregado.

## Changelog (v1.1.0 → v2.0.0)

| Change | Rationale |
|---|---|
| `config.yaml` rewrite | Added pack/process/artifact_contracts/checkpoints/knowledge_sources/invokes (AIOX-native pattern) |
| `squads/research/workflows/tech-research/tech-research-pipeline.yaml` NEW | Aggregate manifest (process_mapping target). Pattern parity with `aiox-pipeline.yaml`. |
| TeamCreate + TaskCreate added | Visual progress tracking (parity with `/processo de mapeamento AIOX`, `/aiox-validate-squad`, `/full-sdc`) |
| Incremental learning log | `.aiox/learning/logs/tech-research/` per `.claude/rules/incremental-learning-log.md`. Replaces ad-hoc `execution-log.jsonl`. |
| COVERAGE_GATE + CITATION_GATE formalized | Soft coverage thresholds promoted to formal VETO/REVIEW/APPROVE gates with bounded fix loops |
| 10 NON-NEGOTIABLE RULES | Pattern parity with reference skills |
| Halt Protocol | Pipeline-wide halt with learning log persistence (no provenance loss on failure) |
| CLI next-command suggestion (P5b) | Per `.claude/rules/cli-next-command-flow.md` |
| Frontmatter | Drop `context`, `agent` (per Frontmatter Purity Rule). Keep `owner_squad`, `aiox_tier` matching reference skills pattern. |
| Owner squad declared | `mega-brain` — research outputs feed knowledge management pipeline |
| Operational config preserved | `playwright_deep_research`, `search_waves`, `mcp_dependencies` unchanged |

Migration impact: zero — existing `docs/research/` folders remain valid; phase YAMLs unchanged; scripts unchanged. New runs write incremental learning logs (replaces ad-hoc `execution-log.jsonl`).

