---
name: data
description: |
  Data Squad - 7 agents. Use quando precisar orquestrar múltiplos especialistas de dados ou não souber qual expert usar

  Use quando: ativar o squad data para executar missoes do dominio.
---

# Data Squad


## Quando usar

- Use esta skill como **porta de entrada** do squad `data` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/data/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/10-data.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


Squad com **7 agentes** especializados.

## Agents

- **Avinash Kaushik** (`avinash-kaushik`) - DIGITAL ANALYTICS EVANGELIST - Attribution, DMMM, Data Storytelling
- **Data Chief** (`data-chief`) - Orquestrador de Data Intelligence & Analytics Strategy
- **David Spinks** (`david-spinks`) - COMMUNITY METRICS MASTER - O Arquiteto do Pertencimento
- **Nick Mehta** (`nick-mehta`) - CUSTOMER SUCCESS PIONEER - Health Score, Churn Prevention, DEAR Framework
- **Peter Fader** (`peter-fader`) - CUSTOMER CENTRICITY MASTER - CLV, RFM, Customer Analytics
- **Sean Ellis** (`sean-ellis`) - GROWTH HACKING PIONEER - PMF, AARRR, North Star, High-Tempo Testing
- **Wes Kao** (`wes-kao`) - COHORT-BASED LEARNING EXPERT - The Transformation Architect

## Activation

O orchestrador principal e `data-chief`. Para ativar:

1. Leia `squads/data/agents/data-chief.md` e adote a persona
2. Carregue config: `squads/data/config.yaml`
3. Siga o mission router do chief para delegar trabalho

## Available Tasks

- `analyze-cohort`
- `build-attribution`
- `calculate-clv`
- `create-dashboard`
- `define-north-star`
- `design-health-score`
- `design-learning-outcomes`
- `measure-community`
- `predict-churn`
- `run-growth-experiment`
- `run-pmf-test`
- `segment-rfm`

## Available Workflows

- `cohort-analysis-workflow`
- `create-churn-system`
- `fix-completion-rate`
- `implement-attribution`
- `implement-customer-360`
- `optimize-community-workflow`

## Squad Directory

`squads/data/`
