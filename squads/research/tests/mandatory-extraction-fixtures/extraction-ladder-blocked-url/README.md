# Fixture: extraction-ladder-blocked-url

> **Tópico:** Validar extraction ladder com URL bloqueada (Cloudflare/paywall)

**Fixture purpose:** validates Story RA-F.3 AC-B2 — when a URL fails all
extraction steps (websearch → webfetch → etl → playwright), it is marked
`extraction_quality: blocked_fallback_used` with explicit `extraction_notes`
and `extraction_ladder_steps_tried` showing the trail. The ladder NEVER
silences failures.

## Expected validator output

When `output_validator.py --skill tech-research` runs against this fixture:

- `check_extraction_ladder()` PASSES (blocked entry has notes + steps log).
- Default `--enforcement warn` → exit code 0.

## Files

- `README.md` — this file
- `02-research-report.md` — minimal narrative atom
- `sources.yaml` — includes a blocked source with full ladder log
- `pipeline-state.yaml` — minimal state
- `metrics.yaml` — minimal metrics
- `curiosity_queue.yaml` — empty queue

## Acceptance criteria covered

- AC-B2 — schema enrichment with extraction_* fields
- AT-3 — extraction success/failure tracked explicitly

## Scope

```
scope_declaration:
  patterns: [single_player]
  candidates_count: 1
```
