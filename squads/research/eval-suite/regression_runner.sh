#!/usr/bin/env bash
# regression_runner.sh — Research eval-suite regression check (skeleton)
#
# Story: STORY-RA-0.2
# Version: 1.0.0
# Scope: SKELETON. Runs llm_judge on a fixture, compares to its baseline, exits 0/1.
#
# Usage:
#   ./regression_runner.sh --fixture <fixture-dir> [--baseline <score>] [--threshold <pts>] [--dry-run]
#
# Exit codes:
#   0 — No regression (score >= baseline - threshold)
#   1 — Regression detected (score < baseline - threshold)
#   2 — Usage/setup error
#
# The fixture-dir must contain at least one research file (README.md or 02-research-report.md).
# --baseline defaults to reading {fixture-dir}/.baseline_score (integer) if the file exists.
# --threshold defaults to 5 (per AC-4: exit 1 when score < baseline - 5pts).
#
# Example:
#   ./regression_runner.sh \
#     --fixture squads/research/eval-suite/fixtures/high-quality \
#     --baseline 82 \
#     --dry-run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JUDGE="${SCRIPT_DIR}/llm_judge.py"

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------
FIXTURE_DIR=""
BASELINE=""
THRESHOLD=5
DRY_RUN=false

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --fixture)
      FIXTURE_DIR="$2"; shift 2 ;;
    --baseline)
      BASELINE="$2"; shift 2 ;;
    --threshold)
      THRESHOLD="$2"; shift 2 ;;
    --dry-run)
      DRY_RUN=true; shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \?//' | head -30
      exit 0 ;;
    *)
      echo "ERROR: Unknown argument: $1" >&2; exit 2 ;;
  esac
done

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [[ -z "$FIXTURE_DIR" ]]; then
  echo "ERROR: --fixture is required." >&2
  exit 2
fi

if [[ ! -d "$FIXTURE_DIR" ]]; then
  echo "ERROR: Fixture directory not found: $FIXTURE_DIR" >&2
  exit 2
fi

if [[ ! -f "$JUDGE" ]]; then
  echo "ERROR: llm_judge.py not found at $JUDGE" >&2
  exit 2
fi

# Auto-detect Python 3
PYTHON=""
for p in python3 python; do
  if command -v "$p" >/dev/null 2>&1 && "$p" -c "import sys; exit(0 if sys.version_info[0] >= 3 else 1)"; then
    PYTHON="$p"
    break
  fi
done
if [[ -z "$PYTHON" ]]; then
  echo "ERROR: Python 3 not found in PATH." >&2
  exit 2
fi

# Resolve baseline: flag > .baseline_score file > error
BASELINE_FILE="${FIXTURE_DIR}/.baseline_score"
if [[ -z "$BASELINE" ]]; then
  if [[ -f "$BASELINE_FILE" ]]; then
    BASELINE=$(cat "$BASELINE_FILE" | tr -d '[:space:]')
  else
    echo "ERROR: --baseline not provided and ${BASELINE_FILE} not found." >&2
    exit 2
  fi
fi

if ! [[ "$BASELINE" =~ ^[0-9]+$ ]] || [[ "$BASELINE" -lt 0 ]] || [[ "$BASELINE" -gt 100 ]]; then
  echo "ERROR: baseline must be an integer 0-100, got: '$BASELINE'" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
echo "======================================================================"
echo " Research Eval-Suite — Regression Runner"
echo "======================================================================"
echo " Fixture   : $FIXTURE_DIR"
echo " Baseline  : $BASELINE pts"
echo " Threshold : -$THRESHOLD pts"
echo " Min pass  : $((BASELINE - THRESHOLD)) pts"
echo " Dry-run   : $DRY_RUN"
echo "----------------------------------------------------------------------"

# ---------------------------------------------------------------------------
# Run judge
# ---------------------------------------------------------------------------
JUDGE_ARGS=("--research-dir" "$FIXTURE_DIR")
if $DRY_RUN; then
  JUDGE_ARGS+=("--dry-run")
fi

echo "Running llm_judge.py..."
JUDGE_OUTPUT=$("$PYTHON" "$JUDGE" "${JUDGE_ARGS[@]}" 2>&1) || {
  echo "ERROR: llm_judge.py failed:"
  echo "$JUDGE_OUTPUT"
  exit 2
}

# Extract total score from output (last JSON block or "Total score:" line)
SCORE=""
if echo "$JUDGE_OUTPUT" | grep -q '"total":'; then
  # BSD grep (macOS) compatible: extract digits after "total":
  SCORE=$(echo "$JUDGE_OUTPUT" | grep '"total":' | head -1 | grep -oE '[0-9]+' | tail -1)
fi
if [[ -z "$SCORE" ]]; then
  SCORE=$(echo "$JUDGE_OUTPUT" | grep "Total score:" | grep -oE '[0-9]+' | head -1)
fi

if [[ -z "$SCORE" ]] || ! [[ "$SCORE" =~ ^[0-9]+$ ]]; then
  echo "ERROR: Could not extract score from judge output:"
  echo "$JUDGE_OUTPUT" | tail -20
  exit 2
fi

# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------
MIN_PASS=$((BASELINE - THRESHOLD))
echo ""
echo "Judge output (summary):"
echo "$JUDGE_OUTPUT" | grep -E '"total":|Total score:|"coverage":|"citation_quality":|"claim_verifiability":|"narrative_coherence":|"actionability":' | head -10
echo ""
echo "======================================================================"
echo " Score    : $SCORE / 100"
echo " Baseline : $BASELINE / 100"
echo " Min pass : $MIN_PASS / 100"

if [[ "$SCORE" -ge "$MIN_PASS" ]]; then
  echo " Result   : PASS — no regression (${SCORE} >= ${MIN_PASS})"
  echo "======================================================================"
  exit 0
else
  DELTA=$((MIN_PASS - SCORE))
  echo " Result   : FAIL — REGRESSION DETECTED"
  echo "            Score dropped $DELTA pts below acceptable floor."
  echo "            Current: $SCORE  |  Floor: $MIN_PASS  |  Baseline: $BASELINE"
  echo "======================================================================"
  exit 1
fi
