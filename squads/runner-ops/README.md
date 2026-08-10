---
tags: [layer/squad, squad/runner-ops]
---

# Runner-Ops Squad

Squad dedicado ao lifecycle management de pipeline runners headless no AIOX platform.

## Activation

```
/runnerOps:runner-chief
```

## What This Squad Does

Governa o **runner-lib framework** (30 modulos, 7.4K LOC) e os **processos** de criacao, integracao, validacao e monitoramento de runners headless.

**NAO governa** runners individuais — eles pertencem aos squads que os usam.
**NAO vira dependencia de runtime** dos runners gerados — eles devem depender apenas do runtime canonico em `infrastructure/scripts/runner-lib/`.

## Boundary Contract

- O pack `runner-ops` deve ser autocontido para distribuicao e instalacao.
- O runtime canonico continua em `infrastructure/scripts/runner-lib/` e `outputs/`.
- Runners criados ou migrados por este squad devem ser 100% independentes de `squads/runner-ops/`.
- O registry canonico fica em `infrastructure/scripts/runner-lib/runner-registry.yaml`.

## Architecture (ADR-046 — Shell & Core)

- **Shell (Runner-Lib):** Exoesqueleto deterministico em Bash. Owns: state persistence (`state.json` via `jq`), budget/cost management, session tracking, metrics JSONL, error flags.
- **Core (Swarm OS):** Motor cognitivo efemero. Owns: deliberacao multi-agente, sintese cruzada, trabalho cognitivo.

## Agents

| Agent | Tier | Executor | Purpose |
|-------|------|----------|---------|
| `runner-chief` | 0 | Agent | Entry point. Roteia requests, gerencia lifecycle, enforces standards |
| `runner-architect` | 1 | Agent | Design de novos runners, evolucao do runner-lib, ADR decisions |
| `runner-integrator` | 1 | Agent | Migracao brownfield de runners para runner-lib modules |
| `runner-validator` | 2 | Worker | Executa `validate-runner.sh`, compliance checks |
| `runner-monitor` | 2 | Worker | Metricas JSONL, cost tracking, health reports |

## Commands (via runner-chief)

| Command | Description |
|---------|-------------|
| `*create-runner` | Scaffold novo runner a partir do template canonico |
| `*validate-runner {id}` | Compliance check contra runner-lib standards |
| `*integrate-runner {id}` | Migrar runner para usar runner-lib modules |
| `*monitor` | Dashboard de metricas do ecossistema |
| `*registry` | Mostrar runner-registry com scores |
| `*evolve-module {name}` | Propor evolucao de modulo do runner-lib |
| `*help` | Mostrar comandos disponiveis |
| `*exit` | Sair |

## Processes Governed

1. **Create Runner** — Scaffolding via template canonico (6 fases)
2. **Integrate Runner** — Migracao brownfield (audit -> plan -> migrate -> verify)
3. **Validate Runner** — Compliance check (scan -> check -> report)
4. **Monitor Runners** — Metricas coleta (collect -> aggregate -> alert)
5. **Evolve Runner-Lib** — Framework evolution (propose -> implement -> test -> register)
6. **Headless Compliance** — 10 regras headless enforcement

## External Assets (governed, not moved)

| Asset | Path | Notes |
|-------|------|-------|
| runner-lib | `infrastructure/scripts/runner-lib/` | 30 modules, 7.4K LOC |
| runner-registry | `infrastructure/scripts/runner-lib/runner-registry.yaml` | 8 runners |
| ADR-046 | `docs/architecture/adrs/ADR-046-*` | Shell & Core |

## Local Scripts

Os scripts do squad existem para tornar o pack instalavel e operacional sem depender de passos externos:

- `scripts/install.sh` prepara diretórios locais e valida os assets canônicos exigidos.
- `scripts/validate-runner.sh` lê/escreve no registry canônico em `infrastructure/`.
- `scripts/register-runner.sh` registra runners no schema real do `runner-registry.yaml`.
- `scripts/monitor-runners.sh` usa `metrics_glob`/`outputs_dir` do registry canônico.

## Runner Ecosystem (current state)

| Runner | Squad | Integration Score |
|--------|-------|-------------------|
| mmos.sh (Golden Master) | mmos | full (100%) |
| books.sh | books | partial |
| copy.sh | copy | partial |
| decoder.sh | domain-decoder | partial |
| aiox-map.sh | aiox-squad | partial |
| aiox-validate.sh | aiox-squad | minimal |
| validate-skill.sh | aiox-squad | minimal |
| validate-squad.sh | squad-creator | minimal |

## Related

- Epic 101: Runner Excellence (integration stories)
- Epic 104: Runner-Ops Squad Creation (this squad)

## Vault (Obsidian)

- Ponte: [[cursos/entradas/squad-runner-ops|entrada · runner-ops]]

Camada leve para o Graph — não altera a execução do squad.

- Aula: [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops|09-runner-ops]]
- Skill: [[skills/runner-ops/SKILL|runner-ops]]
- Mapa: [[cursos/MOC-Squads|MOC · Squads]]
- Home: [[00-HOME]]
