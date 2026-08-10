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
  aiox_advanced: 84
  aiox_advanced_squads: 2
  total: 86
  counted_at: '2026-08-10'
---
# CREATE

Último degrau da heurística: criar uma peça nova somente depois de provar que **REUSE** e **ADAPT** não cobrem o caso. Exige gap real, escopo mínimo e dono de manutenção.

## Como é usado

Use **CREATE** quando a busca por soluções existentes estiver documentada, o gap continuar relevante e a equipe aceitar o custo de manter uma nova peça. Registre a decisão antes de começar a implementação.

**Exemplo prático:** nenhum componente existente atende a uma regra regulatória específica; anexe as buscas e rejeições ao PR, crie apenas o componente mínimo para essa regra e nomeie quem manterá suas versões e testes.

**Não confunda:** **CREATE** não é “fazer do meu jeito” nem uma reescrita motivada por gosto. Criar sem prova de busca é **NIH**; adaptar uma peça até perder seu núcleo também é CREATE disfarçado.

**Frequência nos cursos:** **86** menções (AIOX Advanced: 84 · AIOX Advanced Squads: 2).

## Aulas

- [[54-reuse-adapt-create-heuristica]]

## Ver também

- [[REUSE]]
- [[ADAPT]]
- [[Glossário AIOX Advanced]]
