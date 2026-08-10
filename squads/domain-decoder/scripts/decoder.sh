#!/bin/bash
# Domain Decoder Pipeline Script (runtime-agnostic: Claude, Codex, Gemini)
# External bash loop — each phase runs in a fresh LLM session
# Usage: ./decoder.sh [flags] <system-slug> [mode] [max-iterations]

set -e

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DECODER_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DECODER_DIR/../.." && pwd)"
TEMPLATES_DIR="$DECODER_DIR/templates/pipeline"
OUTPUTS_DIR="$REPO_ROOT/outputs/decoded"

mkdir -p "$OUTPUTS_DIR"
RUNNER_LIB_DIR="$REPO_ROOT/infrastructure/scripts/runner-lib"

# ── Bootstrap runner-lib v2 ──
source "$RUNNER_LIB_DIR/pipeline-bootstrap.sh"
if declare -f preflight_check >/dev/null 2>&1; then
  preflight_check "jq" "" || exit 1
fi

export SESSION_TRACKING=true

REQUESTED_RUNTIME="${DECODER_LLM_RUNTIME:-auto}"
SELECTED_RUNTIME=""
LLM_TIMEOUT_SECONDS="${DECODER_LLM_TIMEOUT:-}"
RETRY_MAX_ATTEMPTS="${DECODER_RETRY_MAX_ATTEMPTS:-}"
RETRY_BASE_DELAY_SECONDS="${DECODER_RETRY_BASE_DELAY:-3}"
DECODER_EXPLICIT_MODEL="${DECODER_MODEL:-}"

# Replan-on-failure: enable for pipeline runners (Story 101.10 AC4)
PHASE_REPLAN="${PHASE_REPLAN:-true}"
REPLAN_MAX_ATTEMPTS="${REPLAN_MAX_ATTEMPTS:-2}"
export PHASE_REPLAN REPLAN_MAX_ATTEMPTS

# Evaluator: phases that run evaluate_phase_output() after LLM (Story 101.11 AC6)
EVAL_PHASES="${EVAL_PHASES:-rule_extraction,decision_model}"
EVALUATOR_RUBRICS_DIR="$DECODER_DIR/rubrics"
export EVAL_PHASES EVALUATOR_RUBRICS_DIR

SOURCE_PATH=""     # --source: path to codebase (../repo, squads/x, /abs/path)

# Model-aware routing: if --model is a runtime name, use it as runtime directly.
# Previous bug: --model gemini tried to use "gemini" as model name in Claude runtime,
# causing Claude to fail and then falling back to Gemini (wasting 10-30s per phase).
_resolve_model_as_runtime() {
  local model="$1"
  case "$model" in
    claude|codex|gemini) echo "$model" ;;  # It's a runtime name, not a model
    *) echo "" ;;                           # It's an actual model name (opus, haiku, sonnet)
  esac
}



decoder_handle_cost_cap_exit() {
  local phase="${1:-$(jq -r '.current_phase // 0' "$STATE_FILE" 2>/dev/null || echo "0")}"
  local ts
  ts="$(date -Iseconds)"

  if [[ -f "$STATE_FILE" ]]; then
    state_update \
      --arg status "cost_cap_exceeded" \
      --arg ts "$ts" \
      --arg phase "$phase" \
      '.status = $status | .last_cost_cap_at = $ts | .current_phase = ($phase | tonumber)' \
      "$STATE_FILE"
  fi

  echo "💾 Saving state before exit..."
  echo "   Increase or remove --max-cost, then resume with:"
  echo "   $0 $SYSTEM_SLUG brownfield $MAX_ITERATIONS"
  exit 75
}

# ═══════════════════════════════════════════════════════════════
# MODEL CONFIGURATION — per-phase agent assignment
# ═══════════════════════════════════════════════════════════════

MODEL_DEFAULT=""  # Set after runtime resolution

get_model_for_phase() {
  # All phases use the same model by default.
  # Override per-phase here if needed (e.g., opus for extraction, haiku for validation).
  echo "$MODEL_DEFAULT"
}

get_phase_agent() {
  case $1 in
    0) echo "eric-evans" ;;
    1) echo "michael-feathers" ;;
    2) echo "ronald-ross" ;;
    3) echo "barbara-von-halle" ;;
    4) echo "graham-witt" ;;
    5) echo "decoder-chief" ;;
    *) echo "decoder-chief" ;;
  esac
}

# ═══════════════════════════════════════════════════════════════
# ARGUMENT PARSING
# ═══════════════════════════════════════════════════════════════

show_help() {
  echo "🧬 Domain Decoder Pipeline Runner"
  echo ""
  echo "Usage: $0 [flags] [system-slug] [mode] [max-iterations]"
  echo ""
  echo "Arguments:"
  echo "  system-slug     System identifier (auto-derived from --source if omitted)"
  echo "  mode            Pipeline mode: auto | greenfield | brownfield (default: auto)"
  echo "  max-iterations  Maximum iterations per phase (default: 10)"
  echo ""
  echo "Flags:"
  echo "  --source <path>    Path to codebase (../repo, squads/x, /abs/path)"
  echo "  --claude           Force Claude runtime"
  echo "  --codex            Force Codex runtime"
  echo "  --gemini           Force Gemini runtime"
  echo "  --model <name>     Override runtime model (e.g., --model opus)"
  echo "  --timeout <s>      Override LLM timeout in seconds"
  echo "  --phase <num>      Resume from specific phase (0-5, requires existing run)"
  echo ""
  echo "Phases:"
  echo "  0  Discovery        — Domain mapping, bounded contexts, glossary (eric-evans)"
  echo "  1  Characterization — Architecture, seams, characterization tests (michael-feathers)"
  echo "  2  Extraction       — Rule extraction, Ross classification, fact model (ronald-ross)"
  echo "  3  Modeling         — Decision Model, DMN tables, DRDs (barbara-von-halle)"
  echo "  4  Expression       — RuleSpeak statements, ambiguity elimination (graham-witt)"
  echo "  5  Validation       — SBVR/quality checklists, final catalog (decoder-chief)"
  echo ""
  echo "Examples:"
  echo "  $0 --source squads/copy --model opus       # auto-detects version from source"
  echo "  $0 --source ../forefy                       # reads version from package.json/config.yaml"
  echo "  $0 --source squads/copy                     # resumes latest or starts new"
  echo "  $0 --phase 3 --source squads/copy            # resume from phase 3 on latest run"
  echo ""
  echo "Versioned runs (version auto-detected from source):"
  echo "  outputs/decoded/{slug}/{version}/   ← each version is a separate run"
  echo "  outputs/decoded/{slug}/latest       ← symlink to most recent"
  echo ""
  echo "Environment:"
  echo "  DECODER_MODEL         Override model"
  echo "  DECODER_LLM_RUNTIME   Force runtime (auto|claude|codex|gemini)"
  echo "  DECODER_LLM_TIMEOUT   Timeout in seconds"
  echo "  DECODER_MAX_TURNS     Max LLM turns per phase (default: 5)"
  echo ""

  # Show existing systems with versioned runs
  echo "Existing systems:"
  if [[ -d "$OUTPUTS_DIR" ]]; then
    for sys_dir in "$OUTPUTS_DIR"/*/; do
      [[ ! -d "$sys_dir" ]] && continue
      slug=$(basename "$sys_dir")
      latest="$sys_dir/latest"
      if [[ -L "$latest" && -d "$latest" ]]; then
        run_id=$(readlink "$latest")
        state_file="$sys_dir/$run_id/decoder-state.json"
        if [[ -f "$state_file" ]]; then
          phase=$(jq -r '.current_phase // 0' "$state_file" 2>/dev/null)
          status=$(jq -r '.status // "unknown"' "$state_file" 2>/dev/null)
          echo "  🧬 $slug/$run_id (Phase $phase - $status)"
        else
          echo "  📁 $slug/$run_id (no state)"
        fi
        # List other versions
        for run_dir in "$sys_dir"/*/; do
          [[ ! -d "$run_dir" || "$(basename "$run_dir")" == "latest" ]] && continue
          other_id=$(basename "$run_dir")
          [[ "$other_id" == "$run_id" ]] && continue
          echo "     └ $slug/$other_id"
        done
      else
        echo "  📁 $slug (no runs)"
      fi
    done
  else
    echo "  (no systems found)"
  fi
  exit 0
}

