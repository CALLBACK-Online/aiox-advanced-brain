---
name: skill-creator-ops
description: |
  Ciclo de vida de skills (criar, validar, aposentar).
  Porta de entrada do squad `skill-creator-ops`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# skill-creator-ops

## Squad

`squads/skill-creator-ops/` · entry agent: `skill-ops-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/22-skill-creator-ops.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/skill-creator-ops/agents/skill-ops-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/skill-creator-ops <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
