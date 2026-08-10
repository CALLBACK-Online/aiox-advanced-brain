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

Use **Migration** para toda mudança de schema ou policy: um arquivo versionado no repositório, revisável em PR e repetível entre ambientes (local → staging → production), com plano de rollback pensado antes de aplicar.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], criar uma nova entidade passa pelo @data-engineer como schema + RLS + migration num arquivo versionado; mudança em produção exige migration + plano de rollback + janela — nunca "SQL herói" direto no dashboard.

**Não confunda:** migration não é ALTER TABLE rodado à mão no dashboard: tabela criada "no calor do PR" sem migration file é o anti-padrão que a aula lista. Se a mudança não está num arquivo reproduzível no repo, ela não existe para o processo.

**Frequência nos cursos:** **66** menções (AIOX Advanced: 59 · AIOX Advanced Squads: 7).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[24-entidade-como-unidade-de-processo]]

## Ver também

- [[Supabase]]
- [[RLS]]
- [[Entidade]]
- [[Glossário AIOX Advanced]]
