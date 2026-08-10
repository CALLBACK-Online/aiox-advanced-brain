---
name: verify-deploy
description: "E2E verification of deployed story artifacts — validates actual production state matches what was deployed"
version: "2.0.0"
owner_squad: infra-ops-squad
aiox_tier: Tier1
context: inline
agent: general-purpose
user-invocable: true
argument-hint: "[story-file-path]"
---

# Verify Deploy Skill

Verifies that a deployed story's artifacts are live and functioning in production. Reads `infrastructure/infrastructure-map.json → deploy_targets[]` to determine health endpoints and detection rules. Populates the `e2e_verification` section of the story file with PASS/FAIL/PARTIAL status.

## Usage

```
/verify-deploy {story-id}
```

Example: `/verify-deploy 101.8`

---

## Pre-Execution: Load infrastructure-map.json

**BEFORE any verification,** read `infrastructure/infrastructure-map.json` to load all deploy target configuration:

1. Open `infrastructure/infrastructure-map.json`
2. Extract the `deploy_targets[]` array
3. **If `deploy_targets[]` is missing or empty → HALT immediately** with message:
   ```
   HALT: infrastructure/infrastructure-map.json does not contain deploy_targets[].
   Cannot proceed with verification — registry required. Add deploy_targets[] to infrastructure-map.json and retry.
   ```
4. Do NOT fall back to any hardcoded values. If the registry is absent, HALT. No silent fallbacks (AP-4).

Also read `.aiox/config/skill-defaults.json` to get `learning.base_path` for the execution log path.

**Do NOT skip this step.** Verification without reading infrastructure-map.json leads to stale configuration and violates the Skill Agnosticism principle (Epic 146).

---

## Execution Protocol

### Step 1: Read Story File

Locate the story file at `docs/stories/epic-{N}/STORY-{id}-*.md`.

Extract from the Dev Agent Record:
- `deploy_type` — must match an `id` in `deploy_targets[]` (or `none`, `multi`, `auto_detect`)
- `deploy-results` — output from deploy-story skill (optional, used for context)

If `deploy_type` is missing or `auto_detect`, scan the story's Files Affected table and match against `deploy_targets[].file_patterns` from `infrastructure/infrastructure-map.json`:
- For each entry in `deploy_targets[]`, check if any file in the story file list matches any pattern in `file_patterns[]`
- If **one target** matches → use that target's `id` as `deploy_type`
- If **multiple targets** match → use `multi` as `deploy_type`
- If **no targets** match → `deploy_type: none`

**Do NOT use a hardcoded mapping table.** Always iterate over `deploy_targets[]` from the registry.

### Step 2: Run Verification Matrix

Execute checks based on detected `deploy_type`. For each deploy target, read `health_endpoint` from `deploy_targets[id={deploy_type}]`:
- If `health_endpoint` is not null → run HTTP health check (expand `${ENV_VAR}` placeholders using env vars)
- If `health_endpoint` is null → **SKIP health check** (record as SKIP with note: "health_endpoint null in infrastructure-map.json for this target — health check skipped")

Record each check result.

### Step 3: Write Results to Story File

Populate the `e2e_verification` section with all check results, overall status, and timestamp.

---

## Verification Matrix

### `none` — Skip

```
deploy_type: none → PASS immediately, no checks required.
```

Write to story:
```yaml
e2e_verification:
  type: auto_detect
  status: PASS
  timestamp: "{ISO8601}"
  checks:
    - name: "skip"
      status: PASS
      details: "deploy_type is none — no deployment to verify"
```

---

### `supabase_migration` — Database Verification

**Health endpoint:** Read `deploy_targets[id=supabase_migration].health_endpoint` from `infrastructure-map.json`. This target has `health_endpoint: null` — **SKIP health check** and record as:
```yaml
- name: "health_endpoint"
  status: SKIP
  details: "health_endpoint null in infrastructure-map.json for supabase_migration — health check skipped"
```

