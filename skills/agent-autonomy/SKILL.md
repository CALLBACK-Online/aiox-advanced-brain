---
name: agent-autonomy
description: |
  Audita e eleva autonomia de agentes (loops, ownership, scoring).
  Porta de entrada do squad `agent-autonomy`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# agent-autonomy

## Squad

`squads/agent-autonomy/` · entry agent: `autonomy-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/05-agent-autonomy.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/agent-autonomy/agents/autonomy-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/agent-autonomy <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
