# Ingest Multimodal Sources

<!-- AIOX accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- AIOX Domain: Tactical -->

## AIOX Task Anatomy (8 sections — STORY-SWI-1)

```yaml
task: ingestMultimodalSources
atomic_layer: Atom
responsavel_type: Worker
Domain: Tactical
session: null
phase: P00.5
Inputs:
  - { name: routing-decisions.yaml, type: yaml, source: route-sources (P00) }
  - { name: briefing.normalized.json, type: json, source: normalize-briefing (P00) }
Outputs:
  - { name: ingestion-bundle.yaml, schema_ref: packages/slides-core/src/ingestion/types.ts#IngestionResult, lifecycle: [draft, validated] }
  - { name: ingestion-bundle-report.json, description: "verdict PASS|FAIL + extraction_gap ratio" }
Pre_conditions:
  - routing-decisions.yaml exists
  - briefing.normalized.json exists
Post_conditions:
  - ingestion-bundle.yaml emitted with one entry per routed source
  - each source status is ok OR extraction_gap
  - ingestion-bundle-report.json written by validate-ingestion-bundle
Acceptance_criteria:
  - All sources in routing-decisions.yaml processed without silent drop
  - Adapter failures emit extraction_gap(reason), never universal fallback content
  - extraction_gap_count / source_count < 0.5 required for PASS
Performance:
  duration_target: "< 2s p99 per source"
  parallelizable_sources: true
Error_handling:
  strategy: "emit extraction_gap(reason) per source; halt P00.5 when gap_ratio >= 0.5"
  on_source_failure: emit_extraction_gap_with_reason
  halt_threshold: "gap_ratio >= 0.5"
  no_universal_fallback: true
handoff_token: ingest-multimodal-sources
```

## Implementation Contract

This task wires `packages/slides-core/src/ingestion/pipeline.ts#ingest()` and the lazy adapters in
`packages/slides-core/src/ingestion/adapters.ts`. It must not re-implement parsing, transcript
extraction, chunking, or media resolution.

Gap states are valid per source. A source-level gap is not a workflow crash unless the bundle-level
gap ratio reaches the blocking threshold:

```yaml
sources:
  - source_index: 2
    adapter_id: null
    status: extraction_gap
    reason: low_confidence_routing
    chunks: []
    evidence_index: []
```
