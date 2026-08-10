#!/bin/bash
set -euo pipefail

MISSION_HANDOFF="${1:-}"
if [[ -z "$MISSION_HANDOFF" ]]; then
  echo "Uso: $0 <mission-clickup-handoff.yaml>" >&2
  exit 1
fi

echo "[clickup-ops] materializing mission from $MISSION_HANDOFF"
echo "[clickup-ops] service_ref=services/clickup/materialize-mission.js"
echo "[clickup-ops] status=delegated_to_runtime"
