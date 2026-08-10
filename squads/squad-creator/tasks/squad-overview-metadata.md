# Task: Squad Overview — Metadata

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `squad-overview-metadata` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: squad-overview-metadata
name: "Squad Overview — Metadata"
category: documentation
agent: squad-chief
elicit: false
autonomous: true
description: "Lê config, README e inventário bruto do squad para montar a base factual do overview."
accountability:
  human: squad-operator
  scope: review_only
domain: Tactical

```


<!-- SINKRA_CONTRACT -->
Domain: `Tactical`
atomic_layer: Atom
Input: request::squad_overview_metadata
Output: artifact::squad_overview_metadata
pre_condition: squad_name fornecido AND config.yaml e README existem no squad directory
post_condition: metadata package com identidade, localização, estatísticas e contexto de ativação do squad
performance: deterministic Worker, < 30s, fail-loud se config.yaml ausente ou malformado
Completion Criteria: config.yaml parseado AND identidade extraída AND estatísticas (agents, tasks, workflows count) calculadas
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Produzir um pacote mínimo, confiável e rastreável com identidade, localização,
estatísticas e contexto de ativação do squad.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Nome do squad |
| `squad_path` | string | No | Path explícito do squad |
| `format` | string | No | `detailed` ou `compact` |

## Workflow

### Step 1: Resolver o path-alvo

- Usar `squad_path` quando informado.
- Caso contrário, assumir `squads/{squad_name}/`.
- Bloquear se `config.yaml` não existir.

### Step 2: Ler identidade primária

Extrair de `config.yaml` e `README.md`:

- `name`
- `version`
- `description`
- `entry_agent`
- `domain`
- `whenToUse`
- título e tagline do README

### Step 3: Medir inventário do squad

Contar:

- agents
- tasks
- workflows
- templates
- checklists
- data files
- tamanho total do diretório

## Output

```yaml
metadata_packet:
  squad_name: ""
  squad_path: ""
  version: ""
  description: ""
  entry_agent: ""
  domain: ""
  when_to_use: ""
  tagline: ""
  counts:
    agents: 0
    tasks: 0
    workflows: 0
    templates: 0
    checklists: 0
    data_files: 0
  size_human: ""
  format: "detailed"
```


## Veto Conditions

- `config.yaml` does not exist or is malformed YAML in the target squad directory -> BLOCK
- Required metadata fields (name, version, entry_agent) are missing from `config.yaml` -> BLOCK

## Acceptance Criteria

- [ ] Path do squad resolvido sem ambiguidade
- [ ] Identidade primária extraída de `config.yaml`
- [ ] Contagens básicas emitidas em `metadata_packet`

## Related Documents

- `squad-overview.md` -- Task composta
- `squad-overview-agents.md` -- Próxima task

---

_Task Version: 1.0.0_
