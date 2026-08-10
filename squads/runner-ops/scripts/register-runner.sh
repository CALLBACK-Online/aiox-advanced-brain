#!/usr/bin/env bash
# register-runner.sh — Runner-Ops Squad
# Registers or updates runners in the canonical runner-lib registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="${RUNNER_OPS_REPO_ROOT:-$(cd "$SQUAD_DIR/../.." && pwd)}"
REGISTRY_FILE="${RUNNER_OPS_REGISTRY_FILE:-$REPO_ROOT/infrastructure/scripts/runner-lib/runner-registry.yaml}"

ACTION=""
RUNNER_ID=""
RUNNER_PATH=""
RUNNER_SQUAD=""
RUNNER_PURPOSE=""
RUNNER_TYPE="pipeline"
RUNNER_SCORE=""
RUNNER_LEVEL="minimal"
RUNNER_OUTPUTS_DIR=""
RUNNER_METRICS_GLOB=""
RUNNER_RUNS_DIR=""

show_help() {
  cat <<EOF
register-runner.sh — Manage canonical runner registry

Usage:
  $(basename "$0") --name <id> --path <path> --squad <squad> --purpose "<text>"
  $(basename "$0") --name <id> --update [--score <N>] [--level <minimal|partial|full>]
  $(basename "$0") --list
  $(basename "$0") --remove <id>

Register flags:
  --name          Runner identifier (canonical registry id)
  --path          Repo-relative path to runner script
  --squad         Owning squad slug
  --purpose       One-line description
  --type          pipeline | validator (default: pipeline)
  --score         Compliance score 0-100
  --level         minimal | partial | full (default: minimal)
  --outputs-dir   Repo-relative outputs root for the runner
  --metrics-glob  Repo-relative glob for metrics.jsonl discovery
  --runs-dir      Repo-relative runs root for the runner

Canonical registry: $REGISTRY_FILE
EOF
}

ensure_registry() {
  [[ -f "$REGISTRY_FILE" ]] || {
    echo "ERROR: canonical registry not found: $REGISTRY_FILE" >&2
    exit 1
  }
}

cmd_list() {
  ensure_registry
  python3 - "$REGISTRY_FILE" <<'PY'
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

data = yaml.safe_load(Path(sys.argv[1]).read_text()) or {}
runners = data.get("runners", [])

if not runners:
    print("  (registry vazio)")
    sys.exit(0)

print()
print(f"  {'ID':<20} {'Squad':<18} {'Type':<10} {'Level':<8} {'Score':>6}  Path")
print("  " + "─" * 94)
for runner in runners:
    score = runner.get("compliance_score")
    score_str = ("—" if score is None else str(score)).rjust(5)
    print(
        f"  {runner.get('id',''):<20} {runner.get('squad',''):<18} {runner.get('type',''):<10} "
        f"{runner.get('integration_score','minimal'):<8} {score_str}/100  {runner.get('path','')}"
    )
print(f"\n  Total: {len(runners)} runner(s)")
print()
PY
}

cmd_register() {
  ensure_registry

  if [[ -z "$RUNNER_ID" || -z "$RUNNER_PATH" || -z "$RUNNER_SQUAD" || -z "$RUNNER_PURPOSE" ]]; then
    echo "ERROR: --name, --path, --squad e --purpose são obrigatórios" >&2
    exit 1
  fi

  local absolute_runner_path="$REPO_ROOT/$RUNNER_PATH"
  [[ -f "$absolute_runner_path" ]] || {
    echo "ERROR: runner not found: $RUNNER_PATH" >&2
    exit 1
  }

  [[ -n "$RUNNER_OUTPUTS_DIR" ]] || RUNNER_OUTPUTS_DIR="outputs/$RUNNER_SQUAD"
  [[ -n "$RUNNER_METRICS_GLOB" ]] || RUNNER_METRICS_GLOB="$RUNNER_OUTPUTS_DIR/**/metrics.jsonl"
  [[ -n "$RUNNER_RUNS_DIR" ]] || RUNNER_RUNS_DIR="$RUNNER_OUTPUTS_DIR"

  python3 - "$REGISTRY_FILE" "$REPO_ROOT" "$RUNNER_ID" "$RUNNER_PATH" "$RUNNER_SQUAD" "$RUNNER_PURPOSE" "$RUNNER_TYPE" "$RUNNER_LEVEL" "$RUNNER_SCORE" "$RUNNER_OUTPUTS_DIR" "$RUNNER_METRICS_GLOB" "$RUNNER_RUNS_DIR" <<'PY'
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

(
    registry_file,
    repo_root,
    runner_id,
    runner_path,
    runner_squad,
    runner_purpose,
    runner_type,
    runner_level,
    runner_score,
    outputs_dir,
    metrics_glob,
    runs_dir,
) = sys.argv[1:]

registry_path = Path(registry_file)
data = yaml.safe_load(registry_path.read_text()) or {"version": "1.0.0", "runners": []}
runners = data.setdefault("runners", [])

if any(r.get("id") == runner_id for r in runners):
    print(f"ERROR: runner '{runner_id}' já existe no registry")
    sys.exit(1)

content = (Path(repo_root) / runner_path).read_text(encoding="utf-8", errors="ignore")

entry = {
    "id": runner_id,
    "path": runner_path,
    "squad": runner_squad,
    "type": runner_type,
    "outputs_dir": outputs_dir,
    "metrics_glob": metrics_glob,
    "runs_dir": runs_dir,
    "uses_run_llm_prompt": bool(re.search(r"RUNNER_LIB_RUNTIME=true|\brun_llm_prompt\b", content)),
    "uses_state_manager": bool(re.search(r"\bstate_(init|update|phase_update|complete)\b", content)),
    "uses_metrics": bool(re.search(r"\brecord_metrics\b|METRICS_FILE=", content)),
    "uses_session_mgr": bool(re.search(r"\bsession_(start|end)\b|SESSION_TRACKING=true", content)),
    "uses_cascade": bool(re.search(r"\bcascade_run\b", content)),
    "integration_score": runner_level,
    "purpose": runner_purpose,
}

if runner_score:
    entry["compliance_score"] = int(runner_score)

runners.append(entry)
registry_path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))
print(f"Registered: {runner_id} -> {registry_file}")
PY
}