handle_extra_args() {
  POSITIONAL_ARGS=()
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --source)
        if [[ -z "${2:-}" ]]; then echo "❌ Missing value for --source" >&2; exit 1; fi
        SOURCE_PATH="$2"; shift 2 ;;
      --max-turns)
        if [[ -z "${2:-}" ]]; then echo "❌ Missing value for --max-turns" >&2; exit 1; fi
        DECODER_MAX_TURNS="$2"; shift 2 ;;
      --no-eval)       EVAL_DISABLED="true"; shift ;;
      --eval-tier1-only) EVAL_TIER1_ONLY="true"; shift ;;
      -*)
        echo "❌ Unknown flag: $1"
        echo "   Use --help for usage."
        exit 1 ;;
      *)
        POSITIONAL_ARGS+=("$1"); shift ;;
    esac
  done
}

POSITIONAL_ARGS=()
START_PHASE=""

parse_common_args "$@"
if [[ -n "${RUNNER_MODEL:-}" ]]; then
  # Model-aware routing: check if --model value is actually a runtime name
  _runtime_from_model=$(_resolve_model_as_runtime "$RUNNER_MODEL")
  if [[ -n "$_runtime_from_model" ]]; then
    # --model gemini/claude/codex → set as runtime, not model name
    REQUESTED_RUNTIME="$_runtime_from_model"
    DECODER_EXPLICIT_MODEL=""  # Let runtime pick its default model
  else
    # --model opus/haiku/sonnet → actual model name within current runtime
    DECODER_EXPLICIT_MODEL="$RUNNER_MODEL"
  fi
fi
if [[ -n "${START_PHASE_ARG:-}" ]]; then
  START_PHASE="$START_PHASE_ARG"
fi
parse_extra_flags "${POSITIONAL_ARGS[@]}"

