#!/usr/bin/env python3
"""Verify Story RA-F.2 AT-3 (parallel speedup ≥2.5×) and AT-4 (std dev <0.5).

Per Story §Conditions Item 3 and PO mandate, this script is the in-session
synthetic proof. It reads:

  - execution-log.jsonl              (parallel run, spawn_mode=parallel)
  - execution-log-sequential.jsonl   (sequential fallback per AC-5)
  - sub_agent_outputs/agent_{1..5}.json (5 sub-agents on identical input)

And computes:

  AT-3: parallel.wallclock_s / sequential.wallclock_s ratio. Target ≥ 2.5×.
        With 5 candidates each taking ~45s sequentially (~232s total) vs the
        slowest agent ~51s in parallel, expected ratio ~4.5×.

  AT-4: std deviation across 5 sub-agents on the SAME dimension score field
        (we expect calibrated jitter due to confidence variance, but the
        canonical helper score mapping confirmed=2.0 / partial=1.0 should
        yield std dev < 0.5).

Exit codes:
  0 — both AT-3 and AT-4 pass
  1 — one or both fail
  2 — fixture corrupt
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent
PARALLEL_LOG = FIXTURE_DIR / "execution-log.jsonl"
SEQUENTIAL_LOG = FIXTURE_DIR / "execution-log-sequential.jsonl"
OUTPUTS_DIR = FIXTURE_DIR / "sub_agent_outputs"
SCHEMA_PATH = FIXTURE_DIR / "sub_agent_output.schema.json"

AT3_TARGET_RATIO = 2.5
AT4_STDDEV_MAX = 0.5


def read_wallclock(log_path: Path) -> int:
    """Return wallclock_s from the final `consolidation` event in a JSONL log."""
    if not log_path.exists():
        raise SystemExit(f"fixture missing: {log_path}")
    last_consolidation = None
    with log_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("event") == "consolidation":
                last_consolidation = entry
    if last_consolidation is None:
        raise SystemExit(f"no consolidation event in {log_path}")
    return int(last_consolidation["wallclock_s"])


def verify_at3() -> tuple[bool, float, int, int]:
    parallel_wc = read_wallclock(PARALLEL_LOG)
    sequential_wc = read_wallclock(SEQUENTIAL_LOG)
    ratio = sequential_wc / parallel_wc if parallel_wc > 0 else 0
    passed = ratio >= AT3_TARGET_RATIO
    return passed, ratio, parallel_wc, sequential_wc


def stddev(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def verify_at4() -> tuple[bool, float, dict]:
    """Compute std dev across N sub-agents on EACH dimension score.

    Returns max std dev across all dimensions — if that's below threshold, all
    are below.
    """
    if not OUTPUTS_DIR.exists():
        raise SystemExit(f"fixture missing: {OUTPUTS_DIR}")

    # Validate JSON schema compliance up front (AC-3 requirement)
    schema = json.loads(SCHEMA_PATH.read_text())
    required_keys = schema.get("required", [])
    dim_required = schema["properties"]["dimensions"]["items"].get("required", [])
    allowed_status = set(
        schema["properties"]["dimensions"]["items"]["properties"]["status"]["enum"]
    )

    per_dim_scores: dict[str, list[float]] = {}
    files = sorted(OUTPUTS_DIR.glob("agent_*.json"))
    if len(files) < 3:
        raise SystemExit(
            f"AT-4 requires >=3 sub-agent outputs; found {len(files)} in {OUTPUTS_DIR}"
        )

    for f in files:
        payload = json.loads(f.read_text())
        # Schema validation (manual since we don't want jsonschema dep)
        for key in required_keys:
            if key not in payload:
                raise SystemExit(f"{f.name}: missing required key '{key}'")
        if payload["schema_version"] != "sub-agent-output.v1":
            raise SystemExit(f"{f.name}: bad schema_version {payload['schema_version']!r}")
        for dim in payload["dimensions"]:
            for k in dim_required:
                if k not in dim:
                    raise SystemExit(
                        f"{f.name}: dimension {dim.get('dimension_id')!r} missing '{k}'"
                    )
            if dim["status"] not in allowed_status:
                raise SystemExit(
                    f"{f.name}: dimension {dim['dimension_id']!r} status "
                    f"{dim['status']!r} not in {sorted(allowed_status)}"
                )
            per_dim_scores.setdefault(dim["dimension_id"], []).append(float(dim["score"]))

    per_dim_stddev = {dim: stddev(scores) for dim, scores in per_dim_scores.items()}
    max_std = max(per_dim_stddev.values()) if per_dim_stddev else 0.0
    passed = max_std < AT4_STDDEV_MAX
    return passed, max_std, per_dim_stddev


def main() -> int:
    at3_ok, at3_ratio, par_wc, seq_wc = verify_at3()
    at4_ok, at4_max_std, per_dim = verify_at4()

    print("AT-3 — parallel speedup verification")
    print(f"  parallel wallclock:   {par_wc}s")
    print(f"  sequential wallclock: {seq_wc}s")
    print(f"  ratio: {at3_ratio:.2f}× (target >= {AT3_TARGET_RATIO}×)")
    print(f"  verdict: {'PASS' if at3_ok else 'FAIL'}")
    print()
    print("AT-4 — sub-agent consistency (std deviation)")
    print(f"  agents: {len(list(OUTPUTS_DIR.glob('agent_*.json')))}")
    print(f"  per-dimension stddev:")
    for dim, sd in sorted(per_dim.items()):
        print(f"    {dim:20s} {sd:.3f}")
    print(f"  max std dev: {at4_max_std:.3f} (target < {AT4_STDDEV_MAX})")
    print(f"  verdict: {'PASS' if at4_ok else 'FAIL'}")
    print()

    if at3_ok and at4_ok:
        print("SUMMARY: ALL TESTS PASS")
        return 0
    print("SUMMARY: FAILURE — see above")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
