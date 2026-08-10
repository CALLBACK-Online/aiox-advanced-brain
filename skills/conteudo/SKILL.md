---
name: conteudo
description: |
  Conteúdo Squad — Instagram: carrosséis, Reels, Stories, campanhas e pesquisa de concorrentes.
  Use quando precisa operar um calendário ou campanha de conteúdo social.
---

# Conteúdo Squad


## Quando usar

- Use esta skill como **porta de entrada** do squad `conteudo` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/conteudo/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/18-conteudo.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


Squad com **10 agentes** especializados.

> **Maturidade neste acervo:** `study` — ver `docs/runtime-dependencies.md`.
> Fonte canônica de materiais: `../upstream-monorepo` (quando sincronizado).

## Agents

- **Carousel Creator — Arquiteto de Carrosseis Imperiais (Tier 1)** (`carousel-creator`)
- **Competitor Analyst — Espiao de Conteudo (Tier 1)** (`competitor-analyst`)
- **content-chief** (`content-chief`)
- **Content Planner — Arquiteto de Influencia Silenciosa (Tier 2)** (`content-planner`)
- **Content Repurposer — Alquimista de Formatos (Tier 2)** (`content-repurposer`)
- **Content Validator — Oraculo Unificado (Tier 2)** (`content-validator`)
- **Positioning Expert — Arquiteto de Dominacao Mental (Tier 1)** (`positioning-expert`)
- **Reels Creator — Engenheiro de Retencao e Conversao (Tier 1)** (`reels-creator`)
- **Stories Strategist — Arquiteto de Sequencias de Conversao (Tier 1)** (`stories-strategist`)
- **Strategist — General de Guerra do Conteudo (Tier 1)** (`strategist`)

## Activation

O orchestrador principal é `content-chief`. Para ativar:

1. Leia `squads/conteudo/agents/content-chief.md` e adote a persona
2. Carregue config: `squads/conteudo/config.yaml`
3. Siga o mission router do chief para delegar trabalho

## Available Tasks

- `analyze-competitor`
- `atomize-content`
- `audit-content`
- `create-bio`
- `create-campaign`
- `create-carousel`
- `create-clc`
- `create-content-series`
- `create-hook-batch`
- `create-impact-phrases`
- `create-levantada-mao`
- `create-reels`
- `create-stories-funil`
- `create-stories-pas`
- `create-stories-venda`
- `create-stories`
- `create-storyadd`
- `create-strategy`
- `delete-content`
- `diagnose-avatar`
- `ingest-pillar`
- `plan-calendar`
- `plan-content`
- `repurpose-content`
- … e mais 4 tasks em `squads/conteudo/tasks/`

## Available Workflows

- `wf-21-days`
- `wf-atomization`
- `wf-campaign`
- `wf-competitor-intel`
- `wf-create-content`
- `wf-hook-testing`
- `wf-multiplicar`
- `wf-positioning`
- `wf-strategy`

## Squad Directory

`squads/conteudo/`
