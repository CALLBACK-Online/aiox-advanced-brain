# Layer 3 — Quality & Validation Modules (SHOULD)

> Reference: `infrastructure/scripts/runner-lib/`
> These modules prevent bad output from being marked as "complete".
> Loaded automatically by `pipeline-bootstrap.sh`.

---

## 1. `evaluator.sh` — Quality Scoring (3 Tiers)

**What it does:** Scores phase output at 3 levels of depth. Tier 1 is deterministic (fast/free), Tier 2 uses LLM (cheap), Tier 3 uses LLM (thorough).

### Tier 1 — Deterministic Gates (always run)

```bash
evaluate_tier1() {
  local output_file="$1"
  local min_chars="${2:-3000}"

  # Gate 1: File exists
  [[ -f "$output_file" ]] || { echo "FAIL: output file missing"; return 1; }

  # Gate 2: Content not empty
  local chars
  chars=$(wc -c < "$output_file")
  [[ "$chars" -gt "$min_chars" ]] || { echo "FAIL: output too short ($chars < $min_chars chars)"; return 1; }

  # Gate 3: Not just whitespace/fixture
  grep -q "[a-zA-Z]" "$output_file" || { echo "FAIL: output appears blank"; return 1; }

  echo "PASS: tier1 ($chars chars)"
  return 0
}
```

### Tier 2 — LLM Quick Score (haiku, ~$0.003/call)

```bash
evaluate_phase_output() {
  local output_file="$1"
  local rubric="$2"       # "What should this output contain?"
  local min_score="${3:-85}"

  # Construct evaluation prompt
  local content
  content="$(head -c 3000 "$output_file")"

  local eval_prompt="Score this output 0-100 against this rubric.
Rubric: $rubric
Output:
$content

Respond with ONLY: {\"score\": N, \"reason\": \"brief reason\"}"

  local eval_result
  eval_result="$(run_llm_prompt "haiku" "$eval_prompt" "/dev/null" "eval")"
  eval_result="$(echo "$eval_result" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(json.dumps(d))')"

  local score
  score="$(echo "$eval_result" | jq '.score')"

  if [[ "$score" -ge "$min_score" ]]; then
    echo "PASS: tier2 score=$score/100"
    return 0
  else
    echo "FAIL: tier2 score=$score/100 (min=$min_score)"
    return 1
  fi
}
```

### Tier 3 — Deep Evaluation (sonnet/opus)

```bash
# Use only for complex outputs where Haiku is insufficient
evaluate_deep() {
  local output_file="$1"
  local rubric_file="$2"   # path to detailed rubric markdown
  local model="${3:-sonnet}"

  local rubric content
  rubric="$(cat "$rubric_file")"
  content="$(cat "$output_file" | head -c 8000)"

  local eval_prompt="Evaluate this output against the rubric below.
$rubric
---
OUTPUT:
$content
---
Return JSON: {\"score\": N, \"pass\": true/false, \"gaps\": [\"...\"], \"strengths\": [\"...\"]}"

  run_llm_prompt "$model" "$eval_prompt" "/dev/null" "deep-eval"
}
```

### Gate Integration Pattern

```bash
run_phase_with_gate() {
  local phase_id="$1"
  local rubric="$2"
  local max_retries=2
  local attempt=0

  while [[ $attempt -lt $max_retries ]]; do
    OUTPUT="$(run_llm_prompt "$DEFAULT_MODEL" "$PROMPT" "$LOG_FILE" "$phase_id")"
    OUTPUT="$(filter_llm_output "$OUTPUT" "$LOG_FILE")"
    echo "$OUTPUT" > "$OUTPUT_FILE"

    # Tier 1: fast check
    if ! evaluate_tier1 "$OUTPUT_FILE" 2000; then
      echo "  ↩ Tier 1 fail, retry $((attempt+1))/$max_retries"
      attempt=$((attempt+1))
      continue
    fi

    # Tier 2: quality score
    if ! evaluate_phase_output "$OUTPUT_FILE" "$rubric" 80; then
      echo "  ↩ Tier 2 fail, retry $((attempt+1))/$max_retries with boost"
      # Add "You must be more thorough" boost to prompt
      PROMPT="$PROMPT\n\nIMPORTANT: Previous attempt was too brief. Be exhaustive."
      attempt=$((attempt+1))
      continue
    fi

    echo "  ✅ Quality gates passed for $phase_id"
    break
  done

  if [[ $attempt -ge $max_retries ]]; then
    echo "⚠️ WARNING: $phase_id did not pass quality gate after $max_retries attempts"
    # Don't fail — record as warning and continue
  fi
}
```

---

## 2. `assertions.sh` — Schema Validation

**What it does:** Validates that output is valid YAML/JSON and matches expected structure. Used before marking phase complete.

