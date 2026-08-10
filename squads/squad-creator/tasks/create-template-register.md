# Task: Create Template — Register

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template-register` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: create-template-register
name: "Create Template — Register"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Grava o template final, atualiza README quando necessário e registra a criação."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_template_register
Output: artifact::create_template_register
pre_condition: create-template-validate passed (SC_TPL_001 PASS) AND template content pronto para gravação
post_condition: template file gravado em templates/ e inventário do squad atualizado
performance: deterministic Worker, < 30s, fail-loud em write error ou inventário inconsistente
Completion Criteria: arquivo gravado em templates/ AND README/índice local atualizado AND registro de criação emitido
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::create_template_register## Purpose

Persistir o template e deixar o squad com o inventário de templates atualizado.


## Veto Conditions

- Template file does not exist at the expected output path -> BLOCK
- Template id already exists in the squad's `templates/` directory (name collision) -> BLOCK

## Acceptance Criteria

- [ ] Arquivo gravado em `templates/`
- [ ] README ou índice local atualizado quando aplicável
- [ ] Registro final da criação emitido

## Related Documents

- `create-template.md`
- `templates/`

---

_Task Version: 1.0.0_
