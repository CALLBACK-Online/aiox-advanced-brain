# Task: Migration Dry-Run

| Field | Value |
|-------|-------|
| **responsavel_type** | `Worker` |
| **atomic_layer** | `Atom` |
| **domain** | `Tactical` |
| **pattern** | EXEC-W-001 |
| **script** | `scripts/db-ops/migration-runner.sh` |
| **rationale** | BEGIN/ROLLBACK é operação determinística do PostgreSQL |

**Purpose**: Execute migration inside BEGIN…ROLLBACK to catch syntax/ordering errors

**Elicit**: true

---

## 🚀 NEW: Use Automated Migration Safe Runner (RECOMMENDED)

**Token Savings: 91% | Time Savings: ~88%**

```bash
# Dry-run migration with automatic error detection
./squads/db-sage/scripts/db-ops/migration-runner.sh {path} --dry-run

# Dry-run after deterministic order verification
./squads/db-sage/scripts/db-ops/migration-runner.sh {path} --verify-order
./squads/db-sage/scripts/db-ops/migration-runner.sh {path} --dry-run

# Benefits:
#   - Automatic syntax validation
#   - Dependency order checking
#   - Pre/post snapshot comparison
#   - Rollback script validation
#   - 91% token savings
```

**OR continue with manual dry-run below:**

---

## Inputs

- `path` (string): Path to SQL migration file

---

## Outputs

- **dry-run verdict**: PASS / FAIL flag printed to console (SQL syntax, dependencies, ordering)
- **error report** (on failure): captured error message, line number, and offending object
- **rollback proof**: transaction `ROLLBACK`-ed — no schema or data change persisted (verifiable via `pg_dump --schema-only` diff = empty)
- **next-step prompt**: console suggestion to run `*snapshot pre_migration` + `*apply-migration {path}` when PASS
- **exit code**: `0` on success; non-zero with error context on failure

---


## Pre-conditions

- Database connection established (validated by db-env-check)

## Process

### 1. Confirm Migration File

Ask user to confirm:
- Migration file path: `{path}`
- Purpose of this migration
- Expected changes (tables, functions, etc)

### 2. Execute Dry-Run

Run migration in transaction that will be rolled back:

```bash
psql "$SUPABASE_DB_URL" -v ON_ERROR_STOP=1 <<'SQL'
BEGIN;
\echo 'Starting dry-run...'
\i {path}
\echo 'Dry-run completed successfully - rolling back...'
ROLLBACK;
SQL
```

### 3. Report Results

**If successful:**
```
✓ Dry-run completed without errors
✓ Migration syntax is valid
✓ No dependency or ordering issues detected
```

**If failed:**
```
❌ Dry-run failed
Error: [error message]
Line: [line number if available]
Fix the migration and try again
```

---

## What This Validates

- ✅ SQL syntax correctness
- ✅ Object dependencies exist
- ✅ Execution order is valid
- ✅ No constraint violations
- ❌ Does NOT validate data correctness
- ❌ Does NOT check performance

---

## Next Steps After Success

1. Review migration one more time
2. Take snapshot: `*snapshot pre_migration`
3. Apply migration: `*apply-migration {path}`
4. Run smoke tests: `*smoke-test`

---

## Error Handling

Common errors and fixes:

**"relation does not exist"**
- Missing table/view dependency
- Check if you need to create dependent objects first

**"function does not exist"**
- Function called before creation
- Reorder: tables → functions → triggers

**"syntax error"**
- Check SQL syntax
- Verify PostgreSQL version compatibility

## Post-conditions

After successful execution:
- Migration SQL at `{path}` executed inside `BEGIN…ROLLBACK` with `ON_ERROR_STOP=1`
- Transaction rolled back — no schema or data change persisted in the target database
- Syntax, ordering, and dependency validity confirmed (or precise error captured with line/object)

Acceptance Criteria:
- [ ] Final database state matches the pre-execution state (verifiable via `pg_dump --schema-only` diff = empty)
- [ ] On success, output explicitly states "Dry-run completed without errors"; on failure, output identifies the failing SQL object or line number
- [ ] No partially-committed transaction remains open (verified by `SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction'`)
