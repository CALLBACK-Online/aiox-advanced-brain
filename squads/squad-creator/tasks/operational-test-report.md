# Task: Operational Test — Report and Decision

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `operational-test-report` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: operational-test-report
name: "Operational Test — Report and Decision"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Apresenta o resultado do teste operacional e o veredito de readiness."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::operational_test_report
Output: artifact::operational_test_report
pre_condition: smoke results, selected target e operational baseline disponíveis
post_condition: operational report com decision (OPERATIONAL/PARTIAL/FAILED) e recommended_next_step
performance: Agent, < 5 min, structured output com decisão clara e próximo passo acionável
Completion Criteria: decision emitida AND ready_for_production avaliado AND recommended_next_step definido
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Transformar a execução operacional em decisão clara: pronto para produção,
parcialmente operacional ou bloqueado.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `selected_target` | object | Yes | Target do teste |
| `smoke_results` | object | Yes | Resultado do fluxo |
| `operational_baseline` | object | Yes | Baseline persistido |

## Output

```yaml
operational_report:
  ready_for_production: false
  decision: "OPERATIONAL|PARTIAL|FAILED"
  recommended_next_step: ""
```


## Veto Conditions

- Smoke test results from upstream sub-task are missing -> BLOCK
- Report template is inaccessible -> BLOCK

## Acceptance Criteria

- [ ] Resultado apresentado de forma legível
- [ ] Veredito operacional emitido
- [ ] Próximo passo recomendado

---

_Task Version: 1.0.0_
