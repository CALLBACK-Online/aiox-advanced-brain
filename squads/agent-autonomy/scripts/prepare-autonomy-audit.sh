#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
source "$REPO_ROOT/infrastructure/scripts/runner-lib/runtime-paths.sh"
OUTPUTS_ROOT="$(resolve_outputs_root "$REPO_ROOT")"
if [[ -z "$target" ]]; then
  echo "usage: prepare-autonomy-audit.sh <agent-or-squad-path>" >&2
  exit 1
fi

mkdir -p "$OUTPUTS_ROOT/aiox-squad/agent-autonomy"
echo "audit_target=${target}"
