# Task: register-runner

> Process: RP-REGISTER-RUNNER | Mode: CONFIGURAR | Version: 1.0.0
> Owner: runner-chief | Executor: Worker

## Purpose

Adicionar um runner ao runner-registry.yaml, tornando-o descobrível pelo squad runner-ops
para monitoramento, validação e governance.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `runner_path` | ✅ | Path do script (ex: `squads/copy/scripts/copy-runner.sh`) |
| `runner_name` | ✅ | Identificador único (ex: `copy-runner`) |
| `squad` | ✅ | Squad owner (ex: `copy`) |
| `purpose` | ✅ | Uma frase descrevendo o que o runner faz |
| `compliance_score` | ⚠️ | Score do validate-runner (0-100). Obrigatório para status: active |

## Veto Conditions

- **BLOCKER:** `runner_name` já existe no registry → STOP, usar update ao invés de add
- **BLOCKER:** `runner_path` não existe no filesystem → STOP
- **BLOCKER:** `compliance_score < 60` → registrar como `status: non-compliant`, não `active`

## Registry Entry Format

```yaml
# infrastructure/scripts/runner-lib/runner-registry.yaml
runners:
  - id: {runner_name}
    path: {runner_path}
    squad: {squad}
    type: pipeline | validator
    outputs_dir: outputs/{squad}
    metrics_glob: outputs/{squad}/**/metrics.jsonl
    runs_dir: outputs/{squad}
    purpose: {purpose}  # opcional, metadata auxiliar
    integration_score: minimal | partial | full
    compliance_score: {X}
    last_validated: {YYYY-MM-DD}
    uses_run_llm_prompt: true | false
    uses_state_manager: true | false
    uses_metrics: true | false
    uses_session_mgr: true | false
    uses_cascade: true | false
```

## Execution

```bash
# Registro recomendado via script autocontido do squad
bash squads/runner-ops/scripts/register-runner.sh \
  --name {runner_name} \
  --path {runner_path} \
  --squad {squad} \
  --purpose "{purpose}"
```

## Completion Criteria

- [ ] Entry adicionada ao runner-registry.yaml
- [ ] YAML válido após edição
- [ ] `integration_score` inicial coerente
- [ ] `last_validated` coerente com compliance_score
- [ ] Confirmação de que runner_name é único
- [ ] Runner registrado sem depender de `squads/runner-ops/`

## Handoff

- **Registered →** Retornar confirmação para runner-chief
- **Non-compliant →** Notificar squad owner + sugerir integrate-runner
