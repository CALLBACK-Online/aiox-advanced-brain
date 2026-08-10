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
  aiox_advanced: 11
  aiox_advanced_squads: 0
  total: 11
  counted_at: '2026-08-10'
---
# atomic-design-taxonomy

A regra do AIOX, no squad design-ops, que governa a classificação dos componentes por nível atômico no repositório.

## Como é usado

Aplique **atomic-design-taxonomy** ao criar ou revisar componentes: a regra define em qual nível atômico (atom, molecule, organism) cada componente se encaixa, onde ele vive no repositório e o que ele pode importar.

**Exemplo prático:** na aula [[42-design-atomico-brad-frost]], um `SearchBar` composto por `Input` + `Button` é classificado como molecule: a regra determina a pasta, a Story correspondente e acusa a violação se um atom tentar importar um organism.

**Não confunda:** **atomic-design-taxonomy** não é nomenclatura decorativa: a classificação define as dependências permitidas e é verificada em gate — componente no nível errado é finding, não detalhe.

**Frequência nos cursos:** **11** menções (AIOX Advanced: 11 · AIOX Advanced Squads: 0).

## Aulas

- [[42-design-atomico-brad-frost]]

## Ver também

- [[Glossário AIOX Advanced]]