Run ALL of the following checks:

#### Check 1: Connection Health

```bash
node services/supabase/cli.js test-connection
```

- PASS if exits 0
- FAIL if exits non-zero or times out

Record as:
```yaml
- name: "connection_health"
  status: PASS|FAIL
  details: "Connection successful" | "Connection failed: {error}"
```

#### Check 2: Table Exists

For each table created in the migration (scan migration file for `CREATE TABLE`):

```bash
node services/supabase/cli.js query "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '{table_name}'"
```

- PASS if result contains `table_name` row
- FAIL if result is empty

Record as:
```yaml
- name: "table_exists: {table_name}"
  status: PASS|FAIL
  details: "Table found in public schema" | "Table not found — migration may not have run"
```

**Failure suggested fix:**
```
Run migration manually: node services/supabase/cli.js query "$(cat {migration_file}.sql)"
Or via Supabase dashboard: Dashboard > SQL Editor > paste migration
```

#### Check 3: RLS Enabled

For each table where migration includes `ENABLE ROW LEVEL SECURITY`:

```bash
node services/supabase/cli.js query "SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename = '{table_name}'"
```

- PASS if `rowsecurity = true`
- FAIL if `rowsecurity = false`

Record as:
```yaml
- name: "rls_enabled: {table_name}"
  status: PASS|FAIL
  details: "rowsecurity = true" | "RLS not enabled — run: ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY"
```

#### Check 4: Triggers Exist

For each trigger defined in migration (scan for `CREATE TRIGGER`):

```bash
node services/supabase/cli.js query "SELECT tgname FROM pg_trigger WHERE tgrelid = '{table_name}'::regclass AND tgname = '{trigger_name}'"
```

- PASS if result contains the trigger name
- SKIP (not run) if migration has no `CREATE TRIGGER` statements

Record as:
```yaml
- name: "trigger_exists: {trigger_name}"
  status: PASS|FAIL|SKIP
  details: "Trigger found on {table_name}" | "Trigger not found — check migration applied correctly"
```

---

### `railway` — API Health Verification

**Health endpoint:** Read `deploy_targets[id=railway].health_endpoint` from `infrastructure-map.json`. This target has `health_endpoint: null` — **SKIP health endpoint check** and record as:
```yaml
- name: "health_endpoint"
  status: SKIP
  details: "health_endpoint null in infrastructure-map.json for railway — health check skipped"
```

Run type-specific checks:

#### Check 1: 404 Handling

```bash
curl -s -o /dev/null -w "%{http_code}" {base_url}/nonexistent-endpoint-verify-deploy
```

Where `{base_url}` is obtained from the story's `deploy-results` or `deploy_notes` (recorded by deploy-story skill).

- PASS if HTTP 404 (proper error handling)
- FAIL if HTTP 500 or 200 (incorrect behavior)

Record as:
```yaml
- name: "error_handling_404"
  status: PASS|FAIL
  details: "HTTP 404 returned correctly" | "HTTP {code} — unexpected response for missing endpoint"
```

#### Check 2: Story-Specific Endpoints (Optional)

If the story's Acceptance Criteria mention specific API endpoints (scan ACs for `/api/...` patterns):

```bash
curl -f -s -o /dev/null -w "%{http_code}" {base_url}{endpoint}
```

Note: Some endpoints require auth — a 401 is a PASS (endpoint exists and auth works).

Record as:
```yaml
- name: "endpoint: {path}"
  status: PASS|FAIL
  details: "HTTP {code} — endpoint reachable" | "HTTP {code} — endpoint not found"
```

**Failure suggested fix:**
```
Check Railway dashboard for deploy status
Check logs: railway logs --tail 50
If deploy is in progress, wait 2-3 minutes and retry
```

---

### `hetzner_docker` — Docker Service Verification

**Health endpoint:** Read `deploy_targets[id=hetzner_docker].health_endpoint` from `infrastructure-map.json`. Expand `${ENV_VAR}` placeholders (e.g., `${HETZNER_SERVER_IP}`) using environment variables before use.

