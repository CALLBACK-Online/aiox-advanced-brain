# Task: Create Greeting Script — Discovery

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-greeting-script-discovery` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-greeting-script-discovery
name: "Create Greeting Script — Discovery"
category: creation
agent: squad-chief
elicit: true
autonomous: false
description: "Resolve config, entry agent, context sources e comandos que alimentam o greeting determinístico."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_greeting_script_discovery
Output: artifact::create_greeting_script_discovery
pre_condition: squad_name fornecido AND config.yaml do squad existe e parseável
post_condition: discovery output com entry_agent resolvido, context sources mapeados e comandos do agente identificados
performance: < 15 min (Hybrid — config parsing + elicitation), escalate se config.yaml inválido
Completion Criteria: config.yaml parseado AND entry_agent resolvido AND context sources e comandos mapeados
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::create_greeting_script_discovery## Purpose

Mapear o contrato estrutural do squad para que a geração do greeting dependa apenas
de sinais determinísticos e paths reais.


## Veto Conditions

- `config.yaml` of the target squad does not exist or fails YAML parsing -> BLOCK
- `squad_name` parameter not provided or resolves to a non-existent directory -> BLOCK

## Acceptance Criteria

- [ ] `config.yaml` do squad parseado com sucesso
- [ ] `entry_agent` resolvido
- [ ] Context sources e comandos do agente mapeados

## Related Documents

- `create-greeting-script.md`
- `create-greeting-script-gap-map.md`

---

_Task Version: 1.0.0_
