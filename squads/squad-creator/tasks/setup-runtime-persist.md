# Task: Setup Runtime — Persist Configuration

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `setup-runtime-persist` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: setup-runtime-persist
name: "Setup Runtime — Persist Configuration"
category: runtime
agent: squad-chief
elicit: false
autonomous: true
description: "Persiste variáveis de ambiente, backup dedicado e baseline de runtime."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::setup_runtime_persist
Output: artifact::setup_runtime_persist
pre_condition: setup-runtime-validate completed com conexões validadas AND credenciais disponíveis
post_condition: .env e .env.{squad_name} persistidos, runtime-baseline.yaml criado com estado validado
performance: deterministic Worker, < 30s, fail-loud em write error ou permission denied
Completion Criteria: .env files persistidos AND runtime-baseline.yaml criado AND backup dedicado disponível
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Salvar a configuração validada em `.env`, `.env.{squad_name}` e
`runtime-baseline.yaml`.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Squad alvo |
| `runtime_credentials` | object | Yes | Credenciais coletadas |
| `runtime_validation` | object | Yes | Resultado da validação |

## Workflow

### Step 1: Atualizar arquivos de ambiente

Persistir variáveis configuradas de forma idempotente.

### Step 2: Registrar baseline

Salvar `squads/{squad_name}/data/runtime-baseline.yaml`.

## Output

```yaml
runtime_persistence:
  env_updated: true
  squad_env_path: ".env.{squad_name}"
  baseline_path: "squads/{squad_name}/data/runtime-baseline.yaml"
```


## Veto Conditions

- `setup-runtime-validate` did not complete or overall_status is FAILED -> BLOCK
- Write to `.env` or `runtime-baseline.yaml` fails due to permission error -> BLOCK

## Acceptance Criteria

- [ ] `.env` atualizado
- [ ] `.env.{squad_name}` criado ou atualizado
- [ ] `runtime-baseline.yaml` persistido

---

_Task Version: 1.0.0_