**Important:** Docker commands require Tailscale VPN access to the server IP from `deploy_targets[id=hetzner_docker].health_endpoint`. If VPN is not connected, all Docker checks will FAIL with a clear message — this is expected and not a deployment failure.

#### Check 1: VPN Connectivity

Extract server IP from `deploy_targets[id=hetzner_docker].health_endpoint` or `deploy_targets[id=hetzner_docker].env_required[]` (look for `HETZNER_SERVER_IP` env var value):

```bash
ping -c 1 -W 3 ${HETZNER_SERVER_IP}
```

- PASS if ping succeeds
- FAIL if unreachable — record as:
```yaml
- name: "tailscale_vpn"
  status: FAIL
  details: "Cannot reach server — Tailscale VPN required for Docker verification. Connect VPN and re-run."
```

If VPN check fails, skip remaining Docker checks and set overall status to PARTIAL (VPN required, not a deploy failure).

#### Check 2: Health Endpoint

```bash
curl -f -s -o /dev/null -w "%{http_code} %{time_total}" {health_endpoint}
```

Where `{health_endpoint}` is read from `deploy_targets[id=hetzner_docker].health_endpoint` with `${HETZNER_SERVER_IP}` expanded.

- PASS if HTTP 200 and response time < 2000ms
- PARTIAL if HTTP 200 but response time >= 2000ms
- FAIL if non-200 or connection refused

Record as:
```yaml
- name: "health_endpoint"
  status: PASS|PARTIAL|FAIL
  details: "HTTP 200 in {time}ms" | "HTTP {code} — service may be down or deploying"
```

#### Check 3: Service Replicas

Extract service name from `deploy-results` or story context (typically the Docker service name).

```bash
docker service ls --filter "name={service_name}" --format "{{.Name}} {{.Replicas}}"
```

- PASS if replicas show `N/N` (e.g., `1/1`, `2/2`)
- FAIL if `0/N` (service not running)
- FAIL if service not found

Record as:
```yaml
- name: "service_replicas: {service_name}"
  status: PASS|FAIL
  details: "Replicas: {actual}/{desired}" | "Service not found or 0 replicas running"
```

**Failure suggested fix:**
```
Check service logs: docker service logs {service_name} --tail 50
Force update: docker service update --force {service_name}
Check image exists: docker image ls | grep {image_name}
```

#### Check 4: Log Health

```bash
docker service logs --tail 20 {service_name} 2>&1
```

Scan output for `ERROR` or `FATAL` patterns (case-insensitive).

- PASS if no ERROR/FATAL in last 20 lines
- PARTIAL if errors found but service is running (may be transient)

Record as:
```yaml
- name: "logs_clean: {service_name}"
  status: PASS|PARTIAL
  details: "No errors in last 20 log lines" | "Found {N} error lines — review: {first_error_line}"
```

#### Check 5: Health Check Status (if configured)

```bash
docker service inspect --format '{{json .Spec.TaskTemplate.ContainerSpec.Healthcheck}}' {service_name}
```

- SKIP if no healthcheck configured (`null` result)
- PASS if healthcheck is configured (existence check only — runtime state checked via replicas)

Record as:
```yaml
- name: "healthcheck_configured: {service_name}"
  status: PASS|SKIP
  details: "Healthcheck configured" | "No healthcheck configured — skipped"
```

---

### `vercel` — Frontend Deployment Verification

**Health endpoint:** Read `deploy_targets[id=vercel].health_endpoint` from `infrastructure-map.json`. This target has `health_endpoint: null` — **SKIP health endpoint check** and record as:
```yaml
- name: "health_endpoint"
  status: SKIP
  details: "health_endpoint null in infrastructure-map.json for vercel — health check skipped"
```

**Env vars:** Read `deploy_targets[id=vercel].env_required[]` from `infrastructure-map.json` to determine which token variable to use (e.g., `VERCEL_TOKEN`). Do NOT hardcode the variable name.