# Resolve source path to absolute (before slug derivation)
if [[ -n "$SOURCE_PATH" ]]; then
  if [[ "$SOURCE_PATH" == /* ]]; then
    SOURCE_PATH_ABS="$SOURCE_PATH"
  else
    SOURCE_PATH_ABS="$(cd "$REPO_ROOT" && cd "$SOURCE_PATH" 2>/dev/null && pwd)" || {
      SOURCE_PATH_ABS="$(cd "$SOURCE_PATH" 2>/dev/null && pwd)" || {
        echo "❌ Source path not found: $SOURCE_PATH"
        echo "   Tried relative to repo root ($REPO_ROOT) and current directory"
        exit 1
      }
    }
  fi
fi

# Derive slug: explicit > from --source basename > show help
if [[ ${#POSITIONAL_ARGS[@]} -ge 1 ]]; then
  SYSTEM_SLUG="${POSITIONAL_ARGS[0]}"
elif [[ -n "$SOURCE_PATH" ]]; then
  SYSTEM_SLUG="$(basename "$SOURCE_PATH" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g; s/__*/_/g; s/^_//; s/_$//')"
else
  echo "❌ Missing: --source <path> or <system-slug>"
  echo ""
  show_help
fi

# --source is required for greenfield (need to know what to decode)
if [[ -z "$SOURCE_PATH" && ! -d "$OUTPUTS_DIR/$SYSTEM_SLUG" ]]; then
  echo "❌ --source is required for new systems (no existing run found for '$SYSTEM_SLUG')"
  exit 1
fi

MODE="${POSITIONAL_ARGS[1]:-auto}"
MAX_ITERATIONS="${POSITIONAL_ARGS[2]:-10}"

# ═══════════════════════════════════════════════════════════════
# AUTO-DETECT VERSION FROM SOURCE
# ═══════════════════════════════════════════════════════════════

detect_source_version() {
  # Reads version from source codebase. Checks in priority order:
  #   1. package.json → .version
  #   2. config.yaml / config.yml → pack.version or version
  #   3. pyproject.toml → [tool.poetry].version or [project].version
  #   4. VERSION file
  #   5. Fallback: timestamp
  local src="$1"

  # 1. package.json
  if [[ -f "$src/package.json" ]]; then
    local v
    v=$(jq -r '.version // empty' "$src/package.json" 2>/dev/null)
    if [[ -n "$v" ]]; then echo "$v"; return; fi
  fi

  # 2. config.yaml (SINKRA squads)
  for cfg in "$src/config.yaml" "$src/config.yml"; do
    if [[ -f "$cfg" ]]; then
      local v
      # Try pack.version first (SINKRA pattern), then top-level version
      v=$(python3 -c "
import yaml, sys
try:
    d = yaml.safe_load(open('$cfg'))
    v = d.get('pack',{}).get('version') or d.get('version') or d.get('squad',{}).get('version')
    if v: print(v)
except: pass
" 2>/dev/null)
      if [[ -n "$v" ]]; then echo "$v"; return; fi
    fi
  done

  # 3. pyproject.toml
  if [[ -f "$src/pyproject.toml" ]]; then
    local v
    v=$(python3 -c "
import re
content = open('$src/pyproject.toml').read()
m = re.search(r'version\s*=\s*[\"'\''](.*?)[\"'\'']\s*', content)
if m: print(m.group(1))
" 2>/dev/null)
    if [[ -n "$v" ]]; then echo "$v"; return; fi
  fi

  # 4. VERSION file
  if [[ -f "$src/VERSION" ]]; then
    local v
    v=$(head -1 "$src/VERSION" | tr -d '[:space:]')
    if [[ -n "$v" ]]; then echo "$v"; return; fi
  fi

  # 5. Fallback: timestamp
  echo "$(date +%Y%m%d-%H%M%S)"
}

if [[ -n "${SOURCE_PATH_ABS:-}" ]]; then
  echo "📂 Source: $SOURCE_PATH_ABS"

  # Warn if source is outside the repo — Gemini CLI cannot read external paths
  if [[ ! "$SOURCE_PATH_ABS" == "$REPO_ROOT"* ]]; then
    echo "⚠️  Source is OUTSIDE this repo ($REPO_ROOT)"
    echo "   Gemini fallback will fail with 'Path not in workspace' errors."
    echo "   Use --claude or --model opus to force Claude (no workspace restriction)."
  fi

  DETECTED_VERSION="$(detect_source_version "$SOURCE_PATH_ABS")"
  echo "📌 Version: $DETECTED_VERSION (auto-detected)"
else
  DETECTED_VERSION="$(date +%Y%m%d-%H%M%S)"
fi
echo "🏷️  Slug: $SYSTEM_SLUG"

# Auto-detect mode based on existing runs
SLUG_BASE_DIR="$OUTPUTS_DIR/$SYSTEM_SLUG"
LATEST_LINK="$SLUG_BASE_DIR/latest"

# Migrate legacy flat state → versioned layout
if [[ -f "$SLUG_BASE_DIR/decoder-state.json" && ! -L "$LATEST_LINK" ]]; then
  echo "🔄 Migrating legacy flat state to versioned layout..."
  LEGACY_VERSION="$(detect_source_version "${SOURCE_PATH_ABS:-$SLUG_BASE_DIR}")"
  mkdir -p "$SLUG_BASE_DIR/$LEGACY_VERSION"
  # Move all phase dirs + state into versioned dir
  for item in decoder-state.json progress.txt logs discovery characterization extraction modeling expression validation; do
    [[ -e "$SLUG_BASE_DIR/$item" ]] && mv "$SLUG_BASE_DIR/$item" "$SLUG_BASE_DIR/$LEGACY_VERSION/" 2>/dev/null || true
  done
  ln -sfn "$LEGACY_VERSION" "$LATEST_LINK"
  echo "   Migrated to $SLUG_BASE_DIR/$LEGACY_VERSION/"
fi

if [[ "$MODE" == "auto" ]]; then
  if [[ -L "$LATEST_LINK" && -d "$LATEST_LINK" ]]; then
    MODE="brownfield"
    echo "🔍 Auto-detected: brownfield (previous runs found)"
  else
    MODE="greenfield"
    echo "🔍 Auto-detected: greenfield (no previous runs)"
  fi
fi

# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════

if [[ "$MODE" != "greenfield" && "$MODE" != "brownfield" ]]; then
  echo "❌ Invalid mode: $MODE"
  echo "   Valid modes: auto, greenfield, brownfield"
  exit 1
fi

SELECTED_RUNTIME="$(detect_runtime "$REQUESTED_RUNTIME")"
if [[ "$SELECTED_RUNTIME" == "invalid" ]]; then
  echo "❌ Invalid DECODER_LLM_RUNTIME: $REQUESTED_RUNTIME"
  exit 1
fi
if [[ "$SELECTED_RUNTIME" == "none" ]]; then
  echo "❌ No supported runtime found in PATH (claude, codex, or gemini)."
  exit 1
fi
validate_runtime "$SELECTED_RUNTIME"

case "$SELECTED_RUNTIME" in
  claude)
    MODEL_DEFAULT="${DECODER_EXPLICIT_MODEL:-$(get_balanced_model "$SELECTED_RUNTIME")}"
    RETRY_MAX_ATTEMPTS="${RETRY_MAX_ATTEMPTS:-2}"
    LLM_TIMEOUT_SECONDS="${LLM_TIMEOUT_SECONDS:-3600}"
    ;;
  codex)
    MODEL_DEFAULT="${DECODER_EXPLICIT_MODEL:-$(get_balanced_model "$SELECTED_RUNTIME")}"
    RETRY_MAX_ATTEMPTS="${RETRY_MAX_ATTEMPTS:-3}"
    LLM_TIMEOUT_SECONDS="${LLM_TIMEOUT_SECONDS:-5400}"
    ;;
  gemini)
    MODEL_DEFAULT="${DECODER_EXPLICIT_MODEL:-$(get_balanced_model "$SELECTED_RUNTIME")}"
    RETRY_MAX_ATTEMPTS="${RETRY_MAX_ATTEMPTS:-2}"
    LLM_TIMEOUT_SECONDS="${LLM_TIMEOUT_SECONDS:-3600}"
    ;;
esac
export SELECTED_RUNTIME LLM_TIMEOUT_SECONDS RETRY_MAX_ATTEMPTS RETRY_BASE_DELAY_SECONDS

# ═══════════════════════════════════════════════════════════════
# SESSION & HOOKS
# ═══════════════════════════════════════════════════════════════

SESSION_TRACKING="${DECODER_SESSION_TRACKING:-true}"
SQUAD_SLUG="domain-decoder"
AGENT_SLUG="decoder-pipeline"
export SESSION_TRACKING SQUAD_SLUG AGENT_SLUG

HISTORY_DIR="$(resolve_outputs_root "$REPO_ROOT")/domain-decoder"
mkdir -p "$HISTORY_DIR"
HISTORY_FILE="$HISTORY_DIR/run-history.jsonl"
export HISTORY_FILE

if declare -f hooks_load >/dev/null 2>&1; then
  hooks_load "$DECODER_DIR" 2>/dev/null || true
fi

# ═══════════════════════════════════════════════════════════════
# VERSIONED RUN DIRECTORY SETUP
# ═══════════════════════════════════════════════════════════════
#
# Layout:
#   outputs/decoded/{slug}/
#     v1.0.0/          ← RUN_ID = version
#       discovery/
#       characterization/
#       extraction/
#       modeling/
#       expression/
#       validation/
#       logs/
#       decoder-state.json
#     v2.0.0/          ← new run for new version
#     latest → v2.0.0  ← symlink to most recent

mkdir -p "$SLUG_BASE_DIR"

# ── --phase N: resume latest existing run ──
if [[ -n "$START_PHASE" ]]; then
  if [[ -L "$LATEST_LINK" && -d "$LATEST_LINK" ]]; then
    RUN_ID="$(readlink "$LATEST_LINK")"
    SYSTEM_DIR="$SLUG_BASE_DIR/$RUN_ID"
    echo "♻️  Resuming run: $RUN_ID (--phase $START_PHASE)"
  else
    echo "❌ --phase requires an existing run, but no 'latest' symlink found."
    echo "   Run a full pipeline first, then resume with --phase."
    exit 1
  fi

# ── brownfield: resume latest run ──
elif [[ "$MODE" == "brownfield" ]]; then
  if [[ -L "$LATEST_LINK" && -d "$LATEST_LINK" ]]; then
    RUN_ID="$(readlink "$LATEST_LINK")"
    SYSTEM_DIR="$SLUG_BASE_DIR/$RUN_ID"
    echo "🔄 Resuming run: $RUN_ID"
  else
    echo "❌ Brownfield requested but no previous run found."
    echo "   Run without mode to start fresh."
    exit 1
  fi

# ── greenfield: new versioned run ──
else
  # Append model name when explicitly set (enables A/B comparison: 4.0.0-haiku vs 4.0.0-opus)
  if [[ -n "$DECODER_EXPLICIT_MODEL" ]]; then
    RUN_ID="${DETECTED_VERSION}-${DECODER_EXPLICIT_MODEL}"
  else
    RUN_ID="$DETECTED_VERSION"
  fi
  SYSTEM_DIR="$SLUG_BASE_DIR/$RUN_ID"

  if [[ -d "$SYSTEM_DIR" ]]; then
    echo "⚠️  Run '$RUN_ID' already exists. Switching to resume."
    MODE="brownfield"
  fi
fi

echo "📁 Run: $RUN_ID → $SYSTEM_DIR"
mkdir -p "$SYSTEM_DIR"/{discovery,characterization,extraction,modeling,expression,validation,logs}

# Update latest symlink (greenfield only)
if [[ "$MODE" == "greenfield" ]]; then
  ln -sfn "$RUN_ID" "$LATEST_LINK"
fi

# ═══════════════════════════════════════════════════════════════
# STATE SETUP
# ═══════════════════════════════════════════════════════════════

STATE_FILE="$SYSTEM_DIR/decoder-state.json"
LOG_FILE="$SYSTEM_DIR/logs/pipeline-$(date +%Y%m%d).log"
METRICS_FILE="$SYSTEM_DIR/logs/job-metrics.jsonl"
MAX_COST="${DECODER_MAX_COST:-5.00}"
DECODER_SESSION_ID=""
export METRICS_FILE MAX_COST

mkdir -p "$(dirname "$LOG_FILE")"

cleanup() {
  local exit_code=$?
  if declare -f session_end >/dev/null 2>&1 && [[ -n "$DECODER_SESSION_ID" ]]; then
    session_end "$DECODER_SESSION_ID" "$exit_code" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

if declare -f session_start >/dev/null 2>&1; then
  DECODER_SESSION_ID="$(session_start "domain-decoder" "pipeline" "decoder-chief" "${MODEL_DEFAULT:-unknown}" "${SELECTED_RUNTIME:-auto}" "$LOG_FILE" "{\"system\":\"$SYSTEM_SLUG\"}" 2>/dev/null || true)"
fi

DECODER_PHASES_JSON=$(cat <<'EOF'
{
  "0_discovery":         { "status": "pending", "task": "map-domain", "agent": "eric-evans" },
  "1_characterization":  { "status": "pending", "task": "characterize-legacy", "agent": "michael-feathers" },
  "2_extraction":        { "status": "pending", "task": "extract-rules", "agent": "ronald-ross" },
  "3_modeling":          { "status": "pending", "task": "model-decisions", "agent": "barbara-von-halle" },
  "4_expression":        { "status": "pending", "task": "express-rules", "agent": "graham-witt" },
  "5_validation":        { "status": "pending", "task": "validation", "agent": "decoder-chief" }
}
EOF
)

if [[ ! -f "$STATE_FILE" ]]; then
  state_init "$STATE_FILE" "$SYSTEM_SLUG" "system"

  # Initialize full state only for NEW runs
  state_update \
    --arg slug "$SYSTEM_SLUG" \
    --arg mode "$MODE" \
    --arg source "${SOURCE_PATH_ABS:-}" \
    --arg version "$RUN_ID" \
    --argjson phase 0 \
    --argjson phases "$DECODER_PHASES_JSON" \
    '.target = $slug
      | .type = "system"
      | .system_slug = $slug
      | .version = $version
      | .mode = $mode
      | .source_path = $source
      | .status = "initialized"
      | .current_phase = $phase
      | .phases = $phases
      | .completed_tasks = []
      | .artifacts = []
      | .bounded_contexts = []
      | .total_rules_extracted = 0' \
    "$STATE_FILE"

  echo "📝 Created decoder-state.json"
else
  # Brownfield: only update mutable fields, preserve phases/progress
  state_update \
    --arg mode "$MODE" \
    --arg source "${SOURCE_PATH_ABS:-}" \
    '.mode = $mode | .source_path = $source' \
    "$STATE_FILE"
fi

if ! state_validate "$STATE_FILE"; then
  echo "❌ Invalid state file: $STATE_FILE"
  exit 1
fi

progress_init "$SYSTEM_DIR/progress.txt" "Domain Decoder Pipeline" "$SYSTEM_SLUG"

PROMPT_FILE="$TEMPLATES_DIR/prompt.md"
if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "❌ No prompt.md template found at: $PROMPT_FILE"
  exit 1
fi

# ═══════════════════════════════════════════════════════════════
# SHOW STATUS
# ═══════════════════════════════════════════════════════════════

display_pipeline_banner "🧬 Domain Decoder Pipeline" \
  "System:$SYSTEM_SLUG" \
  "Source:${SOURCE_PATH_ABS:-not specified}" \
  "Mode:$MODE" \
  "Directory:$SYSTEM_DIR" \
  "Runtime:$SELECTED_RUNTIME" \
  "Model:$MODEL_DEFAULT" \
  "Max iters:$MAX_ITERATIONS per phase"

CURRENT_PHASE=$(jq -r '.current_phase // 0' "$STATE_FILE")
STATUS=$(jq -r '.status // "unknown"' "$STATE_FILE")

echo "📊 Current State:"
echo "   Phase:  $CURRENT_PHASE"
echo "   Status: $STATUS"
echo ""

# ═══════════════════════════════════════════════════════════════
# PHASE HELPERS
# ═══════════════════════════════════════════════════════════════

get_phase_key() {
  case $1 in
    0) echo "0_discovery" ;;
    1) echo "1_characterization" ;;
    2) echo "2_extraction" ;;
    3) echo "3_modeling" ;;
    4) echo "4_expression" ;;
    5) echo "5_validation" ;;
    *) echo "" ;;
  esac
}

