#!/usr/bin/env python3
"""validate_pipeline_emission.py — skill-side M10 CI gate (Python mirror).

Mirrors squads/slides-creator/scripts/validate-pipeline-emission.js for self-contained
runtimes (Codex / external) where Node is unavailable. Scans every
outputs/slides-creator/{run_id}/ directory and verifies each run emitted a
pipeline-execution-log.yaml with the expected event sequence.

Usage:
    python3 skills/slide-creator/scripts/validate_pipeline_emission.py
    python3 skills/slide-creator/scripts/validate_pipeline_emission.py --run-id <id>
    python3 skills/slide-creator/scripts/validate_pipeline_emission.py --strict
    python3 skills/slide-creator/scripts/validate_pipeline_emission.py --json

Exit codes:
    0 — all runs pass (or single --run-id passes)
    1 — at least one run failed minimum-records or required-event checks
    2 — IO error, parse error, or invalid arguments

Determinism: same filesystem → same exit code + report. No network. Stdlib only
(no PyYAML dependency required — minimal record counter via regex).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

MIN_RECORDS_QUICK = 3
MIN_RECORDS_FULL = 8
DEFAULT_MIN_RECORDS = MIN_RECORDS_QUICK

VALID_EVENTS = {
    "workflow_started",
    "phase_transition",
    "gate_verdict",
    "meta_axiom_breach",
    "deviation_logged",
    "killer_item_fired",
    "workflow_completion",
}

# Event line in YAML: looks like `  - event: workflow_started` (possibly indented).
EVENT_PATTERN = re.compile(r"^\s*-\s*event:\s*([a-z_]+)\s*$")


@dataclass
class RunResult:
    run_id: str
    log_path: str
    log_exists: bool = False
    records: int = 0
    events: list[str] = field(default_factory=list)
    has_workflow_started: bool = False
    has_workflow_completion: bool = False
    has_gate_verdict: bool = False
    invalid_events: list[str] = field(default_factory=list)
    verdict: str = "FAIL"
    reasons: list[str] = field(default_factory=list)


def resolve_project(cli_value: str | None) -> Path:
    if cli_value:
        return Path(cli_value).resolve()
    env_value = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_value:
        return Path(env_value).resolve()
    return Path.cwd().resolve()


def list_run_dirs(local_docs: Path) -> list[Path]:
    root = local_docs / "outputs" / "slides-creator"
    if not root.exists():
        return []
    return sorted(
        p
        for p in root.iterdir()
        if p.is_dir() and not p.name.startswith("_") and not p.name.startswith(".")
    )


def parse_events_from_yaml(yaml_text: str) -> list[str]:
    """Minimal event extractor — counts `- event: <name>` lines without PyYAML."""
    events: list[str] = []
    if not yaml_text:
        return events
    for line in yaml_text.splitlines():
        match = EVENT_PATTERN.match(line)
        if match:
            events.append(match.group(1))
    return events


def validate_run(run_dir: Path, min_records: int) -> RunResult:
    log_path = run_dir / "pipeline-execution-log.yaml"
    result = RunResult(run_id=run_dir.name, log_path=str(log_path))

    if not log_path.exists():
        result.reasons.append(f"pipeline-execution-log.yaml missing at {log_path}")
        return result
    result.log_exists = True

    try:
        yaml_text = log_path.read_text(encoding="utf-8")
    except OSError as err:
        result.reasons.append(f"IO error reading {log_path}: {err}")
        return result

    events = parse_events_from_yaml(yaml_text)
    result.events = events
    result.records = len(events)
    result.invalid_events = [e for e in events if e not in VALID_EVENTS]
    result.has_workflow_started = "workflow_started" in events
    result.has_workflow_completion = "workflow_completion" in events
    result.has_gate_verdict = "gate_verdict" in events

    if result.records < min_records:
        result.reasons.append(
            f"Only {result.records} records (need >= {min_records})"
        )
    if not result.has_workflow_started:
        result.reasons.append("Missing workflow_started event")
    if not result.has_workflow_completion:
        result.reasons.append("Missing workflow_completion event")
    if result.invalid_events:
        result.reasons.append(
            f"Invalid events: {', '.join(sorted(set(result.invalid_events)))}"
        )

    result.verdict = "PASS" if not result.reasons else "FAIL"
    return result


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Skill-side M10 CI gate — verify pipeline-execution-log emission per run.",
        epilog="Mirror of squad-side validate-pipeline-emission.js. Use when Node runtime is unavailable.",
    )
    parser.add_argument("--run-id", help="Validate a single run instead of all")
    parser.add_argument("--local_docs", help="Override project root (default: CLAUDE_PROJECT_DIR or CWD)")
    parser.add_argument(
        "--mode",
        choices=["quick", "full"],
        default="quick",
        help="Set minimum records: quick=3 (default), full=8",
    )
    parser.add_argument("--strict", action="store_true", help="Treat invalid events as hard failure")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    local_docs = resolve_project(args.local_docs)
    min_records = MIN_RECORDS_FULL if args.mode == "full" else MIN_RECORDS_QUICK

    if args.run_id:
        single = local_docs / "outputs" / "slides-creator" / args.run_id
        if not single.exists():
            sys.stderr.write(f"ERROR: run dir not found: {single}\n")
            return 2
        run_dirs = [single]
    else:
        run_dirs = list_run_dirs(local_docs)

    results = [validate_run(d, min_records) for d in run_dirs]
    pass_count = sum(1 for r in results if r.verdict == "PASS")
    fail_count = len(results) - pass_count

    summary = {
        "total_runs": len(results),
        "pass": pass_count,
        "fail": fail_count,
        "min_records_required": min_records,
        "mode": args.mode,
        "docs": str(local_docs),
        "runs": [asdict(r) for r in results],
    }

    if args.json:
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    else:
        sys.stdout.write(f"validate-pipeline-emission (skill-side, Python) — {len(results)} run(s)\n")
        for r in results:
            tag = "PASS" if r.verdict == "PASS" else "FAIL"
            reasons = " — " + "; ".join(r.reasons) if r.reasons else ""
            sys.stdout.write(f"  [{tag}] {r.run_id}: {r.records} records{reasons}\n")
        sys.stdout.write(f"\nTotal: {pass_count} PASS / {fail_count} FAIL (mode={args.mode}, min={min_records})\n")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as err:  # noqa: BLE001
        sys.stderr.write(f"FATAL: {type(err).__name__}: {err}\n")
        sys.exit(2)
