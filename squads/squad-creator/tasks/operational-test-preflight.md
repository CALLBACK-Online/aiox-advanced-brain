# Task: Operational Test — Preflight

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `operational-test-preflight` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: operational-test-preflight
name: "Operational Test — Preflight"
category: validation
agent: squad-chief
elicit: false
autonomous: true
description: "Valida baseline de runtime, conexões críticas e pré-condições do teste operacional."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::operational_test_preflight
Output: artifact::operational_test_preflight
pre_condition: squad_name fornecido AND squad directory existe com runtime configurado
post_condition: preflight validado com baseline_exists, critical_connections_valid e target_ready
performance: deterministic Worker, < 30s, fail-loud se baseline ou conexões críticas inválidas
Completion Criteria: baseline exists AND critical connections valid AND target ready para teste
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Garantir que o squad está elegível para um teste operacional real antes de
executar smoke flow ou gerar artefatos.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Squad alvo |
| `target_id` | string | No | Target explícito |

## Output

```yaml
operational_preflight:
  baseline_exists: true
  critical_connections_valid: true
  target_ready: true
```


## Veto Conditions

- Target squad does not have a `data/` directory with runtime configuration -> BLOCK
- `config.yaml` of the target squad does not exist or fails YAML parsing -> BLOCK

## Acceptance Criteria

- [ ] `runtime-baseline.yaml` validado
- [ ] APIs críticas verificadas
- [ ] Target elegível confirmado

---

_Task Version: 1.0.0_
