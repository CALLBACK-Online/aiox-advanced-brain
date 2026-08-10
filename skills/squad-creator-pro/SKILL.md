---
name: squad-creator-pro
description: |
  Criação avançada de squads (DNA, gates). Use squad-creator se for scaffold simples.
  Porta de entrada do squad `squad-creator-pro`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# squad-creator-pro

## Squad

`squads/squad-creator-pro/` · entry agent: `squad-chief`

## Aula do curso

`Cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/squad-creator-pro/agents/squad-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/squad-creator-pro <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `Cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
