# Task: monitor-runners

> Process: RP-MONITOR-RUNNERS | Mode: GERENCIAR | Version: 1.0.0
> Owner: runner-monitor | Executor: Worker

## Purpose

Coletar métricas de execução de todos os runners registrados, gerar health report
e detectar anomalias de custo, falha ou performance.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `scope` | ⚠️ | `all` (default) ou nome de squad específico |
| `period` | ⚠️ | `today`, `week`, `month`. Default: `today` |
| `alert_threshold_cost` | ⚠️ | Custo máximo por runner em USD. Default: `$5.00` |
| `alert_threshold_failures` | ⚠️ | % de falhas para alerta. Default: `20%` |

## Data Sources

```bash
# JSONL metrics por runner
outputs/{squad}/{business}/metrics.jsonl

# Runner registry
infrastructure/scripts/runner-lib/runner-registry.yaml

# Session logs
outputs/{squad}/{business}/session-*.log
```

## Execution

```bash
# Dashboard do ecossistema
bash squads/runner-ops/scripts/monitor-runners.sh --days 7

# Runner específico + artifact JSON
bash squads/runner-ops/scripts/monitor-runners.sh --runner copy --days 30 --report --json
```

## Output Format

```
RUNNER HEALTH REPORT
====================
Period: {period}
Generated: {timestamp}

SUMMARY
-------
Total runners monitored: {N}
Total runs: {X}
Total cost: ${Y}
Alert count: {Z}

RUNNER STATUS
-------------
| Runner | Runs | Cost | Failures | Avg Duration | Status |
|--------|------|------|----------|--------------|--------|
| copy-runner | 12 | $1.20 | 0 (0%) | 45s | 🟢 HEALTHY |
| books-runner | 3 | $0.80 | 1 (33%) | 120s | 🟡 WARN |
| mmos-runner | 0 | $0.00 | - | - | ⚫ IDLE |

ALERTS
------
🔴 [COST] books-runner: $4.80 this week (threshold: $5.00 — approaching limit)
🟡 [FAILURES] books-runner: 33% failure rate (threshold: 20%)

RECOMMENDATIONS
---------------
1. Investigate books-runner failures (check session-*.log)
2. Consider cost cap reduction for books-runner
```

## Veto Conditions

- **WARN:** Nenhum arquivo metrics.jsonl encontrado → reportar "No metrics available for period"
- **ALERT:** Runner com custo > threshold → notificar runner-chief
- **ALERT:** Runner com failure rate > threshold → notificar runner-chief

## Completion Criteria

- [ ] Todos os runners no registry verificados
- [ ] Report gerado em `outputs/runner-ops/health/`
- [ ] Alerts identificados e documentados
- [ ] Recommendations claras e acionáveis
- [ ] Leitura feita a partir do registry canônico em `infrastructure/`

## Handoff

- **Alerts presentes →** runner-chief imediatamente
- **Clean report →** Salvar em registry, nenhuma ação necessária
