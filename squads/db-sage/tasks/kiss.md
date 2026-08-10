# Task: KISS Gate Analysis

| Field | Value |
|-------|-------|
| **responsavel_type** | `Agent` |
| **atomic_layer** | `Atom` |
| **domain** | `Strategic` |
| **pattern** | EXEC-A-001 |
| **rationale** | Worker coleta sinais e red flags; humano decide a opcao final de schema/integracao |

Executa o workflow `kiss-gate-workflow.yaml` de forma automática, sem pedir inputs ao usuário.

## Inputs

- `context` (string, optional): PRD file path, free-text description of the feature/entity, or empty (agent extracts from current conversation)
- `keyword` (string, optional): Override keyword used for schema similarity queries; inferred from `context` if not provided

## Outputs

- **inferred workflow fields**: `what_storing`, `how_many`, `how_often`, `who_access`, `need_joins` populated with rationale (and flagged when assumed)
- **similar-tables list**: tables matching `{keyword}` with column counts, row counts, and related FKs (or explicit "no similar tables")
- **red-flag count**: tally of REUSE/EXTEND/CREATE/RECONSIDER red flags with descriptions
- **recommendation verdict**: classification as `REUSE` / `EXTEND` / `CREATE` / `RECONSIDER` plus three options (recommended + two alternatives)
- **user decision**: captured option (1, 2, or 3) recorded for downstream task handoff


## Pre-conditions

- Database connection established (validated by db-env-check)

## Execution

### STEP 1: Capturar Contexto

```
Se {context} é path de arquivo → ler arquivo
Se {context} é texto → usar diretamente
Se vazio → extrair da conversa atual
```

### STEP 2: Análise Automática do Schema

Executar queries para descobrir o que já existe:

```sql
-- Tabelas com nomes similares ao contexto
SELECT table_name,
       (SELECT COUNT(*) FROM information_schema.columns c
        WHERE c.table_name = t.table_name) as cols
FROM information_schema.tables t
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
  AND table_name ILIKE '%{keyword}%';

-- Row counts das tabelas candidatas
SELECT schemaname || '.' || relname as table_name, n_live_tup as rows
FROM pg_stat_user_tables
WHERE relname ILIKE '%{keyword}%'
ORDER BY n_live_tup DESC;

-- FKs relacionadas
SELECT tc.table_name, ccu.table_name as references_table
FROM information_schema.table_constraints tc
JOIN information_schema.constraint_column_usage ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND (tc.table_name ILIKE '%{keyword}%' OR ccu.table_name ILIKE '%{keyword}%');
```

### STEP 3: Preencher Campos do Workflow Automaticamente

Inferir valores para os campos do `kiss-gate-workflow.yaml`:

| Campo | Como Inferir |
|-------|--------------|
| `what_storing` | Extrair do contexto/PRD (entidade principal) |
| `how_many` | Estimar: "poucos/alguns" → 50, "milhares" → 10000, sem menção → 1000 |
| `how_often` | Inferir: "logs/eventos" → frequente, "config" → raramente |
| `who_access` | Detectar: multi-tenant → "multiple users", single app → "application" |
| `need_joins` | Analisar: menciona relacionamentos/FKs → true, dados isolados → false |

### STEP 4: Executar Lógica de Red Flags

Aplicar regras do workflow:

```
RED_FLAGS = 0

Se how_many < 100:
  → 🚩 "Poucos registros (<100) - considerar JSON/YAML"
  → RED_FLAGS++

Se who_access contém "just me" ou "single":
  → 🚩 "Usuário único - considerar SQLite local"
  → RED_FLAGS++

Se need_joins == false:
  → 🚩 "Sem relacionamentos - reconsiderar necessidade de DB"
  → RED_FLAGS++

Se tabela similar encontrada no STEP 2:
  → 🚩 "Tabela similar existe: {table_name} ({rows} rows)"
  → RED_FLAGS++
```

### STEP 5: Apresentar Diagnóstico

```markdown
## 🔍 KISS Analysis

**Contexto:** {resumo em 1 linha}

**Valores inferidos:**
- Armazenando: {what_storing}
- Volume estimado: {how_many} registros
- Frequência de mudança: {how_often}
- Acesso: {who_access}
- Relacionamentos: {need_joins ? "Sim" : "Não"}

**Schema existente relevante:**
{lista de tabelas similares encontradas ou "Nenhuma tabela similar"}

**Red Flags:** {RED_FLAGS}
{lista de red flags ou "✅ Nenhum"}

---

### Recomendação: {REUSE|EXTEND|CREATE|RECONSIDER}

{explicação em 1-2 frases}

### Opções

1. **{opção recomendada}** - {descrição}
2. **{alternativa}** - {descrição}
3. **{outra alternativa}** - {descrição}
```

### STEP 6: Aguardar Decisão

Usuário escolhe 1, 2 ou 3.

## Error Handling

| Condition | Action |
|-----------|--------|
| `context` is empty and no active conversation context is available | Prompt user to provide a PRD path or feature description before continuing |
| Database queries in STEP 2 fail (no DB connection) | Skip schema discovery, set `existing_tables = []`, flag in diagnostics as "schema check skipped — no DB connection" |
| SQL query returns no results for keyword | Treat as "no similar tables found"; proceed without red flag for existing tables |
| `how_many` / `how_often` / `who_access` cannot be inferred from context | Use safe defaults (1000 records, unknown frequency, multi-user) and flag assumptions explicitly in the output |
| User does not select option 1, 2, or 3 in STEP 6 | Re-present the three options and wait for valid input |

## Post-conditions

After successful execution:
- Existing schema scanned for tables matching `{keyword}` and reused candidates surfaced
- Workflow fields (`what_storing`, `how_many`, `how_often`, `who_access`, `need_joins`) populated with inferred values + flagged assumptions
- Red-flag count computed and recommendation classified as REUSE / EXTEND / CREATE / RECONSIDER
- User decision captured (option 1, 2, or 3) and recorded for downstream tasks

Acceptance Criteria:
- [ ] Output report lists all similar tables found (or explicit "no similar tables found")
- [ ] Recommendation includes the recommended option plus at least two alternatives
- [ ] User decision is captured before the task terminates (no silent exit)

## Principle

> "Workflow executa, agente preenche, usuário decide"
