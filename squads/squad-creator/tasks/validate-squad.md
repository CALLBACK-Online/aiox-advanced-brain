# Task: Validate Squad (Composed)

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `validate-squad` |
| **Version** | `5.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Composed` |

## Metadata

```yaml
id: validate-squad
name: "Validate Squad"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Composed task that orchestrates 4 validation sub-tasks in sequence."
accountability:
  human: squad-operator
  scope: review_only
domain: Tactical

```


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Molecule
Input: request::validate_squad
Output: artifact::validate_squad
pre_condition: squad_name fornecido AND squad directory existe com config.yaml válido
post_condition: validation report com PASS/FAIL verdict, scores por dimensão e veto gates avaliados
performance: Composed (4 sub-tasks), preflight deterministic + optional deep review, < 10 min total
Completion Criteria: preflight PASS AND classification completed AND verdict final emitido com score consolidado
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Validate a squad against AIOX principles using deterministic gates plus optional deep semantic review. This composed task orchestrates the full validation pipeline by invoking atomic sub-tasks in sequence.

**Core Philosophy:** Facts first. Judgment second. Score last. Deterministic failures are not negotiable.

## PRO DETECTION

> At execution time, check if `squads/squad-creator-pro/workflows/validate-squad.yaml` exists.
> If YES and pro mode is active -- delegate to pro workflow override.
> If NO -- continue with this base version.

## Execution Sequence

```
INPUT (squad_name)
    |
[1] validate-squad-preflight
    -> Run worker scripts, collect deterministic signals
    -> Check blocking conditions (structure, security, refs)
    -> IF BLOCK -> STOP, report issues
    |
[2] validate-squad-classify
    -> Detect squad type (Expert/Pipeline/Hybrid/Operational)
    -> Load type-specific requirements
    -> Validate governance compliance (artifact_contracts, bu_mapping, modes)
    -> Check agnosticism, calculate compliance score
    |
[3] validate-squad-deep-review (OPTIONAL)
    -> CLI-assisted semantic review with canonical input pack
    -> Score prompt quality, coherence, checklists, documentation
    -> Skipped in quick mode
    |
[4] validate-squad-verdict
    -> Reconcile deterministic facts with reviewer verdicts
    -> Apply blocker caps and penalties, produce final score
    -> Evaluate veto gates (universal + type-specific)
    -> Emit backward-compatible JSON + human-readable report
    |
OUTPUT: Validation Report + Final Score
```

## Sub-Task References

| Sequence | Task ID | File | Type |
|----------|---------|------|------|
| 1 | `validate-squad-preflight` | `tasks/validate-squad-preflight.md` | Worker |
| 2 | `validate-squad-classify` | `tasks/validate-squad-classify.md` | Agent |
| 3 | `validate-squad-deep-review` | `tasks/validate-squad-deep-review.md` | Agent |
| 4 | `validate-squad-verdict` | `tasks/validate-squad-verdict.md` | Worker |

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Name of squad to validate |
| `squad_path` | string | No | Override default path |
| `type_override` | string | No | Force squad type |
| `mode` | string | No | `deep` (default) or `quick` |

## Outputs

| Output | Location |
|--------|----------|
| Validation Report | `{squad_path}/docs/validation-report-{date}.md` |
| JSON Report | `{squad_path}/docs/validation-report-{date}.json` |
| Console Summary | stdout |


## Veto Conditions

- Squad directory does not exist or has no `config.yaml` -> BLOCK
- `config.yaml` fails YAML parsing -> BLOCK
- Validation script `scripts/validate-squad.sh` is inaccessible -> BLOCK

## Related Documents

| Reference | File |
|-----------|------|
| Checklist | `checklists/squad-checklist.md` |
| Type Definitions | `data/squad-type-definitions.yaml` |
| Quality Framework | `data/quality-dimensions-framework.md` |
| Executor Decision Tree | `data/executor-decision-tree.md` |
| Composition Rules | `governance/composition-rules.yaml` |