get_phase_name() {
  case $1 in
    0) echo "Discovery" ;;
    1) echo "Characterization" ;;
    2) echo "Extraction" ;;
    3) echo "Modeling" ;;
    4) echo "Expression" ;;
    5) echo "Validation" ;;
    *) echo "Unknown" ;;
  esac
}

_phase_dir_name() {
  case $1 in
    0) echo "discovery" ;;
    1) echo "characterization" ;;
    2) echo "extraction" ;;
    3) echo "modeling" ;;
    4) echo "expression" ;;
    5) echo "validation" ;;
  esac
}

# ═══════════════════════════════════════════════════════════════
# PROGRESS DASHBOARD
# ═══════════════════════════════════════════════════════════════

show_progress_dashboard() {
  local state_file="$1"
  local current_phase=$(jq -r '.current_phase // 0' "$state_file")

  echo ""
  echo "╔══════════════════════════════════════════════════════════════╗"
  echo "║                  🧬 PIPELINE PROGRESS                        ║"
  echo "╠══════════════════════════════════════════════════════════════╣"
  printf "║  🎯 Current: Phase %-5s                                     ║\n" "$current_phase"
  echo "╠══════════════════════════════════════════════════════════════╣"

  local phases="0:0_discovery:Discovery (eric-evans)
1:1_characterization:Characterization (michael-feathers)
2:2_extraction:Extraction (ronald-ross)
3:3_modeling:Modeling (barbara-von-halle)
4:4_expression:Expression (graham-witt)
5:5_validation:Validation (decoder-chief)"

  echo "$phases" | while IFS=: read -r phase_num phase_key phase_name; do
    local status=$(jq -r ".phases.\"$phase_key\".status // \"pending\"" "$state_file")
    local icon="⬜"
    [[ "$status" == "complete" ]] && icon="✅"
    [[ "$status" == "in_progress" ]] && icon="🔄"
    [[ "$status" == "failed" ]] && icon="❌"
    printf "║  %s [%s] %-42s ║\n" "$icon" "$phase_num" "$phase_name"
  done

  echo "╚══════════════════════════════════════════════════════════════╝"
  echo ""
}



