# Layer 1 — Core Modules (MUST)

> Reference: `infrastructure/scripts/runner-lib/`
> All runners MUST source `pipeline-bootstrap.sh` which loads these via `loader.sh`.
> These 4 modules are non-negotiable — no custom reimplementation allowed.

---

## 1. `pipeline-bootstrap.sh` — Entry Point

**What it does:** Resolves `RUNNER_LIB_DIR`, sets `REPO_ROOT`, sources `loader.sh` which loads ALL modules.

**How to source:**
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNNER_LIB_DIR="$REPO_ROOT/infrastructure/scripts/runner-lib"
source "$RUNNER_LIB_DIR/pipeline-bootstrap.sh"
```

**Sets after sourcing:**
- `RUNNER_LIB_DIR` — absolute path to runner-lib
- `REPO_ROOT` — absolute path to repo root
- `RUNNER_LIB_RUNTIME=true` — flag all modules can check

**Anti-pattern:** `source runner-lib/runtime.sh` directly — always go through `pipeline-bootstrap.sh`.

---

## 2. `runtime.sh` — LLM Execution Engine (Heart of the Runner)

**What it does:** Executes LLM calls with retry, fallback between runtimes (Claude/Gemini/Codex), and auto-records metrics.

**Primary function:**
```bash
run_llm_prompt "$model" "$prompt" "$log_file" "$phase_id"
# Returns: cleaned LLM output (stdout)
# Side effects: writes metrics to $METRICS_FILE, logs to $log_file

# Parameters:
# $1 model     — e.g. "opus", "sonnet", "haiku", "gemini-pro", "codex"
# $2 prompt    — the full prompt string (not a file path)
# $3 log_file  — where raw CLI output is captured
# $4 phase_id  — for metrics tagging
```

**Retry behavior:**
- Retries up to 3x on transient errors
- On billing error → automatic fallback to Gemini → Codex
- On Gemini fail → Codex

**Runtime flags used internally:**
```bash
claude -p "$prompt" \
  --dangerously-skip-permissions \
  --allowedTools "Read,Grep,Glob,Bash" \
  --model "$model_id"
```

**Supported model aliases:**

| Alias | Resolves to | Provider |
|-------|------------|---------|
| `opus` | claude-opus-4-6 | Anthropic |
| `sonnet` | claude-sonnet-4-6 | Anthropic |
| `haiku` | claude-haiku-4-5-20251001 | Anthropic |
| `gemini-pro` | gemini-2.5-pro-preview | Google |
| `codex` | o4-mini | OpenAI |

> **RULE (from memory):** NUNCA usar `gemini-flash` em runners — only `gemini-2.5-pro-preview`.

**Output filtering:**
```bash
raw_output="$(run_llm_prompt "$model" "$prompt" "$log_file" "$phase_id")"
raw_output="$(filter_llm_output "$raw_output" "$log_file")"
# filter_llm_output strips JSON metadata, tool-use blocks, system noise
```

**Anti-patterns:**
```bash
# ❌ NEVER — direct CLI call without runner-lib
claude -p "$prompt" > output.md

# ❌ NEVER — calling claude without --dangerously-skip-permissions in headless
claude -p "$prompt"

# ✅ CORRECT
raw_output="$(run_llm_prompt "sonnet" "$prompt" "$LOG_FILE" "phase-1")"
```

---

## 3. `metrics.sh` / `runner-metrics.sh` — Cost & Token Tracking

**What it does:** Records tokens in/out, cost, duration per phase in JSONL format. Auto-called by `run_llm_prompt()`.

**Required export (set before first LLM call):**
```bash
METRICS_FILE="$RUN_DIR/metrics.jsonl"
export METRICS_FILE
```

**Output format (one JSON line per LLM call):**
```jsonl
{"phase":"phase-1","model":"sonnet","tokens_in":3400,"tokens_out":2100,"cost_usd":0.028,"duration_s":12.8,"ts":"2026-04-03T10:00:00Z"}
```

**Manual metrics recording (if needed):**
```bash
record_metrics "$phase_id" "$model" "$tokens_in" "$tokens_out" "$cost_usd" "$duration_s"
```

**Budget cap check:**
```bash
# After each phase, enforce max cost:
check_cost_cap "$MAX_COST" || {
  echo "Budget cap $MAX_COST reached — stopping"
  exit 75  # exit code 75 = budget exceeded
}
```

**Reading metrics for reports:**
```bash
# Total cost for this run:
jq -s 'map(.cost_usd) | add' "$METRICS_FILE"

# Most expensive phase:
jq -s 'sort_by(.cost_usd) | last | .phase' "$METRICS_FILE"
```

---

## 4. `models.sh` — Model Catalog & Pricing

**What it does:** Defines model IDs, pricing per 1M tokens, capability tiers.

**Capability matrix:**

| Alias | Use case | Approx cost/1M tokens (in/out) |
|-------|---------|-------------------------------|
| `haiku` | Validation, classification, templated output | $0.25 / $1.25 |
| `sonnet` | Analysis, reasoning, structured generation | $3 / $15 |
| `opus` | Complex synthesis, creative, strategic | $15 / $75 |
| `gemini-pro` | Cost-efficient alternative to sonnet | ~$2.50 / $10 |
| `codex` | Code generation, structured logic | ~$1 / $4 |

**Phase model selection guide:**

| Phase type | Recommended | Fallback |
|-----------|------------|---------|
| Simple extraction / classification | `haiku` | `gemini-pro` |
| Analysis / scoring | `sonnet` | `gemini-pro` |
| Complex synthesis / writing | `opus` | `sonnet` |
| QA / validation | `haiku` | `haiku` |
| Code generation | `sonnet` | `codex` |

**Model selection in runner config:**
```yaml
# pipeline-phases.yaml
phases:
  - id: phase-1-extraction
    recommended_model: haiku
    budget_usd: 0.05
  - id: phase-2-analysis
    recommended_model: sonnet
    budget_usd: 0.30
  - id: phase-3-synthesis
    recommended_model: opus
    budget_usd: 1.00
```

---

## Minimum Viable Runner (Layer 1 only)

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNNER_LIB_DIR="$REPO_ROOT/infrastructure/scripts/runner-lib"
source "$RUNNER_LIB_DIR/pipeline-bootstrap.sh"

TARGET="$1"
MODEL="${2:-sonnet}"
RUN_DIR="$REPO_ROOT/outputs/my-squad/$TARGET/$(date +%Y%m%d-%H%M%S)"
METRICS_FILE="$RUN_DIR/metrics.jsonl"
mkdir -p "$RUN_DIR"

PROMPT="Analyze $TARGET and produce a summary."
OUTPUT="$(run_llm_prompt "$MODEL" "$PROMPT" "$RUN_DIR/phase-1.log" "phase-1")"
OUTPUT="$(filter_llm_output "$OUTPUT" "$RUN_DIR/phase-1.log")"
echo "$OUTPUT" > "$RUN_DIR/phase-1.md"

check_cost_cap "5.00"
echo "Done. Output: $RUN_DIR"
```

This runner: calls LLM, filters output, tracks metrics, enforces budget. Add Layers 2-5 incrementally.

---

*Layer 1 Core — runner-ops squad template v1.0.0 | Source: infrastructure/scripts/runner-lib/*
