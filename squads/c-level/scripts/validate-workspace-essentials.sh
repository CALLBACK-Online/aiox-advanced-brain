#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "validate-workspace-essentials.sh: compat wrapper legado -> validate-c-level-essentials.sh"
exec "${SCRIPT_DIR}/validate-c-level-essentials.sh" "$@"
