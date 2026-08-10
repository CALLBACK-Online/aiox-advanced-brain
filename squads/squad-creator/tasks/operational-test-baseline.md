# Task: Operational Test — Baseline Registration

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `operational-test-baseline` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: operational-test-baseline
name: "Operational Test — Baseline Registration"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Registra o known-good state do teste operacional em operational-baseline.yaml."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::operational_test_baseline
Output: artifact::operational_test_baseline
pre_condition: smoke flow executado com results AND target usado disponível
post_condition: operational-baseline.yaml persistido em data/ com status OPERATIONAL/PARTIAL/FAILED
performance: deterministic Worker, < 30s, fail-loud em write error
Completion Criteria: operational-baseline.yaml gravado AND status derivado dos smoke results AND baseline comparável
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Persistir o estado conhecido como operacional para comparação futura.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Squad alvo |
| `selected_target` | object | Yes | Target usado |
| `smoke_results` | object | Yes | Resultado do smoke flow |

## Output

```yaml
operational_baseline:
  file: "squads/{squad_name}/data/operational-baseline.yaml"
  status: "OPERATIONAL|PARTIAL|FAILED"
```


## Veto Conditions

- Target squad does not have prior test results to compare against -> WARN (proceed as first baseline)
- `config.yaml` of the target squad does not exist or fails YAML parsing -> BLOCK

## Acceptance Criteria

- [ ] `operational-baseline.yaml` persistido
- [ ] Target e evidências registrados
- [ ] Status operacional final serializado

---

_Task Version: 1.0.0_
