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
  aiox_advanced: 59
  aiox_advanced_squads: 7
  total: 66
  counted_at: '2026-08-10'
---
# Migration

Mudança versionada de schema de banco. No AIOX, migration é artefato revisável com rollback mental — não ALTER solto em production.

## Como é usado

Use **Migration** ao modelar, alterar ou verificar a parte de dados/infra descrita na definição, sempre com ambiente e risco explícitos.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], aplique **Migration** a um caso de dados, execute a verificação em staging e registre contagem, política, log ou migration como evidência.

**Não confunda:** não confunda **Migration** com uma alteração manual sem rastreio: a mudança precisa ser reproduzível e revisável.

**Frequência nos cursos:** **66** menções (AIOX Advanced: 59 · AIOX Advanced Squads: 7).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[24-entidade-como-unidade-de-processo]]

## Ver também

- [[Supabase]]
- [[RLS]]
- [[Entidade]]
- [[Glossário AIOX Advanced]]
