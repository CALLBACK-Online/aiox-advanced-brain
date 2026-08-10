---
name: squad-creator
description: |
  Cria squads canônicos. Skill irmã: squad-chief.
  Porta de entrada do squad `squad-creator`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# squad-creator

## Squad

`squads/squad-creator/` · entry agent: `squad-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/23-squad-creator.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/squad-creator/agents/squad-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/squad-creator <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
