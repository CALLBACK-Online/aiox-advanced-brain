# Extract Evidence From Ingestions

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Tactical -->

## SINKRA Task Anatomy (8 sections — STORY-SWI-1)

```yaml
task: extractEvidenceFromIngestions
atomic_layer: Atom
responsavel_type: Worker
session: null
phase: P00.5
Inputs:
  - { name: ingestion-bundle.yaml, type: yaml, source: ingest-multimodal-sources (P00.5) }
Outputs:
  - { name: claims-draft.yaml, description: "per-source claims with chunk_id and confidence scores", lifecycle: [draft] }
Pre_conditions:
  - ingestion-bundle.yaml exists
Post_conditions:
  - claims-draft.yaml emitted
  - successful sources produce claims from IngestionResult.evidence_index when present
  - extraction_gap sources produce zero fabricated claims
Acceptance_criteria:
  - Claims preserve source_index and chunk_id references into ingestion-bundle.yaml
  - Sources with extraction_gap markers propagate as zero-claim sources
  - claims-draft.yaml is consumable by validate-evidence-ledger in P05
Performance:
  duration_target: "< 500ms total"
  deterministic: true
Error_handling:
  strategy: "empty claims array for errored sources; log diagnostics"
  on_source_error: emit_empty_claims_array_with_diagnostics
  no_fabrication: true
handoff_token: extract-evidence-from-ingestions
```

## Implementation Contract

This task reads the existing `evidence_index[]` emitted by the ingestion pipeline. It does not perform
freshness scoring, contradiction detection, APA formatting, or final evidence validation. Those checks
belong to STORY-SWI-2 and the `validate-evidence-ledger` task.
