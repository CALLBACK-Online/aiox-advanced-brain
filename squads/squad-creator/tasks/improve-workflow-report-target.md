# Task: Improve Workflow Report — Target

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-target` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: improve-workflow-report-target
name: "Improve Workflow Report — Target"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Valida o workflow alvo citado no report, checa existência, parse YAML e reconcilia id/versão."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_target
Output: artifact::improve_workflow_report_target
pre_condition: ingest completed com workflow_analyzed path extraído do report
post_condition: workflow alvo validado (existe, parseia YAML), id reconciliado com report, version divergence registrada
performance: deterministic Worker, < 30s, fail-loud se workflow alvo não existe ou YAML inválido
Completion Criteria: workflow target exists AND YAML parses AND workflow.id matches report AND version checked
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::improve_workflow_report_target## Purpose

Garantir que a remediação está apontando para um workflow real e compatível com o
report antes de qualquer mutação.


## Veto Conditions

- Ingested report from `improve-workflow-report-ingest` is missing -> BLOCK
- No actionable improvements identified in the report (empty improvement list) -> BLOCK

## Acceptance Criteria

- [ ] Workflow alvo existe e parseia em YAML
- [ ] `workflow.id` reconciliado com o report
- [ ] Divergência de versão registrada quando houver

## Related Documents

- `improve-workflow-report-ingest.md`
- `improve-workflow-report-backup.md`

---

_Task Version: 1.0.0_
