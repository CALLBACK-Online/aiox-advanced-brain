# Task: Create Greeting Script — Integrate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-greeting-script-integrate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: create-greeting-script-integrate
name: "Create Greeting Script — Integrate"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Persiste o script gerado, atualiza STEP 3.5 do entry agent e registra o script no config do squad."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_greeting_script_integrate
Output: artifact::create_greeting_script_integrate
pre_condition: greeting script .cjs gerado AND entry agent acessível AND squad config.yaml writable
post_condition: script salvo em scripts/generate-{squad}-greeting.cjs, entry agent atualizado com STEP 3.5 e config registrado
performance: deterministic Worker, < 30s, fail-loud em write error ou entry agent malformado
Completion Criteria: script salvo em scripts/ AND entry agent STEP 3.5 atualizado AND config.yaml registra o script
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::create_greeting_script_integrate## Purpose

Conectar o artefato gerado ao ciclo real de ativação do squad sem quebrar o
agent de entrada nem o inventário de scripts.


## Veto Conditions

- Generated greeting script from `create-greeting-script-generate` does not exist -> BLOCK
- Target squad `scripts/` directory is not writable -> BLOCK

## Acceptance Criteria

- [ ] Script salvo em `scripts/generate-{squad}-greeting.cjs`
- [ ] Entry agent atualizado com STEP 3.5
- [ ] `config.yaml` do squad registra o script

## Related Documents

- `create-greeting-script-generate.md`
- `create-greeting-script-validate.md`

---

_Task Version: 1.0.0_