#### Check 1: Deployment Status

```bash
vercel ls --json 2>/dev/null | head -c 5000
```

If `vercel` CLI is not installed or not authenticated, use the API token from `env_required[]`:

```bash
curl -s -H "Authorization: Bearer ${<token_var>}" "https://api.vercel.com/v6/deployments?limit=5" 2>/dev/null
```

Where `{<token_var>}` is the first entry in `deploy_targets[id=vercel].env_required[]`.

- PASS if most recent deployment for the project shows `READY`
- FAIL if `ERROR` or `BUILDING`
- SKIP with warning if Vercel CLI/token unavailable

Record as:
```yaml
- name: "deployment_status"
  status: PASS|FAIL|SKIP
  details: "Deployment READY — {deployment_url}" | "Deployment in state {state}" | "Vercel CLI not available — manual check required"
```

#### Check 2: URL Accessible

Extract deployment URL from step 1 result, or use the production URL from story context.

```bash
curl -f -s -o /dev/null -w "%{http_code}" {deployment_url}
```

- PASS if HTTP 200
- FAIL if non-200 or connection refused

Record as:
```yaml
- name: "url_accessible"
  status: PASS|FAIL
  details: "HTTP 200 — {url}" | "HTTP {code} — {url} not accessible"
```

**Failure suggested fix:**
```
Check Vercel dashboard
Re-deploy: vercel --prod
Check build logs for errors
```

---

### `coolify` — Coolify PaaS Verification

**Health endpoint:** Read `deploy_targets[id=coolify].health_endpoint` from `infrastructure-map.json`. Expand `${COOLIFY_API_URL}` using the corresponding env var.

#### Check 1: Health Endpoint

```bash
curl -f -s -o /dev/null -w "%{http_code} %{time_total}" {health_endpoint}
```

Where `{health_endpoint}` is `deploy_targets[id=coolify].health_endpoint` with env vars expanded.

- PASS if HTTP 200 and response time < 2000ms
- PARTIAL if HTTP 200 but response time >= 2000ms
- FAIL if non-200 or connection refused

Record as:
```yaml
- name: "health_endpoint"
  status: PASS|PARTIAL|FAIL
  details: "HTTP 200 in {time}ms" | "HTTP {code} — Coolify may be down"
```

---

### `multi` — Multi-Deploy Verification

Detect which sub-types are present from `deploy-results` and story context. For each sub-type, find the corresponding entry in `deploy_targets[]` from `infrastructure-map.json`. Run all applicable checks from each detected sub-type. Aggregate results.

Overall status rules (same as single-type, applied across all sub-type results).

---

## Results Output Format

After all checks complete, write to the story file's `e2e_verification` section:

```yaml
e2e_verification:
  type: auto_detect
  status: PASS  # PASS | FAIL | PARTIAL
  timestamp: "2026-04-05T15:00:00Z"
  checks:
    - name: "{check_name}"
      status: PASS|FAIL|PARTIAL|SKIP
      details: "{human-readable result}"
```

### Overall Status Rules

| Condition | Overall Status |
|-----------|---------------|
| ALL checks PASS or SKIP | PASS |
| All critical checks PASS, some non-critical PARTIAL/FAIL | PARTIAL |
| ANY critical check FAIL | FAIL |

**Critical checks** (FAIL triggers overall FAIL):
- `connection_health` (supabase)
- `table_exists: *` (supabase)
- `health_endpoint` (hetzner_docker, coolify) — when not null in registry
- `service_replicas: *` (docker) — when VPN is connected
- `url_accessible` (vercel)

**Non-critical checks** (PARTIAL if fail, does not block):
- `rls_enabled: *`
- `trigger_exists: *`
- `error_handling_404`
- `logs_clean: *`
- `healthcheck_configured: *`
- `deployment_status` (vercel — if CLI unavailable)
- `tailscale_vpn` — sets PARTIAL (Docker checks skipped), not FAIL
- `health_endpoint` when `health_endpoint: null` in registry — always SKIP, never FAIL

