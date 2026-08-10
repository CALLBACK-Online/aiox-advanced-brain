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
  aiox_advanced: 155
  aiox_advanced_squads: 0
  total: 155
  counted_at: '2026-08-10'
---
# Greenfield

Projeto ou fatia que começa do zero, sem código herdado nem decisões antigas para decifrar. Mesmo em greenfield, ainda valem contrato, gates e a busca por REUSE antes de criar.

## Como é usado

Use **Greenfield** quando não houver estrutura viva herdada na área que será construída. Defina a arquitetura e o contrato diretamente, mas confirme primeiro se já existe uma peça reutilizável no ecossistema.

**Exemplo prático:** um produto novo ainda não tem módulo de billing; desenhe o contrato das cobranças, crie a primeira implementação com testes e passe-a pelo gate, sem precisar decifrar um módulo legado inexistente.

**Não confunda:** uma feature nova dentro de um repositório antigo pode ser **Greenfield** só naquela fatia, enquanto o projeto continua **Brownfield**. Greenfield descreve a ausência de legado na área, não o fato de a tela ser visualmente nova.

**Frequência nos cursos:** **155** menções (AIOX Advanced: 155 · AIOX Advanced Squads: 0).

## Aulas

- [[32-design-system-greenfield-brownfield]]
- [[31-brownfield-discovery]]

## Ver também

- [[Brownfield Discovery]]
- [[Brownfield Enhancement]]
- [[REUSE]]
- [[ADAPT]]
- [[CREATE]]
- [[Glossário AIOX Advanced]]
