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
  aiox_advanced: 33
  aiox_advanced_squads: 0
  total: 33
  counted_at: '2026-08-10'
---
# agents/

A pasta dos especialistas que pensam e decidem dentro do domínio. Cada agent interpreta o contexto e dispara tasks; a transformação concreta fica em **tasks/**.

## Como é usado

Use **agents/** para separar julgamento de execução: coloque ali o papel, os critérios e a decisão de rota do especialista, deixando passos transformadores nas tasks e conhecimento reutilizável em data/.

**Exemplo prático:** em um squad de dados, um agent decide se o pedido exige modelagem ou validação; depois dispara a task correspondente, que recebe a entrada e devolve o artefato. O agent não esconde SQL ou passos de execução dentro do próprio arquivo.

**Não confunda:** **agents/** não é sinônimo de **tasks/** nem de **workflows/**. Agents julgam, tasks transformam estados e workflows ordenam as tasks; misturar esses papéis torna o squad difícil de auditar.

**Frequência nos cursos:** **33** menções (AIOX Advanced: 33 · AIOX Advanced Squads: 0).

## Aulas

- [[33-anatomia-de-um-squad]]

## Ver também

- [[Glossário AIOX Advanced]]
