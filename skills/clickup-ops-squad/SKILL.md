---
name: clickup-ops-squad
description: |
  Materializa processos validados no ClickUp.
  Porta de entrada do squad `clickup-ops-squad`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# clickup-ops-squad

## Squad

`squads/clickup-ops-squad/` · entry agent: `clickup-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/clickup-ops-squad/agents/clickup-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/clickup-ops-squad <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