---

## Failure Reporting

On FAIL, output a clear error block:

```
VERIFY-DEPLOY FAILED
====================
Story: {story-id}
Deploy type: {deploy_type}
Timestamp: {ISO8601}

FAILED CHECKS:
  - {check_name}
    Expected: {expected_value}
    Actual:   {actual_value}
    Fix:      {suggested_fix_command}

PARTIAL CHECKS:
  - {check_name}: {details}

The story has NOT been automatically rolled back.
Human decision required. Options:
  1. Fix the deployment issue and re-run: /verify-deploy {story-id}
  2. Rollback migration: node services/supabase/cli.js query "DROP TABLE IF EXISTS {table_name};"
  3. Rollback Docker: use rollback_command from deploy_targets[id={deploy_type}] in infrastructure-map.json
  4. Escalate to @devops for further diagnosis
```

Failure details are also recorded in `e2e_verification.checks[]` with `status: FAIL` and `details` containing expected vs actual.

The skill NEVER auto-rollbacks. It reports only. Human decision required.

---

## Story File Update

After verification, update the story file:

1. Locate the `e2e_verification:` block in the story front-matter or Dev Agent Record
2. Replace the existing block with the populated results
3. If no `e2e_verification` block exists, add it after `deploy-results:` in the Dev Agent Record

The story status is NOT automatically changed by this skill. Status transitions are managed by `workflow-chains.yaml` Step 7 (which calls this skill) and the close-story workflow.

---

## Error Handling

| Error | Behavior |
|-------|----------|
| `deploy_targets[]` missing from infrastructure-map.json | HALT immediately — no fallback |
| Story file not found | HALT with clear message — provide expected path |
| `deploy_type` missing | Auto-detect from `deploy_targets[].file_patterns`, warn if ambiguous |
| Supabase CLI not found | FAIL connection_health with install instructions |
| `vercel` CLI not installed | SKIP vercel checks, record SKIP with warning |
| Docker not accessible (no VPN) | SKIP docker checks, record PARTIAL with VPN instruction |
| curl not available | FAIL railway/vercel checks with message |
| `health_endpoint: null` for a target | SKIP health check — never FAIL for null endpoint |
| Migration file not found for scan | Run generic checks only, warn about limited coverage |
| `${ENV_VAR}` in health_endpoint not set | HALT — report which var is missing, do not expand to empty string |

---

## Workflow Phases

### Phase 1: Environment Check

- [ ] `infrastructure/infrastructure-map.json` exists and contains `deploy_targets[]` — if missing: **HALT**
- [ ] `deploy_targets[]` loaded into working memory for this execution
- [ ] `.aiox/config/skill-defaults.json` read — `learning.base_path` extracted
- [ ] Story file located at `docs/stories/epic-{N}/STORY-{id}-*.md`
- [ ] `deploy_type` extracted from Dev Agent Record (or auto-detected by matching file list against `deploy_targets[].file_patterns`)
- [ ] If `deploy_type: none` → write PASS immediately, exit — no further phases
- [ ] `deploy-results` section read for context (optional, used for check targeting)
- [ ] Environment-specific prerequisites checked by reading `deploy_targets[id={deploy_type}].env_required[]`:
  - For each required var: verify it is set in the environment
  - If any missing: HALT and report which vars are absent
- [ ] `health_endpoint` for matched target read — null endpoint → SKIP recorded, not FAIL

> **STOP** — Do not proceed to Phase 2 until deploy type is confirmed and environment prerequisites are evaluated.

### Phase 2: Endpoint Verification

- [ ] For each applicable check per `deploy_type`, execute as defined in Verification Matrix
- [ ] `health_endpoint` from `deploy_targets[id={deploy_type}]` used — if null, SKIP recorded
- [ ] `${ENV_VAR}` placeholders in `health_endpoint` expanded before use
- [ ] Each check result recorded with name, status (PASS/FAIL/PARTIAL/SKIP), and details