cmd_update() {
  ensure_registry

  [[ -n "$RUNNER_ID" ]] || {
    echo "ERROR: --name é obrigatório para --update" >&2
    exit 1
  }

  python3 - "$REGISTRY_FILE" "$RUNNER_ID" "$RUNNER_LEVEL" "$RUNNER_SCORE" <<'PY'
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

registry_file, runner_id, runner_level, runner_score = sys.argv[1:]
registry_path = Path(registry_file)
data = yaml.safe_load(registry_path.read_text()) or {"runners": []}

updated = False
for runner in data.get("runners", []):
    if runner.get("id") != runner_id:
        continue
    if runner_level:
      runner["integration_score"] = runner_level
    if runner_score:
      runner["compliance_score"] = int(runner_score)
    updated = True
    break

if not updated:
    print(f"ERROR: runner '{runner_id}' não encontrado")
    sys.exit(1)

registry_path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))
print(f"Updated: {runner_id}")
PY
}

cmd_remove() {
  ensure_registry

  [[ -n "$RUNNER_ID" ]] || {
    echo "ERROR: runner id obrigatório para --remove" >&2
    exit 1
  }

  python3 - "$REGISTRY_FILE" "$RUNNER_ID" <<'PY'
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

registry_file, runner_id = sys.argv[1:]
registry_path = Path(registry_file)
data = yaml.safe_load(registry_path.read_text()) or {"runners": []}

before = len(data.get("runners", []))
data["runners"] = [runner for runner in data.get("runners", []) if runner.get("id") != runner_id]
after = len(data["runners"])

if before == after:
    print(f"ERROR: runner '{runner_id}' não encontrado")
    sys.exit(1)

registry_path.write_text(yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False))
print(f"Removed: {runner_id}")
PY
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --list)          ACTION="list"; shift ;;
      --update)        ACTION="update"; shift ;;
      --remove)        ACTION="remove"; RUNNER_ID="${2:-}"; shift 2 ;;
      --name)          RUNNER_ID="${2:-}"; shift 2 ;;
      --path)          RUNNER_PATH="${2:-}"; shift 2 ;;
      --squad)         RUNNER_SQUAD="${2:-}"; shift 2 ;;
      --purpose)       RUNNER_PURPOSE="${2:-}"; shift 2 ;;
      --type)          RUNNER_TYPE="${2:-}"; shift 2 ;;
      --score)         RUNNER_SCORE="${2:-}"; shift 2 ;;
      --level)         RUNNER_LEVEL="${2:-}"; shift 2 ;;
      --outputs-dir)   RUNNER_OUTPUTS_DIR="${2:-}"; shift 2 ;;
      --metrics-glob)  RUNNER_METRICS_GLOB="${2:-}"; shift 2 ;;
      --runs-dir)      RUNNER_RUNS_DIR="${2:-}"; shift 2 ;;
      --help|-h)       show_help; exit 0 ;;
      *)               echo "Unknown flag: $1" >&2; show_help; exit 1 ;;
    esac
  done

  if [[ -z "$ACTION" ]]; then
    if [[ -n "$RUNNER_ID" && -n "$RUNNER_PATH" ]]; then
      ACTION="register"
    else
      show_help
      exit 1
    fi
  fi
}

main() {
  parse_args "$@"

  case "$ACTION" in
    list)     cmd_list ;;
    register) cmd_register ;;
    update)   cmd_update ;;
    remove)   cmd_remove ;;
  esac
}

main "$@"
