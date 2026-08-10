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
  aiox_advanced: 56
  aiox_advanced_squads: 1
  total: 57
  counted_at: '2026-08-10'
---
# SDC

Story Development Cycle: ciclo controlado da Story — `draft → ready → in progress → in review → done` — com validação, donos de transição, quality gates e evidência; deploy/verify pode seguir em trilho próprio.

## Como é usado

Use **SDC** para acompanhar o estado real de uma Story, o dono da próxima seta, o critério de passagem e a evidência. Valide `draft → ready` antes de codar e trate FAIL como `fix → re-gate`, não como aprovação por feeling.

**Exemplo prático:** na aula [[47-ciclo-de-vida-do-story]], pegue uma Story em Draft, escreva o aceite, faça o PO validar para Ready, passe ao Dev, leve o PR ao QG e feche em Done somente com a evidência; registre deploy separadamente se houver.

**Não confunda:** **SDC** não é só um quadro Kanban nem o nome de uma única revisão. É o método que conecta estados, autoridade, gates e prova; **Full SDC** é a execução ponta a ponta desse ciclo.

**Frequência nos cursos:** **57** menções (AIOX Advanced: 56 · AIOX Advanced Squads: 1).

## Aulas

- [[47-ciclo-de-vida-do-story]]
- [[10-processo-ciclo-do-story]]
- [[46-etapas-de-desenvolvimento]]

## Ver também

- [[Ciclo do Story]]
- [[Story]]
- [[Quality Gate]]
- [[Story Development Cycle]]
- [[Glossário AIOX Advanced]]
