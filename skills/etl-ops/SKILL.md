---
name: etl-ops
description: |
  Pipelines ETL e collectors repetíveis.
  Porta de entrada do squad `etl-ops`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# etl-ops

## Squad

`squads/etl-ops/` · entry agent: `etl-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/08-etl-ops.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/etl-ops/agents/etl-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/etl-ops <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
