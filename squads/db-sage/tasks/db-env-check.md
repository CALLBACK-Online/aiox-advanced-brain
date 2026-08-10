# Task: DB Env Check

| Field | Value |
|-------|-------|
| **responsavel_type** | `Worker` |
| **atomic_layer** | `Atom` |
| **domain** | `Operational` |
| **pattern** | EXEC-W-001 |
| **script** | `scripts/db-ops/health-checker.sh` |
| **rationale** | Verificação de env vars e conectividade é determinística |

**Purpose**: Validate environment for DB operations without leaking secrets

**Elicit**: false

---

## Outputs

- **env-var status**: `SUPABASE_DB_URL` or `DATABASE_URL` validated as present (value never printed)
- **client-tool versions**: `psql --version` and `pg_dump --version` echoed to console
- **connectivity check**: confirmation that `SELECT version()` returned successfully against the target DB
- **ssl/pooler classification**: `sslmode` and pooler usage flagged as present / advisory / not detected
- **exit code**: `0` on full pass, non-zero on missing env vars, missing clients, or failed connection

---

## Pre-conditions

- Environment variables available (SUPABASE_DB_URL or DATABASE_URL)

## 🚀 NEW: Use Automated Health Checker (RECOMMENDED)

**Token Savings: 95% | Time Savings: ~90%**

```bash
# Use the health-checker script for complete environment validation
./squads/db-sage/scripts/db-ops/health-checker.sh --quick

# Full health check
./squads/db-sage/scripts/db-ops/health-checker.sh --full

# Benefits:
#   - Environment validation
#   - Connection pool status
#   - Security checks
#   - Performance metrics
#   - 95% token savings
```

**OR continue with manual environment checks below:**

---

## Steps (Manual Method)

### 1. Validate Required Environment Variables

```bash
DB_URL="${SUPABASE_DB_URL:-${DATABASE_URL:-}}"
test -n "$DB_URL" || { echo "❌ Missing SUPABASE_DB_URL or DATABASE_URL"; exit 1; }

if [ -n "${SUPABASE_DB_URL:-}" ]; then
  echo "✓ SUPABASE_DB_URL present (redacted)"
else
  echo "✓ DATABASE_URL present (redacted)"
fi
```

### 2. Check SSL Mode and Pooler

```bash
case "$DB_URL" in
  *"sslmode="*) echo "✓ sslmode present";;
  *) echo "⚠️ Consider adding sslmode=require";;
esac

printf '%s' "$DB_URL" | grep -q "pooler" && echo "✓ Using pooler" || echo "ℹ Pooler not detected"
```

### 3. Check Client Versions

```bash
psql --version || { echo "❌ psql missing"; exit 1; }
pg_dump --version || { echo "❌ pg_dump missing"; exit 1; }
echo "✓ PostgreSQL client tools available"
```

### 4. Check Server Connectivity

```bash
psql "$DB_URL" -v ON_ERROR_STOP=1 -t -c "SELECT version();" > /dev/null \
  && echo "✓ Database connection successful"
```

---

## Success Criteria

- All environment variables present
- PostgreSQL client tools installed
- Database connection successful
- SSL and pooler configuration validated

## Error Handling

If any check fails:
1. Show clear error message
2. Provide remediation steps
3. Exit with non-zero status

## Post-conditions

After successful execution:
- `SUPABASE_DB_URL` or `DATABASE_URL` validated as present (value never printed)
- `psql` and `pg_dump` confirmed available on PATH with versions logged
- Connectivity to the database verified via `SELECT version()` round-trip
- SSL mode and pooler usage classified (present / advisory / not detected)

Acceptance Criteria:
- [ ] Script exits with code 0 when all four checks (env var, client tools, connectivity, SSL/pooler) pass
- [ ] No secret value (full connection string, password) appears in stdout/stderr
- [ ] On any failure the script exits non-zero with a remediation message identifying the failed check
