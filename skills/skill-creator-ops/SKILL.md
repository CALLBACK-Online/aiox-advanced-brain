---
name: skill-creator-ops
description: |
  Ciclo de vida de skills (criar, validar, aposentar).
  Porta de entrada do squad `skill-creator-ops`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# skill-creator-ops


## Quando usar

- Use esta skill como **porta de entrada** do squad `skill-creator-ops` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/skill-creator-ops/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/22-skill-creator-ops.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


## Squad

`squads/skill-creator-ops/` · entry agent: `skill-ops-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/22-skill-creator-ops.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/skill-creator-ops/agents/skill-ops-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/skill-creator-ops <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
