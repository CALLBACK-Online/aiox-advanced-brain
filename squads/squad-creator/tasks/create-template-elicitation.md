# Task: Create Template — Elicitation

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template-elicitation` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-template-elicitation
name: "Create Template — Elicitation"
category: creation
agent: squad-chief
elicit: true
autonomous: false
description: "Configura o fluxo de elicitação quando o template é interativo, ou emite skip explícito quando ele é automático."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_template_elicitation
Output: artifact::create_template_elicitation
pre_condition: create-template-structure completed com seções e placeholders definidos
post_condition: fluxo de elicitação configurado (interativo) ou skip_reason emitido (automático)
performance: < 15 min (Hybrid — configuração de elicitation flow), escalate se modo ambíguo
Completion Criteria: templates interativos com fluxo configurado AND templates automáticos com skip_reason explícito
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::create_template_elicitation## Purpose

Serializar a experiência de elicitação do template e evitar que a interatividade
fique implícita ou incompleta.


## Veto Conditions

- Template type not identified or not one of the valid template categories -> BLOCK
- `squad_name` parameter not provided or resolves to a non-existent directory -> BLOCK

## Acceptance Criteria

- [ ] Templates interativos têm fluxo configurado
- [ ] Templates automáticos produzem `skip_reason` explícito
- [ ] Opções e seções de elicitação ficaram claras

## Related Documents

- `create-template.md`
- `create-template-validate.md`

---

_Task Version: 1.0.0_
