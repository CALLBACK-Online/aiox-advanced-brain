# Task: QA Check Completeness

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `qa-check-completeness` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: qa-check-completeness
name: QA Check Completeness
category: qa-validation
agent: squad-chief
elicit: false
autonomous: true
description: >
  Check completeness of a created component against Definition of Done
  criteria. Runs quality scoring with weighted criteria per component type
  and produces a numeric score (0-10).
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::qa_check_completeness
Output: artifact::qa_check_completeness
pre_condition: qa-check-structure e qa-check-schema passaram, componente e Definition of Done criteria disponíveis
post_condition: completeness_score (0-10) calculado com weighted criteria, gaps listados com prioridade
performance: < 10 min (Hybrid — scoring + human review), escalate se score < quality_threshold
Completion Criteria: completeness_score >= 8.5 AND zero P0 gaps AND Definition of Done checklist 100% verificado
error_handling: escalate to squad-chief on failure, persist error contextcheckpoints:
  - id: PV_PA_001
    phase: completeness_validation
    description: "Systemic Coherence Scan — componente está completo e coerente com o que foi planejado?"
    threshold: 0.7
    on_fail: REVIEW

## Purpose

Evaluate the qualitative completeness of a component beyond structural and schema correctness. This task answers: "Is this component good enough to ship?" by scoring it against weighted quality criteria specific to each component type.

## Prerequisites

- [ ] qa-check-structure has passed
- [ ] qa-check-schema has passed
- [ ] qa-check-references has passed
- [ ] `data/quality-dimensions-framework.md` accessible

## Inputs

```yaml
inputs:
  - name: created_component
    type: string
    required: true
    description: "Path to created component"

  - name: component_type
    type: enum
    required: true
    values: ["squad", "agent", "task", "workflow", "template"]
    description: "Type of component created"

  - name: references_result
    type: object
    required: true
    source: qa-check-references
    description: "Result from references check (must be PASS)"
```

## Workflow

### Step 1: Select Quality Criteria

Load scoring criteria based on `component_type`:

**For squads:**

Run `validate-squad {squad_name}` and extract:
- Tier 1 result (structural)
- Tier 2 result (schema)
- Tier 3 score (quality)
- Tier 4 score (depth)
- Final score
- Veto triggered (boolean)

**For agents:**

| Criterion | Weight | Checks |
|-----------|--------|--------|
| Persona completeness | 0.20 | role, style, identity, focus defined |
| Commands functionality | 0.20 | *help exists, commands map to capabilities |
| Voice consistency | 0.15 | voice_dna present (if Expert), vocabulary used |
| Examples quality | 0.15 | output_examples present, realistic |
| Dependencies valid | 0.15 | all references exist (from qa-check-references) |
| Documentation | 0.15 | whenToUse clear, description helpful |

**For tasks:**

| Criterion | Weight | Checks |
|-----------|--------|--------|
| Task Anatomy complete | 0.25 | 8 required fields present |
| Prompt quality | 0.25 | specific, includes examples, anti-patterns |
| Validation defined | 0.20 | success criteria, failure handling |
| Integration | 0.15 | references valid, outputs defined |
| Documentation | 0.15 | purpose clear, usage examples |

**For workflows:**

| Criterion | Weight | Checks |
|-----------|--------|--------|
| Phase completeness | 0.30 | all phases have tasks, inputs, outputs |
| Sequence validity | 0.25 | no collisions, output-input chain valid |
| Error handling | 0.20 | failure paths defined |
| Documentation | 0.25 | purpose, usage, examples |

### Step 2: Score Each Criterion

For each criterion:
1. Run the specified checks
2. Calculate a score (0.0 to 1.0) based on how many checks pass
3. Multiply by weight to get weighted score
4. Sum all weighted scores and scale to 0-10

### Step 3: Apply Thresholds

| Score | Verdict | Meaning |
|-------|---------|---------|
| >= 7.0 | PASS | Component is ready for delivery |
| >= 5.0 and < 7.0 | CONDITIONAL | Component has issues but may proceed |
| < 5.0 | FAIL | Component requires fixes before delivery |

### Step 4: Compile Results

```yaml
completeness_result:
  final_score: X.X
  verdict: "PASS | CONDITIONAL | FAIL"
  breakdown:
    - criterion: "Persona completeness"
      weight: 0.20
      score: 0.85
      weighted: 1.70
      details: "Missing: focus field"
    - criterion: "Commands functionality"
      weight: 0.20
      score: 1.00
      weighted: 2.00
      details: "All checks passed"
  veto_triggered: false
```

## Output

```yaml
output:
  name: completeness_result
  type: object
  description: "Quality scoring results with per-criterion breakdown"
  passed_to: qa-generate-report
```

## Acceptance Criteria

- [ ] Correct criteria loaded per component type
- [ ] Each criterion scored independently with weighted calculation
- [ ] Final score is on 0-10 scale
- [ ] Threshold verdicts applied correctly (PASS/CONDITIONAL/FAIL)
- [ ] Breakdown includes per-criterion detail
- [ ] For squads, validate-squad is invoked and results extracted

### Doom Loop Awareness Check (C1 — EPIC-109 Wave 1)

As an advisory (non-blocking) dimension in the completeness scoring:

```yaml
doom_loop_awareness:
  dimension_id: doom_loop_awareness
  weight: 0.05   # advisory weight, does not block
  penalty: -0.5  # applied to final score if doom loop not addressed
  check: >
    Verify that the squad design acknowledges repeated-output scenarios.
    Specifically: does any workflow or error_handling section reference
    doom loop detection or repeat-output guards?
  pass_condition: "workflow error_handling.recovery references doom_loop_check OR
                   config.yaml declares doom_loop_detection: true"
  fail_action: "advisory — deduct -0.5 from score, log warning, do NOT block"
  note: >
    Doom loop detection is handled by scripts/lib/doom-loop-detector.js (C1).
    This check promotes awareness in squad design, it does NOT run the script.
```

**Integration:** When `doom_loop_check` field is present in the validation state
(injected by `wf-qa-after-creation.yaml`), extract its `detected` and `action`
fields and include them in the advisory dimension result.

## Veto Conditions

| Condition | Action |
|-----------|--------|
| validate-squad reports veto_triggered | FAIL regardless of score |
| Score < 5.0 | FAIL -- component not ready |
| Any criterion scores 0.0 | FAIL -- critical gap detected |

## Related Documents

| Document | Purpose |
|----------|---------|
| `qa-after-creation.md` | Parent orchestrator task |
| `validate-squad.md` | Called for squad-type components |
| `data/quality-dimensions-framework.md` | Quality criteria definitions |
| `qa-generate-report.md` | Consumes this task's output |
