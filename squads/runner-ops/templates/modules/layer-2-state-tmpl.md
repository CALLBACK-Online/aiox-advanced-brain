# Layer 2 — State & Context Modules (MUST)

> Reference: `infrastructure/scripts/runner-lib/`
> These modules give runners crash-resilience and context management.
> Loaded automatically by `pipeline-bootstrap.sh`.

---

## 1. `state-manager.sh` — Phase State Persistence (Save Game)

**What it does:** Reads and writes `state.json` atomically (`.tmp` → rename). Tracks which phases completed so the runner can resume after a crash.

**State file location:**
```bash
STATE_FILE="$RUN_DIR/state.json"
```

**Lifecycle:**
```bash
# 1. Initialize (once, before first phase)
state_init "$STATE_FILE" "$TARGET_SLUG" "runner" '{"mode":"greenfield","runner":"my-runner"}'

# 2. Mark phase as running (before LLM call)
state_phase_update "$STATE_FILE" "$phase_id" "running" "$RUNNER_NAME"
state_update --argjson phase "$phase_num" '.current_phase = $phase' "$STATE_FILE"

# 3. Mark phase as complete (after successful output)
state_phase_update "$STATE_FILE" "$phase_id" "complete" "$RUNNER_NAME"
state_add_artifact "$STATE_FILE" "$output_file"

# 4. Mark run as complete
state_complete "$STATE_FILE" 0       # 0 = exit code

# 5. On failure (in trap)
state_update --arg status "failed" '.status = $status' "$STATE_FILE"
```

**Resume logic (skip completed phases):**
```bash
for phase_id in "${PHASES[@]}"; do
  # Check if already done
  STATUS=$(state_get "$STATE_FILE" ".phases.${phase_id}.status" 2>/dev/null || echo "pending")
  [[ "$STATUS" == "complete" ]] && echo "Skipping $phase_id (cached)" && continue

  # Execute phase...
done
```

**State file structure:**
```json
{
  "target": "my-squad",
  "type": "runner",
  "status": "in_progress",
  "started_at": "2026-04-03T10:00:00Z",
  "current_phase": 2,
  "phases": {
    "phase-1-discovery": {
      "status": "complete",
      "completed_at": "2026-04-03T10:05:00Z",
      "output": "outputs/my-squad/run-001/phase-1-discovery.md"
    },
    "phase-2-analysis": {
      "status": "running"
    }
  },
  "artifacts": ["outputs/my-squad/run-001/phase-1-discovery.md"],
  "meta": {"mode": "greenfield", "runner": "my-runner"}
}
```

**Cleanup trap (always add):**
```bash
cleanup() {
  local exit_code=$?
  if [[ -n "${STATE_FILE:-}" && -f "${STATE_FILE:-}" && $exit_code -ne 0 ]]; then
    state_update --arg status "failed" '.status = $status' "$STATE_FILE" || true
  fi
}
trap cleanup EXIT
```

**Anti-patterns:**
```bash
# ❌ NEVER — writing state manually
echo '{"status":"done"}' > state.json

# ❌ NEVER — non-atomic write (corrupts on crash)
jq '.status = "done"' state.json > state.json

# ✅ CORRECT — atomic via state-manager.sh
state_update --arg status "done" '.status = $status' "$STATE_FILE"
```

---

## 2. `session-mgr.sh` — Session Lifecycle (SHOULD)

**What it does:** Manages the "session" container — the directory that holds all artifacts, logs, and metrics for one complete run.

**Session directory structure:**
```
$SESSION_DIR/
  session.json       ← session metadata
  state.json         ← phase state (from state-manager.sh)
  metrics.jsonl      ← cost/token tracking
  logs/
    phase-1.log      ← raw LLM output
    phase-2.log
  phase-1.md         ← clean output per phase
  phase-2.md
```

**Usage:**
```bash
SESSION_DIR="$OUTPUT_ROOT/$(date +%Y%m%d-%H%M%S)-$TARGET_SLUG"
mkdir -p "$SESSION_DIR/logs"

# Start session (creates session.json)
session_start "$SESSION_DIR"

# ... run phases ...

# End session (updates session.json with duration + status)
session_end "$SESSION_DIR"

# On failure (in cleanup trap)
session_fail "$SESSION_DIR" "$error_message"
```

**Session metadata (session.json):**
```json
{
  "session_id": "20260403-100000-my-squad",
  "runner": "my-runner",
  "target": "my-squad",
  "started_at": "2026-04-03T10:00:00Z",
  "ended_at": "2026-04-03T10:45:00Z",
  "duration_s": 2700,
  "status": "complete",
  "phases_completed": 4,
  "total_cost_usd": 0.45
}
```

