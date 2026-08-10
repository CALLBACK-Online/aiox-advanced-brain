# Task: Setup Runtime — Summary and Handoff

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `setup-runtime-handoff` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: setup-runtime-handoff
name: "Setup Runtime — Summary and Handoff"
category: runtime
agent: squad-chief
elicit: false
autonomous: true
description: "Apresenta o resumo final do setup e prepara o handoff para o teste operacional."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::setup_runtime_handoff
Output: artifact::setup_runtime_handoff
pre_condition: setup-runtime-persist completed com runtime-baseline.yaml disponível
post_condition: resumo operacional com comandos de manutenção apresentado e handoff para operational-test preparado
performance: Agent, < 5 min, structured summary com next steps acionáveis
Completion Criteria: summary com status e maintenance commands AND próximo passo canônico (operational-test) indicado
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Fechar o setup de runtime com um resumo operacional claro, listar comandos de
manutenção e indicar o próximo passo canônico.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Squad alvo |
| `runtime_requirements` | object | Yes | Requisitos normalizados |
| `runtime_validation` | object | Yes | Resultado das validações |
| `runtime_persistence` | object | Yes | Evidência de persistência |

## Output

```yaml
runtime_handoff:
  ready_for_operational_test: true
  commands:
    - "*setup-runtime --status"
    - "*setup-runtime --validate"
    - "*operational-test"
```


## Veto Conditions

- Runtime validation did not complete or overall_status is FAILED -> BLOCK
- Handoff artifact write fails -> BLOCK

## Acceptance Criteria

- [ ] Resumo final apresentado
- [ ] Comandos de manutenção listados
- [ ] Handoff para `operational-test` explicitado

---

_Task Version: 1.0.0_
