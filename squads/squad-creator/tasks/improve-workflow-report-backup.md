# Task: Improve Workflow Report — Backup

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-backup` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: improve-workflow-report-backup
name: "Improve Workflow Report — Backup"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Cria e verifica backup antes de qualquer edição, exceto quando o fluxo está em dry-run."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_backup
Output: artifact::improve_workflow_report_backup
pre_condition: workflow target validado AND dry_run flag conhecido
post_condition: backup criado e verificado (se dry_run=false) OR skip explícito com no-mutation policy (se dry_run=true)
performance: deterministic Worker, < 30s, fail-loud se backup write fails
Completion Criteria: backup criado e path registrado (live) OR dry_run policy explícita (dry-run)
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::improve_workflow_report_backup## Purpose

Impor a proteção `backup-first` do processo de melhoria, impedindo edição sem
rollback verificável.


## Veto Conditions

- Target workflow file does not exist at the expected path -> BLOCK
- Backup write to `backups/` directory fails due to permission error -> BLOCK

## Acceptance Criteria

- [ ] Backup criado quando `dry_run=false`
- [ ] Backup verificado e caminho registrado
- [ ] Em `dry_run`, a política de não mutação fica explícita

## Related Documents

- `improve-workflow-report-target.md`
- `improve-workflow-report-apply-p1.md`

---

_Task Version: 1.0.0_
