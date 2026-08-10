---
name: domain-decoder
description: |
  Extrai regras de negócio e taxonomias de brownfield. Alias conceitual: decoder-chief.
  Porta de entrada do squad `domain-decoder`. Preferir o router `aiox-squads` se a intenção for ambígua.
---

# domain-decoder


## Quando usar

- Use esta skill como **porta de entrada** do squad `domain-decoder` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/domain-decoder/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/04-domain-decoder.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


## Squad

`squads/domain-decoder/` · entry agent: `decoder-chief`

## Aula do curso

`cursos/AIOX-Advanced-Squads/aulas/04-domain-decoder.md`

## Router

Se a missão for escolha entre vários squads, use a skill `aiox-squads` e o manifesto em `skills/aiox-squads/references/`.

## Activation

1. Leia `squads/domain-decoder/agents/decoder-chief.md` e `config.yaml`
2. Se o squad não estiver no projeto ativo: `cp -R squads/domain-decoder <projeto>/squads/`
3. Siga o briefing da aula; não invente comandos de runtime
4. Guia agent-readable: `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md`
