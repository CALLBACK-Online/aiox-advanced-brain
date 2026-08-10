#!/usr/bin/env bash
set -euo pipefail

report_path="${1:-}"
if [[ -z "$report_path" ]]; then
  echo "usage: publish-autonomy-report.sh <report-path>" >&2
  exit 1
fi

echo "report_path=${report_path}"
