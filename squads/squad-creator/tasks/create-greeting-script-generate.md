# Task: Create Greeting Script — Generate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-greeting-script-generate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-greeting-script-generate
name: "Create Greeting Script — Generate"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Preenche o template greeting-script-tmpl.cjs com context sources, gap map, seções do greeting e directives de runtime."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_greeting_script_generate
Output: artifact::create_greeting_script_generate
pre_condition: discovery e gap-map outputs disponíveis AND greeting-script-tmpl.cjs acessível como base
post_condition: script .cjs renderizado com collectContext, inferNextAction, buildGreeting e buildDirectives
performance: < 15 min (Hybrid — template fill + review), fail-loud se placeholder obrigatório não preenchido
Completion Criteria: template usado como base AND placeholders obrigatórios preenchidos AND Next Action e Runtime Directives presentes
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::create_greeting_script_generate## Purpose

Renderizar um script `.cjs` completo a partir do template canônico, preservando
as funções `collectContext`, `inferNextAction`, `buildGreeting` e
`buildDirectives`.


## Veto Conditions

- Gap map output from `create-greeting-script-gap-map` is missing -> BLOCK
- Greeting template (`templates/greeting-script-tmpl.cjs`) is inaccessible -> BLOCK
- Generated script has syntax errors when parsed with `node --check` -> BLOCK

## Acceptance Criteria

- [ ] `templates/greeting-script-tmpl.cjs` foi usado como base
- [ ] Placeholders obrigatórios foram preenchidos
- [ ] Output inclui Next Action e Runtime Directives

## Related Documents

- `templates/greeting-script-tmpl.cjs`
- `create-greeting-script-integrate.md`

---

_Task Version: 1.0.0_
