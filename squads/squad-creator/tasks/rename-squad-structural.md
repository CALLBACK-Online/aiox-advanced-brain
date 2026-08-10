# Task: Rename Squad — Structural

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `rename-squad-structural` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: rename-squad-structural
name: "Rename Squad — Structural"
category: maintenance
agent: squad-chief
elicit: false
autonomous: true
description: "Executa branch opcional, git mv do diretório, ajuste interno do squad e rename de scripts locais."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::rename_squad_structural
Output: artifact::rename_squad_structural
pre_condition: rename-squad-map completed sem vetoes AND blast radius explícito disponível
post_condition: diretório movido via git mv, config.yaml e arquivos internos refletem new_name, scripts renomeados
performance: deterministic Worker, < 30s, fail-loud em git mv error ou config parse failure
Completion Criteria: directory moved AND config.yaml updated AND internal scripts renamed AND agent IDs preservados
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::rename_squad_structural## Purpose

Aplicar a mutação estrutural central do rename sem ainda propagar referências
externas pelo restante do repositório.


## Veto Conditions

- Blast radius map from `rename-squad-map` is missing -> BLOCK
- Veto conditions from blast radius map have unresolved items -> BLOCK

## Acceptance Criteria

- [ ] Diretório do squad foi movido corretamente
- [ ] `config.yaml` e arquivos internos refletem `new_name`
- [ ] Scripts internos críticos foram renomeados

## Related Documents

- `rename-squad-map.md`
- `rename-squad-propagate.md`

---

_Task Version: 1.0.0_
