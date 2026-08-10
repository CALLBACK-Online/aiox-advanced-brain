# Validate Evidence Ledger

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Operational -->

## SINKRA Task Anatomy (8 sections — STORY-SWI-2)

```yaml
task: validateEvidenceLedger
atomic_layer: Atom
responsavel_type: Worker
session: SESSION-QA
phase: P05
Inputs:
  - { name: deck-spec.yaml, type: yaml, source: emit-deck-spec (P04) }
  - { name: claims-draft.yaml, type: yaml, source: extract-evidence-from-ingestions (P00.5) }
  - { name: ingestion-bundle.yaml, type: yaml, source: ingest-multimodal-sources (P00.5) }
Outputs:
  - { name: evidence-ledger.final.yaml, schema_ref: apps/squad-engine/openapi/slides.yaml#EvidenceLedger, lifecycle: [draft, validated] }
  - { name: evidence-validation-report.json, description: "verdict PASS|CONCERNS|FAIL + stale/no-match/contradicting lists" }
  - { name: outputs/slides-creator/_monitoring/evidence-freshness-runs.jsonl, description: "append-only freshness monitoring (AC10) — one line per run; feeds ADR-054-amendment-1 per-domain threshold calibration after 20 runs" }
Pre_conditions:
  - deck-spec.yaml exists
  - ingestion-bundle.yaml exists
  - claims-draft.yaml exists OR deck-spec.yaml has extractable claims
Post_conditions:
  - evidence-ledger.final.yaml emitted with verdict PASS, CONCERNS, or FAIL
  - evidence-validation-report.json summarizes coverage and blockers
  - KI-11 fires when ledger verdict FAIL OR contradicting_evidence_count > 0
  - one JSONL line appended to outputs/slides-creator/_monitoring/evidence-freshness-runs.jsonl (AC10)
Acceptance_criteria:
  - buildEvidenceLedger() validates claim-to-evidence matches
  - freshness scoring uses qa-rubric.yaml global threshold policy (global_default_years: 5)
  - ingestion gaps downgrade to CONCERNS when remaining claim coverage is sufficient, not fabricated PASS
  - evidence-ledger.final.yaml schema validates against apps/squad-engine/openapi/slides.yaml#EvidenceLedger (OpenAPI SoT per ADR-054 §2.5)
  - KI-11 verifiably FIRES (verdict FAIL) on contradicting_evidence_count > 0 AND on stale_evidence_ratio > 0.20
  - monitoring JSONL appended: {run_id, timestamp, total_claims, stale_count, fresh_count, freshness_threshold_years_used, deck_domain}
Performance:
  duration_target: "< 800ms p99"
  deterministic: true
  monitors_jsonl: outputs/slides-creator/_monitoring/evidence-freshness-runs.jsonl
Error_handling:
  strategy: "If infrastructure unavailable, emit CONCERNS with degraded_mode: true; never fabricate evidence"
  on_freshness_threshold_breach: downgrade_to_CONCERNS
  on_contradicting_evidence: fire_KI-11_FAIL
  no_fabrication: true
handoff_token: validate-evidence-ledger
```

## Implementation Contract

This task wires `packages/slides-core/src/evidence/validate.ts#buildEvidenceLedger()`.
It complements, but does not replace, `validate-fontes-apa`:

- `validate-fontes-apa` checks citation shape.
- `validate-evidence-ledger` checks semantic claim-evidence match, freshness, and contradiction blockers.

KI-11 is a P1 gate. Citation shape is not enough for factual fidelity.
