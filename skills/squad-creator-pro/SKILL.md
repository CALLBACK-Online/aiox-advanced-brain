---
name: squad-creator-pro
description: |
  Criação avançada de squads (DNA, gates). Use squad-creator se for scaffold simples.
  Porta de entrada do squad `squad-creator-pro`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# squad-creator-pro


## Quando usar

- Use esta skill como **porta de entrada** do squad `squad-creator-pro` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/squad-creator-pro/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


## Squad

`squads/squad-creator-pro/` · entry agent: `squad-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/squad-creator-pro/agents/squad-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/squad-creator-pro <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
