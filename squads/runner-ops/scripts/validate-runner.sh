#!/usr/bin/env bash
# validate-runner.sh — Runner-Ops Squad
# Validates runner-lib integration compliance for one or all registered runners.
#
# Reads from:  infrastructure/scripts/runner-lib/runner-registry.yaml  (canonical)
# Writes to:   outputs/runner-ops/validation/                           (reports)
# Updates:     infrastructure/scripts/runner-lib/runner-registry.yaml  (scores, via --update-registry)
#
# Self-contained pack: script lives in runner-ops, but targets canonical runtime assets.
# Runners validated by this script are NOT modified — only the registry entry is updated.
#
# Usage:
#   ./validate-runner.sh <path/to/runner.sh>
#   ./validate-runner.sh --all [--verbose] [--json] [--update-registry] [--strict]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${RUNNER_OPS_REPO_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
REGISTRY_FILE="${RUNNER_OPS_REGISTRY_FILE:-$REPO_ROOT/infrastructure/scripts/runner-lib/runner-registry.yaml}"
REPORTS_DIR="${RUNNER_OPS_REPORTS_DIR:-$REPO_ROOT/outputs/runner-ops/validation}"

TARGET_PATH=""
VALIDATE_ALL="false"
OUTPUT_JSON="false"
VERBOSE="false"
UPDATE_REGISTRY="false"
STRICT="false"

show_help() {
  cat <<EOF
validate-runner.sh — Runner-Ops compliance checker

Usage:
  $(basename "$0") <path>                      Validate one runner (by path)
  $(basename "$0") --all                       Validate all runners in registry
  $(basename "$0") --all --verbose             Show per-check details
  $(basename "$0") --all --json                JSON output
  $(basename "$0") --all --update-registry     Write scores back to registry
  $(basename "$0") --all --strict              Exit 1 on any error (CI mode)

Registry (canonical): $REGISTRY_FILE
Reports output:       $REPORTS_DIR/
EOF
}

registry_rows() {
  [[ -f "$REGISTRY_FILE" ]] || { echo "ERROR: registry not found: $REGISTRY_FILE" >&2; exit 1; }
  node - "$REGISTRY_FILE" <<'NODE'
const fs = require("fs");
const yaml = require("js-yaml");
const data = yaml.load(fs.readFileSync(process.argv[2], "utf8")) || {};
for (const r of data.runners || []) {
  if (r.path) console.log([r.id || "", r.path, r.squad || "", r.type || "pipeline"].join("\t"));
}
NODE
}

