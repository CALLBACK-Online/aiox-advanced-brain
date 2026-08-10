# DB-Sage Squad — Production Examples

Outputs do squad `db-sage` são migrations SQL, RLS policies e schema artifacts que vivem em bancos reais (Supabase) e em `supabase/` no repo.

## Onde os outputs reais vivem

| Tipo | Localização |
|---|---|
| Migrations | `supabase/migrations/` |
| Schema docs | `supabase/docs/` |
| Seed data | `supabase/seed.sql` |
| RLS policies (ativas) | Supabase database (production) |
| Schema audit reports | Gerados sob demanda via `*schema-audit` |

## Evidência de uso

- Pipeline Supabase integrado (ver `supabase/` no root)
- Migrations versionadas commitadas
- `*db-best-practices-audit` e `*schema-audit` executados em ciclos de review

## Tasks canônicas

- `tasks/schema-audit.md` — auditoria contra 30 Supabase Agent Skills rules
- `tasks/db-best-practices-audit.md` — best practices check
- `tasks/db-squad-integration.md` — integração com squads consumidores

## Provenance

Outputs estruturais vivem no Supabase (instância produção), não no filesystem do squad. Reports pontuais são gerados sob demanda e arquivados fora do repo por conterem dados sensíveis.
