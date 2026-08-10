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
  aiox_advanced: 16
  aiox_advanced_squads: 1
  total: 17
  counted_at: '2026-08-10'
---
# Aceite testável

Critério de done que dá pra provar sem 'acho que tá bom'.

## Como é usado

Escreva o **Aceite testável** na própria Story, antes de implementar: cada critério deve poder ser verificado por um teste, um comando ou uma observação binária — passa ou não passa, sem depender de opinião.

**Exemplo prático:** na aula [[46-etapas-de-desenvolvimento]], em vez de "o login deve funcionar bem", o critério vira "POST /login com credenciais válidas retorna 200 e cria sessão; com senha errada retorna 401" — qualquer pessoa consegue executar e conferir.

**Não confunda:** não use **Aceite testável** como justificativa posterior: o critério nasce junto com a Story e é ele que autoriza o Done — não uma sensação de "acho que tá bom" depois da entrega.

**Frequência nos cursos:** **17** menções (AIOX Advanced: 16 · AIOX Advanced Squads: 1).

## Aulas

- [[46-etapas-de-desenvolvimento]]

## Ver também

- [[Glossário AIOX Advanced]]