```bash
# Assert output is valid YAML
assert_yaml_valid "$output_file" || {
  echo "FAIL: invalid YAML in $output_file"
  return 1
}

# Assert output is valid JSON
assert_json_valid "$output_file" || {
  echo "FAIL: invalid JSON in $output_file"
  return 1
}

# Assert required fields exist in YAML
assert_yaml_fields "$output_file" "name" "version" "phases" || {
  echo "FAIL: missing required fields"
  return 1
}

# Assert required fields in JSON
assert_json_fields "$output_file" ".phases" ".executor" ".quality_gate" || {
  echo "FAIL: missing required JSON fields"
  return 1
}
```

**Pattern for JSON-output phases:**
```bash
# Phase that must return JSON
OUTPUT="$(run_llm_prompt "sonnet" "$JSON_PROMPT" "$LOG" "phase-json")"
OUTPUT="$(filter_llm_output "$OUTPUT" "$LOG")"

# Extract JSON block if wrapped in markdown
CLEAN_JSON="$(echo "$OUTPUT" | python3 -c '
import sys, re, json
text = sys.stdin.read()
# Try to find JSON block
match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
if match:
    text = match.group(1)
try:
    obj = json.loads(text)
    print(json.dumps(obj, indent=2))
except:
    print(text)
')"

echo "$CLEAN_JSON" > "$OUTPUT_FILE"
assert_json_valid "$OUTPUT_FILE"
```

---

## 3. `headless-guard.sh` — Safety & Security Filters

**What it does:** Prevents the LLM from doing dangerous things in headless mode (writing to protected paths, leaking metadata, exceeding context limits).

**Core functions:**

```bash
# Filter out JSON metadata and tool-use blocks from stdout
# (run_llm_prompt calls this internally, but call manually if needed)
filter_llm_output "$raw_output" "$log_file"

# Truncate context to safe length (prevents OOM/token overflow)
truncate_prior_context "$prompt" 6000    # 6000 chars max

# Check if a path is safe to write to
guard_write_path "$output_path" || {
  echo "BLOCKED: attempt to write to protected path $output_path"
  exit 1
}

# Sanitize model output (remove potential prompt injections)
sanitize_output "$raw_output"
```

**Protected paths (always blocked):**
- `.git/`
- `.claude/`
- `node_modules/`
- `infrastructure/secrets/`
- Any path outside `outputs/` and `squads/` (configurable)

**Integration in run_phase():**
```bash
run_phase() {
  local phase_id="$1"
  local output_file="$RUN_DIR/${phase_id}.md"

  # Guard: output path must be in allowed zone
  guard_write_path "$output_file"

  local log_file="$LOG_DIR/${phase_id}.log"
  local prompt
  prompt="$(build_phase_prompt "$phase_id")"

  # Truncate to safe size before sending to LLM
  prompt="$(truncate_prior_context "$prompt" 6000)"

  local raw_output
  raw_output="$(run_llm_prompt "$DEFAULT_MODEL" "$prompt" "$log_file" "$phase_id")"

  # Filter metadata/tool-use noise from output
  raw_output="$(filter_llm_output "$raw_output" "$log_file")"

  printf '%s\n' "$raw_output" > "$output_file"
}
```

---

## 4. `validate-runner.sh` — Runner Compliance Checker

**What it does:** Checks a runner script against runner-lib standards. Produces a compliance score and violation list.

**Usage:**
```bash
# Validate a specific runner
bash infrastructure/scripts/runner-lib/validate-runner.sh \
  --runner squads/copy/scripts/copy-runner.sh \
  --report outputs/runner-ops/validation/copy-runner-$(date +%Y%m%d).txt

# Strict mode (fails on warnings too)
bash infrastructure/scripts/runner-lib/validate-runner.sh \
  --runner squads/copy/scripts/copy-runner.sh \
  --strict

# Validate all runners in registry
bash infrastructure/scripts/runner-lib/validate-runner.sh --all
```

**What it checks:**

| Check | Code | Severity |
|-------|------|---------|
| Sources `pipeline-bootstrap.sh` | C001 | CRITICAL |
| Uses `run_llm_prompt()` not direct `claude -p` | C002 | CRITICAL |
| Exports `METRICS_FILE` | C003 | CRITICAL |
| Calls `check_cost_cap()` | C004 | CRITICAL |
| Uses `state_init()` / `state_phase_update()` | H001 | HIGH |
| Uses `filter_llm_output()` | H002 | HIGH |
| Uses `--dangerously-skip-permissions` flag | H003 | HIGH |
| Uses `session_start()` / `session_end()` | W001 | WARN |
| Uses `evaluate_phase_output()` | W002 | WARN |
| Uses `cascade_run()` | W003 | WARN |
| Injects prior outputs inline (not file paths) | W004 | WARN |
| Has cleanup trap on EXIT | W005 | WARN |

**Score formula:**
- CRITICAL violations: -15 each
- HIGH violations: -8 each
- WARNINGS: -2 each
- Base score: 100

**Integration levels:**
- `full` ≥ 90 (production ready)
- `partial` 60-89 (review required)
- `minimal` < 60 (significant migration needed)

---

*Layer 3 Quality & Validation — runner-ops squad template v1.0.0 | Source: infrastructure/scripts/runner-lib/*
