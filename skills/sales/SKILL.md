---
name: sales
description: |
  Sales Squad — diagnóstico, qualificação, prospecção, negociação, fechamento e escala comercial.
  Use quando a missão envolve o funil de vendas completo, e não apenas uma peça de copy.
---

# Sales Squad


## Quando usar

- Use esta skill como **porta de entrada** do squad `sales` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/sales/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/20-sales.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


Squad com **9 agentes** especializados.

> **Maturidade neste acervo:** `study` — ver `docs/runtime-dependencies.md`.
> Fonte canônica de materiais: `../upstream-monorepo` (quando sincronizado).

## Agents

- **aaron-ross** (`aaron-ross`)
- **challenger-sale** (`challenger-sale`)
- **chet-holmes** (`chet-holmes`)
- **chris-voss** (`chris-voss`)
- **david-sandler** (`david-sandler`)
- **jeb-blount** (`jeb-blount`)
- **Keenan - Gap Selling Specialist** (`keenan`)
- **neil-rackham** (`neil-rackham`)
- **sales-chief** (`sales-chief`)

## Activation

O orchestrador principal é `sales-chief`. Para ativar:

1. Leia `squads/sales/agents/sales-chief.md` e adote a persona
2. Carregue config: `squads/sales/config.yaml`
3. Siga o mission router do chief para delegar trabalho

## Available Tasks

- `close-deal`
- `create-cold-outreach`
- `create-email-sequences`
- `create-followup-sequence`
- `create-sales-copy`
- `create-sales-scripts`
- `diagnose-deal`
- `negotiate-deal`
- `qualify-prospect`

## Available Workflows

- _(nenhum workflow yaml no pacote; use tasks e o chief)_

## Squad Directory

`squads/sales/`
