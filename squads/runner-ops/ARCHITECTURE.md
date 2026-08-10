# Runner-Ops Squad — Architecture

## Overview

O squad `runner-ops` governa o lifecycle de pipeline runners headless no AIOX platform.
Não executa runners — governa o FRAMEWORK e o PROCESSO.

## Shell & Core (ADR-046)

```
┌──────────────────────────────────────────────────────┐
│  Runner (Shell)                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  runner-lib (~30 módulos, 7.4K LOC)            │  │
│  │  state-manager | session-mgr | metrics | runtime│  │
│  │  evaluator | cascade | hooks | headless-guard  │  │
│  └────────────────────────────────────────────────┘  │
│         ↕ orquestra                                  │
│  ┌────────────────────────────────────────────────┐  │
│  │  Swarm OS (Core) — efêmero                     │  │
│  │  Agents destruídos após reportar resultado     │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

- **Shell (Runner):** Exoesqueleto determinístico em Bash. Owns: state persistence, budget/cost management, session tracking, metrics JSONL, error flags.
- **Core (Swarm):** Motor cognitivo efêmero. Times destruídos após reportar.

## Agent Hierarchy

```
runner-chief (Tier 0 — Orchestrator)
├── runner-architect (Tier 1 — Agent)    # Design + evolução de módulos
├── runner-integrator (Tier 1 — Agent)   # Migração brownfield
├── runner-validator (Tier 2 — Worker)   # validate-runner.sh + compliance
└── runner-monitor (Tier 2 — Worker)     # Métricas JSONL + health reports
```

## Runner-Lib Layers

| Layer | Módulos | Requirement |
|-------|---------|-------------|
| L1 Core | pipeline-bootstrap, runtime, metrics, models | MUST |
| L2 State | state-manager, session-mgr, context-engine | MUST |
| L3 Quality | evaluator, assertions, headless-guard, validate-runner | SHOULD |
| L4 Utility | display, arg-parser, progress-logger, json-validator, preflight | SHOULD |
| L5 Advanced | cascade, hooks, dispatch, worktree, replan, compress | NICE |

## Runner Type Taxonomy

The ecosystem supports 3 runner types, each with distinct execution patterns:

```
                          Runner Ecosystem
                               |
              ┌────────────────┼────────────────┐
              v                v                v
         PIPELINE          VALIDATOR         GATEWAY
    (sequential phases)  (artifact check)  (message bridge)
              |                |                |
    ┌─────────────┐    ┌──────────┐    ┌──────────────┐
    │ mmos.sh     │    │validate- │    │ message-     │
    │ books.sh    │    │squad.sh  │    │ gateway.sh   │
    │ copy.sh     │    │validate- │    │ telegram-    │
    │ decoder.sh  │    │skill.sh  │    │ gateway.sh   │
    │ aiox-     │    │aiox-   │    └──────────────┘
    │ map.sh      │    │validate  │
    └─────────────┘    └──────────┘
```

| Type | Input | Processing | Output | Latency |
|------|-------|-----------|--------|---------|
| Pipeline | Config + context files | Sequential LLM phases (3-8) | Generated artifacts | Minutes |
| Validator | Target artifact path | Rule checking + LLM evaluation | Compliance report | Seconds-minutes |
| Gateway | External message (webhook) | Single-turn or multi-turn LLM | Response to channel | < 5s SLA |

**Key Differences:**
- **Pipeline** runners own their execution timeline. No external SLA.
- **Validator** runners are invoked on-demand. Deterministic where possible, LLM for judgment.
- **Gateway** runners are event-driven with latency constraints. Must use smart routing (Haiku for simple, Sonnet for complex).

## Runner Registry

Fonte unica de verdade: `infrastructure/scripts/runner-lib/runner-registry.yaml`

8 runners gerenciados:

| Runner | Squad | Integration Score |
|--------|-------|------------------|
| mmos.sh | mmos | full |
| aiox-map.sh | aiox-squad | partial |
| books.sh | books | partial |
| decoder.sh | domain-decoder | partial |
| copy.sh | copy | partial |
| aiox-validate.sh | aiox-squad | minimal |
| validate-skill.sh | aiox-squad | minimal |
| validate-squad.sh | squad-creator | minimal |

## Process Flows

### Create Runner
```
Decision Tree → runner-architect (design) → create-runner (scaffold) → runner-validator (compliance)
```

### Integrate Runner (brownfield)
```
runner-integrator (audit) → plan → migrate incremental → runner-validator (verify)
```

### Validate Runner
```
runner-validator → validate-runner.sh → integration_score report → runner-chief (summary)
```

### Monitor Ecosystem
```
runner-monitor → aggregate JSONL → cost/perf/health report → runner-chief (alerts)
```

## Boundaries

**Governa:**
- `infrastructure/scripts/runner-lib/` — framework compartilhado
- `infrastructure/scripts/runner-lib/runner-registry.yaml` — registry canônico
- Processo de criação, integração, validação, monitoramento de runners

**NÃO governa:**
- Runners individuais (pertencem aos squads que os usam)
- Lógica de negócio de cada runner
- Swarm OS (runners são a Shell, Swarm é o Core)

## References

- ADR-046: `docs/architecture/adrs/ADR-046-RUNNER-SWARM-HYBRID-ARCHITECTURE.md`
- Epic 101: `docs/stories/epic-101/EPIC-101-RUNNER-EXCELLENCE.md`
- Epic 104: `docs/stories/epic-104/EPIC-104-RUNNER-OPS-SQUAD.md`
- Gap Analysis: `.aiox/squad-runtime/aiox-squad/mmos-runner/runner-gap-analysis.md`
