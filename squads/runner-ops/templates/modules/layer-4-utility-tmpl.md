# Layer 4 — Utility Modules (SHOULD/NICE)

> Reference: `infrastructure/scripts/runner-lib/`
> Utilities handle UX, argument parsing, logging, and cross-run memory.
> Loaded automatically by `pipeline-bootstrap.sh`.

---

## 1. `arg-parser.sh` — Argument Parsing (SHOULD)

**What it does:** Standardizes `--source`, `--model`, `--phase`, `--dry-run`, `--max-cost` flags across all runners.

**Standard arguments (all runners should support):**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--source <path>` | string | required | Target directory or file to process |
| `--model <alias>` | string | `sonnet` | Model alias: opus/sonnet/haiku/gemini-pro/codex |
| `--phase <id>` | string | all | Run only a specific phase (resume/debug) |
| `--dry-run` | flag | false | Skip LLM calls, write fixture output |
| `--max-cost <usd>` | float | none | Stop if accumulated cost exceeds this |
| `--help` / `-h` | flag | — | Show usage |

**Usage:**
```bash
# Standard parse (sets SOURCE, MODEL, PHASE, DRY_RUN, MAX_COST)
parse_common_args "$@"

# After calling, these vars are set:
echo "$SOURCE"    # target path
echo "$MODEL"     # model alias
echo "$PHASE"     # specific phase or "all"
echo "$DRY_RUN"   # "true" or "false"
echo "$MAX_COST"  # "" or float string
```

**Custom flags (extend standard parser):**
```bash
parse_args() {
  # Call standard parser first
  parse_common_args "$@"

  # Then handle custom flags
  local positional=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --output-kind)
        OUTPUT_KIND="${2:?Missing value for --output-kind}"
        shift 2
        ;;
      --mode)
        MODE="${2:?Missing value for --mode}"
        shift 2
        ;;
      *)
        positional+=("$1")
        shift
        ;;
    esac
  done
}
```

---

## 2. `display.sh` — Terminal Output Formatting (NICE)

**What it does:** Consistent headers, section dividers, status indicators, and progress output.

```bash
# Section header with runner name
display_header "My Runner" "Processing $TARGET_SLUG"
# Output: ═══════════════════════════════════
#         ⚡ MY RUNNER — Processing my-squad
#         ═══════════════════════════════════

# Phase start
display_phase_start "phase-1-discovery" 1 4
# Output: ── Phase 1/4: phase-1-discovery ──────────

# Phase result
display_phase_result "phase-1-discovery" "PASS" "$cost_usd" "$duration_s"
# Output: ✅ phase-1-discovery PASS ($0.05 | 12s)

# Phase failure
display_phase_result "phase-1-discovery" "FAIL" "" ""
# Output: ❌ phase-1-discovery FAIL

# Final summary
display_completion "My Runner" "$total_cost" "$total_duration" "$RUN_DIR"
# Output: ══════════ COMPLETE ══════════
#         ✅ My Runner finished
#         Cost: $0.45 | Duration: 180s
#         Output: outputs/my-squad/run-001/
```

**Status prefix convention:**
```bash
echo "  ✅ Phase complete"
echo "  ❌ Phase failed"
echo "  ↩ Retrying (attempt 2/3)"
echo "  ⚠️ Warning: output shorter than expected"
echo "  → Delegating to cascade"
echo "  💾 State saved"
echo "  💰 Cost: \$0.05 | Total: \$0.12"
```

---

## 3. `progress-logger.sh` — Structured Logging (SHOULD)

**What it does:** Writes structured logs in both human-readable markdown and machine-readable JSONL.

**Log locations:**
```
$SESSION_DIR/
  logs/
    progress.md        ← human readable
    progress.jsonl     ← machine readable
    phase-1.log        ← raw LLM output for phase-1
    phase-2.log
```

**Usage:**
```bash
# Initialize logger
progress_init "$SESSION_DIR/logs/progress"

# Log phase start
progress_log_phase_start "$phase_id" "$phase_num" "$total_phases"

# Log phase complete
progress_log_phase_complete "$phase_id" "$cost_usd" "$duration_s" "$output_file"

# Log phase failure
progress_log_phase_fail "$phase_id" "$error_message"

# Log custom event
progress_log_event "RETRY" "attempt=2 phase=$phase_id"

# Log final summary
progress_log_summary "$total_cost" "$total_duration" "complete"
```

**JSONL log format:**
```jsonl
{"ts":"2026-04-03T10:00:00Z","event":"phase_start","phase":"phase-1","num":1,"total":4}
{"ts":"2026-04-03T10:05:00Z","event":"phase_complete","phase":"phase-1","cost_usd":0.05,"duration_s":12}
{"ts":"2026-04-03T10:05:01Z","event":"retry","phase":"phase-2","attempt":2,"reason":"tier1_fail"}
```

---

## 4. `json-validator.sh` — JSON Extraction & Repair

**What it does:** Extracts JSON from LLM output (which often wraps it in markdown), validates, and attempts repair on malformed JSON.

```bash
# Extract JSON from mixed markdown/JSON output
json_extract "$raw_output"
# Finds first valid JSON object or array in the string

