#!/usr/bin/env bash
# audit-autonomy.sh — Audit autonomy levels of all squads in ecosystem
# Migrated from kaizen squad (STORY-108.3). Renamed from kaizen-audit-autonomy.sh.
# Usage: bash scripts/audit-autonomy.sh
set -euo pipefail

SQUADS_DIR="${1:-squads}"
echo "=== Autonomy Audit ==="
echo "Scanning: $SQUADS_DIR"

for config in "$SQUADS_DIR"/*/config.yaml; do
  squad_dir=$(dirname "$config")
  squad_name=$(basename "$squad_dir")

  # Check for entry_agent, workflows, and scripts as autonomy indicators
  agent_count=$(find "$squad_dir/agents" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  workflow_count=$(find "$squad_dir/workflows" -name "*.yaml" 2>/dev/null | wc -l | tr -d ' ')
  script_count=$(find "$squad_dir/scripts" -name "*.sh" -o -name "*.py" -o -name "*.js" 2>/dev/null | wc -l | tr -d ' ')

  # Autonomy score: basic heuristic
  autonomy=0
  [ "$agent_count" -ge 1 ] && autonomy=$((autonomy + 30))
  [ "$workflow_count" -ge 3 ] && autonomy=$((autonomy + 30))
  [ "$script_count" -ge 2 ] && autonomy=$((autonomy + 20))

  # Check for quality gates
  if grep -q "quality_gates" "$config" 2>/dev/null; then
    autonomy=$((autonomy + 20))
  fi

  echo "  $squad_name: agents=$agent_count workflows=$workflow_count scripts=$script_count autonomy=$autonomy%"
done

echo "=== Audit Complete ==="
