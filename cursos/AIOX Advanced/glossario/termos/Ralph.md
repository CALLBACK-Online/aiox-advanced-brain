---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 52
  aiox_advanced_squads: 0
  total: 52
  counted_at: '2026-08-10'
---
# Ralph

Padrão de orquestração multi-agente paralela com fila/estado, ownership particionado e workers de escopo fechado; só acelera quando o grafo permite.

## Como é usado

Use **Ralph** depois de decidir que vale paralelizar: materialize estado, divida paths sem overlap, despache workers e planeje o fan-in.

**Exemplo prático:** na aula [[58-ralph-paralelizacao]], separe quatro Stories em paths disjuntos, registre dono/status no board, execute o batch e faça fan-in com diff, ordem de merge e QG.

**Não confunda:** **Ralph** não é persona, agente extra ou paralelismo sem estado; é um padrão de batch com partição, capacidade e barreira de reintegração.

**Frequência nos cursos:** **52** menções (AIOX Advanced: 52 · AIOX Advanced Squads: 0).

## Aulas

- [[58-ralph-paralelizacao]]
- [[59-quando-paralelizar-vs-sequencial]]

## Ver também

- [[Wave Execute]]
- [[Paralelização]]
- [[Glossário AIOX Advanced]]
