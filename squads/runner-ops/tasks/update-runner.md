# Task: update-runner

> Process: RO-UPDATE-RUNNER | Mode: GERENCIAR | Version: 1.0.0
> Owner: runner-integrator | Executor: Agent

## Purpose

Atualizar um runner existente para incorporar novas versões de módulos do runner-lib
ou adaptar a mudanças de interface sem migração brownfield completa.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `runner_id` | ✅ | ID do runner no registry (ex: `decoder`, `books`) |
| `update_type` | ✅ | `module-upgrade`, `interface-change`, `config-update` |
| `target_version` | ✅ | Versão alvo do módulo ou runner-lib |
| `breaking_change` | ✅ | `true` / `false` |

## Veto Conditions

- **BLOCKER:** `breaking_change: true` sem migration guide → STOP
- **BLOCKER:** Atualizar sem rodar smoke test antes e depois → STOP
- **BLOCKER:** Runner não está no registry → registrar primeiro via `register-runner`
- **WARN:** Atualização afeta mais de 1 runner simultaneamente → planejar rollout incremental

## Execution Steps

### Fase 1: Pre-Update Audit (runner-integrator)
1. Ler `runner-registry.yaml` — capturar estado atual do runner
2. Identificar módulos afetados pela atualização
3. Rodar smoke test baseline: `bash {runner}.sh --max-turns 1 --model echo`
4. Documentar: current_version, modules_used, integration_score

### Fase 2: Apply Update
1. Atualizar imports/sources do módulo modificado
2. Adaptar chamadas de função se interface mudou
3. Ajustar parâmetros ou flags se necessário
4. Não alterar lógica de negócio do runner

### Fase 3: Post-Update Validation (runner-validator)
1. Rodar smoke test pós-update
2. Rodar `validate-runner.sh {runner_id}`
3. Comparar integration_score antes vs depois
4. Se score regrediu → reverter e investigar

### Fase 4: Registry Update (runner-monitor)
1. Atualizar `runner-registry.yaml` com nova versão
2. Registrar data de atualização
3. Reportar para runner-chief

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| Update report | `outputs/runner-ops/updates/{runner_id}-{date}.md` | Antes/depois, score delta |
| Updated registry | `infrastructure/scripts/runner-lib/runner-registry.yaml` | Versão atualizada |

## Acceptance Criteria

- [ ] Smoke test passa antes e depois da atualização
- [ ] integration_score não regride
- [ ] runner-registry.yaml atualizado com nova versão
- [ ] Update report gerado em `outputs/runner-ops/updates/`

## Handoff

- Se update causa regressão → runner-integrator inicia `integrate-runner` brownfield completo
- Se breaking change requer ADR → escalar para runner-architect