# ═══════════════════════════════════════════════════════════════
# CONTEXT INJECTION (MMOS-pattern: inline task + agent + checklist)
# ═══════════════════════════════════════════════════════════════

# Maps phase number → task file(s) to inject
resolve_task_files() {
  local phase_num="$1"
  case "$phase_num" in
    0) echo "tasks/map-domain.md tasks/classify-rules.md" ;;
    1) echo "tasks/characterize-legacy.md" ;;
    2) echo "tasks/extract-rules.md" ;;
    3) echo "tasks/model-decisions.md" ;;
    4) echo "tasks/express-rules.md" ;;
    5) echo "" ;;  # Phase 5 uses checklists instead
  esac
}

# Maps phase number → agent summary file(s) to inject
resolve_agent_summaries() {
  local phase_num="$1"
  case "$phase_num" in
    0) echo "eric-evans.md ronald-ross.md" ;;
    1) echo "michael-feathers.md martin-fowler.md" ;;
    2) echo "ronald-ross.md michael-feathers.md" ;;
    3) echo "barbara-von-halle.md james-taylor.md" ;;
    4) echo "graham-witt.md ronald-ross.md" ;;
    5) echo "" ;;  # decoder-chief (no external persona needed)
  esac
}

# Builds the {TASK_CONTENT} block by concatenating task files
build_task_content() {
  local phase_num="$1"
  local task_files
  task_files=$(resolve_task_files "$phase_num")
  [[ -z "$task_files" ]] && echo "(No task file for validation phase — see checklists below)" && return

  local content=""
  for tf in $task_files; do
    local full_path="$DECODER_DIR/$tf"
    if [[ -f "$full_path" ]]; then
      content+="
### From: $tf
$(cat "$full_path")

---
"
    else
      content+="
### ⚠️ Task file not found: $tf
"
    fi
  done
  echo "$content"
}

# Builds the {AGENT_SUMMARY} block by concatenating agent summaries
build_agent_summary() {
  local phase_num="$1"
  local summary_files
  summary_files=$(resolve_agent_summaries "$phase_num")
  [[ -z "$summary_files" ]] && echo "(Phase 5: You are the decoder-chief performing final validation.)" && return

  local content=""
  for sf in $summary_files; do
    local full_path="$DECODER_DIR/agents/summaries/$sf"
    if [[ -f "$full_path" ]]; then
      content+="$(cat "$full_path")

---
"
    else
      content+="
### ⚠️ Agent summary not found: $sf
"
    fi
  done
  echo "$content"
}

# Builds the {CHECKLIST_CONTENT} block (Phase 5 only)
build_checklist_content() {
  local phase_num="$1"
  [[ "$phase_num" -ne 5 ]] && echo "" && return

  local content="### SBVR Validation Checklist (validate each item)
"
  local sbvr_file="$DECODER_DIR/checklists/sbvr-validation.md"
  if [[ -f "$sbvr_file" ]]; then
    content+="$(cat "$sbvr_file")

---

### Extraction Quality Checklist (validate each item)
"
  fi

  local quality_file="$DECODER_DIR/checklists/extraction-quality.md"
  if [[ -f "$quality_file" ]]; then
    content+="$(cat "$quality_file")"
  fi
  echo "$content"
}

# Assembles the complete prompt with all injections
build_phase_prompt() {
  local phase_num="$1"
  local prior_context="$2"
  local retry_boost="${3:-}"

  # Resolve injected content
  local task_content
  task_content="$(build_task_content "$phase_num")"
  local agent_summary
  agent_summary="$(build_agent_summary "$phase_num")"
  local checklist_content
  checklist_content="$(build_checklist_content "$phase_num")"

  # Get max turns for display in prompt
  local model
  model=$(get_model_for_phase "$phase_num")
  local display_turns=10
  case "$model" in
    *haiku*) display_turns=12 ;;
    *sonnet*) display_turns=10 ;;
    *opus*)  display_turns=15 ;;
  esac

  # Read template and perform substitutions
  local template
  template=$(cat "$PROMPT_FILE" 2>/dev/null || echo "Execute phase $phase_num for system: $SYSTEM_SLUG")

  # Perform all placeholder substitutions
  template="${template//\{SYSTEM_SLUG\}/$SYSTEM_SLUG}"
  template="${template//\{SYSTEM_DIR\}/$SYSTEM_DIR}"
  template="${template//\{SOURCE_PATH\}/${SOURCE_PATH_ABS:-not_specified}}"
  template="${template//\{DECODER_DIR\}/$DECODER_DIR}"
  template="${template//\{FORCE_PHASE\}/$phase_num}"
  template="${template//\{MAX_TURNS\}/$display_turns}"
  template="${template//\{AGENT_SUMMARY\}/$agent_summary}"
  template="${template//\{TASK_CONTENT\}/$task_content}"
  template="${template//\{CHECKLIST_CONTENT\}/$checklist_content}"

  # Assemble final prompt
  echo "$template
$retry_boost
$prior_context"
}

# ═══════════════════════════════════════════════════════════════
# E9: PHASE GATE VALIDATION
# ═══════════════════════════════════════════════════════════════

