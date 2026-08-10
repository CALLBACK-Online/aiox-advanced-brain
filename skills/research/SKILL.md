---
name: research
description: |
  Research Squad — research técnica profunda, inteligência competitiva, discovery, benchmarking, OSINT e revisões sistemáticas.
  Use quando: a investigação atravessa fontes e disciplinas ou sustenta uma decisão de alto impacto.
---

# Research Squad

Squad com **14 agentes** e **65 tasks** (benchmark, marketing, product-discovery, tech-research).

> **Maturidade neste acervo:** `partial` — ver `docs/runtime-dependencies.md`.
> Sucessor canônico de `spy`, `deep-research` e do pipeline tech-research no monorepo.
> Fonte canônica: `../upstream-monorepo/squads/research`.

## Agents

- **bench-analyst** (`bench-analyst`)
- **Benchmark Runtime** (`benchmark-runtime`)
- **booth** (`booth`)
- **creswell** (`creswell`)
- **dr-orchestrator** (`dr-orchestrator`)
- **forsgren** (`forsgren`)
- **gilad** (`gilad`)
- **klein** (`klein`)
- **research-head** (`marketing-deepdive`)
- **Reference Competitor Clone** (`reference-competitor-clone`)
- **research-chief** (`research-chief`)
- **Research Operator** (`research-operator`)
- **sackett** (`sackett`)
- **tech-research-agent** (`tech-research-agent`)

## Activation

O orchestrador principal é `research-chief`. Para ativar:

1. Leia `squads/research/agents/research-chief.md` e adote a persona
2. Carregue config: `squads/research/config.yaml`
3. Para bench comparativo: tasks em `squads/research/tasks/benchmark/`
4. Para research técnica: tasks em `squads/research/tasks/tech-research/` e skill `tech-research`

## Available Tasks (amostra)

- `benchmark/bench-absorb`
- `benchmark/bench-battle-card`
- `benchmark/bench-codebase-recon`
- `benchmark/bench-company-intel`
- `benchmark/bench-deep-compare`
- `benchmark/bench-detect`
- `benchmark/bench-framework`
- `benchmark/bench-gap-analysis`
- `benchmark/bench-gap-company`
- `benchmark/bench-gap-llm`
- `benchmark/bench-gap-product`
- `benchmark/bench-gap-technology`
- `benchmark/bench-gap`
- `benchmark/bench-hooks`
- `benchmark/bench-inventory`
- `benchmark/bench-llm-eval`
- `benchmark/bench-matrix-codebase`
- `benchmark/bench-matrix-company`
- `benchmark/bench-matrix-llm`
- `benchmark/bench-matrix-product`
- `benchmark/bench-matrix-technology`
- `benchmark/bench-matrix`
- `benchmark/bench-migrate`
- `benchmark/bench-product-research`
- `benchmark/bench-quick-compare`
- `benchmark/bench-report-load-evidence`
- `benchmark/bench-report-publish`
- `benchmark/bench-report-synthesize-findings`
- `benchmark/bench-report`
- `benchmark/bench-score`
- … e mais 35 tasks em `squads/research/tasks/`

## Available Workflows

- `bench-comparison-pipeline`
- `wf-competitive-intel`
- `wf-deep-research`
- `wf-product-discovery`
- `wf-quick-research`

## Squad Directory

`squads/research/`
