#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${SQUAD_DIR}/../.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-${REPO_ROOT}/workspace}"

created_dirs=0
warnings=0

declare -a REQUIRED_DIRS=(
  "${WORKSPACE_ROOT}"
  "${WORKSPACE_ROOT}/_system"
  "${WORKSPACE_ROOT}/businesses"
  "${WORKSPACE_ROOT}/_templates"
  "${WORKSPACE_ROOT}/_templates/business-template"
  "${WORKSPACE_ROOT}/scripts"
  "${REPO_ROOT}/docs/qa/workspace-health"
)

for dir in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "${dir}" ]]; then
    mkdir -p "${dir}"
    created_dirs=$((created_dirs + 1))
    echo "created_dir: ${dir}"
  fi
done

declare -a REQUIRED_FILES=(
  "${WORKSPACE_ROOT}/_system/config.yaml"
  "${WORKSPACE_ROOT}/scripts/scaffold-workspace.js"
  "${WORKSPACE_ROOT}/scripts/scan-document-inventory.js"
  "${WORKSPACE_ROOT}/_templates/business-template/README.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "${file}" ]]; then
    warnings=$((warnings + 1))
    echo "warning: missing workspace essential ${file}"
  fi
done

echo "bootstrap-c-level-workspace: created_dirs=${created_dirs} warnings=${warnings}"
