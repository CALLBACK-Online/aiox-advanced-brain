# Task: Create Greeting Script — Gap Map

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-greeting-script-gap-map` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: create-greeting-script-gap-map
name: "Create Greeting Script — Gap Map"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Transforma sinais observáveis do squad em tabela signal -> severity -> next_action seguindo a prioridade obrigatória do greeting."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_greeting_script_gap_map
Output: artifact::create_greeting_script_gap_map
pre_condition: create-greeting-script-discovery completed com context sources e sinais observáveis mapeados
post_condition: gap map com tabela signal -> severity -> next_action com prioridade blocking > non_blocking > intake
performance: Agent, < 5 min, structured output com deterministic priority ordering
Completion Criteria: gap map inclui prioridades blocking/non_blocking/intake AND blockers têm precedência AND cada sinal tem next_action
error_handling: fail-loud, persist error context, escalate to squad-chief

## Inputs

- request::create_greeting_script_gap_map## Purpose

Construir a heurística determinística de `inferNextAction()` sem permitir CTA
genérico quando houver blocker explícito.


## Veto Conditions

- Discovery output from `create-greeting-script-discovery` is missing or incomplete -> BLOCK
- Entry agent file does not exist at the resolved path -> BLOCK

## Acceptance Criteria

- [ ] Gap map inclui prioridades `blocking`, `non_blocking` e `intake|ready`
- [ ] Blockers têm precedência explícita
- [ ] Cada sinal produz `next_action` e `reason`

## Related Documents

- `create-greeting-script-discovery.md`
- `create-greeting-script-generate.md`

---

_Task Version: 1.0.0_
