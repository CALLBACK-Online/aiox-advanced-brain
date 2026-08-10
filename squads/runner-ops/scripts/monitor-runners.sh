#!/usr/bin/env bash
# monitor-runners.sh — Runner-Ops Squad
# Aggregates metrics using the canonical runner registry.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQUAD_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="${RUNNER_OPS_REPO_ROOT:-$(cd "$SQUAD_DIR/../.." && pwd)}"
REGISTRY_FILE="${RUNNER_OPS_REGISTRY_FILE:-$REPO_ROOT/infrastructure/scripts/runner-lib/runner-registry.yaml}"
REPORTS_DIR="${RUNNER_OPS_REPORTS_DIR:-$REPO_ROOT/outputs/runner-ops/health}"

TARGET_RUNNER=""
DAYS=30
OUTPUT_JSON="false"
SAVE_REPORT="false"

show_help() {
  cat <<EOF
monitor-runners.sh — Runner-Ops health dashboard

Usage:
  $(basename "$0")                        Full ecosystem dashboard (last 30d)
  $(basename "$0") --runner <id>          Single runner deep-dive
  $(basename "$0") --days <N>             Time window in days (default: 30)
  $(basename "$0") --json                 JSON output
  $(basename "$0") --report               Save JSON report to $REPORTS_DIR/

Canonical registry: $REGISTRY_FILE
EOF
}

generate_dashboard() {
  [[ -f "$REGISTRY_FILE" ]] || {
    echo "ERROR: canonical registry not found: $REGISTRY_FILE" >&2
    exit 1
  }

  python3 - "$REPO_ROOT" "$REGISTRY_FILE" "$DAYS" "$OUTPUT_JSON" "$TARGET_RUNNER" <<'PY'
import glob
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

repo_root, registry_path, days_str, output_json, target_runner = sys.argv[1:]
repo_root = Path(repo_root)
days = int(days_str)
cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)

data = yaml.safe_load(Path(registry_path).read_text()) or {}
runners = data.get("runners", [])

if target_runner:
    runners = [runner for runner in runners if runner.get("id") == target_runner]

def iter_metrics_files(runner):
    metrics_glob = runner.get("metrics_glob")
    outputs_dir = runner.get("outputs_dir")

    if metrics_glob:
        pattern = str(repo_root / metrics_glob)
        for path_str in glob.glob(pattern, recursive=True):
            yield Path(path_str)
        return

    if outputs_dir:
        base = repo_root / outputs_dir
        if base.exists():
            yield from base.rglob("metrics.jsonl")

def parse_ts(raw):
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except Exception:
        return None

runner_stats = []

for runner in runners:
    metrics = []
    metrics_files = list(iter_metrics_files(runner))

    for metrics_file in metrics_files:
        try:
            for line in metrics_file.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue

                ts = parse_ts(record.get("ts"))
                if ts and ts < cutoff:
                    continue

                metrics.append(record)
        except Exception:
            continue

    costs = [float(item.get("cost_usd", 0) or 0) for item in metrics]
    durations = [float(item.get("duration_s", 0) or 0) for item in metrics if item.get("duration_s") is not None]
    failures = [item for item in metrics if str(item.get("status", "")).lower() in {"failed", "error"}]
    unique_runs = {
        item.get("session_id") or item.get("run_id") or item.get("ts", "")[:13]
        for item in metrics
        if item.get("session_id") or item.get("run_id") or item.get("ts")
    }
    models_used = sorted({item.get("model") for item in metrics if item.get("model")})

    compliance_score = runner.get("compliance_score")
    integration_level = runner.get("integration_score", "minimal")
    run_count = len(unique_runs)

    if run_count == 0:
        health = "idle"
    elif integration_level == "minimal":
        health = "risk"
    elif len(failures) > 0:
        health = "warn"
    else:
        health = "healthy"

    runner_stats.append({
        "id": runner.get("id", ""),
        "squad": runner.get("squad", ""),
        "type": runner.get("type", ""),
        "integration_level": integration_level,
        "compliance_score": compliance_score,
        "total_cost_usd": round(sum(costs), 4),
        "estimated_runs": run_count,
        "total_phases_tracked": len(metrics),
        "avg_cost_per_run": round(sum(costs) / run_count, 4) if run_count else None,
        "avg_duration_s": round(sum(durations) / len(durations), 1) if durations else None,
        "failures": len(failures),
        "models_used": models_used,
        "metrics_files": [str(path.relative_to(repo_root)) for path in metrics_files if path.exists()],
        "health": health,
    })

