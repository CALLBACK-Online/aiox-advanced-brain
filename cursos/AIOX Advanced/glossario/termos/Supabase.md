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
  aiox_advanced_squads: 4
  total: 54
  counted_at: '2026-08-10'
---
# Supabase

Plataforma gerenciada sobre Postgres que oferece banco, APIs, autenticação, storage e Row Level Security (RLS). No curso, serve como camada de dados quando schema, migrations e políticas de acesso precisam ser verificáveis.

## Como é usado

Use **Supabase** para persistir dados e controlar acesso no backend da aplicação. Modele o schema, aplique migrations, defina a RLS por tabela e teste tanto o acesso permitido quanto o negado antes de integrar a UI.

**Exemplo prático:** numa tabela `tasks`, crie a migration, associe cada linha ao usuário autenticado e escreva uma política RLS que permita ler apenas as próprias tarefas; valide com um usuário autorizado e outro sem acesso.

**Não confunda:** **Supabase** não é apenas um Postgres sem configuração e não torna os dados seguros automaticamente. Auth, RLS, migrations e regras de negócio precisam ser definidos, testados e operados pelo projeto.

**Frequência nos cursos:** **54** menções (AIOX Advanced: 50 · AIOX Advanced Squads: 4).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[73-prontidao-de-producao]]

## Ver também

- [[RLS]]
- [[Migration]]
- [[Deploy]]
- [[Glossário AIOX Advanced]]