> **STOP** — Do not proceed to Phase 3 until all checks for the detected `deploy_type` are complete.

### Phase 3: E2E Sign-off

- [ ] Overall status determined by critical/non-critical check rules
- [ ] `e2e_verification` block written to story file (replaces existing block or appended after `deploy-results`)
- [ ] Failure report output if overall status is FAIL (with suggested fix commands)
- [ ] Story status NOT changed by this skill (status transitions managed by workflow chain)
- [ ] FAIL result: human decision required — skill never auto-rollbacks

> **STOP** — Verification is not complete until `e2e_verification` is written to the story file.

---

## Red Flags

| Rationalization | Why It Fails |
|----------------|--------------|
| "The deployment succeeded — verification is a formality" | Successful deployment and functioning deployment are not the same. Tables can exist without RLS. Services can start with 0/N replicas. URLs can return 200 on a cached error page. |
| "Tailscale is down — I'll mark Docker checks as PASS manually" | VPN unavailability produces PARTIAL, not PASS. Manually marking PASS obscures this. |
| "I'll skip the 404 check — it's non-critical" | Non-critical checks inform the PARTIAL/PASS boundary. Skipping them silently inflates the PASS rate. |
| "The service shows 1/1 replicas — I don't need to check logs" | Replica count confirms the container is running; it does not confirm the application started correctly. |
| "I'll run verification before the deployment has stabilized" | Services take time to start. Running verification immediately produces false FAILs. |
| "The story has no `deploy-results` section — I'll skip verification" | Missing `deploy-results` is a data gap, not a skip condition. Auto-detect from Files Affected and run the matrix. |
| "I'll auto-rollback on FAIL to keep things clean" | The skill never auto-rollbacks. Rollback is a human decision. |
| "health_endpoint is null — I'll FAIL the health check" | null `health_endpoint` in the registry means this target has no health endpoint defined. Always SKIP, never FAIL. |
| "I know the file patterns — I'll skip reading deploy_targets[]" | Hardcoded patterns drift from the registry. deploy_targets[] is the SOT; skill memory is not. |
| "infrastructure-map.json deploy_targets[] is empty, I'll use the old mapping table as fallback" | AP-4 from Epic 146: no silent fallback. If registry missing, HALT explicitly. |

---

## Blocking Conditions

HALT verification and surface to user when:

1. **`deploy_targets[]` missing from infrastructure-map.json** — `infrastructure/infrastructure-map.json` exists but has no `deploy_targets[]` key or it is empty. Action: HALT. Output: "HALT: deploy_targets[] missing from infrastructure-map.json. Cannot proceed with verification. Add deploy_targets[] and retry." Resolution: Update infrastructure-map.json with the required deploy_targets array.

2. **Story file not found** — File does not exist at the expected path. Action: HALT. Output: "Story file not found at {path}. Cannot verify deployment." Resolution: User provides correct story ID or path.

3. **`deploy_type` cannot be determined** — Neither Dev Agent Record nor Files Affected table yields a detectable type after matching against `deploy_targets[].file_patterns`. Action: HALT. Output the ambiguity. Do not run any checks against an unknown target. Resolution: Story author sets `deploy_type` explicitly.

4. **`${ENV_VAR}` in health_endpoint cannot be expanded** — A required env var referenced in `health_endpoint` is not set. Action: HALT. Output which var is missing. Do not use empty string as endpoint URL. Resolution: Set missing env var and retry.

5. **Critical check fails with no suggested fix available** — A critical check fails and the failure message does not provide a clear resolution path. Action: HALT after recording FAIL status. Output: full failure report with escalation instruction to `@devops`. Resolution: Human diagnoses root cause; re-run after fix.

6. **`e2e_verification` write fails** — Story file cannot be updated with verification results. Action: HALT. Output the write error. Do not report a verbal result without the written record. Resolution: Resolve file access issue and re-run verification.

