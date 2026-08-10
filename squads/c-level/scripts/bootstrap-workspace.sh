#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "bootstrap-workspace.sh: compat wrapper -> bootstrap-c-level-workspace.sh"
exec "${SCRIPT_DIR}/bootstrap-c-level-workspace.sh" "$@"
