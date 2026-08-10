#!/usr/bin/env python3
"""Tool-call counter for tech-research pipeline runs.

Atom: atm_count_tool_calls
Records per-phase tool invocations into pipeline-state.yaml#tool_calls_per_phase[].

Schema per entry:
  phase_id       : str   — pipeline phase (e.g. "P3", "P4.5")
  tool_name      : str   — tool name (WebSearch, WebFetch, Read, Write, etc.)
  count          : int   — number of successful invocations
  total_latency_ms: int  — cumulative latency in milliseconds
  failures       : int   — number of failed/errored calls

Usage:
    # Record a single tool event
    python tool_call_counter.py record --phase P3 --tool WebSearch \\
        --count 1 --latency-ms 843 --dir docs/research/2026-05-19-my-slug

    # Batch-record from a JSON array of events
    python tool_call_counter.py record-batch \\
        --events '[{"tool":"WebSearch","count":3,"latency_ms":2100,"failures":0}]' \\
        --phase P3 --dir docs/research/2026-05-19-my-slug

    # Dump tool-call summary from pipeline-state.yaml
    python tool_call_counter.py summary --dir docs/research/2026-05-19-my-slug

Stories: STORY-RA-0.1
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ---------------------------------------------------------------------------
# YAML helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    if not HAS_YAML:
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _save_yaml(path: Path, data: dict) -> None:
    if not HAS_YAML:
        raise RuntimeError("PyYAML not installed — cannot write YAML files")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, allow_unicode=True, sort_keys=False, default_flow_style=False)


# ---------------------------------------------------------------------------
# Core record builder
# ---------------------------------------------------------------------------

def build_tool_record(
    phase_id: str,
    tool_name: str,
    count: int,
    total_latency_ms: int,
    failures: int,
    recorded_at: str | None = None,
) -> dict:
    """Build a tool_calls_per_phase record per AC-2 schema."""
    return {
        "phase_id": phase_id,
        "tool_name": tool_name,
        "count": count,
        "total_latency_ms": total_latency_ms,
        "failures": failures,
        "recorded_at": recorded_at or _now_iso(),
    }


# ---------------------------------------------------------------------------
# pipeline-state.yaml persistence
# ---------------------------------------------------------------------------

def _find_existing(records: list[dict], phase_id: str, tool_name: str) -> dict | None:
    """Find an existing record to merge into (same phase + tool)."""
    for r in records:
        if r.get("phase_id") == phase_id and r.get("tool_name") == tool_name:
            return r
    return None


def record_tool_call(
    output_dir: Path,
    phase_id: str,
    tool_name: str,
    count: int,
    total_latency_ms: int,
    failures: int,
    merge: bool = True,
) -> dict:
    """Append or merge a tool_call record into pipeline-state.yaml.

    When merge=True (default), calls for the same (phase_id, tool_name) are
    accumulated rather than creating duplicate rows. This matches the expected
    usage pattern where individual events arrive per call.

    Returns the final record as stored.
    """
    state_path = output_dir / "pipeline-state.yaml"
    state = _load_yaml(state_path)

    if "tool_calls_per_phase" not in state:
        state["tool_calls_per_phase"] = []

    existing = _find_existing(state["tool_calls_per_phase"], phase_id, tool_name) if merge else None

    if existing is not None:
        existing["count"] = existing.get("count", 0) + count
        existing["total_latency_ms"] = existing.get("total_latency_ms", 0) + total_latency_ms
        existing["failures"] = existing.get("failures", 0) + failures
        existing["recorded_at"] = _now_iso()
        record = existing
    else:
        record = build_tool_record(
            phase_id=phase_id,
            tool_name=tool_name,
            count=count,
            total_latency_ms=total_latency_ms,
            failures=failures,
        )
        state["tool_calls_per_phase"].append(record)

    _save_yaml(state_path, state)
    return record


def record_batch(
    output_dir: Path,
    phase_id: str,
    events: list[dict],
    merge: bool = True,
) -> list[dict]:
    """Record multiple tool events at once. Each event dict must have:
      tool_name, count, latency_ms, failures (all with defaults).
    Returns list of stored records.
    """
    results = []
    for ev in events:
        tool_name = ev.get("tool", ev.get("tool_name", "unknown"))
        count = int(ev.get("count", 1))
        latency = int(ev.get("latency_ms", ev.get("total_latency_ms", 0)))
        failures = int(ev.get("failures", 0))
        r = record_tool_call(
            output_dir=output_dir,
            phase_id=phase_id,
            tool_name=tool_name,
            count=count,
            total_latency_ms=latency,
            failures=failures,
            merge=merge,
        )
        results.append(r)
    return results


# ---------------------------------------------------------------------------
# Summary utility
# ---------------------------------------------------------------------------

def summarize(output_dir: Path) -> dict:
    """Return aggregated tool-call stats across all phases.

    Output:
        total_calls    : int
        total_failures : int
        total_latency_ms: int
        by_tool        : {tool_name: {count, failures, total_latency_ms}}
        by_phase       : {phase_id: [{tool_name, count, failures, latency_ms}]}
    """
    state = _load_yaml(output_dir / "pipeline-state.yaml")
    records = state.get("tool_calls_per_phase", [])

    total_calls = sum(r.get("count", 0) for r in records)
    total_failures = sum(r.get("failures", 0) for r in records)
    total_latency = sum(r.get("total_latency_ms", 0) for r in records)

    by_tool: dict[str, dict] = {}
    by_phase: dict[str, list] = {}

    for r in records:
        tn = r.get("tool_name", "unknown")
        pid = r.get("phase_id", "unknown")

        if tn not in by_tool:
            by_tool[tn] = {"count": 0, "failures": 0, "total_latency_ms": 0}
        by_tool[tn]["count"] += r.get("count", 0)
        by_tool[tn]["failures"] += r.get("failures", 0)
        by_tool[tn]["total_latency_ms"] += r.get("total_latency_ms", 0)

        by_phase.setdefault(pid, []).append({
            "tool_name": tn,
            "count": r.get("count", 0),
            "failures": r.get("failures", 0),
            "total_latency_ms": r.get("total_latency_ms", 0),
        })

    return {
        "total_calls": total_calls,
        "total_failures": total_failures,
        "total_latency_ms": total_latency,
        "by_tool": by_tool,
        "by_phase": by_phase,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_record(args: argparse.Namespace) -> int:
    output_dir = Path(args.dir).resolve()
    try:
        record = record_tool_call(
            output_dir=output_dir,
            phase_id=args.phase,
            tool_name=args.tool,
            count=args.count,
            total_latency_ms=args.latency_ms,
            failures=args.failures,
            merge=(not args.no_merge),
        )
        print(json.dumps(record, indent=2))
        return 0
    except Exception as exc:
        print(f"[tool_call_counter] ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_record_batch(args: argparse.Namespace) -> int:
    output_dir = Path(args.dir).resolve()
    try:
        events = json.loads(args.events)
        records = record_batch(
            output_dir=output_dir,
            phase_id=args.phase,
            events=events,
            merge=(not args.no_merge),
        )
        print(json.dumps(records, indent=2))
        return 0
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"[tool_call_counter] ERROR: invalid events JSON: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"[tool_call_counter] ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_summary(args: argparse.Namespace) -> int:
    output_dir = Path(args.dir).resolve()
    try:
        stats = summarize(output_dir)
        print(json.dumps(stats, indent=2))
        return 0
    except Exception as exc:
        print(f"[tool_call_counter] ERROR: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tool_call_counter",
        description="Record tool-call events for tech-research pipeline phases.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # record
    rec = sub.add_parser("record", help="Record a single tool-call event")
    rec.add_argument("--phase", required=True, help="Pipeline phase ID")
    rec.add_argument("--tool", required=True, help="Tool name (e.g. WebSearch, Read)")
    rec.add_argument("--dir", required=True, help="Research output directory")
    rec.add_argument("--count", type=int, default=1, help="Number of calls (default 1)")
    rec.add_argument("--latency-ms", dest="latency_ms", type=int, default=0,
                     help="Total latency for these calls in ms")
    rec.add_argument("--failures", type=int, default=0, help="Number of failed calls")
    rec.add_argument("--no-merge", dest="no_merge", action="store_true",
                     help="Append new row instead of merging into existing (phase, tool) row")

    # record-batch
    batch = sub.add_parser("record-batch", help="Record multiple tool events at once")
    batch.add_argument("--phase", required=True, help="Pipeline phase ID")
    batch.add_argument("--dir", required=True, help="Research output directory")
    batch.add_argument("--events", required=True,
                       help='JSON array: [{"tool":"WebSearch","count":1,"latency_ms":500,"failures":0}]')
    batch.add_argument("--no-merge", dest="no_merge", action="store_true",
                       help="Append rows instead of merging")

    # summary
    summ = sub.add_parser("summary", help="Print aggregated tool-call stats")
    summ.add_argument("--dir", required=True, help="Research output directory")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "record":
        return cmd_record(args)
    if args.command == "record-batch":
        return cmd_record_batch(args)
    if args.command == "summary":
        return cmd_summary(args)
    parser.print_help()
    return 3


if __name__ == "__main__":
    sys.exit(main())