validate_phase_gate() {
  local phase_num="$1"
  local phase_name=$(get_phase_name "$phase_num")
  local phase_dir
  case $phase_num in
    0) phase_dir="discovery" ;;
    1) phase_dir="characterization" ;;
    2) phase_dir="extraction" ;;
    3) phase_dir="modeling" ;;
    4) phase_dir="expression" ;;
    5) phase_dir="validation" ;;
  esac

  local out_path="$SYSTEM_DIR/$phase_dir"
  echo "🔍 E9 Gate Check: Phase $phase_num ($phase_name)"

  # Check 1: Directory has files
  local file_count=$(find "$out_path" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$file_count" -eq 0 ]]; then
    echo "   ❌ No .md or .yaml files in $phase_dir/"
    return 1
  fi
  echo "   ✅ $file_count files found"

  # Check 2: Files > 500 bytes
  local small_files=$(find "$out_path" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) -size -500c 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$small_files" -gt 0 ]]; then
    echo "   ⚠️  $small_files files under 500 bytes"
  fi

  # Check 3: No status-level VETO/BLOCKED/FAILED markers
  # IMPORTANT: Only check the LATEST phase output file, not all files from previous iterations.
  # Previous bug: old iteration outputs (phase2-output.md from iter 1,2,3...) contained
  # VETO/BLOCKED as semantic content (not status markers), causing infinite retry loops.
  # Fix: Only check files modified in the last 5 minutes AND use strict status-only patterns.
  local recent_files=$(find "$out_path" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) -mmin -5 2>/dev/null)
  if [[ -z "$recent_files" ]]; then
    # No recent files — fall back to checking all files but with strict patterns only
    recent_files=$(find "$out_path" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) 2>/dev/null)
  fi
  # Strict patterns: only match explicit status declarations, not mentions in content
  # - "^VETO$" or "^BLOCKED$" or "^FAILED$" (standalone line = status signal)
  # - "status: VETO" (YAML status field)
  # - "<promise>PHASE_VETO" (LLM signal)
  local blockers=0
  if [[ -n "$recent_files" ]]; then
    blockers=$(echo "$recent_files" | xargs grep -lE "^(VETO|BLOCKED|FAILED)$|^status:\s*(VETO|BLOCKED|FAILED)$|<promise>PHASE_VETO" 2>/dev/null | wc -l | tr -d ' ')
  fi
  if [[ "$blockers" -gt 0 ]]; then
    echo "   ❌ $blockers files contain VETO/BLOCKED/FAILED status markers"
    echo "$recent_files" | xargs grep -lE "^(VETO|BLOCKED|FAILED)$|^status:\s*(VETO|BLOCKED|FAILED)$|<promise>PHASE_VETO" 2>/dev/null | while read -r f; do
      echo "      $(basename "$f")"
    done
    return 1
  fi
  echo "   ✅ No blocker markers"

  # E7: Check for extraction phase (WARNING, not blocking — LLM may include in output)
  if [[ "$phase_num" -eq 2 ]]; then
    if [[ ! -f "$out_path/dedup-matrix.md" ]]; then
      echo "   ⚠️  E7: dedup-matrix.md not found as separate file (may be in phase output)"
    else
      echo "   ✅ E7: dedup-matrix.md exists"
    fi
  fi

  # E5: Specific check for characterization phase (WARNING)
  if [[ "$phase_num" -eq 1 ]]; then
    local test_count=$(find "$out_path/tests" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$test_count" -eq 0 ]]; then
      echo "   ⚠️  E5: No characterization tests in tests/"
    else
      echo "   ✅ E5: $test_count characterization tests found"
    fi
  fi

  # Phase 5 specific: checklists must be FILLED, not template stubs
  # Proven: claude_code_main run had sbvr-checklist.md with all scores at 0/N
  if [[ "$phase_num" -eq 5 ]]; then
    local unfilled=0
    for checklist_file in "$out_path/sbvr-checklist.md" "$out_path/extraction-quality.md"; do
      if [[ -f "$checklist_file" ]] && grep -qE "score: 0 / |Score: 0/" "$checklist_file" 2>/dev/null; then
        echo "   ⚠️  Checklist $(basename "$checklist_file") has unfilled scores (template stub)"
        unfilled=$((unfilled + 1))
      fi
    done
    if [[ "$unfilled" -gt 0 ]]; then
      echo "   ❌ $unfilled checklist(s) not filled — validation incomplete"
      return 1
    fi
  fi

  echo "   ✅ Gate PASSED"
  return 0
}

# ═══════════════════════════════════════════════════════════════
# PRIOR PHASE CONTEXT BUILDER (incremental pipeline)
# ═══════════════════════════════════════════════════════════════

build_prior_context() {
  # Injects CONTENT of prior phase outputs directly into the prompt.
  # This prevents the LLM from spending turns on Read calls (context explosion).
  # Each file truncated to MAX_INJECT_CHARS to control prompt size.
  local current_phase="$1"
  local MAX_INJECT_CHARS=3000  # ~750 tokens per file
  local phase_dirs=("discovery" "characterization" "extraction" "modeling" "expression" "validation")
  local phase_names=("Discovery" "Characterization" "Extraction" "Modeling" "Expression" "Validation")

  if [[ "$current_phase" -eq 0 ]]; then
    echo "## Prior Phase Outputs

No prior phases — this is Phase 0 (first phase)."
    return
  fi

  local context="## Prior Phase Outputs (ALREADY IN CONTEXT — do NOT re-read)

Content from completed phases is below. Do NOT use Read tool on these files.
Spend your turns reading SOURCE files instead.

"

  for (( p=0; p<current_phase; p++ )); do
    local pdir="${phase_dirs[$p]}"
    local pname="${phase_names[$p]}"
    local full_path="$SYSTEM_DIR/$pdir"

    [[ ! -d "$full_path" ]] && continue

    # Find main output file
    local main_file=""
    if [[ -f "$full_path/phase${p}-output.md" ]]; then
      main_file="$full_path/phase${p}-output.md"
    else
      main_file=$(find "$full_path" -maxdepth 1 -name "*.md" -size +500c 2>/dev/null | head -1)
    fi
    [[ -z "$main_file" ]] && continue

    local file_content
    file_content=$(head -c "$MAX_INJECT_CHARS" "$main_file")
    local file_size=$(wc -c < "$main_file" | tr -d ' ')

    context+="### Phase $p — $pname ($(basename "$main_file"), ${file_size}B)

$file_content
"
    if [[ "$file_size" -gt "$MAX_INJECT_CHARS" ]]; then
      context+="
*(truncated at ${MAX_INJECT_CHARS} chars)*
"
    fi

    # List other files for reference
    local other_files
    other_files=$(find "$full_path" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) -size +0c ! -name "$(basename "$main_file")" 2>/dev/null | sort)
    if [[ -n "$other_files" ]]; then
      context+="
Also in $pdir/: "
      while IFS= read -r f; do
        context+="$(basename "$f") "
      done <<< "$other_files"
      context+="
"
    fi
    context+="
"
  done

  echo "$context"
}

