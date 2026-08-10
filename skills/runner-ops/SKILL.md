---
name: runner-ops
description: |
  Runners headless e governança de execução determinística.
  Porta de entrada do squad `runner-ops`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# runner-ops


## Quando usar

- Use esta skill como **porta de entrada** do squad `runner-ops` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/runner-ops/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/09-runner-ops.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


## Squad

`squads/runner-ops/` · entry agent: `runner-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/09-runner-ops.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/runner-ops/agents/runner-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/runner-ops <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