summary = {
    "period_days": days,
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "total_runners": len(runner_stats),
    "total_cost_usd": round(sum(item["total_cost_usd"] for item in runner_stats), 4),
    "total_estimated_runs": sum(item["estimated_runs"] for item in runner_stats),
    "at_risk_runners": sum(1 for item in runner_stats if item["health"] in {"risk", "warn"}),
}

payload = {"summary": summary, "runners": runner_stats}

if output_json == "true":
    print(json.dumps(payload, indent=2))
    sys.exit(0)

print()
print(f"  Runner-Ops Health Dashboard — Last {days} days")
print(f"  Generated: {summary['generated_at']}")
print()
print(f"  {'Runner':<18} {'Health':<8} {'Level':<8} {'Score':>6} {'Cost':>9} {'Runs':>5} {'Fail':>5}  Metrics")
print("  " + "─" * 108)

for item in runner_stats:
    score = "—" if item["compliance_score"] is None else str(item["compliance_score"])
    metrics_count = len(item["metrics_files"])
    print(
        f"  {item['id']:<18} {item['health']:<8} {item['integration_level']:<8} "
        f"{score:>6} {item['total_cost_usd']:>8.3f} {item['estimated_runs']:>5} {item['failures']:>5}  {metrics_count:>3} file(s)"
    )

print()
print(
    f"  Totals: {summary['total_runners']} runners | "
    f"${summary['total_cost_usd']:.3f} | "
    f"{summary['total_estimated_runs']} runs | "
    f"{summary['at_risk_runners']} at risk"
)
print()

alerts = []
for item in runner_stats:
    if item["estimated_runs"] > 0 and item["integration_level"] == "minimal":
        alerts.append(f"{item['id']}: minimal integration com atividade recente")
    if item["failures"] > 0:
        alerts.append(f"{item['id']}: {item['failures']} failure(s) na janela")
    if item["avg_cost_per_run"] and item["avg_cost_per_run"] > 1.0:
        alerts.append(f"{item['id']}: avg_cost_per_run ${item['avg_cost_per_run']:.2f}")

if alerts:
    print("  Alerts:")
    for alert in alerts:
        print(f"  - {alert}")
    print()
PY
}

save_report() {
  mkdir -p "$REPORTS_DIR"
  local report_file="$REPORTS_DIR/health-$(date +%Y%m%d-%H%M%S).json"

  python3 - "$REPO_ROOT" "$REGISTRY_FILE" "$DAYS" "$TARGET_RUNNER" "$report_file" <<'PY'
import glob
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed")
    sys.exit(1)

repo_root, registry_path, days_str, target_runner, report_file = sys.argv[1:]
repo_root = Path(repo_root)
days = int(days_str)
cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)

data = yaml.safe_load(Path(registry_path).read_text()) or {}
runners = data.get("runners", [])

if target_runner:
    runners = [runner for runner in runners if runner.get("id") == target_runner]

payload = {
    "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "period_days": days,
    "runners": [],
}

for runner in runners:
    metrics_glob = runner.get("metrics_glob") or f"{runner.get('outputs_dir','outputs')}/**/metrics.jsonl"
    metrics_files = [str(Path(path).relative_to(repo_root)) for path in glob.glob(str(repo_root / metrics_glob), recursive=True)]
    payload["runners"].append({
        "id": runner.get("id"),
        "squad": runner.get("squad"),
        "type": runner.get("type"),
        "integration_score": runner.get("integration_score"),
        "compliance_score": runner.get("compliance_score"),
        "metrics_files": metrics_files,
    })

Path(report_file).write_text(json.dumps(payload, indent=2))
print(f"Health report saved: {report_file}")
PY
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --runner)  TARGET_RUNNER="${2:-}"; shift 2 ;;
      --days)    DAYS="${2:-}"; shift 2 ;;
      --json)    OUTPUT_JSON="true"; shift ;;
      --report)  SAVE_REPORT="true"; shift ;;
      --help|-h) show_help; exit 0 ;;
      *)         echo "Unknown flag: $1" >&2; show_help; exit 1 ;;
    esac
  done
}

main() {
  parse_args "$@"
  generate_dashboard
  if [[ "$SAVE_REPORT" == "true" ]]; then
    save_report
  fi
}

main "$@"
