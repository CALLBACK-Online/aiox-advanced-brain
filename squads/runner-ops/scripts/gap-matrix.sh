#!/usr/bin/env bash
# gap-matrix.sh — Runner-Ops Squad
# Generates a comparative gap matrix for all registered runners using live data
# from validate-runner.sh --all --json.
#
# Output: outputs/runner-ops/gap-matrix/latest.json (+ timestamped copy)
#
# Usage:
#   ./gap-matrix.sh              Generate matrix and save to outputs/
#   ./gap-matrix.sh --stdout     Print to stdout only (no file save)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${RUNNER_OPS_REPO_ROOT:-$(cd "$SCRIPT_DIR/../../.." && pwd)}"
OUTPUT_DIR="$REPO_ROOT/outputs/runner-ops/gap-matrix"
VALIDATE_SCRIPT="$SCRIPT_DIR/validate-runner.sh"

STDOUT_ONLY="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --stdout) STDOUT_ONLY="true"; shift ;;
    --help|-h)
      echo "gap-matrix.sh — Generate comparative runner gap matrix from live data"
      echo ""
      echo "Usage:"
      echo "  $(basename "$0")            Generate matrix, save to outputs/runner-ops/gap-matrix/"
      echo "  $(basename "$0") --stdout   Print JSON to stdout only"
      exit 0
      ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -x "$VALIDATE_SCRIPT" && ! -f "$VALIDATE_SCRIPT" ]]; then
  echo "ERROR: validate-runner.sh not found at $VALIDATE_SCRIPT" >&2
  exit 1
fi

# Run validate-runner.sh --all --json to get live data
stderr_file=$(mktemp)
raw_json=$(bash "$VALIDATE_SCRIPT" --all --json 2>"$stderr_file") || {
  echo "ERROR: validate-runner.sh failed:" >&2
  cat "$stderr_file" >&2
  rm -f "$stderr_file"
  exit 1
}
rm -f "$stderr_file"

# Transform into comparative gap matrix
matrix_json=$(python3 - "$raw_json" <<'PY'
import json
import sys
from datetime import datetime, timezone

raw = json.loads(sys.argv[1])

# Extract unique check names in order from first runner
check_names = []
if raw:
    for check in raw[0].get("checks", []):
        name = check.get("code", check.get("name", "unknown"))
        if name not in check_names:
            check_names.append(name)

# Build matrix: runner_id -> {check_code: passed}
matrix = {}
runner_summary = []

for runner in raw:
    rid = runner["id"]
    checks_map = {}
    for check in runner.get("checks", []):
        code = check.get("code", check.get("name", "unknown"))
        checks_map[code] = {
            "passed": check["passed"],
            "severity": check["severity"],
            "name": check.get("name", code),
        }
    matrix[rid] = checks_map
    runner_summary.append({
        "id": rid,
        "squad": runner.get("squad", "unknown"),
        "type": runner.get("type", "unknown"),
        "score": runner.get("score", 0),
        "integration_score": runner.get("integration_score", "unknown"),
        "errors": len(runner.get("errors", [])),
        "warnings": len(runner.get("warnings", [])),
    })

# Build the comparative table (check_code x runner_id)
comparative = {}
for code in check_names:
    row = {}
    for runner in raw:
        rid = runner["id"]
        entry = matrix.get(rid, {}).get(code, {})
        row[rid] = "PASS" if entry.get("passed", False) else "FAIL"
    comparative[code] = row

# Sort runners by score ascending (worst first = highest priority)
runner_summary.sort(key=lambda r: r["score"])

# Priority list: runners sorted by gap severity
priority = []
for rs in runner_summary:
    if rs["score"] < 100:
        priority.append({
            "runner_id": rs["id"],
            "score": rs["score"],
            "integration_score": rs["integration_score"],
            "gap_count": rs["errors"] + rs["warnings"],
        })

avg_score = sum(r["score"] for r in runner_summary) // len(runner_summary) if runner_summary else 0

output = {
    "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "source": "validate-runner.sh --all --json",
    "total_runners": len(raw),
    "average_score": avg_score,
    "check_codes": check_names,
    "runners": runner_summary,
    "comparative_matrix": comparative,
    "migration_priority": priority,
}

print(json.dumps(output, indent=2))
PY
)

if [[ "$STDOUT_ONLY" == "true" ]]; then
  echo "$matrix_json"
  exit 0
fi

# Save to outputs
mkdir -p "$OUTPUT_DIR"

echo "$matrix_json" > "$OUTPUT_DIR/latest.json"

timestamp=$(date +%Y%m%d-%H%M%S)
echo "$matrix_json" > "$OUTPUT_DIR/gap-matrix-${timestamp}.json"

# Print summary and comparative table
python3 - "$OUTPUT_DIR/latest.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1]))
runners = [r["id"] for r in data["runners"]]
checks = data["check_codes"]
matrix = data["comparative_matrix"]

print()
print(f"Gap Matrix generated for {data['total_runners']} runners (avg score: {data['average_score']}/100)")
print()

# Header
header = f"{'Check':<12}"
for rid in runners:
    header += f" {rid:<16}"
print(header)
print("-" * len(header))

# Rows
for code in checks:
    row = f"{code:<12}"
    for rid in runners:
        val = matrix.get(code, {}).get(rid, "?")
        row += f" {val:<16}"
    print(row)

print()
print("Migration Priority (worst first):")
for p in data["migration_priority"]:
    print(f"  {p['runner_id']:<18} score={p['score']:>3}/100  level={p['integration_score']:<8}  gaps={p['gap_count']}")
PY

echo ""
echo "Saved: outputs/runner-ops/gap-matrix/latest.json"
echo "Saved: outputs/runner-ops/gap-matrix/gap-matrix-${timestamp}.json"