# ═══════════════════════════════════════════════════════════════
# PHASE EXECUTION
# ═══════════════════════════════════════════════════════════════

run_phase() {
  local phase_num="$1"
  local phase_key=$(get_phase_key "$phase_num")
  local phase_name=$(get_phase_name "$phase_num")
  local agent=$(get_phase_agent "$phase_num")
  local phase_log="$SYSTEM_DIR/logs/phase${phase_num}-$(date +%Y%m%d).log"

  for iter in $(seq 1 $MAX_ITERATIONS); do
    # Check if already complete
    local phase_status=$(jq -r ".phases.\"$phase_key\".status // \"pending\"" "$STATE_FILE")
    if [[ "$phase_status" == "complete" ]]; then
      echo "✅ Phase $phase_num ($phase_name) already complete"
      return 0
    fi

    echo ""
    local model=$(get_model_for_phase "$phase_num")

    if declare -f warn_recurring_failures >/dev/null 2>&1; then
      warn_recurring_failures "phase-$phase_num" "$model" 2>/dev/null || true
    fi

    echo "═══════════════════════════════════════"
    echo "═══ Phase $phase_num | $phase_name | Agent: $agent | Iter $iter ═══"
    echo "═══════════════════════════════════════"
    echo "🚀 Starting at $(date +%H:%M:%S) with model: $model"

    local start_time=$(date +%s)

    if declare -f hooks_run_pre >/dev/null 2>&1; then
      hooks_run_pre "phase-$phase_num" || true
    fi

    # Build prior phase context (incremental reads)
    local PRIOR_CONTEXT
    PRIOR_CONTEXT="$(build_prior_context "$phase_num")"

    if declare -f read_focused_context >/dev/null 2>&1 && [[ -n "${SOURCE_PATH_ABS:-}" && -d "$SOURCE_PATH_ABS" ]]; then
      local config_yaml="$SOURCE_PATH_ABS/config.yaml"
      if [[ -f "$config_yaml" ]] && grep -q "kind: Squad" "$config_yaml"; then
        PRIOR_CONTEXT+=$'\n'$'\n'"## Squad Context (Focused)"$'\n'
        PRIOR_CONTEXT+="$(read_focused_context "$phase_num" "$SOURCE_PATH_ABS")"
      fi
    fi

    # Retry boost: if iter > 1, add explicit instruction about what went wrong
    local RETRY_BOOST=""
    if [[ "$iter" -gt 1 ]]; then
      local existing_files
      existing_files=$(find "$SYSTEM_DIR/$(_phase_dir_name "$phase_num")" -maxdepth 1 \( -name "*.md" -o -name "*.yaml" \) 2>/dev/null | wc -l | tr -d ' ')
      RETRY_BOOST="
## RETRY (attempt $iter)

Previous attempt was insufficient. Issues to fix:
- Your text response must be over $phase_min_chars characters (detailed analysis, not summary)
- You must use the Write tool to create EACH mandatory artifact file listed above
- You have already created $existing_files files — create the MISSING ones
- Read the source files at SOURCE_PATH first, then write detailed analysis
- End with <promise>PHASE_COMPLETE</promise>
"
    fi

    # Build prompt with injected task content + agent summary + checklists + prior context
    local PHASE_PROMPT
    PHASE_PROMPT="$(build_phase_prompt "$phase_num" "$PRIOR_CONTEXT" "$RETRY_BOOST")"

    # Update state to in_progress
    state_phase_update "$STATE_FILE" "$phase_key" "$phase_num" "in_progress"

    # Run LLM
    local default_turns=10
    case "$model" in
      *haiku*) default_turns=12 ;;
      *sonnet*) default_turns=10 ;;
      *opus*)  default_turns=15 ;;
    esac
    PHASE_MAX_TURNS="${DECODER_MAX_TURNS:-$default_turns}"
    PHASE_ALLOWED_TOOLS="Read,Write,Glob,Grep,Bash(ls),Bash(wc),Bash(head)"
    export PHASE_MAX_TURNS PHASE_ALLOWED_TOOLS

    local raw_output
    raw_output=$(run_llm_prompt_with_replan "$model" "$PHASE_PROMPT" "$phase_log" "phase-$phase_num") || true
    
    local OUTPUT
    OUTPUT=$(filter_llm_output "$raw_output" "$phase_log")

    local end_time=$(date +%s)
    local output_chars=${#OUTPUT}
    local phase_out_dir="$SYSTEM_DIR/$(_phase_dir_name "$phase_num")"

    echo "⏱️  Iteration $iter completed at $(date +%H:%M:%S) ($output_chars chars)"

    # ── ALWAYS save LLM output to disk (script responsibility, not LLM's) ──
    mkdir -p "$phase_out_dir"
    if [[ "$output_chars" -gt 200 ]]; then
      local saved_file="$phase_out_dir/phase${phase_num}-output.md"
      echo "$OUTPUT" > "$saved_file"
      echo "   💾 Saved: $saved_file ($output_chars chars)"
    fi

    # ── Check for veto first (last 30 lines) ──
    local OUTPUT_TAIL
    OUTPUT_TAIL="$(echo "$OUTPUT" | tail -30)"
    if echo "$OUTPUT_TAIL" | grep -q "<promise>PHASE_VETO:"; then
      local veto_reason=$(echo "$OUTPUT_TAIL" | grep -o "<promise>PHASE_VETO:[^<]*</promise>" | sed 's/<[^>]*>//g' | sed 's/PHASE_VETO://')
      echo "🚫 VETO in Phase $phase_num: $veto_reason"
      state_phase_update "$STATE_FILE" "$phase_key" "$phase_num" "failed" "$veto_reason"

      return 1
    fi

    # ── Determine if phase is complete ──
    # Signal: explicit PHASE_COMPLETE tag OR substantial output above phase-specific threshold
    # Phase-specific minimum thresholds (chars) to prevent premature completion
    local phase_min_chars=2000
    case "$phase_num" in
      0) phase_min_chars=3000 ;;  # Discovery: contexts + glossary + map
      1) phase_min_chars=3000 ;;  # Characterization: tests + seams + smells
      2) phase_min_chars=4000 ;;  # Extraction: rules + catalog + dedup
      3) phase_min_chars=3000 ;;  # Modeling: decisions + tables + DRDs
      4) phase_min_chars=3000 ;;  # Expression: RuleSpeak for all rules
      5) phase_min_chars=4000 ;;  # Validation: 2 checklists + matrix
    esac

    local has_signal=false
    local completion_method="none"

    if echo "$OUTPUT_TAIL" | grep -q "<promise>PHASE_COMPLETE</promise>"; then
      if [[ "$output_chars" -ge "$phase_min_chars" ]]; then
        has_signal=true
        completion_method="signal"
      else
        echo "   ⚠️  PHASE_COMPLETE signal found but output too short ($output_chars < $phase_min_chars chars). Retrying..."
      fi
    elif [[ "$output_chars" -gt "$phase_min_chars" ]]; then
      has_signal=true
      completion_method="substantial_output"
    fi

    if [[ "$has_signal" == "true" ]]; then
      # Verify gate (files on disk)
      if validate_phase_gate "$phase_num"; then
        # ── Evaluator: run after E9 gate passes (Story 101.11 AC6) ──
        # E9 Gate is semantic (content), evaluator is structural (format/schema).
        # Evaluator runs AFTER E9 — if E9 rejects, evaluator doesn't run (fail-fast).
        local eval_verdict="PASS"
        if declare -f run_phase_evaluator >/dev/null 2>&1; then
          local saved_file="$phase_out_dir/phase${phase_num}-output.md"
          if [[ -f "$saved_file" ]]; then
            local eval_exit=0
            eval_verdict=$(run_phase_evaluator "$saved_file" "phase-$phase_num" "$phase_log") || eval_exit=$?
            case "$eval_verdict" in
              RETRY)
                echo "  🔄 Evaluator: RETRY — re-executing phase $phase_num"
                continue
                ;;
              REMEDIATE)
                echo "  ⚠️  Evaluator: REMEDIATE — continuing with degraded quality"
                PHASES_DEGRADED="${PHASES_DEGRADED:+$PHASES_DEGRADED,}phase-$phase_num"
                ;;
              HALT)
                echo "  🛑 Evaluator: HALT — critical quality failure in phase $phase_num"
                state_phase_update "$STATE_FILE" "$phase_key" "$phase_num" "failed" "evaluator_halt"
                return 1
                ;;
            esac
          fi
        fi

        # Update both phase status AND current_phase to next phase.
        # Previous bug: current_phase wasn't updated on completion, causing brownfield
        # resume after Ctrl+Z to re-execute already-completed phases.
        local next_phase=$((phase_num + 1))
        state_update \
          --arg phase_key "$phase_key" \
          --argjson phase "$next_phase" \
          --arg status "phase_${phase_num}_complete" \
          '.phases[$phase_key].status = "complete" | .current_phase = $phase | .status = $status' \
          "$STATE_FILE"

        echo "✅ Phase $phase_num ($phase_name) COMPLETE ($completion_method)"

        if declare -f record_run >/dev/null 2>&1; then
          local duration_ms=$(( (end_time - start_time) * 1000 ))
          record_run "phase-$phase_num" "true" "$duration_ms" "0" 2>/dev/null || true
        fi

        if declare -f hooks_run_post >/dev/null 2>&1; then
          hooks_run_post "phase-$phase_num" || true
        fi

        return 0
      else
        echo "⚠️  Gate check incomplete after $completion_method — retrying for better output..."
        state_update \
          --arg phase_key "$phase_key" \
          '.phases[$phase_key].status = "in_progress"' \
          "$STATE_FILE"

      fi
    else
      echo "   ⏳ No completion signal and output too short ($output_chars chars). Retrying..."
    fi

    sleep 1
  done

  echo "⚠️  Phase $phase_num ($phase_name) reached max iterations ($MAX_ITERATIONS)"

  if declare -f record_run >/dev/null 2>&1; then
    record_run "phase-$phase_num" "false" "0" "0" "max_iterations" 2>/dev/null || true
  fi

  return 1
}

