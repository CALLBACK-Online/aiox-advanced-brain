# Runner-Ops Squad — Production Examples

Outputs do squad `runner-ops` são módulos do framework runner-lib e runners individuais que vivem em `infrastructure/scripts/`.

## Onde os outputs reais vivem

| Tipo | Localização |
|---|---|
| Runner-lib framework (~30 módulos) | `infrastructure/scripts/runner-lib/` |
| Runner registry (8 runners) | `infrastructure/scripts/runner-lib/runner-registry.yaml` |
| Runners individuais | `infrastructure/scripts/runners/` |
| Metrics JSONL (produção) | Cada runner emite `metrics.jsonl` em runtime |
| Pipeline state | `.aiox/runner-state/` (runtime) |

## Evidência de uso

- Framework runner-lib em produção (~7.4K LOC, 30 módulos)
- 8 runners registrados e ativos (validate-squad, deep-research, etc.)
- Headless compliance enforcement em todos os runners
- ADR-046 (Runner/Swarm Hybrid Architecture) implementado

## Tasks canônicas

- `tasks/create-runner.md` — scaffolding de novos runners
- `tasks/integrate-runner.md` — migração brownfield
- `tasks/validate-runner.md` — compliance check
- `tasks/monitor-runner.md` — métricas de custo/performance

## Provenance

Outputs do squad são o próprio framework compartilhado. Execuções específicas deixam `metrics.jsonl` files. Squad foi testado extensivamente para criação e integração de runners.
