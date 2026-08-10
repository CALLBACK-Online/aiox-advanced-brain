# Layer 5 — Advanced Modules (NICE / On-Demand)

> Reference: `infrastructure/scripts/runner-lib/`
> Advanced modules for complex pipelines. Load on-demand — not auto-loaded.
> Source explicitly: `source "$RUNNER_LIB_DIR/cascade.sh"`

---

## 1. `cascade.sh` — Model Escalation (Quality → Cost Tradeoff)

**What it does:** Automatically escalates to a more capable (more expensive) model when quality gates fail. Prevents cheap models from producing unacceptable output.

**Cascade chain:**
```
haiku (fast, $0.25/1M) → sonnet (capable, $3/1M) → opus (best, $15/1M)
```

**Usage:**
```bash
source "$RUNNER_LIB_DIR/cascade.sh"

# Define quality threshold and cascade chain
QUALITY_THRESHOLD=85
CASCADE_CHAIN=("haiku" "sonnet" "opus")

# Run phase with auto-cascade
OUTPUT="$(cascade_run "$phase_id" "$PROMPT" "$LOG_FILE" "$QUALITY_THRESHOLD" "${CASCADE_CHAIN[@]}")"
```

**What cascade_run() does internally:**
1. Tries `haiku` → scores output
2. If score < 85 → tries `sonnet` → scores output
3. If score < 85 → tries `opus` → uses this regardless
4. Records which model was used in metrics
5. Updates `memory.sh` with best model for this phase

**Manual cascade pattern:**
```bash
cascade_phase() {
  local phase_id="$1"
  local prompt="$2"
  local log_file="$3"

  for model in "haiku" "sonnet" "opus"; do
    local output
    output="$(run_llm_prompt "$model" "$prompt" "$log_file" "$phase_id")"
    output="$(filter_llm_output "$output" "$log_file")"

    local score
    score="$(evaluate_phase_output_score "$output" "$RUBRIC")"

    echo "  → cascade: $model score=$score"

    if [[ $score -ge 85 ]]; then
      echo "$output"
      return 0
    fi

    check_cost_cap "$MAX_COST" || break
  done

  # Return best effort (opus output)
  echo "$output"
}
```

**When to use cascade:**
- Phases where quality varies significantly by model
- Expensive phases where starting cheap saves money on easy inputs
- Long-running pipelines where cost per run matters

