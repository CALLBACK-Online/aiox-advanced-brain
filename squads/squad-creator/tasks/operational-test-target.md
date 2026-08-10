# Task: Operational Test — Target Selection

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `operational-test-target` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: operational-test-target
name: "Operational Test — Target Selection"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Seleciona o melhor target para o teste operacional com base no modo e no domínio do squad."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::operational_test_target
Output: artifact::operational_test_target
pre_condition: operational-test-preflight PASS AND squad mode e domínio conhecidos
post_condition: target selecionado com type, id e details para maximizar cobertura do teste
performance: deterministic Worker, < 30s, fail-loud se nenhum target elegível encontrado
Completion Criteria: target selecionado AND type/id/name/details preenchidos AND cobertura justificada
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Escolher o alvo do teste operacional para maximizar cobertura e reduzir risco.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Squad alvo |
| `test_mode` | enum | No | `live` ou `sandbox` |
| `target_id` | string | No | Target explícito |

## Output

```yaml
selected_target:
  type: ""
  id: ""
  name: ""
  details: ""
```


## Veto Conditions

- Target squad does not exist or `config.yaml` is absent -> BLOCK
- No testable entry points identified in the squad (no agents, no scripts, no workflows) -> BLOCK

## Acceptance Criteria

- [ ] Target explícito respeitado quando fornecido
- [ ] Seleção automática aplicada quando necessário
- [ ] Evidência do target registrada

---

_Task Version: 1.0.0_
