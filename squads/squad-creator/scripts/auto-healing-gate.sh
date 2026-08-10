#!/usr/bin/env bash
# auto-healing-gate.sh — Run auto-healing gate checks across squads
# Migrated from kaizen squad (STORY-108.3).
# Usage: bash scripts/auto-healing-gate.sh [--all]
set -euo pipefail

SQUADS_DIR="squads"
echo "=== Auto-Healing Gate ==="

check_count=0
pass_count=0
needs_review=0

for config in "$SQUADS_DIR"/*/config.yaml; do
  squad_dir=$(dirname "$config")
  squad_name=$(basename "$squad_dir")
  check_count=$((check_count + 1))

  # Check 1: config.yaml is valid YAML
  if node -e "require('js-yaml').load(require('fs').readFileSync('$config'))" 2>/dev/null; then
    config_ok=true
  else
    config_ok=false
    echo "  FAIL: $squad_name — config.yaml invalid YAML"
    needs_review=$((needs_review + 1))
    continue
  fi

  # Check 2: entry_agent exists
  entry_agent=$(node -e "const y=require('js-yaml').load(require('fs').readFileSync('$config'));console.log(y.entry_agent||'')" 2>/dev/null)
  if [ -n "$entry_agent" ] && [ -f "$squad_dir/agents/$entry_agent.md" ]; then
    agent_ok=true
  else
    agent_ok=false
    echo "  WARN: $squad_name — entry_agent '$entry_agent' missing"
    needs_review=$((needs_review + 1))
    continue
  fi

  pass_count=$((pass_count + 1))
done

echo ""
echo "Summary: checked=$check_count pass=$pass_count needs_review=$needs_review"

if [ "$needs_review" -gt 0 ]; then
  echo "Result: NEEDS_REVIEW"
else
  echo "Result: PASS"
fi

echo "=== Gate Complete ==="
