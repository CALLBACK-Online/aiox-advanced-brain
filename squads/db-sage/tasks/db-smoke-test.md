# Task: DB Smoke Test

| Field | Value |
|-------|-------|
| **responsavel_type** | `Worker` |
| **atomic_layer** | `Atom` |
| **domain** | `Operational` |
| **pattern** | EXEC-W-001 |
| **script** | `scripts/db-ops/health-checker.sh` |
| **rationale** | Smoke tests são queries determinísticas de validação |

## Inputs

- `smoke_test_file` (string, optional): Explicit path to smoke test SQL file — if omitted, the task auto-discovers in order: `supabase/tests/smoke/v_current.sql`, `supabase/tests/smoke_test.sql`, `squads/db-sage/templates/migration.sql.tmpl`

**Purpose**: Run post-migration validation checks

**Elicit**: false

---

## Outputs

- **smoke-test verdict**: PASS / FAIL flag printed to console
- **resolved test file**: path to the SQL file that was actually executed (auto-discovered or explicit)
- **per-check results**: validation outcomes for table existence, RLS coverage, policy installation, function callability, and basic queries
- **failure context** (on FAIL): captured psql error message routed to console with remediation hints (rollback, re-apply, etc.)
- **exit code**: `0` on success, non-zero on failure or missing smoke-test file

---


## Pre-conditions

- Database connection established (validated by db-env-check)

## 🚀 NEW: Use Automated Health Checker (RECOMMENDED)

**Token Savings: 89% | Time Savings: ~85%**

```bash
# Run comprehensive smoke tests
./squads/db-sage/scripts/db-ops/health-checker.sh --smoke-test

# Smoke tests with verbose logging
./squads/db-sage/scripts/db-ops/health-checker.sh --smoke-test --verbose

# Benefits:
#   - Automatic table/view/function validation
#   - RLS policy verification
#   - Index integrity checks
#   - Foreign key validation
#   - 89% token savings
```

**OR continue with manual smoke test below:**

---

## Process

### 1. Locate Smoke Test File

Check for smoke test in this order:

1. `supabase/tests/smoke/v_current.sql` (project-specific)
2. `supabase/tests/smoke_test.sql` (project-specific)
3. `squads/db-sage/templates/migration.sql.tmpl` (template fallback)

### 2. Run Smoke Test

```bash
SMOKE_TEST=""
DB_URL="${SUPABASE_DB_URL:-${DATABASE_URL:-}}"
test -n "$DB_URL" || { echo "❌ Missing SUPABASE_DB_URL or DATABASE_URL"; exit 1; }

if [ -f "supabase/tests/smoke/v_current.sql" ]; then
  SMOKE_TEST="supabase/tests/smoke/v_current.sql"
elif [ -f "supabase/tests/smoke_test.sql" ]; then
  SMOKE_TEST="supabase/tests/smoke_test.sql"
elif [ -f "squads/db-sage/templates/migration.sql.tmpl" ]; then
  SMOKE_TEST="squads/db-sage/templates/migration.sql.tmpl"
else
  echo "❌ No smoke test file found"
  exit 1
fi

echo "Running smoke test: $SMOKE_TEST"
psql "$DB_URL" -v ON_ERROR_STOP=1 -f "$SMOKE_TEST"
```

### 3. Report Results

**If successful:**
```
✅ Smoke Test Passed

Checks completed:
  ✓ Table count validation
  ✓ Policy count validation
  ✓ Function existence checks
  ✓ Basic query sanity
```

**If failed:**
```
❌ Smoke Test Failed

Review errors above and:
  1. Check migration completeness
  2. Verify RLS policies installed
  3. Confirm functions created
  4. Consider rollback if critical
```

---

## What Is Tested

Basic smoke tests typically check:

### Schema Objects
- Expected tables exist
- Expected views exist
- Expected functions exist
- Expected triggers exist

### RLS Coverage
- RLS enabled on sensitive tables
- Policies exist and are named correctly
- Basic RLS queries don't error

### Data Integrity
- Foreign keys valid
- Check constraints valid
- Sample queries return expected results

### Performance
- Basic queries complete in reasonable time
- No missing indexes on FKs

---

## Creating Custom Smoke Tests

Create `supabase/tests/smoke/v_X_Y_Z.sql`:

```sql
-- Smoke Test for v1.2.0
SET client_min_messages = warning;

-- Table count
SELECT COUNT(*) AS tables FROM information_schema.tables 
WHERE table_schema='public';
-- Expected: 15

-- RLS enabled
SELECT tablename FROM pg_tables 
WHERE schemaname='public' AND rowsecurity = false;
-- Expected: empty (all tables have RLS)

-- Critical functions exist
SELECT proname FROM pg_proc 
WHERE pronamespace = 'public'::regnamespace
AND proname IN ('function1', 'function2');
-- Expected: 2 rows

-- Sample data query
SELECT COUNT(*) FROM users WHERE deleted_at IS NULL;
-- Expected: > 0

-- RLS sanity (doesn't error)
SET LOCAL request.jwt.claims = '{"sub":"00000000-0000-0000-0000-000000000000","role":"authenticated"}';
SELECT 1 FROM protected_table LIMIT 1;
```

---

## Best Practices

1. **Version-specific tests** - Name by schema version
2. **Fast execution** - Under 5 seconds
3. **No side effects** - Read-only queries
4. **Clear expectations** - Document expected results
5. **Fail fast** - Use ON_ERROR_STOP

---

## Next Steps After Pass

✓ Migration validated  
→ Update migration log  
→ Run RLS audit: `*rls-audit`  
→ Check performance: `*analyze-hotpaths`

## Next Steps After Fail

❌ Migration issues detected  
→ Review errors  
→ Consider rollback: `*rollback {snapshot}`  
→ Fix migration  
→ Retry

## Error Handling

| Condition | Action |
|-----------|--------|
| `SUPABASE_DB_URL` and `DATABASE_URL` both unset | Exit with `❌ Missing SUPABASE_DB_URL or DATABASE_URL` |
| No smoke test file found in any discovery path | Exit with `❌ No smoke test file found`; suggest creating one at `supabase/tests/smoke_test.sql` |
| Smoke test SQL execution error | Print error output, recommend `*rollback {snapshot}` if failure is critical |
| `ON_ERROR_STOP` triggers mid-test | Report which check failed, do not silently continue |
| Smoke test file exists but is empty | Warn `⚠️ Smoke test file is empty` and exit without running |

## Post-conditions

After successful execution:
- Smoke test SQL file resolved via discovery order (`supabase/tests/smoke/v_current.sql` → `supabase/tests/smoke_test.sql` → `squads/db-sage/templates/migration.sql.tmpl`)
- All checks in the resolved smoke test executed under `ON_ERROR_STOP=1` against the active database
- Result categorized as PASS or FAIL with which check failed surfaced on FAIL

Acceptance Criteria:
- [ ] Output identifies the resolved smoke test file path before running it
- [ ] `psql` exit code is 0 for PASS or non-zero for FAIL (no silent continuation past failed assertions)
- [ ] No write/DML statements executed during smoke test (read-only validation only)
