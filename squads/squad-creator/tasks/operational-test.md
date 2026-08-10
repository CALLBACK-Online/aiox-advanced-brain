# Task: Operational Test (Composed)

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `operational-test` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Composed` |

## Metadata

```yaml
id: operational-test
name: "Operational Test"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Composed task that orchestrates 5 atomic sub-tasks to validar operacionalmente um squad."
owner_workflow: "workflows/wf-operational-test.yaml"
template_source: "templates/operational-test-task-tmpl.md"
accountability:
  human: squad-operator
  scope: review_only
domain: Tactical

```


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Molecule
Input: request::operational_test
Output: artifact::operational_test
pre_condition: squad_name fornecido AND squad com runtime configurado AND baseline de runtime acessível
post_condition: validação E2E completa com smoke results, baseline registrado e veredito de readiness emitido
performance: Composed (5 sub-tasks), < 10 min total, fail-loud em preflight blocking condition
Completion Criteria: smoke flow executado AND baseline registrado AND readiness verdict (OPERATIONAL/PARTIAL/FAILED) emitido
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief

## Inputs

- request::operational_test## Purpose

Executar a validação E2E mínima de um squad operacional com runtime já
configurado, registrar a baseline resultante e emitir o veredito de readiness.

## Execution Sequence

```
INPUT (squad_name + test_mode + test_scope + target_id)
    |
[1] operational-test-preflight
    -> Verifica baseline de runtime e pré-condições
    |
[2] operational-test-target
    -> Seleciona o target do teste
    |
[3] operational-test-smoke
    -> Executa fetch, process, output e notificação quando aplicável
    |
[4] operational-test-baseline
    -> Registra operational-baseline.yaml
    |
[5] operational-test-report
    -> Emite veredito operacional final
    |
OUTPUT: operational_report
```

## Sub-Task Reference

| # | Task ID | Responsibility | Executor |
|---|---------|----------------|----------|
| 1 | `operational-test-preflight` | Validar pré-condições | Worker |
| 2 | `operational-test-target` | Selecionar target | Worker |
| 3 | `operational-test-smoke` | Rodar fluxo E2E mínimo | Agent |
| 4 | `operational-test-baseline` | Persistir baseline operacional | Worker |
| 5 | `operational-test-report` | Emitir decisão e próximos passos | Agent |

## Commands

```yaml
commands:
  standard: "*operational-test"
  full: "*operational-test --scope=full"
  specific_target: "*operational-test --target={id}"
  sandbox: "*operational-test --mode=sandbox"
  verbose: "*operational-test --verbose"
```


## Veto Conditions

- Target squad directory does not exist or `config.yaml` is absent -> BLOCK
- Preflight sub-task emits FAIL (critical connections invalid) -> BLOCK
- A blocking sub-task in the execution sequence emits FAIL or ABORT -> BLOCK

## Related Documents

- `workflows/wf-operational-test.yaml` -- Workflow canônico
- `templates/operational-test-task-tmpl.md` -- Fonte usada para squads gerados
- `setup-runtime.md` -- Pré-requisito operacional

---

_Task Version: 2.0.0_
_Last Updated: 2026-03-27_
_Sub-tasks: 5 atomic tasks_