**Archive completed sessions:**
```bash
session_archive "$SESSION_DIR"
# Compresses session dir to .tar.gz in outputs/archive/
```

---

## 3. `context-engine.sh` — Prior Output Injection (MUST for multi-phase)

**What it does:** Injects prior phase outputs into the next phase's prompt. Handles truncation to stay within token limits.

**Core function:**
```bash
# Inject prior output inline (never tell LLM to read files — inject content directly)
PRIOR_CONTEXT="$(read_focused_context "$prior_output_file" 3000)"
# 3000 = max chars to inject (~750 tokens)

# Truncate and inject into prompt
PROMPT="$(truncate_prior_context "$base_prompt" 6000)"
# 6000 = max total prompt chars before truncation
```

**Multi-phase prompt pattern:**
```bash
build_phase_prompt() {
  local phase_id="$1"
  local prior_output="$2"

  local prior_content=""
  if [[ -f "$prior_output" ]]; then
    prior_content="$(read_focused_context "$prior_output" 3000)"
  fi

  cat <<EOF
# My Runner — Phase: $phase_id

## Context from previous phase:
$prior_content

## Your task for this phase:
[Phase-specific instructions here]

Deliver only the artifact for this phase.
EOF
}

# Usage in phase loop:
prior_file="$RUN_DIR/phase-1.md"
PROMPT="$(build_phase_prompt "phase-2" "$prior_file")"
PROMPT="$(truncate_prior_context "$PROMPT" 6000)"
```

**Why inject inline (not file path):**
- LLMs in headless mode cannot reliably read files via tool use
- Injecting inline guarantees the content is in the context window
- `read_focused_context()` handles file-not-found gracefully

**Truncation behavior:**
- `truncate_prior_context()` cuts from the middle if over limit
- Preserves first 2000 chars and last 1000 chars (beginning + end)
- Middle gets replaced with `[... truncated ...]`

---

## Full Layer 2 Integration Pattern

```bash
# After parse_args(), before first phase:

SESSION_DIR="$OUTPUT_ROOT/$(date +%Y%m%d-%H%M%S)-$TARGET_SLUG"
LOG_DIR="$SESSION_DIR/logs"
STATE_FILE="$SESSION_DIR/state.json"
METRICS_FILE="$SESSION_DIR/metrics.jsonl"

mkdir -p "$SESSION_DIR" "$LOG_DIR"

# Crash handler
cleanup() {
  local exit_code=$?
  if [[ $exit_code -ne 0 ]]; then
    state_update --arg status "failed" '.status = $status' "$STATE_FILE" || true
    session_fail "$SESSION_DIR" "exit_code=$exit_code" || true
  fi
}
trap cleanup EXIT

session_start "$SESSION_DIR"
state_init "$STATE_FILE" "$TARGET_SLUG" "runner" "{\"mode\":\"$MODE\"}"

PHASES=("phase-1-discovery" "phase-2-analysis" "phase-3-synthesis")

for i in "${!PHASES[@]}"; do
  phase_id="${PHASES[$i]}"
  phase_num=$((i + 1))

  STATUS=$(state_get "$STATE_FILE" ".phases.${phase_id}.status" 2>/dev/null || echo "pending")
  [[ "$STATUS" == "complete" ]] && echo "  ↩ Skipping $phase_id (cached)" && continue

  prior_file="$SESSION_DIR/${PHASES[$((i-1))]:-}.md"
  PROMPT="$(build_phase_prompt "$phase_id" "$prior_file")"
  PROMPT="$(truncate_prior_context "$PROMPT" 6000)"

  state_phase_update "$STATE_FILE" "$phase_id" "running" "$RUNNER_NAME"
  state_update --argjson phase "$phase_num" '.current_phase = $phase' "$STATE_FILE"

  OUTPUT="$(run_llm_prompt "$DEFAULT_MODEL" "$PROMPT" "$LOG_DIR/${phase_id}.log" "$phase_id")"
  OUTPUT="$(filter_llm_output "$OUTPUT" "$LOG_DIR/${phase_id}.log")"
  echo "$OUTPUT" > "$SESSION_DIR/${phase_id}.md"

  check_cost_cap "$MAX_COST" || break

  state_phase_update "$STATE_FILE" "$phase_id" "complete" "$RUNNER_NAME"
  state_add_artifact "$STATE_FILE" "$SESSION_DIR/${phase_id}.md"
done

state_complete "$STATE_FILE" 0
session_end "$SESSION_DIR"
```

---

*Layer 2 State & Context — runner-ops squad template v1.0.0 | Source: infrastructure/scripts/runner-lib/*
