# Ingest Prior Deck

<!-- AIOX accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- AIOX Domain: Tactical -->

## AIOX Task Anatomy (8 sections — STORY-SWI-4)

```yaml
task: ingestPriorDeck
atomic_layer: Atom
responsavel_type: Worker
Domain: Tactical
session: null
phase: P00.5
conditional_on: "briefing.references[].extension == '.pptx'"
Inputs:
  - { name: briefing.normalized.json, type: json, source: normalize-briefing (P00), field: references[] }
Outputs:
  - { name: prior_deck_signals.yaml, schema_ref: squads/slides-creator/data/prior-deck-signals.schema.yaml, lifecycle: [draft, validated] }
Pre_conditions:
  - briefing.normalized.json exists
  - briefing.references[] contains at least one path with extension .pptx
Post_conditions:
  - prior_deck_signals.yaml emitted with signal_authority: false at root
  - extraction failures emit structured gaps per K6
  - if 0 .pptx refs: task skips cleanly and workflow continues
Acceptance_criteria:
  - parsePptx() invoked per .pptx reference via packages/slides-core/src/ingestion/pptx-reverse/index.ts
  - prior_deck_signals.yaml contains dominant_motif, chart_patterns, layout_inventory, palette_extracted, typography_extracted
  - signal_authority: false present at YAML root in complete, partial, and gap states
  - corrupt/empty .pptx emits structured gap and never fabricates a motif
Performance:
  duration_target: "< 3s p99 per .pptx file"
  optional_task: true  # skips cleanly if no .pptx refs
Error_handling:
  strategy: "emit extraction_gap(reason) per file; workflow continues regardless"
  on_parse_failure: emit_gap_workflow_continues
  no_fabrication: true
handoff_token: ingest-prior-deck
```

## K7 Boundary

`prior_deck_signals.yaml` is advisory only. It may enrich `define-design-direction`, but it never
replaces `design-direction.yaml` and never bypasses KI-10. The root field is immutable:

```yaml
signal_authority: false
```

Gap output must stay explicit:

```yaml
signal_authority: false
extraction_status: gap
gap_reason: corrupt_zip
dominant_motif: null
chart_patterns: []
layout_inventory: []
palette_extracted: []
typography_extracted: {}
```
