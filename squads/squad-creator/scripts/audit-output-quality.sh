#!/usr/bin/env bash
# audit-output-quality.sh — Audit output quality of squad-generated artifacts
# Migrated from kaizen squad (STORY-108.3). Renamed from kaizen-audit-output-quality.sh.
# Usage: bash scripts/audit-output-quality.sh [squad-name] [output-type]
set -euo pipefail

SQUAD_NAME="${1:-}"
OUTPUT_TYPE="${2:-}"
OUTPUTS_DIR="outputs"

echo "=== Output Quality Audit ==="
if [ -n "$SQUAD_NAME" ]; then
  echo "Squad: $SQUAD_NAME"
  SCAN_DIR="$OUTPUTS_DIR/$SQUAD_NAME"
else
  echo "Scope: all squads"
  SCAN_DIR="$OUTPUTS_DIR"
fi

if [ ! -d "$SCAN_DIR" ]; then
  echo "WARN: No outputs found at $SCAN_DIR"
  exit 0
fi

total=0
with_yaml=0
with_content=0
empty=0

for file in $(find "$SCAN_DIR" -type f \( -name "*.md" -o -name "*.yaml" \) 2>/dev/null | head -50); do
  total=$((total + 1))
  size=$(wc -c < "$file" | tr -d ' ')

  if [ "$size" -lt 10 ]; then
    empty=$((empty + 1))
    echo "  EMPTY: $file ($size bytes)"
  elif echo "$file" | grep -q "\.yaml$"; then
    with_yaml=$((with_yaml + 1))
  else
    with_content=$((with_content + 1))
  fi
done

echo ""
echo "Summary: total=$total yaml=$with_yaml markdown=$with_content empty=$empty"

if [ "$total" -gt 0 ]; then
  quality_pct=$(( (total - empty) * 100 / total ))
  echo "Quality: ${quality_pct}% non-empty"
else
  echo "Quality: N/A (no outputs found)"
fi

echo "=== Audit Complete ==="
