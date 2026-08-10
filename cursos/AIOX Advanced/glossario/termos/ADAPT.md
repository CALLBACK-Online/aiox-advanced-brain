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
  aiox_advanced: 50
  aiox_advanced_squads: 1
  total: 51
  counted_at: '2026-08-10'
---
# ADAPT

Extensão ou fork mínimo de algo que quase atende ao caso, preservando a origem reconhecível e mantendo pequeno o delta de manutenção.

## Como é usado

Use **ADAPT** depois de procurar uma solução reutilizável e constatar que ela cobre a maior parte do caso. Delimite o delta: um parâmetro, wrapper, variante ou agente adicional — não uma reescrita.

**Exemplo prático:** um logger existente atende a aplicação, mas falta uma opção de correlação; adicione esse parâmetro e mantenha o logger original como base, registrando a origem e o delta.

**Não confunda:** **ADAPT** não é reescrever uma solução inteira com outro nome. Se o fork deixa de preservar o núcleo ou explode a superfície de manutenção, a decisão é **CREATE** — ou a busca por **REUSE** ainda não terminou.

**Frequência nos cursos:** **51** menções (AIOX Advanced: 50 · AIOX Advanced Squads: 1).

## Aulas

- [[54-reuse-adapt-create-heuristica]]

## Ver também

- [[Glossário AIOX Advanced]]