validate_one() {
  local runner_id="$1"
  local path="$2"
  local squad="$3"
  local runner_type="$4"

  python3 - "$REPO_ROOT" "$path" "$runner_id" "$squad" "$runner_type" <<'PY'
import json, re, sys
from pathlib import Path

repo_root = Path(sys.argv[1])
raw_path = Path(sys.argv[2])
path = raw_path if raw_path.is_absolute() else repo_root / raw_path
runner_id, squad, runner_type = sys.argv[3], sys.argv[4], sys.argv[5]

result = {
    "id": runner_id, "path": str(path), "squad": squad, "type": runner_type,
    "checks": [], "errors": [], "warnings": [], "info": [],
    "score": 0, "integration_score": "minimal"
}

if not path.exists():
    result["errors"].append(f"File not found: {path}")
    print(json.dumps(result)); sys.exit(0)

content = path.read_text(encoding="utf-8", errors="ignore")
claude_lines = [l.strip() for l in content.splitlines() if "claude " in l and "-p" in l]

def chk(name, passed, sev, detail, code):
    result["checks"].append({"code": code, "name": name, "passed": passed, "severity": sev, "detail": detail})
    if not passed:
        (result["errors"] if sev == "error" else result["warnings"] if sev == "warning" else result["info"]).append(f"[{code}] {detail}")

# LAYER 1 — CRITICAL (−15 each)
chk("bootstrap",           bool(re.search(r"pipeline-bootstrap\.sh|loader\.sh", content)),                         "error",   "Must source pipeline-bootstrap.sh or loader.sh",               "C001")
chk("run_llm_prompt",      bool(re.search(r"RUNNER_LIB_RUNTIME=true|\brun_llm_prompt\b", content)),                "error",   "Must use run_llm_prompt() — no direct LLM CLI calls",           "C002")
chk("no_hardcoded_claude", not bool(re.search(r"(^|\s)claude\s+-p\b", content, re.MULTILINE)),                     "error",   "Contains hardcoded `claude -p` (use run_llm_prompt)",           "C003")
chk("trap_exit",           bool(re.search(r"trap\s+.*\bEXIT\b", content)),                                         "error",   "Must declare `trap cleanup EXIT` for crash safety",             "C004")
chk("metrics_file",        bool(re.search(r"METRICS_FILE=|export METRICS_FILE", content)),                         "error",   "Must export METRICS_FILE",                                      "C005")
chk("cost_cap",            bool(re.search(r"\bcheck_cost_cap\b", content)),                                        "error",   "Must call check_cost_cap() to enforce budget",                  "C006")
chk("permissions_flag",    all("--dangerously-skip-permissions" in l for l in claude_lines) if claude_lines else True,
                                                                                                                    "error",   "All claude calls must use --dangerously-skip-permissions",      "C007")

# LAYER 2 — HIGH (−8 each)
chk("state_manager",  bool(re.search(r"\bstate_(init|update|phase_update|complete|add_artifact)\b", content)), "warning", "Must use state_init/phase_update for crash-resume",  "H001")
chk("session_mgr",    bool(re.search(r"\bsession_(start|end)\b|SESSION_TRACKING=true", content)),              "warning", "Should use session_start/session_end lifecycle",      "H002")
chk("filter_output",  bool(re.search(r"\bfilter_llm_output\b", content)),                                      "warning", "Must use filter_llm_output() to strip CLI metadata",  "H003")
chk("prior_context",  bool(re.search(r"\btruncate_prior_context\b|\bread_focused_context\b", content)),        "warning", "Should use truncate_prior_context/read_focused_context","H004")

# LAYER 3 — INFO only
for name, pat, code in [
    ("cascade",   r"\bcascade_run\b",                  "W001"),
    ("hooks",     r"\bhooks_(load|run)\b",              "W002"),
    ("evaluator", r"\bevaluate_phase_output\b",         "W003"),
]:
    if not re.search(pat, content):
        result["info"].append(f"[{code}] No {name} — consider for full integration")

# Anti-pattern
if re.search(r"jq .*>\s*.*\.tmp\s*&&\s*mv", content):
    result["warnings"].append("[H005] Manual jq atomic write — use state_update() instead")

# SCORING
c_fail = sum(1 for c in result["checks"] if c["severity"] == "error"   and not c["passed"])
h_fail = sum(1 for c in result["checks"] if c["severity"] == "warning" and not c["passed"])
score  = max(0, 100 - c_fail * 15 - h_fail * 8)
result["score"] = score
result["integration_score"] = "full" if score >= 90 else "partial" if score >= 60 else "minimal"
print(json.dumps(result))
PY
}

render_results() {
  python3 - "$1" "$2" "$VERBOSE" <<'PY'
import json, sys
path, mode, verbose = sys.argv[1:4]
items = [json.loads(l) for l in open(path) if l.strip()]

if mode == "json":
    print(json.dumps(items, indent=2)); sys.exit(0)

ICON = {"full": "✅", "partial": "⚠️ ", "minimal": "❌"}
print()
print(f"  {'ID':<20} {'Score':>6}  {'Level':<8}  {'Err':>4} {'Warn':>5}  Path")
print("  " + "─" * 88)
for i in items:
    print(f"  {i['id']:<20} {i['score']:>5}/100  {ICON.get(i['integration_score'],'?')} {i['integration_score']:<7}  {len(i['errors']):>3}E  {len(i['warnings']):>4}W  {i['path']}")
    if verbose == "true":
        for c in i["checks"]:
            sym = "✓" if c["passed"] else "✗"
            print(f"    {sym} [{c['code']}] {c['name']}: {c['detail']}")
        for info in i.get("info", []):
            print(f"    → {info}")

print()
full = sum(1 for i in items if i["integration_score"] == "full")
part = sum(1 for i in items if i["integration_score"] == "partial")
mini = sum(1 for i in items if i["integration_score"] == "minimal")
avg  = sum(i["score"] for i in items) // len(items) if items else 0
print(f"  Summary: {len(items)} runners | ✅ {full} full | ⚠️  {part} partial | ❌ {mini} minimal | avg {avg}/100")
print()
PY
}

