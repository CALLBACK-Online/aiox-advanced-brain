# Task: Improve Workflow Report — Ingest

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `improve-workflow-report-ingest` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: improve-workflow-report-ingest
name: "Improve Workflow Report — Ingest"
category: improvement
agent: squad-chief
elicit: false
autonomous: true
description: "Lê o gap report, valida o contrato mínimo e extrai workflow, versão, score e remediações."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::improve_workflow_report_ingest
Output: artifact::improve_workflow_report_ingest
pre_condition: gap report file path fornecido AND arquivo legível
post_condition: gap report parseado com workflow_analyzed, workflow_version, score e remediations extraídos
performance: deterministic Worker, < 30s, fail-loud se YAML inválido ou contrato mínimo ausente
Completion Criteria: YAML parseado AND workflow_analyzed extraído AND >= 1 gap ou remediation item presente
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::improve_workflow_report_ingest## Purpose

Transformar o gap report em um contrato de entrada confiável para as fases
seguintes, sem inferir nada além do que o relatório declara.


## Veto Conditions

- Report file path does not exist or is not readable -> BLOCK
- Report does not contain structured findings (no recommendations section) -> BLOCK

## Acceptance Criteria

- [ ] Gap report parseado como YAML válido
- [ ] `workflow_analyzed` e `workflow_version` extraídos
- [ ] Pelo menos um gap ou remediation item presente

## Related Documents

- `improve-workflow-from-report.md`
- `improve-workflow-report-target.md`

---

_Task Version: 1.0.0_
