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
  aiox_advanced: 4
  aiox_advanced_squads: 0
  total: 4
  counted_at: '2026-08-10'
---
# Full SDC

Execução ponta a ponta de uma Story no SDC: validação, desenvolvimento, review/quality gate, deploy/verify e fechamento, em vez de rodar apenas um passo isolado.

## Como é usado

Use **Full SDC** quando a Story precisar atravessar o ciclo completo com o mesmo contrato, donos e evidências. Se o tempo apertar, corte escopo; não pule o gate ou o smoke mínimo.

**Exemplo prático:** no caso integrado da aula [[74-caso-integrado-end-to-end]], leve o fluxo form → resultado por Brief/PRD, Stories ready, build, QG, deploy com smoke e ROI/retro; arquive a evidência de cada etapa antes do close.

**Não confunda:** **Full SDC** não é só `/validate`, só desenvolvimento ou só deploy. É a passagem completa da Story pelos gates; deploy pode ter dono próprio, mas verify e close ainda precisam de evidência.

**Frequência nos cursos:** **4** menções (AIOX Advanced: 4 · AIOX Advanced Squads: 0).

## Aulas

- [[47-ciclo-de-vida-do-story]]
- [[74-caso-integrado-end-to-end]]

## Ver também

- [[SDC]]
- [[Ciclo do Story]]
- [[Glossário AIOX Advanced]]