7. **Multi-deploy type with zero detectable sub-types** — `deploy_type: multi` is set but no matching sub-types can be identified. Action: HALT. Output which sub-types were expected and not found. Resolution: Story author or deployer identifies the correct sub-types.

---

## Post-Execution Learning (MANDATORY — Write Log Before HALT)

> **This is an EXECUTABLE step.** You MUST use the Write tool to create the log file.

**BEFORE completing this skill, create the execution log:**

1. **Read** `.aiox/config/skill-defaults.json` → extract `learning.base_path`
2. **Construct file path:** `{learning.base_path}logs/verify-deploy/verify-deploy-{story-id}-{YYYYMMDD}-{HHmmss}.yaml`
   - Example: if `learning.base_path` is `.aios/learning/`, path becomes `.aios/learning/logs/verify-deploy/verify-deploy-146.5-20260505-120000.yaml`
3. **Use Write tool** to create the file with this content:

```yaml
schema_version: "1.0"
skill_id: "verify-deploy"
timestamp: "{current ISO-8601}"
story_id: "{story-id from $ARGUMENTS}"
executor: "{agent who executed}"
duration_minutes: {estimate}
mode: null
files_modified: [{list}]
decisions: []
errors: []
outcome: "{completed|halted|failed}"
coderabbit_iterations: 0
gate_result: "N/A"
epilogue:
  what_worked: "{patterns}"
  what_failed: "{anti-patterns or null}"
  decision_drift: "{drift or null}"
  confidence: "{HIGH|MEDIUM|LOW}"
  source_type: "skill_execution"
```

4. **NEVER skip** — even on failure, write with `outcome: failed`.
5. **NEVER hardcode** `.aios/learning/` — always read from `skill-defaults.json`.

> This log feeds `scripts/learning-digester.js` which generates observations for the unified learning system.

---

## Skill Chain Decision (SCD)

> **This is the FINAL executable step.** After writing the learning log, evaluate chain routing.

**Chain Position:** `verify-deploy` → **close-story**
**Irreversible:** No (but next skill `close-story` IS irreversible — propose-commit applies there)

### Confidence Evaluation

| Signal | HIGH | MEDIUM | LOW |
|--------|------|--------|-----|
| E2E verification result | PASS | PARTIAL (non-critical failures only) | FAIL |
| All critical checks | Pass | Pass | 1+ fail |
| Blocking conditions hit | 0 | 0 | 1+ |
| Outcome in learning log | `completed` | `completed` | `halted` or `failed` |

### Routing

Based on the `confidence` value you wrote in the learning log:

- **HIGH** → Propose (NOT auto-chain — next skill is irreversible): Output: `SCD: HIGH confidence — verification PASS. Run /close-story {story-id} to close? (y/n)` — HALT and wait for user confirmation.
- **MEDIUM** → Propose with warning: Output: `SCD: MEDIUM confidence — verification PARTIAL. Review results above, then run /close-story {story-id} if acceptable. Proceed? (y/n)` — HALT and wait.
- **LOW** → Halt: Output: `SCD: LOW confidence — verification FAIL. Resolve failing checks before closure.` — Do NOT propose.

### Rules

1. **NEVER auto-chain to close-story** — close-story is irreversible, always require user confirmation even on HIGH confidence
2. **NEVER skip the learning log** to chain faster — SCD runs AFTER the log is written
3. **NEVER auto-chain if outcome is `halted` or `failed`** — override to LOW regardless of other signals
4. The user can always override: "skip chain" cancels proposal, "force chain" overrides MEDIUM/LOW

---

## Files

| File | Purpose |
|------|---------|
| `skills/verify-deploy/SKILL.md` | This file — skill definition |
| `infrastructure/infrastructure-map.json` | SOT for deploy targets, health endpoints, file patterns, env_required |
| `.aiox/config/skill-defaults.json` | SOT for learning log base path |

---
