# DB-Sage Squad — Architecture

## Overview

O squad `db-sage` é o expert agent de PostgreSQL e Supabase: governa schema design, migrations, RLS policies, performance tuning e operações de banco. Exclusivamente responsável por mudanças estruturais e operacionais no database (delegado pelos demais squads).

## Agent Hierarchy

Single-agent squad especializado em profundidade, não em largura:

```
db-sage (Architect + Operator)
├── Schema design & migrations
├── RLS policies & security
├── Performance tuning (indexes, pooling, vacuum)
├── Query optimization & EXPLAIN analysis
└── Best practices enforcement (30 Supabase Agent Skills)
```

## Execution Flow

```
Squad consumidor identifica necessidade de DB change
                              ↓
           Proposta via handoff → @db-sage
                              ↓
                 db-sage executa em staging
                              ↓
                 Dry-run + validation passed
                              ↓
            Handoff para @devops (production exec)
                              ↓
                 @devops aplica em produção
```

## Capabilities

| Categoria | Tasks |
|-----------|-------|
| Schema operations | Design, migrations, constraint validation, schema differ |
| Security | RLS audit, permission audit, security scanner |
| Performance | Vacuum optimizer, explain analyzer, slow query detection |
| Best practices | `*db-best-practices-audit` (30 rules), schema audit |
| Squad integration | `*db-squad-integration` (preflight + baseline) |
| Backup & recovery | Backup manager with metadata hash |

## Connection Patterns (Supabase)

| Port | Use Case | Mode |
|------|----------|------|
| 5432 | Edge Functions | Direct |
| 5432 | Migrations | Direct |
| 5432 | Prepared statements | Session |
| 6543 | Edge Functions, Serverless | Transaction (Supavisor) |
| 6543 | Persistent servers | Transaction (Supavisor) |

## Pool Sizing Rules

- Com PostgREST active: ≤40% of max_connections
- Sem PostgREST: até 80%
- Sempre reservar 20% para Auth, Realtime, internal services

## Outputs Location

| Tipo | Local |
|------|-------|
| Migrations | `supabase/migrations/` |
| Schema docs | `supabase/docs/` |
| Seed data | `supabase/seed.sql` |
| Active RLS policies | Supabase database (production) |
| Audit reports | Generated on demand via `*schema-audit` |

## Infrastructure Map

```yaml
postgresql_connection:
  service_ref: postgresql-primary
  connection: "$SUPABASE_DB_URL or $DATABASE_URL"
  integration: "Primary database connection for all operations"
  type: external-database
```

## Delegation Protocol

| Squad Request | db-sage Response |
|---------------|------------------|
| @dev proposes schema change | db-sage reviews, drafts migration, tests in staging |
| @dev needs query optimization | db-sage runs EXPLAIN, recommends indexes |
| @architect plans new feature | db-sage advises on data model |
| @devops executes production | db-sage hands off validated migration |

## Boundary

- **In scope:** All DB structural/operational work, migrations, RLS, performance, Supabase platform
- **Exclusive authority:** Schema changes, migration design, RLS policies
- **Out of scope:** Application code accessing DB (@dev), production migration execution (@devops — db-sage proposes)

## Tasks Canônicas (25 total)

Incluindo: schema-audit, db-best-practices-audit, db-squad-integration, RLS design patterns, migration safety guide, postgres tuning guide, pipeline execution log, deviation registry.
