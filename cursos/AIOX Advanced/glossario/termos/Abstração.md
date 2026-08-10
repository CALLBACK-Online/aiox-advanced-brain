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
  aiox_advanced: 34
  aiox_advanced_squads: 0
  total: 34
  counted_at: '2026-08-10'
---
# Abstração

O espaço em branco que a IA preenche sozinha quando falta critério externo.

## Como é usado

No AIOX, **Abstração** nomeia o inimigo do determinismo progressivo: toda lacuna de prompt, spec ou gate que a LLM preenche "do jeito dela". O trabalho do operador é fechar esses espaços com critério externo — spec, exemplo, rubrica, gate — antes de delegar.

**Exemplo prático:** na aula [[09-conceito-determinismo-progressivo]], os níveis de confiança 30/60/90 medem quanta abstração já foi removida: 30% é rascunho útil para iterar, 90% é artefato travado para publicar. Cada gate (QA, CodeRabbit, review) remove uma camada de abstração antes do PR.

**Não confunda:** aqui abstração não é o conceito positivo de engenharia de software (esconder detalhes atrás de uma interface): é o espaço em branco sem critério que deixa a IA decidir sozinha o que deveria ter sido especificado.

**Frequência nos cursos:** **34** menções (AIOX Advanced: 34 · AIOX Advanced Squads: 0).

## Aulas

- [[09-conceito-determinismo-progressivo]]

## Ver também

- [[Glossário AIOX Advanced]]
