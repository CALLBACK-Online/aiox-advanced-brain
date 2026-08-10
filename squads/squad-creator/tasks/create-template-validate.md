# Task: Create Template — Validate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template-validate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: create-template-validate
name: "Create Template — Validate"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Compila o arquivo de template e aplica o quality gate SC_TPL_001 antes da gravação final."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_template_validate
Output: artifact::create_template_validate
pre_condition: template compilado disponível (identity + structure + elicitation phases completed)
post_condition: template validado por SC_TPL_001 sem erros estruturais, aprovado para gravação
performance: Agent, < 5 min, fail-loud em erro estrutural ou requisito bloqueante
Completion Criteria: SC_TPL_001 PASS AND template compilado sem erro AND requisitos bloqueantes aprovados
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::create_template_validate## Purpose

Garantir que o template compilado é válido, completo e apto para ser gravado no
squad.


## Veto Conditions

- Template file does not exist at the expected output path -> BLOCK
- Template contains hardcoded values where parameters should be used -> BLOCK
- Template YAML/Markdown fails syntax validation -> BLOCK

## Acceptance Criteria

- [ ] Template compilado sem erro estrutural
- [ ] `SC_TPL_001` avaliado
- [ ] Requisitos bloqueantes aprovados antes do write

## Related Documents

- `create-template.md`
- `create-template-register.md`

---

_Task Version: 1.0.0_