# Extract from code block
json_extract_codeblock "$raw_output"
# Finds ```json...``` or ```...``` block and extracts content

# Validate JSON
json_validate "$json_string" || echo "Invalid JSON"

# Repair common LLM JSON mistakes (trailing commas, unquoted keys, etc.)
json_repair "$malformed_json"

# Full pipeline: extract → validate → repair if needed
json_safe_parse "$raw_output"
```

**Integration pattern for JSON-producing phases:**
```bash
# Phase that should return JSON
OUTPUT="$(run_llm_prompt "haiku" "$JSON_PROMPT" "$LOG" "score-phase")"
OUTPUT="$(filter_llm_output "$OUTPUT" "$LOG")"

# Extract and validate JSON
CLEAN_JSON="$(json_extract_codeblock "$OUTPUT")"
if ! json_validate "$CLEAN_JSON"; then
  CLEAN_JSON="$(json_repair "$CLEAN_JSON")"
fi

SCORE="$(echo "$CLEAN_JSON" | jq -r '.score // 0')"
```

---

## 5. `python-resolver.sh` — Python Environment Detection

**What it does:** Finds a working Python3 + PyYAML installation. Used by YAML validation scripts.

```bash
# Find Python with PyYAML
PYTHON="$(resolve_python)"
if [[ -z "$PYTHON" ]]; then
  echo "WARNING: Python3 + PyYAML not available, skipping YAML validation"
else
  "$PYTHON" -c "import yaml; yaml.safe_load(open('$file'))" || echo "Invalid YAML"
fi
```

**Graceful fallback:** If Python not available, emit warning but don't block runner execution.

---

## 6. `memory.sh` — Cross-Run Learning

**What it does:** Persists which model performed best for which phase across runs. Used by runners to auto-select the optimal model.

**Memory file:** `outputs/{squad}/{runner}/memory.json`

```bash
# Initialize memory for this runner
memory_init "$MEMORY_FILE" "$RUNNER_NAME"

# Record model performance for a phase
memory_record "$MEMORY_FILE" "$phase_id" "$model" "$score" "$cost_usd"
# Records: model, quality_score, cost_usd, timestamp

# Get best model for a phase (highest score, lowest cost weighted)
BEST_MODEL="$(memory_get_best_model "$MEMORY_FILE" "$phase_id")"
echo "Using learned model: $BEST_MODEL for $phase_id"

# Fallback if no memory yet
MODEL="${BEST_MODEL:-$DEFAULT_MODEL}"
```

**Memory file format:**
```json
{
  "runner": "my-runner",
  "phase_history": {
    "phase-1-discovery": [
      {"model": "sonnet", "score": 88, "cost_usd": 0.05, "ts": "2026-04-01"},
      {"model": "haiku",  "score": 72, "cost_usd": 0.01, "ts": "2026-04-02"},
      {"model": "opus",   "score": 95, "cost_usd": 0.40, "ts": "2026-04-03"}
    ]
  },
  "best_models": {
    "phase-1-discovery": "sonnet"
  }
}
```

---

## 7. `preflight.sh` — Pre-Run Validation

**What it does:** Verifies environment before starting a run (tools available, paths exist, credentials set).

```bash
# Run all preflight checks
preflight_check || {
  echo "Preflight failed. Aborting."
  exit 1
}
```

**Built-in checks:**
- `claude` CLI available and authenticated
- `jq` available (required for state management)
- `REPO_ROOT` resolves to git repo
- Output directory is writable
- No conflicting lock files

**Custom preflight checks:**
```bash
preflight_add_check "input-exists" "test -d '$SOURCE_DIR'" "Source directory not found: $SOURCE_DIR"
preflight_add_check "model-set" "test -n '$DEFAULT_MODEL'" "DEFAULT_MODEL must be set"
preflight_run_all
```

---

## 8. `loader.sh` — Module Registry

**What it does:** Sources all runner-lib modules in the correct dependency order. Called by `pipeline-bootstrap.sh`.

**You never call this directly.** But know what it loads:

```bash
# loader.sh sources in order:
source models.sh          # 1. Model catalog
source runtime.sh         # 2. LLM execution (depends on models)
source metrics.sh         # 3. Cost tracking (depends on runtime)
source state-manager.sh   # 4. State persistence
source session-mgr.sh     # 5. Session lifecycle
source context-engine.sh  # 6. Prompt context
source evaluator.sh       # 7. Quality scoring
source assertions.sh      # 8. Schema validation
source headless-guard.sh  # 9. Safety filters
source display.sh         # 10. Terminal output
source arg-parser.sh      # 11. CLI arguments
source progress-logger.sh # 12. Structured logging
source json-validator.sh  # 13. JSON extraction
source python-resolver.sh # 14. Python detection
source memory.sh          # 15. Cross-run learning
source preflight.sh       # 16. Pre-run checks
# (advanced modules loaded on-demand)
```

---

*Layer 4 Utilities — runner-ops squad template v1.0.0 | Source: infrastructure/scripts/runner-lib/*
