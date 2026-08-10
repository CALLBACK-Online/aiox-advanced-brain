# Task: Rename Squad — Propagate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `rename-squad-propagate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: rename-squad-propagate
name: "Rename Squad — Propagate"
category: maintenance
agent: squad-chief
elicit: false
autonomous: true
description: "Propaga o novo nome para mirrors IDE, cross-squad refs, workspace, infraestrutura, apps e registries textuais."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::rename_squad_propagate
Output: artifact::rename_squad_propagate
pre_condition: rename-squad-structural completed AND blast radius com superfícies externas mapeadas
post_condition: referências externas propagadas em IDE mirrors, cross-squad refs, workspace, infra e registries
performance: deterministic Worker, < 30s, fail-loud se superfície crítica não propagada
Completion Criteria: IDE mirrors atualizados AND cross-squad refs propagadas AND zero superfícies críticas pendentes
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::rename_squad_propagate## Purpose

Eliminar referências residuais ao nome antigo fora do diretório do squad
renomeado.


## Veto Conditions

- Structural rename from `rename-squad-structural` did not complete -> BLOCK
- Residual references to `old_name` found in critical config files after propagation -> BLOCK

## Acceptance Criteria

- [ ] Mirrors IDE atualizados
- [ ] Refs cross-squad e infra propagadas
- [ ] Nenhuma superfície crítica ficou fora do replace

## Related Documents

- `rename-squad-structural.md`
- `rename-squad-validate.md`

---

_Task Version: 1.0.0_
