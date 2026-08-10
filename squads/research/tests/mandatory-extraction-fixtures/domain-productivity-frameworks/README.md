# Fixture: domain-productivity-frameworks

> **Tópico:** Como melhorar a produtividade em equipes remotas

**Fixture purpose:** validates Story RA-F.3 AC-A2 — when the inferred domain
includes `productivity_frameworks`, Phase 1.5 must consult
`squads/research/data/mandatory-sources.yaml` and inject sub-queries from
literatures NOT covered by the base SCOPE angles. The learning log records
`mandatory_additions: [...]`.

## Expected validator output

When `output_validator.py --skill tech-research` runs against this fixture:

- `check_mandatory_sources_coverage()` PASSES (key `mandatory_additions` found
  in `pipeline-state.yaml`).
- Default `--enforcement warn` → exit code 0.

## Files

- `README.md` — this file
- `02-research-report.md` — minimal narrative atom (skeleton)
- `pipeline-state.yaml` — declares `mandatory_additions`
- `metrics.yaml` — minimal metrics
- `curiosity_queue.yaml` — minimal queue
- `sources.yaml` — minimal source manifest

## Acceptance criteria covered

- AC-A2 — mandatory_additions logged in learning provenance
- AT-1 — coverage activation (mandatory_additions present)

## Scope

```
scope_declaration:
  patterns: [single_player]
  candidates_count: 1
```
