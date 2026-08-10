# Task: Create Greeting Script — Validate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-greeting-script-validate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: create-greeting-script-validate
name: "Create Greeting Script — Validate"
category: creation
agent: squad-chief
elicit: false
autonomous: true
description: "Executa o script gerado, valida 3 cenários obrigatórios e aplica o checklist de greeting script."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_greeting_script_validate
Output: artifact::create_greeting_script_validate
pre_condition: greeting script integrado AND greeting-script-checklist.md acessível AND node runtime disponível
post_condition: script validado com 3 cenários obrigatórios, checklist aplicado, veredito PASS/FAIL emitido
performance: deterministic Worker, < 30s para execução + checklist, fail-loud se exit code != 0
Completion Criteria: script executa com exit 0 AND 3 cenários verificados AND greeting-script-checklist PASS
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::create_greeting_script_validate## Purpose

Fechar o quality gate do greeting garantindo execução sem erro, presença de
Runtime Directives e priorização correta do Next Action.


## Veto Conditions

- Greeting script does not exist at the expected output path -> BLOCK
- Script execution (`node scripts/generate-squad-greeting.js {squad} {agent}`) returns non-zero exit code -> BLOCK
- Output does not contain `SQUAD_RUNTIME_DIRECTIVES` marker -> BLOCK

## Acceptance Criteria

- [ ] Script executa com exit code `0`
- [ ] 3 cenários obrigatórios foram verificados
- [ ] `checklists/greeting-script-checklist.md` passa

## Related Documents

- `create-greeting-script.md`
- `checklists/greeting-script-checklist.md`

---

_Task Version: 1.0.0_
