# Emit Native PPTX

<!-- AIOX accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- AIOX Domain: Tactical -->

## AIOX Task Anatomy (8 sections — STORY-SWI-5)

```yaml
task: emitNativePptx
atomic_layer: Atom
responsavel_type: Worker
session: null
phase: P06
conditional_on: "feature_flags.enable_native_pptx_emission == true"
Inputs:
  - { name: deck-spec.yaml, type: yaml, source: emit-deck-spec (P06 final state) }
  - { name: active-palette.yaml, type: yaml, source: resolve-active-palette (P03), optional: true }
  - { name: deck.ir.json, type: json, source: slides-core Native IR compiler, derived_from: deck-spec.yaml }
Outputs:
  - { name: "outputs/slides-creator/{run_id}/exports/{run_id}.pptx", type: pptx, lifecycle: [draft, approved] }
  - { name: "outputs/slides-creator/{run_id}/exports/editability-report.json", schema_ref: packages/slides-renderer/src/validators/editability-report.schema.json, lifecycle: [draft, validated] }
Pre_conditions:
  - deck-spec.yaml exists and has passed P05 release gates
  - feature_flags.enable_native_pptx_emission == true
  - Native IR compiler can derive deck.ir.json from deck-spec.yaml without schema violation
Post_conditions:
  - Native editable .pptx exists in exports directory
  - editability-report.json verdict is PASS before the native PPTX artifact can be released
  - failed native output is blocked as NATIVE_PPTX_BLOCKED without affecting TSX/app handoff path when the flag is false
Acceptance_criteria:
  - packages/slides-renderer/src/pptx/render.ts emits .pptx from NativeSlideIR
  - packages/slides-renderer/src/validators/editability.ts writes editability-report.json
  - missing image/path assets emit gap_at_slide_N markers and never fabricate placeholder images
  - if verdict != PASS and feature flag is true, P06 release is halted with NATIVE_PPTX_BLOCKED
Performance:
  duration_target: "< 10s p99 per deck in PoC fixture set"
  cacheable: false
  deterministic: true  # same Native IR → same .pptx
Error_handling:
  strategy: "fail-loud for schema violations; emit structured gaps for missing assets; never silently ship partial .pptx"
  on_schema_violation: halt_and_surface
  on_asset_missing: emit_gap_at_slide_N_marker
handoff_token: emit-native-pptx
```

## Execution Protocol

1. Load the final `deck-spec.yaml` and optional `active-palette.yaml`.
2. Derive Native Slide IR through the deterministic slides-core compiler.
3. Validate Native IR against `packages/slides-renderer/src/ir/native-slide-ir.schema.json`.
4. Invoke `packages/slides-renderer/src/pptx/render.ts`.
5. Invoke `packages/slides-renderer/src/validators/editability.ts`.
6. Write `.pptx` and `editability-report.json` under `outputs/slides-creator/{run_id}/exports/`.
7. If `editability-report.json.verdict != PASS`, mark the native PPTX branch as `NATIVE_PPTX_BLOCKED`.

## K6 Asset Rule

When a slide references a missing visual asset, emit an explicit gap marker instead of a fallback:

```json
{
  "gap_at_slide_0": {
    "reason": "missing_asset",
    "slot": "visual_elements[0].path",
    "extraction_gap": true
  }
}
```

Do not generate stock placeholders, brand-pattern backgrounds, or hardcoded paths to make the export pass.

## K7 Boundary

This task is downstream of narrative, design direction, and QA. It does not read, rewrite, or validate
`design-direction.yaml`; KI-10 remains owned by P03_DIRECTION and P05. If `deck-spec.yaml` is invalid,
this task fails with `DECK_SPEC_SCHEMA_VIOLATION` instead of repairing design intent.
