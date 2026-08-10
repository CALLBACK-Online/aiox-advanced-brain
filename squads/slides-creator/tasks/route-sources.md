# Route Sources

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Tactical -->

## SINKRA Task Anatomy (8 sections — STORY-SWI-3)

```yaml
task: routeSources
atomic_layer: Atom
responsavel_type: Worker
session: null
phase: P00
Inputs:
  - { name: briefing.normalized.json, type: json, source: normalize-briefing }
Outputs:
  - { name: routing-decisions.yaml, schema_ref: apps/squad-engine/openapi/slides.yaml#/components/schemas/RoutingDecision, lifecycle: [draft, validated] }
Pre_conditions:
  - briefing.normalized.json exists
  - briefing.normalized.json.sources[] is present OR source_materials are empty
Post_conditions:
  - routing-decisions.yaml emitted with one route per source
  - each route has source_index, adapter_id, confidence, fallback, rationale
  - unmatched sources emit adapter_id: null with extraction_gap reason
Acceptance_criteria:
  - YouTube URLs route to @sinkra/etl#extractYouTube when confidence >= 0.6
  - PDF/DOCX/XLSX/CSV/MD/TXT/PPTX local paths route to @sinkra/file-service when confidence >= 0.6
  - arXiv sources route to research-adapters#arxiv when confidence >= 0.6
  - mixed source arrays are routed independently by source_index
  - unknown sources emit null + extraction_gap(no_rule_matched_min_confidence_0.6), never a hardcoded fallback
Performance:
  duration_target: "< 200ms p99 for up to 10 sources"
  deterministic: true
  parallelizable_sources: true
Error_handling:
  strategy: "emit extraction_gap(reason) per source; never fabricate adapter_id"
  on_unknown_source: emit_adapter_id_null_with_extraction_gap
  no_fabrication: true
  min_confidence_threshold: 0.6
handoff_token: route-sources
```

## Implementation Contract

`route-sources` wires the existing deterministic router at `packages/slides-core/src/sources/router.ts#routeSource`.
The task does not implement new routing logic. It converts normalized briefing sources into route entries:

```yaml
routes:
  - source_index: 0
    source: "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    adapter_id: "@sinkra/etl#extractYouTube"
    confidence: 1
    fallback: null
    rationale: "top intent=video confidence=1 signals=youtube_url"
```

When no candidate reaches `min_confidence: 0.6`, the route is explicit gap state:

```yaml
routes:
  - source_index: 0
    source: "internal company database"
    adapter_id: null
    confidence: null
    fallback: null
    extraction_gap: true
    reason: "no_rule_matched_min_confidence_0.6"
```

No universal fallback adapter is allowed unless a future `source_fallback_policy` explicitly permits it in `squads/slides-creator/data/asset-resolution.yaml`.
