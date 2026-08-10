# Task: Create Template — Identity

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template-identity` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-template-identity
name: "Create Template — Identity"
category: creation
agent: squad-chief
elicit: true
autonomous: false
description: "Resolve squad-alvo, identidade do template, formato e modo de uso antes da composição."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_template_identity
Output: artifact::create_template_identity
pre_condition: template_name e squad_name fornecidos AND squad-alvo existe com config.yaml válido
post_condition: identidade do template resolvida com template_id único, formato e modo de uso definidos
performance: < 15 min (Hybrid — elicitation de identidade), escalate se colisão de template_id detectada
Completion Criteria: squad-alvo validado AND template_id único no squad AND formato e modo explicitados
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::create_template_identity## Purpose

Definir a identidade do template, bloquear colisões e produzir o contrato base
que será usado pelas fases seguintes.


## Veto Conditions

- Elicitation output from `create-template-elicitation` is missing or incomplete -> BLOCK
- Template identity fields (id, name, version) not resolved -> BLOCK

## Acceptance Criteria

- [ ] Squad-alvo resolvido e validado
- [ ] `template_id` único dentro do squad
- [ ] Formato e modo de uso explicitados

## Related Documents

- `create-template.md`
- `create-template-structure.md`

---

_Task Version: 1.0.0_
