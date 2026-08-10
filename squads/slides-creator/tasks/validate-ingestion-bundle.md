# Validate Ingestion Bundle

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Operational -->

## SINKRA Task Anatomy

### 1. task
```yaml
task: validateIngestionBundle
```

### 2. atomic_layer
```yaml
atomic_layer: Atom
```

### 3. responsavel_type
```yaml
responsavel_type: Worker
```

### 4. Inputs
```yaml
Inputs:
  - name: ingestion_bundle
    type: YAML
    source: "{output_dir}/ingestion-bundle.yaml"
  - name: routing_decisions
    type: YAML
    source: "{output_dir}/routing-decisions.yaml"
    optional: true
```

### 5. Outputs
```yaml
Outputs:
  - name: ingestion_bundle_report
    type: JSON
    destination: "{output_dir}/ingestion-bundle-report.json"
    schema:
      verdict: "PASS | FAIL"
      total_sources: number
      ok_sources: number
      gap_sources: number
      gap_ratio: number
      blocking_reasons: "array<string>"
```

### 6. Pre-conditions
```yaml
Pre_conditions:
  - "ingestion-bundle.yaml exists"
```

### 7. Post-conditions + Acceptance
```yaml
Post_conditions:
  - "ingestion-bundle-report.json exists"
  - "verdict PASS only when gap_ratio < 0.5"

Acceptance_criteria:
  - "Every source has status ok or extraction_gap"
  - "Every extraction_gap has explicit reason"
  - "No universal fallback strings are accepted as source text"
  - "P00.5 halts when gap_ratio >= 0.5"
```

### 8. Performance + Error Handling
```yaml
Performance:
  duration: "<1s for 25 sources"
  deterministic: true

Error_handling:
  strategy: fail_fast
  on_missing_bundle: "verdict = FAIL; blocking_reasons += missing_ingestion_bundle"
  on_gap_ratio_block: "halt_and_surface"
```

## K6 Boundary

This validator preserves extraction honesty. It must never convert `extraction_gap` entries into
generic text, placeholder claims, or fabricated source summaries. Gaps remain explicit and operator-visible.