**When NOT to use cascade:**
- Phases that always need opus (don't bother with cascade, just use opus)
- Validation/scoring phases (haiku is always sufficient)
- Simple extraction (haiku is always sufficient)

---

## 2. `hooks.sh` — Lifecycle Extensibility

**What it does:** Executes shell scripts at lifecycle events (pre/post phase, on failure, on completion). Configured via YAML.

**Hooks config file:**
```yaml
# squads/{squad}/config/runner-hooks.yaml
hooks:
  pre_phase:
    - "emit-metrics-start"    # scripts/hooks/emit-metrics-start.sh
  post_phase:
    - "check-quality-gate"    # scripts/hooks/check-quality-gate.sh
    - "emit-metrics-end"
  on_failure:
    - "notify-slack"          # scripts/hooks/notify-slack.sh
    - "archive-failed-run"
  on_complete:
    - "archive-session"       # scripts/hooks/archive-session.sh
    - "update-registry"
```

**Usage in runner:**
```bash
source "$RUNNER_LIB_DIR/hooks.sh"

HOOKS_CONFIG="$SQUAD_DIR/config/runner-hooks.yaml"
hooks_load "$HOOKS_CONFIG"

# In phase loop:
hooks_run "pre_phase" "$phase_id" "$SESSION_DIR"
# ... run LLM ...
hooks_run "post_phase" "$phase_id" "$SESSION_DIR" "$output_file"

# On completion:
hooks_run "on_complete" "" "$SESSION_DIR"

# On failure (in trap):
hooks_run "on_failure" "$phase_id" "$SESSION_DIR" "$error_message"
```

**Hook script interface:**
```bash
# scripts/hooks/check-quality-gate.sh
#!/bin/bash
# Args: $1=phase_id, $2=session_dir, $3=output_file
PHASE_ID="$1"
SESSION_DIR="$2"
OUTPUT_FILE="$3"

CHARS=$(wc -c < "$OUTPUT_FILE")
if [[ $CHARS -lt 2000 ]]; then
  echo "HOOK WARNING: output too short ($CHARS chars)"
  exit 1  # non-zero exits trigger on_failure hooks
fi
exit 0
```

---

## 3. `dispatch.sh` — Cross-Squad Communication

**What it does:** Sends events/results from one squad's runner to another squad. Used when a runner needs to trigger downstream processing.

```bash
source "$RUNNER_LIB_DIR/dispatch.sh"

# Dispatch event to another squad
dispatch_event "aiox-squad" "runner-validation-complete" '{
  "runner": "copy-runner",
  "score": 92,
  "artifacts": ["outputs/runner-ops/validation/copy-runner-20260403.txt"]
}'

# Dispatch with callback (wait for acknowledgment)
dispatch_request "squad-creator" "create-squad-from-mapping" \
  "$MAPPING_YAML" \
  --timeout 300

# Check dispatch queue (for monitoring)
dispatch_queue_status "runner-ops"
```

**Dispatch file locations:**
```
.aiox/squad-dispatch/
  runner-ops/
    outbox/         ← events waiting to be delivered
    inbox/          ← events received from other squads
    delivered/      ← archive of delivered events
```

**When to use dispatch:**
- Runner completes and needs to trigger Squad Creator
- Runner needs to notify monitoring system
- Cross-squad handoffs defined in AIOX pipeline

---

## 4. `worktree.sh` — Git Worktree Isolation

**What it does:** Creates a temporary git worktree so the runner works on an isolated copy of the repository. Prevents concurrent runners from conflicting.

```bash
source "$RUNNER_LIB_DIR/worktree.sh"

# Create isolated worktree for this run
WORKTREE_DIR="$(worktree_create "$TARGET_SLUG" "$RUN_ID")"
# Creates: /tmp/runner-worktrees/run-20260403-001-my-squad/

# Run phases in the worktree
cd "$WORKTREE_DIR"
# ... all file operations happen in isolation ...

# Commit and merge changes back
worktree_commit "$WORKTREE_DIR" "feat: generated artifacts for $TARGET_SLUG [Runner]"
worktree_merge "$WORKTREE_DIR" "main"

# Cleanup
worktree_cleanup "$WORKTREE_DIR"
```

> **RULE:** NUNCA usar `isolation: "worktree"` em agents — apenas em runners via `worktree.sh`. Agents em worktrees causam erros 500 e cleanup problems.

**When to use:**
- Runner generates code/files that need commit isolation
- Multiple runners running concurrently on same repo
- Long-running runner where main branch may change during execution

**When NOT to use:**
- Output-only runners (write to `outputs/`, no repo changes)
- Single concurrent runner (no isolation needed)

---

## 5. `replan.sh` — Failure Recovery & Replanning

**What it does:** When a phase fails repeatedly, analyzes why and proposes a revised strategy (different model, different prompt, different approach).

```bash
source "$RUNNER_LIB_DIR/replan.sh"

# After max retries exhausted:
if [[ $attempt -ge $MAX_RETRIES ]]; then
  # Analyze failure pattern
  REPLAN="$(replan_analyze "$phase_id" "$LOG_FILE" "$METRICS_FILE")"

  # Replan returns: {"strategy": "change_model", "new_model": "opus", "rationale": "..."}
  NEW_STRATEGY="$(echo "$REPLAN" | jq -r '.strategy')"

  case "$NEW_STRATEGY" in
    "change_model")
      DEFAULT_MODEL="$(echo "$REPLAN" | jq -r '.new_model')"
      echo "  → Replan: switching to $DEFAULT_MODEL"
      ;;
    "simplify_prompt")
      echo "  → Replan: simplifying prompt (complex prompt caused failures)"
      # Adjust prompt building strategy
      ;;
    "skip_phase")
      echo "  → Replan: skipping $phase_id (non-critical)"
      state_phase_update "$STATE_FILE" "$phase_id" "skipped" "$RUNNER_NAME"
      continue
      ;;
  esac
fi
```

**Replan strategies:**
- `change_model` — try a more capable model
- `simplify_prompt` — reduce prompt complexity
- `split_phase` — break one large phase into two smaller ones
- `inject_example` — add few-shot example to prompt
- `skip_phase` — mark as non-critical and continue (with warning)

---

## 6. `compress.sh` — Session Archival & Compression

**What it does:** Compresses completed session directories to save disk space. Keeps a summary JSON for monitoring without needing to decompress.

```bash
source "$RUNNER_LIB_DIR/compress.sh"

# Compress session after completion
compress_session "$SESSION_DIR"
# Creates: $SESSION_DIR.tar.gz + $SESSION_DIR.summary.json
# Removes: $SESSION_DIR/ (raw files)

# Compress all sessions older than 7 days
compress_sessions_older_than "$OUTPUT_ROOT" 7

# Read summary without decompressing
compress_read_summary "$SESSION_DIR.summary.json"
```

**Summary JSON format:**
```json
{
  "session_id": "20260403-100000-my-squad",
  "runner": "my-runner",
  "target": "my-squad",
  "status": "complete",
  "total_cost_usd": 0.45,
  "phases_completed": 4,
  "artifacts": ["phase-1.md", "phase-2.md", "phase-3.md", "phase-4.md"],
  "compressed_at": "2026-04-03T11:00:00Z",
  "archive_path": "outputs/my-squad/archive/20260403-100000-my-squad.tar.gz"
}
```

---

## When to Use Advanced Modules

| Scenario | Module |
|----------|--------|
| Phase quality varies with model, cost matters | `cascade.sh` |
| Need pre/post phase automation | `hooks.sh` |
| Runner triggers another squad's workflow | `dispatch.sh` |
| Runner generates files that need git isolation | `worktree.sh` |
| Phase fails repeatedly, need auto-recovery | `replan.sh` |
| Long-running, many sessions accumulate | `compress.sh` |

---

## Combining Advanced Modules (Full Pattern)

```bash
source "$RUNNER_LIB_DIR/cascade.sh"
source "$RUNNER_LIB_DIR/hooks.sh"
source "$RUNNER_LIB_DIR/replan.sh"

HOOKS_CONFIG="$SQUAD_DIR/config/runner-hooks.yaml"
hooks_load "$HOOKS_CONFIG"

run_phase_advanced() {
  local phase_id="$1"
  local phase_rubric="$2"
  local max_retries=2
  local attempt=0

  hooks_run "pre_phase" "$phase_id" "$SESSION_DIR"

  while [[ $attempt -le $max_retries ]]; do
    # Use cascade for optimal model selection
    OUTPUT="$(cascade_run "$phase_id" "$PROMPT" "$LOG_FILE" 85 "haiku" "sonnet" "opus")"
    OUTPUT="$(filter_llm_output "$OUTPUT" "$LOG_FILE")"

    if evaluate_tier1 "$OUTPUT" 2000; then
      echo "$OUTPUT" > "$SESSION_DIR/${phase_id}.md"
      hooks_run "post_phase" "$phase_id" "$SESSION_DIR" "$SESSION_DIR/${phase_id}.md"
      return 0
    fi

    attempt=$((attempt+1))
    check_cost_cap "$MAX_COST" || return 75
  done

  # Replanning after exhausted retries
  REPLAN="$(replan_analyze "$phase_id" "$LOG_FILE" "$METRICS_FILE")"
  hooks_run "on_failure" "$phase_id" "$SESSION_DIR" "$REPLAN"
  return 1
}
```

---

*Layer 5 Advanced — runner-ops squad template v1.0.0 | Source: infrastructure/scripts/runner-lib/*
