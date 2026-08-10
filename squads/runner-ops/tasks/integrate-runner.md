# Task: integrate-runner

> Process: RP-INTEGRATE-RUNNER | Mode: GERENCIAR | Version: 1.0.0
> Owner: runner-integrator | Executor: Agent

## Purpose

Migrar runner existente (brownfield) para uso completo dos módulos runner-lib.
Elimina reimplementações locais, adota padrões de estado, métricas e lifecycle.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `runner_path` | ✅ | Path do runner a migrar (ex: `squads/copy/scripts/copy-runner.sh`) |
| `validation_report` | ⚠️ | Output do validate-runner.md (lista de violations) |
| `dry_run` | ⚠️ | Se `true`, gera diff sem aplicar. Default: false |

## Veto Conditions

- **BLOCKER:** Runner não tem backup antes de modificar → criar backup primeiro
- **BLOCKER:** Runner está em uso em produção ativo → confirmar janela de manutenção
- **BLOCKER:** Sem relatório de validação → executar validate-runner primeiro
- **WARN:** Mais de 50% do runner é custom logic → escalar para runner-architect review

## Migration Checklist

### Phase 1: Audit (~15 min)
- [ ] Ler runner completo, mapear todas as funções custom
- [ ] Identificar overlaps com runner-lib (o que pode ser deletado)
- [ ] Estimar impacto da migração (low/medium/high)
- [ ] Criar backup: `cp {runner_path} {runner_path}.bak`

### Phase 2: Bootstrap Integration (~10 min)
- [ ] Adicionar `source "$(dirname "$0")/../../infrastructure/scripts/runner-lib/pipeline-bootstrap.sh"` no topo
- [ ] Verificar que `RUNNER_LIB_DIR` resolve corretamente
- [ ] Testar `--dry-run` após bootstrap
- [ ] Confirmar que nenhuma dependência para `squads/runner-ops/` foi introduzida

### Phase 3: Replace Core Functions (~20 min)
- [ ] Substituir chamadas LLM diretas por `run_llm_prompt()`
- [ ] Substituir state management local por `state_init()` + `state_update()`
- [ ] Substituir metrics tracking por `METRICS_FILE` export (auto-handled)
- [ ] Adicionar `check_cost_cap()` em cada fase

### Phase 4: Lifecycle (~10 min)
- [ ] Adicionar `session_start()` no início do main
- [ ] Adicionar `session_end()` no final do main
- [ ] Adicionar `filter_llm_output()` em outputs críticos

### Phase 5: Validation (~10 min)
- [ ] Executar `validate-runner.md` no runner migrado
- [ ] Score deve ser >= 80/100 para PASS
- [ ] Testar com `--dry-run` e modelo haiku

## Output Format

```
MIGRATION REPORT
================
Runner: {runner_path}
Pre-migration score: {X}/100
Post-migration score: {Y}/100
Delta: +{Z} points

Changes applied:
  ✅ Added pipeline-bootstrap.sh
  ✅ Replaced 3 direct LLM calls with run_llm_prompt()
  ✅ Replaced local state dict with state_init/update
  ✅ Added session lifecycle
  ⚠️  custom_transform() kept (no runner-lib equivalent)

Backup: {runner_path}.bak
Status: COMPLETE | PARTIAL | FAILED
```

## Completion Criteria

- [ ] Backup criado antes de qualquer modificação
- [ ] Score pós-migração >= 80/100
- [ ] Runner executa sem erros com `--dry-run`
- [ ] Relatório de migração gerado
- [ ] Custom logic documentada (o que ficou e por quê)

## Handoff

- **COMPLETE →** runner-validator para re-validação final
- **PARTIAL →** runner-chief com relatório do que ficou pendente
- **FAILED →** runner-architect para redesign
