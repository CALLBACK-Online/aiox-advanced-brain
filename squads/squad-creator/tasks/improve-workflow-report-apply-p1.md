# Task: Improve Workflow Report — Apply P1

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-apply-p1` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: improve-workflow-report-apply-p1
name: "Improve Workflow Report — Apply P1"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Aplica remediações P1 rastreáveis ao report e registra diff log de cada mudança crítica."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_apply_p1
Output: artifact::improve_workflow_report_apply_p1
pre_condition: backup verificado AND remediações P1 extraídas do report com gap_refs
post_condition: P1 remediações aplicadas com diff log (antes/depois + gap_ref) para cada mudança
performance: Agent, < 5 min, fail-loud se fix extrapola contrato do report, mark unresolved se inaplicável
Completion Criteria: todas P1 aplicadas ou marcadas unresolved AND cada mudança tem before/after + gap_ref
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::improve_workflow_report_apply_p1## Purpose

Executar as correções obrigatórias sem inventar melhoria fora do contrato do gap
report.


## Veto Conditions

- Target identification from `improve-workflow-report-target` is missing -> BLOCK
- Backup from `improve-workflow-report-backup` does not exist (cannot apply without safety net) -> BLOCK

## Acceptance Criteria

- [ ] Todas as remediações P1 foram aplicadas ou marcadas como unresolved
- [ ] Cada mudança registra antes/depois e `gap_ref`
- [ ] Nenhuma fix extrapola o conteúdo do report

## Related Documents

- `improve-workflow-report-backup.md`
- `improve-workflow-report-apply-secondary.md`

---

_Task Version: 1.0.0_
