# Pipeline Execution Log — Emission Protocol

The skill SHOULD emit a pipeline execution log per run so the squad's M10 observability is satisfied even when execution happens through the skill (Codex/external) rather than the squad runtime.

## When to Emit

Emission is required when the skill operates in **Full deck mode** or any mode where the run is non-trivial enough to require provenance. Emission is optional for **Quick deck** mode but recommended.

## Where to Write

```
outputs/slides-creator/{run_id}/pipeline-execution-log.yaml
```

`run_id` SHOULD be a deterministic slug if available (e.g., `{date}-{briefing-slug}`) or a UUID4. **Never** invent a fake run_id retroactively.

## How to Emit

Two paths — pick whichever is available:

### Path 1 — When monorepo is available (preferred)

Use the squad's emit script:

```bash
node squads/slides-creator/scripts/emit-pipeline-log.js \
  --run-id <run_id> \
  --event <event> \
  --payload '<json>'
```

Valid events: `workflow_started | phase_transition | gate_verdict | meta_axiom_breach | deviation_logged | killer_item_fired | workflow_completion`.

### Path 2 — Standalone (Codex / external consumers)

When `squads/slides-creator/scripts/emit-pipeline-log.js` is unavailable, emit a minimal log directly:

```yaml
---
schema_version: "1.0"
run_id: "<run_id>"
schema_ref: "squads/slides-creator/data/pipeline-execution-log.yaml"
events:
  - event_id: "EV-<8char>"
    event: workflow_started
    timestamp: "<ISO8601>"
    payload:
      workflow_mode: <quick|full|brand-fidelity|...>
      briefing_slug: "<slug>"

  - event_id: "EV-<8char>"
    event: phase_transition
    timestamp: "<ISO8601>"
    payload:
      from_phase: P00_briefing
      to_phase: P01_narrative
      verdict: PASS

  - event_id: "EV-<8char>"
    event: workflow_completion
    timestamp: "<ISO8601>"
    payload:
      total_slides: <N>
      duration_seconds: <N>
      qa_verdict: <PASS|CONCERNS|FAIL>
      meta_axiomas_overall: <0-100>
      cost_attribution:
        model_calls: []
        total_cost_usd: <float>
```

## Minimum Event Set

For every run, at minimum emit:

1. `workflow_started` — at start
2. `gate_verdict` — for each gate transition (key-slide gate, narrative gate, design gate, final QA gate)
3. `workflow_completion` — at end with summary

Extended events (`phase_transition`, `meta_axiom_breach`, `deviation_logged`, `killer_item_fired`) are optional but improve traceability.

## Why

- **M10 (Mandamento 10):** every workflow run MUST append at least 1 execution record (per squad `data/pipeline-execution-log.yaml#emission_protocol.ci_check`).
- **Cost attribution:** finops dashboards filter by `X-Sinkra-Squad: slides-creator` and aggregate per `run_id`.
- **Audit trail:** post-hoc reviews of why a deck failed/passed need the gate history.

## Declarative Emission Matrix

Read **`templates/runtime/phase-emit-matrix.yaml`** (skill mirror of the squad workflow `phase_emit_matrix`) to know exactly which events to emit per skill step + per gate. The matrix lists 12 phase entries (P00_briefing → P11_package) with `on_enter` + `on_exit` events, plus 4 gates (key_slide_gate, narrative_critique_gate, design_critique_gate, qa_final_gate) with `on_verdict` templates, plus 3 conditional events (meta_axiom_breach, deviation_logged, killer_item_fired).

The matrix is the SOT for "what to emit when" — do not invent events outside its `valid_events` enum.

## Validation (CI Gate)

After emitting the log, verify it with one of:

```bash
# Python validator (always available — skill-side, stdlib only)
python3 .claude/skills/slide-creator/scripts/validate_pipeline_emission.py --run-id <run_id>

# Node validator (squad-side, when monorepo present — equivalent behavior)
node squads/slides-creator/scripts/validate-pipeline-emission.js --run-id <run_id>
```

Both validators apply the same rule: minimum 3 records quick / 8 records full, REQUIRED events `workflow_started` + `workflow_completion`, only events in the canonical enum.

Run with `--mode full` (Python) or default (Node) for full-deck threshold. Exit 0 = pass, exit 1 = fail, exit 2 = IO/parse error.

## Reference

- Schema SoT: `squads/slides-creator/data/pipeline-execution-log.yaml`
- Emit script (Node, when available): `squads/slides-creator/scripts/emit-pipeline-log.js`
- Meta-axiom validator: `squads/slides-creator/scripts/validate-meta-axioms.js`
- Squad declarative matrix: `squads/slides-creator/workflows/generate-presentation.yaml#phase_emit_matrix`
- Skill declarative matrix (this side): `.claude/skills/slide-creator/templates/runtime/phase-emit-matrix.yaml`
- Skill validator (Python): `.claude/skills/slide-creator/scripts/validate_pipeline_emission.py`
- Squad validator (Node): `squads/slides-creator/scripts/validate-pipeline-emission.js`
