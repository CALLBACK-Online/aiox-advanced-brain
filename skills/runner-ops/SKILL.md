---
name: runner-ops
description: |
  Runners headless e governança de execução determinística.
  Porta de entrada do squad `runner-ops`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# runner-ops

## Squad

`squads/runner-ops/` · entry agent: `runner-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/09-runner-ops.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/runner-ops/agents/runner-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/runner-ops <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
