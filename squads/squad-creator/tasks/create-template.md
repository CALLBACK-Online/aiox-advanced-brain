# Task: Create Template (Composed)

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-template` |
| **Version** | `2.1.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Composed` |

## Metadata

```yaml
id: create-template
name: "Create Template"
category: creation
agent: squad-chief
elicit: true
autonomous: false
description: "Task composta que orquestra 5 subtasks atômicas para criar templates de output com elicitação, quality gate e registro final."
owner_workflow: "workflows/wf-create-template.yaml"
accountability:
  human: squad-operator
  scope: review_only
domain: Tactical

```


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Molecule
Input: request::create_template
Output: artifact::create_template
pre_condition: template_name, template_id, squad_name e output_format fornecidos AND squad target existe
post_condition: template file criado em templates/, validado por SC_TPL_001 e registrado no inventário do squad
performance: Composed (5 subtasks), < 15 min total com elicitation, veto em SC_TPL_001 bloqueia pipeline
Completion Criteria: template file salvo AND SC_TPL_001 PASS AND inventário do squad atualizado
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief

## Inputs

- request::create_template## Purpose

Criar templates de output reutilizáveis para squads, com estrutura explícita,
documentação de placeholders e validação antes da gravação final.

## Execution Sequence

```text
INPUT (template_name + template_id + squad_name + output_format)
    |
[1] create-template-identity
    -> Resolve squad, identidade e modo do template
    |
[2] create-template-structure
    -> Define seções, placeholders e recursos especiais
    |
[3] create-template-elicitation
    -> Configura o fluxo interativo ou emite skip explícito
    |
[4] create-template-validate
    -> Compila o template e aplica SC_TPL_001
    |
[5] create-template-register
    -> Grava o arquivo e atualiza o inventário do squad
    |
OUTPUT: template_registration
```

## Sub-Task Reference

| # | Task ID | Responsibility | Executor |
|---|---------|----------------|----------|
| 1 | `create-template-identity` | Identidade e vetoes iniciais | Hybrid |
| 2 | `create-template-structure` | Estrutura e placeholders | Hybrid |
| 3 | `create-template-elicitation` | Fluxo interativo | Hybrid |
| 4 | `create-template-validate` | Quality gate SC_TPL_001 | Agent |
| 5 | `create-template-register` | Persistência e registro | Worker |

## Commands

```yaml
commands:
  standard: "*create-template {template_id} --squad {squad_name}"
  interactive: "*create-template {template_id} --squad {squad_name} --interactive"
```


## Veto Conditions

- Target squad directory does not exist or `config.yaml` is absent -> BLOCK
- A blocking sub-task in the execution sequence emits FAIL or ABORT -> BLOCK
- Template id already exists in `squads/{squad}/templates/` (name collision) -> BLOCK

## Related Documents

- `workflows/wf-create-template.yaml`
- `create-template-validate.md`

---

_Task Version: 2.1.0_
