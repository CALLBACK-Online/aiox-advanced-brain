# Task: retire-runner

> Process: RO-RETIRE-RUNNER | Mode: GERENCIAR | Version: 1.0.0
> Owner: runner-chief | Executor: Hybrid

## Purpose

Deprecar e remover um runner do ecossistema SINKRA de forma segura,
garantindo que nenhum processo dependente seja quebrado.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `runner_id` | ✅ | ID do runner no registry (ex: `copy`, `books`) |
| `reason` | ✅ | Justificativa: `replaced`, `obsolete`, `merged`, `squad-dissolved` |
| `replacement` | ❌ | ID do runner/skill substituto (se houver) |
| `approved_by` | ✅ | Owner do squad dono do runner |

## Veto Conditions

- **BLOCKER:** `approved_by` ausente ou não é owner do squad do runner → STOP
- **BLOCKER:** Runner tem execuções ativas (estado `EM_EXECUCAO`) → aguardar conclusão
- **BLOCKER:** Nenhum `replacement` documentado para runner em produção ativo → STOP
- **WARN:** Runner com integration_score `full` sendo aposentado → exige justificativa explícita

## Execution Steps

### Fase 1: Impact Assessment (runner-chief)
1. Verificar runner no registry — squads dependentes, última execução
2. Confirmar `approved_by` é owner legítimo do squad
3. Verificar se há execuções em andamento ou agendadas
4. Documentar: last_run, total_runs, avg_cost, integration_score

### Fase 2: Deprecation Notice (runner-architect)
1. Adicionar flag `deprecated: true` + `deprecated_at` no runner-registry.yaml
2. Adicionar header de deprecação no arquivo `.sh` do runner:
   ```bash
   # DEPRECATED: {date} — Reason: {reason}
   # Replacement: {replacement or "none"}
   ```
3. Notificar squad owner (via docs/stories ou handoff)

### Fase 3: Registry Removal (runner-monitor)
1. Após período de quarentena (mínimo 7 dias após deprecação)
2. Remover entry do runner-registry.yaml
3. Mover arquivo `.sh` para `_archive/` no squad respectivo (não deletar)
4. Atualizar contagem de runners no README do squad

### Fase 4: Closure Report
1. Gerar retire report em `outputs/runner-ops/retirements/`
2. Atualizar runner-chief registry display
3. Reportar ao squad owner

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| Retire report | `outputs/runner-ops/retirements/{runner_id}-{date}.md` | Histórico completo |
| Updated registry | `infrastructure/scripts/runner-lib/runner-registry.yaml` | Entry removida |

## Acceptance Criteria

- [ ] `approved_by` validado como owner do squad
- [ ] Flag `deprecated: true` adicionada antes da remoção
- [ ] Quarentena de 7 dias respeitada
- [ ] Arquivo `.sh` movido para `_archive/`, não deletado
- [ ] runner-registry.yaml atualizado sem a entry
- [ ] Retire report gerado em `outputs/runner-ops/retirements/`

## Handoff

- Se runner deve ser substituído por skill → escalar para `runner-architect` para assessment
- Se squad owner discorda → escalar para `@master` para arbitragem
