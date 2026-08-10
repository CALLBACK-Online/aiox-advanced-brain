# Task: Improve Workflow Report — Apply Secondary

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-apply-secondary` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: improve-workflow-report-apply-secondary
name: "Improve Workflow Report — Apply Secondary"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Aplica P2 quando permitido pelo filtro e converte P3 em tech debt explícita para o diff report."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_apply_secondary
Output: artifact::improve_workflow_report_apply_secondary
pre_condition: P1 apply completed AND P2/P3 remediações identificadas com priority_filter
post_condition: P2 aplicados respeitando filtro, P3 documentados como tech debt explícita no diff report
performance: < 15 min (Hybrid — P2 apply + P3 documentation), escalate se P2 complexo demais
Completion Criteria: P2 respeitam priority_filter AND P3 documentados como tech debt AND nenhuma fix não rastreável
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::improve_workflow_report_apply_secondary## Purpose

Separar o que deve ser aplicado agora do que precisa virar backlog técnico,
mantendo o ciclo conservador de melhoria.


## Veto Conditions

- P1 improvements from `improve-workflow-report-apply-p1` did not complete -> BLOCK
- Secondary improvement would revert a P1 change already applied -> BLOCK

## Acceptance Criteria

- [ ] P2 respeita `priority_filter`
- [ ] P2 complexos demais viram nota explícita
- [ ] P3 documentados como tech debt

## Related Documents

- `improve-workflow-report-apply-p1.md`
- `improve-workflow-report-validate-report.md`

---

_Task Version: 1.0.0_
