# Task: Rename Squad — Map

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `rename-squad-map` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: rename-squad-map
name: "Rename Squad — Map"
category: maintenance
agent: squad-chief
elicit: false
autonomous: true
description: "Executa o blast radius mapping do rename, categoriza superfícies e valida vetoes iniciais."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::rename_squad_map
Output: artifact::rename_squad_map
pre_condition: old_name e new_name fornecidos AND old_name existe como squad directory
post_condition: blast radius mapeado por zona com superfícies categorizadas e vetoes iniciais avaliados
performance: deterministic Worker, < 30s, fail-loud se old_name não existe ou new_name colide
Completion Criteria: blast radius gerado AND old_name validado AND new_name sem colisão AND vetoes avaliados
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::rename_squad_map## Purpose

Mapear todas as superfícies impactadas antes de qualquer rename estrutural,
bloqueando a operação quando o blast radius não estiver explícito.


## Veto Conditions

- Source squad directory does not exist -> BLOCK
- `new_name` already exists as a squad directory (name collision) -> BLOCK
- `old_name` equals `new_name` (no-op rename) -> BLOCK

## Acceptance Criteria

- [ ] Blast radius gerado e categorizado por zona
- [ ] `old_name` existe e `new_name` não colide
- [ ] Vetoes iniciais avaliados

## Related Documents

- `rename-squad.md`
- `rename-squad-structural.md`

---

_Task Version: 1.0.0_
