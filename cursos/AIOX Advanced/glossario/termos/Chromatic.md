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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# Chromatic

Regressão visual e review de UI sobre Storybook. Gate visual: detecta drift de pixels/composição antes do merge.

## Como é usado

Use **Chromatic** como gate visual sobre o Storybook: cada push publica snapshots das Stories e o serviço compara pixel a pixel com a baseline aprovada, listando os diffs para aceite ou rejeição antes do merge.

**Exemplo prático:** na aula [[56-tailwind-shadcn-storybook]], uma mudança no padding do `Button` faz o **Chromatic** marcar todas as Stories que usam o componente com diff visual; o revisor aprova o que foi intencional e rejeita o drift que ninguém pediu.

**Não confunda:** **Chromatic** não substitui teste funcional: ele detecta mudança visual (pixels e composição), não valida comportamento — e sem uma baseline revisada o diff não significa nada.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[56-tailwind-shadcn-storybook]]
- [[57-storybook-para-variantes]]

## Ver também

- [[Storybook]]
- [[Design Ops]]
- [[Gate]]
- [[Addon sem gate]]
- [[Glossário AIOX Advanced]]
