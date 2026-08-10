#!/usr/bin/env python3
"""Cost tracker for tech-research pipeline runs.

Atom: atm_track_cost
Records per-phase token counts and USD estimates into pipeline-state.yaml#cost_per_phase[].
Aggregates into cost-latency.yaml at run end.

Token sources (priority order):
  1. Anthropic SDK usage object (exact)
  2. tiktoken cl100k_base tokenizer (approximate)
  3. Unavailable — emits cost_confidence: unavailable, cost_usd_estimate: null

Usage:
    python cost_tracker.py record --phase P3 --tokens-in 1200 --tokens-out 400 \\
        --wallclock 12.5 --dir docs/research/2026-05-19-my-slug

    python cost_tracker.py record --phase P3 --anthropic-usage '{"input_tokens":1200,"output_tokens":400}' \\
        --wallclock 12.5 --dir docs/research/2026-05-19-my-slug

    python cost_tracker.py aggregate --dir docs/research/2026-05-19-my-slug \\
        --out docs/research/2026-05-19-my-slug/cost-latency.yaml

Stories: STORY-RA-0.1
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

# ---------------------------------------------------------------------------
# Cost model (Anthropic claude-sonnet-4-x as baseline — update as needed)
# Prices in USD per 1M tokens, as of 2026-05.
# Agents should inject their own pricing via env vars if available.
# ---------------------------------------------------------------------------
_INPUT_COST_PER_M = float(os.environ.get("COST_INPUT_PER_M_USD", "3.0"))
_OUTPUT_COST_PER_M = float(os.environ.get("COST_OUTPUT_PER_M_USD", "15.0"))


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_yaml(path: Path) -> dict:
    """Load YAML file; return empty dict if missing or yaml unavailable."""
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


def _count_tokens_tiktoken(text: str) -> int | None:
    """Count tokens using tiktoken cl100k_base. Returns None if unavailable."""
    if not HAS_TIKTOKEN:
        return None
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return None


def _estimate_cost(tokens_in: int | None, tokens_out: int | None) -> float | None:
    """Compute USD estimate from token counts. Returns None if either count is None."""
    if tokens_in is None or tokens_out is None:
        return None
    cost = (tokens_in / 1_000_000) * _INPUT_COST_PER_M + (tokens_out / 1_000_000) * _OUTPUT_COST_PER_M
    return round(cost, 8)


def _determine_confidence(
    tokens_in: int | None,
    tokens_out: int | None,
    from_sdk: bool,
) -> str:
    """Return cost_confidence level per AC-1 spec.

    exact        — counts from Anthropic SDK usage object
    approximate  — counts estimated via tiktoken
    unavailable  — no counting method succeeded
    """
    if tokens_in is None or tokens_out is None:
        return "unavailable"
    return "exact" if from_sdk else "approximate"


# ---------------------------------------------------------------------------
# Core record builder
# ---------------------------------------------------------------------------

def build_cost_record(
    phase_id: str,
    tokens_in: int | None,
    tokens_out: int | None,
    wallclock_sec: float,
    from_sdk: bool,
    recorded_at: str | None = None,
) -> dict:
    """Build a cost_per_phase record dict per AC-1 schema."""
    confidence = _determine_confidence(tokens_in, tokens_out, from_sdk)
    cost_usd = _estimate_cost(tokens_in, tokens_out) if confidence != "unavailable" else None

    return {
        "phase_id": phase_id,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd_estimate": cost_usd,
        "cost_confidence": confidence,
        "wallclock_sec": round(wallclock_sec, 3),
        "recorded_at": recorded_at or _now_iso(),
    }


# ---------------------------------------------------------------------------
# pipeline-state.yaml persistence
# ---------------------------------------------------------------------------

def record_phase(
    output_dir: Path,
    phase_id: str,
    tokens_in: int | None,
    tokens_out: int | None,
    wallclock_sec: float,
    from_sdk: bool,
) -> dict:
    """Append a cost record to pipeline-state.yaml#cost_per_phase[].

    Creates or updates the file atomically (best-effort).
    Returns the cost record that was appended.
    """
    state_path = output_dir / "pipeline-state.yaml"
    state = _load_yaml(state_path)

    # Ensure cost_per_phase list exists
    if "cost_per_phase" not in state:
        state["cost_per_phase"] = []

    record = build_cost_record(
        phase_id=phase_id,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        wallclock_sec=wallclock_sec,
        from_sdk=from_sdk,
    )
    state["cost_per_phase"].append(record)

    _save_yaml(state_path, state)
    return record


# ---------------------------------------------------------------------------
# Aggregation — produces cost-latency.yaml
# ---------------------------------------------------------------------------

def _aggregate_confidence(records: list[dict]) -> str:
    """Aggregate confidence across phases.

    unavailable  — any phase is unavailable
    approximate  — all measured, at least one approximate
    exact        — all exact
    """
    values = [r.get("cost_confidence", "unavailable") for r in records]
    if "unavailable" in values:
        return "unavailable"
    if "approximate" in values:
        return "approximate"
    return "exact"


def aggregate(output_dir: Path, out_path: Path, run_id: str | None = None) -> dict:
    """Read pipeline-state.yaml and emit cost-latency.yaml.

    Returns the cost-latency dict for validation/testing.
    """
    state_path = output_dir / "pipeline-state.yaml"
    state = _load_yaml(state_path)

    cost_records = state.get("cost_per_phase", [])
    tool_records = state.get("tool_calls_per_phase", [])

    # Aggregate cost
    valid_costs = [r["cost_usd_estimate"] for r in cost_records if r.get("cost_usd_estimate") is not None]
    total_cost = round(sum(valid_costs), 8) if valid_costs else None

    total_in = sum(r["tokens_in"] for r in cost_records if r.get("tokens_in") is not None)
    total_out = sum(r["tokens_out"] for r in cost_records if r.get("tokens_out") is not None)

    # Wallclock: use per-phase records if available
    total_wallclock = round(sum(r.get("wallclock_sec", 0) for r in cost_records), 3)

    slug = run_id or output_dir.name

    result = {
        "run_id": slug,
        "generated_at": _now_iso(),
        "total_cost_usd": total_cost,
        "cost_confidence_aggregate": _aggregate_confidence(cost_records) if cost_records else "unavailable",
        "total_wallclock_sec": int(total_wallclock),
        "total_tokens": {
            "in": total_in,
            "out": total_out,
        },
        "phases": cost_records,
        "tool_calls": tool_records,
    }

    _save_yaml(out_path, result)
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_record(args: argparse.Namespace) -> int:
    output_dir = Path(args.dir).resolve()
    tokens_in: int | None = None
    tokens_out: int | None = None
    from_sdk = False

    if args.anthropic_usage:
        # JSON usage object from Anthropic SDK: {"input_tokens": N, "output_tokens": N}
        try:
            usage = json.loads(args.anthropic_usage)
            tokens_in = int(usage.get("input_tokens") or usage.get("tokens_in", 0))
            tokens_out = int(usage.get("output_tokens") or usage.get("tokens_out", 0))
            from_sdk = True
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            print(f"[cost_tracker] WARNING: failed to parse --anthropic-usage: {exc}", file=sys.stderr)

    elif args.tokens_in is not None and args.tokens_out is not None:
        tokens_in = args.tokens_in
        tokens_out = args.tokens_out
        from_sdk = False

    elif args.text:
        # Estimate via tiktoken if raw text provided
        count = _count_tokens_tiktoken(args.text)
        if count is not None:
            # Rough heuristic: 80% input, 20% output for untracked splits
            tokens_in = int(count * 0.8)
            tokens_out = int(count * 0.2)
            from_sdk = False

    wallclock = args.wallclock or 0.0

    try:
        record = record_phase(
            output_dir=output_dir,
            phase_id=args.phase,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            wallclock_sec=wallclock,
            from_sdk=from_sdk,
        )
        print(json.dumps(record, indent=2))
        return 0
    except Exception as exc:
        print(f"[cost_tracker] ERROR: {exc}", file=sys.stderr)
        return 1


def cmd_aggregate(args: argparse.Namespace) -> int:
    output_dir = Path(args.dir).resolve()
    out_path = Path(args.out).resolve() if args.out else output_dir / "cost-latency.yaml"

    try:
        result = aggregate(output_dir=output_dir, out_path=out_path, run_id=args.run_id)
        print(f"[cost_tracker] Aggregated → {out_path}", file=sys.stderr)
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(f"[cost_tracker] ERROR: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cost_tracker",
        description="Record and aggregate LLM cost/token data for tech-research pipeline runs.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # record sub-command
    rec = sub.add_parser("record", help="Record a single phase cost entry into pipeline-state.yaml")
    rec.add_argument("--phase", required=True, help="Phase ID (e.g. P3, P4.5)")
    rec.add_argument("--dir", required=True, help="Research output directory (docs/research/{slug}/)")
    rec.add_argument("--anthropic-usage", dest="anthropic_usage", default=None,
                     help='Anthropic SDK usage JSON: {"input_tokens":N,"output_tokens":N}')
    rec.add_argument("--tokens-in", dest="tokens_in", type=int, default=None,
                     help="Input token count (tiktoken-estimated, from_sdk=False)")
    rec.add_argument("--tokens-out", dest="tokens_out", type=int, default=None,
                     help="Output token count (tiktoken-estimated, from_sdk=False)")
    rec.add_argument("--text", default=None,
                     help="Raw text to auto-count via tiktoken (fallback)")
    rec.add_argument("--wallclock", type=float, default=0.0,
                     help="Phase wall-clock seconds (float)")

    # aggregate sub-command
    agg = sub.add_parser("aggregate", help="Aggregate pipeline-state.yaml into cost-latency.yaml")
    agg.add_argument("--dir", required=True, help="Research output directory")
    agg.add_argument("--out", default=None,
                     help="Output path for cost-latency.yaml (default: {dir}/cost-latency.yaml)")
    agg.add_argument("--run-id", dest="run_id", default=None,
                     help="Override run_id (default: directory name)")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "record":
        return cmd_record(args)
    if args.command == "aggregate":
        return cmd_aggregate(args)
    parser.print_help()
    return 3


if __name__ == "__main__":
    sys.exit(main())
