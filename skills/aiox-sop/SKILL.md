---
name: aiox-sop
description: |
  Cria e otimiza SOPs para humanos e agentes.
  Porta de entrada do squad `aiox-sop`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# aiox-sop

## Squad

`squads/aiox-sop/` · entry agent: `sop-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/07-aiox-sop.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/aiox-sop/agents/sop-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/aiox-sop <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