update_registry() {
  python3 - "$1" "$REGISTRY_FILE" <<'PY'
import sys, json
from pathlib import Path
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required for --update-registry"); sys.exit(1)

results_path, registry_path = sys.argv[1], sys.argv[2]
scores = {json.loads(l)["id"]: json.loads(l) for l in open(results_path) if l.strip()}

data = yaml.safe_load(Path(registry_path).read_text())
updated = 0
for runner in data.get("runners", []):
    rid = runner.get("id", "")
    if rid in scores:
        item = scores[rid]
        runner["integration_score"] = item["integration_score"]
        # Optionally persist numeric score as a new field
        runner["compliance_score"] = item["score"]
        updated += 1

Path(registry_path).write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))
print(f"Registry updated: {updated} runners → {registry_path}")
PY
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --all)             VALIDATE_ALL="true";     shift ;;
      --json)            OUTPUT_JSON="true";       shift ;;
      --verbose)         VERBOSE="true";           shift ;;
      --update-registry) UPDATE_REGISTRY="true";   shift ;;
      --strict)          STRICT="true";            shift ;;
      --help|-h)         show_help; exit 0 ;;
      *)                 TARGET_PATH="$1";         shift ;;
    esac
  done
  if [[ "$VALIDATE_ALL" != "true" && -z "$TARGET_PATH" ]]; then show_help; exit 1; fi
}

main() {
  parse_args "$@"
  mkdir -p "$REPORTS_DIR"

  local tmp; tmp="$(mktemp)"

  if [[ "$VALIDATE_ALL" == "true" ]]; then
    if [[ "$OUTPUT_JSON" != "true" ]]; then
      echo "Scanning: $REGISTRY_FILE"
    fi
    while IFS=$'\t' read -r id path squad type; do
      [[ -z "$id" ]] && continue
      if [[ "$OUTPUT_JSON" != "true" ]]; then
        echo "  → $id"
      fi
      validate_one "$id" "$path" "$squad" "$type" >> "$tmp"
    done < <(registry_rows)
  else
    validate_one "$(basename "$TARGET_PATH" .sh)" "$TARGET_PATH" "unknown" "unknown" >> "$tmp"
  fi

  local mode; [[ "$OUTPUT_JSON" == "true" ]] && mode="json" || mode="table"
  render_results "$tmp" "$mode"

  # Save JSON report
  local report="$REPORTS_DIR/validation-$(date +%Y%m%d-%H%M%S).json"
  python3 -c "
import json, sys, datetime
items = [json.loads(l) for l in open('$tmp') if l.strip()]
json.dump({'runners': items, 'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')}, open('$report','w'), indent=2)
" 
  if [[ "$OUTPUT_JSON" != "true" ]]; then
    echo "Report: $report"
  fi


  [[ "$UPDATE_REGISTRY" == "true" ]] && update_registry "$tmp"

  local has_errors
  has_errors=$(python3 -c "
import json,sys
sys.exit(1 if any(json.loads(l).get('errors') for l in open('$tmp') if l.strip()) else 0)
" && echo "false" || echo "true")

  rm -f "$tmp"
  [[ "$STRICT" == "true" && "$has_errors" == "true" ]] && exit 1 || exit 0
}

main "$@"
