#!/bin/bash
set -euo pipefail

REPORT_PATH="${1:-}"
if [[ -z "$REPORT_PATH" ]]; then
  echo "Uso: $0 <materialization-report.md>" >&2
  exit 1
fi

echo "[clickup-ops] publishing report $REPORT_PATH"
echo "[clickup-ops] service_ref=services/google-drive/docs.js"
echo "[clickup-ops] status=delegated_to_runtime"
