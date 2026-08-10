# Task: Create Template — Structure

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template-structure` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-template-structure
name: "Create Template — Structure"
category: creation
agent: squad-chief
elicit: true
autonomous: false
description: "Define seções, placeholders e recursos especiais do template."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_template_structure
Output: artifact::create_template_structure
pre_condition: create-template-identity completed com template_id e formato definidos
post_condition: estrutura do template com seções, placeholders documentados e recursos especiais definidos
performance: < 15 min (Hybrid — design de estrutura com elicitation), escalate em placeholder ambíguo
Completion Criteria: seções principais definidas AND placeholders documentados AND recursos especiais explicitados
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::create_template_structure## Purpose

Projetar a estrutura do template com seções, placeholders documentados e regras
de repetição, condicionalidade ou diagrama quando existirem.


## Veto Conditions

- Identity output from `create-template-identity` is missing -> BLOCK
- Template structure does not contain at least one parameterizable field (`{placeholder}`) -> BLOCK

## Acceptance Criteria

- [ ] Seções principais definidas
- [ ] Placeholders documentados
- [ ] Recursos especiais explicitados quando aplicáveis

## Related Documents

- `create-template.md`
- `create-template-elicitation.md`

---

_Task Version: 1.0.0_
