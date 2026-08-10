# Fixture: multi-player-gap-analysis

> **Tópico:** Comparar 3 frameworks de research (multi_player)

**Fixture purpose:** validates Story RA-F.3 AC-C1 / AC-C2 — when
`comparison_pattern: multi_player` and there are ≥2 candidates,
`gap-analysis.md` MUST exist as standalone atom, and `02-research-report.md`
MUST cross-link to it.

## Expected validator output

When `output_validator.py --skill tech-research` runs against this fixture:

- `check_gap_analysis_presence()` PASSES (`gap-analysis.md` exists + cross-link present).
- Default `--enforcement warn` → exit code 0.

## Files

- `README.md` — this file
- `02-research-report.md` — narrative with cross-link to gap-analysis.md
- `gap-analysis.md` — standalone gap-analysis atom
- `matrices.yaml` — multi_player scored atom (3 candidates)
- `pipeline-state.yaml` — declares comparison_pattern: multi_player
- `metrics.yaml` — minimal metrics
- `curiosity_queue.yaml` — minimal queue

## Acceptance criteria covered

- AC-C1 — gap-analysis.md atomo presente quando multi_player
- AC-C2 — cross-link em 02-research-report.md
- AT-4 — gap-analysis adoption (mandatory in multi_player)

## Scope

```
scope_declaration:
  patterns: [multi_player]
  candidates_count: 3
```