# ═══════════════════════════════════════════════════════════════
# MAIN PIPELINE LOOP
# ═══════════════════════════════════════════════════════════════

PHASES=(0 1 2 3 4 5)

# Determine start phase
FIRST_PHASE=0
if [[ -n "$START_PHASE" ]]; then
  FIRST_PHASE="$START_PHASE"
  echo "⏩ Starting from phase $FIRST_PHASE"
elif [[ "$MODE" == "brownfield" ]]; then
  for p in "${PHASES[@]}"; do
    phase_key=$(get_phase_key "$p")
    status=$(jq -r ".phases.\"$phase_key\".status // \"pending\"" "$STATE_FILE")
    if [[ "$status" != "complete" ]]; then
      FIRST_PHASE="$p"
      break
    fi
  done
  echo "🔄 Resuming from phase $FIRST_PHASE"
fi

state_update --arg status "in_progress" '.status = $status' "$STATE_FILE"

PIPELINE_START=$(date +%s)

for phase in "${PHASES[@]}"; do
  if [[ "$phase" -lt "$FIRST_PHASE" ]]; then
    continue
  fi

  if declare -f check_cost_cap >/dev/null 2>&1; then
    check_cost_cap "${MAX_COST:-}" || decoder_handle_cost_cap_exit "$phase"
  fi

  show_progress_dashboard "$STATE_FILE"

  if ! run_phase "$phase"; then
    echo ""
    echo "❌ Pipeline stopped at Phase $phase"
    echo "   Resume with: $0 $SYSTEM_SLUG brownfield $MAX_ITERATIONS"

    state_update --arg status "failed" '.status = $status' "$STATE_FILE"
    exit 1
  fi
done

# ═══════════════════════════════════════════════════════════════
# PIPELINE COMPLETE
# ═══════════════════════════════════════════════════════════════

PIPELINE_END=$(date +%s)
PIPELINE_DURATION=$(( PIPELINE_END - PIPELINE_START ))

# Propagate degraded phases to state.json (Story 101.10 AC11)
if [[ -n "${PHASES_DEGRADED:-}" ]]; then
  _degraded_json=$(echo "$PHASES_DEGRADED" | tr ',' '\n' | jq -R . | jq -s .)
  state_update \
    --arg ts "$(date -Iseconds)" \
    --argjson dur "$PIPELINE_DURATION" \
    --argjson degraded "$_degraded_json" \
    '.status = "completed" | .completed_at = $ts | .pipeline_duration_seconds = $dur | .degraded_phases = $degraded' \
    "$STATE_FILE"
else
  state_update \
    --arg ts "$(date -Iseconds)" \
    --argjson dur "$PIPELINE_DURATION" \
    '.status = "completed" | .completed_at = $ts | .pipeline_duration_seconds = $dur' \
    "$STATE_FILE"
fi

show_progress_dashboard "$STATE_FILE"

echo "═══════════════════════════════════════"
echo "🎉 Domain Decoder Pipeline COMPLETE!"
echo "═══════════════════════════════════════"
echo "   System:   $SYSTEM_SLUG"
echo "   Duration: ${PIPELINE_DURATION}s"
echo "   Model:    $MODEL_DEFAULT"
echo "   Runtime:  $SELECTED_RUNTIME"
echo "   Output:   $SYSTEM_DIR/"
echo ""
echo "   Deliverables:"
echo "   📋 $SYSTEM_DIR/validation/rule-catalog.md"
echo "   📊 $SYSTEM_DIR/validation/traceability-matrix.yaml"
echo "   ✅ $SYSTEM_DIR/validation/sbvr-validation.md"
echo "═══════════════════════════════════════"
