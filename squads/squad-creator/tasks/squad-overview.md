# Task: Squad Overview (Composed)

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `squad-overview` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Composed` |

## Metadata

```yaml
id: squad-overview
name: "Squad Overview"
category: documentation
agent: squad-chief
elicit: false
autonomous: true
description: "Task composta que orquestra 6 subtasks atômicas para gerar SQUAD-OVERVIEW.md com análise, síntese e checklist de saída."
owner_workflow: "workflows/wf-squad-overview.yaml"
accountability:
  human: squad-operator
  scope: review_only
domain: Tactical

```


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Molecule
Input: request::squad_overview
Output: artifact::squad_overview
pre_condition: squad_name fornecido AND squad directory existe com config.yaml e agents/
post_condition: SQUAD-OVERVIEW.md gerado consolidando identidade, arquitetura, comandos e integrações do squad
performance: Composed (6 subtasks), < 10 min total, análise + síntese + checklist de saída
Completion Criteria: SQUAD-OVERVIEW.md gerado AND todas seções preenchidas AND checklist de saída PASS
error_handling: fail-loud, persist error context, escalate to squad-chief

## Inputs

- request::squad_overview## Purpose

Gerar um `SQUAD-OVERVIEW.md` confiável e reutilizável, consolidando identidade,
arquitetura, comandos, estrutura, integrações e sinais de DNA do squad.

## Execution Sequence

```text
INPUT (squad_name + squad_path? + include_minds + format)
    |
[1] squad-overview-metadata
    -> Resolve path, lê config/README e mede inventário bruto
    |
[2] squad-overview-agents
    -> Analisa agents, tiers, handoffs e comandos
    |
[3] squad-overview-minds
    -> Coleta DNA e perfis apenas se houver evidência real
    |
[4] squad-overview-structure
    -> Monta árvore, workflows, integrações, compliance e quality gates
    |
[5] squad-overview-generate
    -> Compõe o markdown final sem placeholders
    |
[6] squad-overview-write
    -> Grava SQUAD-OVERVIEW.md e aplica checklist de saída
    |
OUTPUT: overview_report
```

## Sub-Task Reference

| # | Task ID | Responsibility | Executor |
|---|---------|----------------|----------|
| 1 | `squad-overview-metadata` | Identidade e inventário base | Worker |
| 2 | `squad-overview-agents` | Arquitetura humana e comandos | Agent |
| 3 | `squad-overview-minds` | DNA e perfis condicionais | Agent |
| 4 | `squad-overview-structure` | Estrutura, workflows e compliance | Agent |
| 5 | `squad-overview-generate` | Síntese do markdown final | Agent |
| 6 | `squad-overview-write` | Persistência e scoring final | Worker |

## Commands

```yaml
commands:
  standard: "*squad-overview {name}"
  compact: "*squad-overview {name} --format=compact"
  no_minds: "*squad-overview {name} --include-minds=false"
```

## Quality Gate

```yaml
quality_gate:
  id: "QG-SQOV-001"
  name: "Squad Overview Quality Gate"
  checklist: "checklists/squad-overview-checklist.md"
  pass_threshold: 80
  veto_conditions:
    - "File doesn't exist"
    - "No commands section"
    - "Contains placeholder text"
```


## Veto Conditions

- Target squad directory does not exist or `config.yaml` is absent -> BLOCK
- A blocking sub-task in the execution sequence emits FAIL or ABORT -> BLOCK

## Related Documents

- `workflows/wf-squad-overview.yaml` -- Workflow canônico
- `checklists/squad-overview-checklist.md` -- Checklist de saída
- `squad-analytics.md` -- Métricas complementares

---

_Task Version: 2.0.0_
_Last Updated: 2026-03-27_
_Sub-tasks: 6 atomic tasks_
