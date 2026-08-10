# Task: Improve Workflow Report — Validate and Report

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-validate-report` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: improve-workflow-report-validate-report
name: "Improve Workflow Report — Validate and Report"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Executa validação pós-edição, rollback quando necessário, aplica version bump e gera o relatório final de melhoria."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_validate_report
Output: artifact::improve_workflow_report_validate_report
pre_condition: P1 e P2/P3 phases completed AND workflow editado disponível para validação
post_condition: workflow final validado (YAML parseable), version bump aplicado e diff report final gerado
performance: deterministic Worker, < 30s, rollback automático se YAML parse fails
Completion Criteria: workflow parseia YAML AND version bump aplicado AND diff report com unresolved e tech debt emitido
error_handling: rollback on failure, persist error evidence, notify squad-chief

## Inputs

- request::improve_workflow_report_validate_report## Purpose

Fechar o ciclo com validação estrutural, version bump apropriado e diff report
completo, preservando rollback automático em falhas.


## Veto Conditions

- Applied improvements from upstream sub-tasks are missing -> BLOCK
- Modified workflow fails YAML syntax validation -> BLOCK
- Modified workflow `sequence[].id` fields have duplicates or gaps -> BLOCK

## Acceptance Criteria

- [ ] Workflow final parseia em YAML e permanece alcançável
- [ ] Version bump aplicado quando houver mudança real
- [ ] Diff report final gerado com unresolved e tech debt

## Related Documents

- `improve-workflow-from-report.md`
- `workflow-tmpl.yaml`

---

_Task Version: 1.0.0_
