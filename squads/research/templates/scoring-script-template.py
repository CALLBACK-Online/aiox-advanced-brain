#!/usr/bin/env python3
"""scoring-{SLUG}.py — Reproducible composite scoring for a research/bench run.

Usage:
    python scoring-{SLUG}.py {bench_or_research_dir}

Exit codes:
    0 — success, scoring CSV emitted
    1 — input data missing or malformed
    2 — score divergence vs prior emission (only when re-running with --check)
    3 — argument/environment error

Reproducibility contract (Story RA-F.1 AC-3, AT-3):
    Running this script against the SAME raw inputs MUST re-produce the
    output CSV BIT-EXACT. Any divergence is a bug — fix the script, not the
    output. Weights and normalizations are declared IN CODE below, not in
    prose, because prose drifts and code does not.

Python version: 3.11+ (matches research-bench tooling baseline)
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ────────────────────────────────────────────────────────────────────────
# Weights (declared in code — single source of truth for this run)
# ────────────────────────────────────────────────────────────────────────
# Replace placeholders. ALL weights MUST sum to 1.0 (or 100 if scale is 0-100).
# If composite scoring is multi-weighted (>=3 sub-scores), this script is REQUIRED
# per Story RA-F.1 AC-3. If single-dimension scoring, this template is NOT needed.

WEIGHTS: dict[str, float] = {
    "fit": 0.25,
    "maturity": 0.20,
    "evidence": 0.20,
    "adoption": 0.20,
    "activity": 0.10,
    "license": 0.05,
}

# Guardrail: weights MUST sum to 1.0 ± 1e-6
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-6, (
    f"WEIGHTS sum to {sum(WEIGHTS.values())}, expected 1.0. "
    "Fix the script before running."
)

# ────────────────────────────────────────────────────────────────────────
# Normalizations (declared in code)
# ────────────────────────────────────────────────────────────────────────
# Power-law fields (stars, forks, citations, contributors) MUST be
# log-normalized BEFORE aggregation — otherwise a single outlier dominates
# the composite. log1p maps 0 → 0 and avoids ln(0) singularities.
#
# Caps in field names (Story RA-F.1 AC-4) are HONORED here: if the raw
# field is named `contributors_api_capped_100`, we read it as-is and DO
# NOT attempt to un-cap. The cap is the data.

LOG_NORMALIZED_FIELDS: tuple[str, ...] = (
    "stargazers_count",
    "forks_count",
    "contributors_api_capped_100",
    "citations_semantic_scholar_capped_1000",
    "commits_90d_capped_N",
)

# Empirical baselines for each subscore. Replace with actual signals from the run.
# Each baseline tuple is (raw_field_name, max_raw_value_for_normalization).
SUBSCORE_BASELINES: dict[str, tuple[str, float]] = {
    "fit":      ("fit_score_raw",                       5.0),
    "maturity": ("maturity_score_raw",                  5.0),
    "evidence": ("evidence_score_raw",                  5.0),
    "adoption": ("stargazers_count",                  10000.0),   # log-normalized; baseline tracks log scale
    "activity": ("commits_90d_capped_N",                100.0),   # capped at N per AC-4
    "license":  ("license_permissiveness_score_raw",     5.0),
}


@dataclass
class PlayerRow:
    """One row per player. Raw fields are strings as read from CSV."""

    player_key: str
    raw: dict[str, str] = field(default_factory=dict)
    subscores: dict[str, float] = field(default_factory=dict)
    total: float = 0.0


# ────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────


def _to_float(value: str) -> float:
    """Parse a raw CSV cell to float. Empty / non-numeric → 0.0."""
    if value is None or value == "":
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0


def normalize(raw_value: float, field_name: str, baseline_max: float) -> float:
    """Normalize a raw value to the 0-1 range. Power-law fields use log1p."""
    if field_name in LOG_NORMALIZED_FIELDS:
        # log1p(x) / log1p(baseline_max) — anti-outlier-domination
        if baseline_max <= 0:
            return 0.0
        return min(math.log1p(raw_value) / math.log1p(baseline_max), 1.0)
    # Linear normalization for interpretive scores already on a small scale.
    if baseline_max <= 0:
        return 0.0
    return min(raw_value / baseline_max, 1.0)


def compute_subscores(row: PlayerRow) -> None:
    """Populate row.subscores in-place from row.raw using SUBSCORE_BASELINES."""
    for sub_id, (raw_field, baseline_max) in SUBSCORE_BASELINES.items():
        raw = _to_float(row.raw.get(raw_field, ""))
        row.subscores[sub_id] = normalize(raw, raw_field, baseline_max)


def compute_total(row: PlayerRow) -> None:
    """Weighted sum of subscores. WEIGHTS sum to 1.0 → total in [0, 1]."""
    row.total = sum(WEIGHTS[k] * row.subscores.get(k, 0.0) for k in WEIGHTS)


def load_players(raw_csv: Path) -> list[PlayerRow]:
    """Read raw player data from CSV. First column MUST be `player_key`."""
    if not raw_csv.exists():
        print(f"ERROR: raw input not found: {raw_csv}", file=sys.stderr)
        sys.exit(1)
    rows: list[PlayerRow] = []
    with raw_csv.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for raw_row in reader:
            key = raw_row.get("player_key", "").strip()
            if not key:
                continue
            rows.append(PlayerRow(player_key=key, raw=dict(raw_row)))
    return rows


def emit_scoring_csv(rows: Iterable[PlayerRow], output_csv: Path) -> None:
    """Write `scoring-{slug}.csv` with deterministic column order."""
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    headers = (
        ["player_key"]
        + [f"sub_{k}" for k in WEIGHTS]
        + [f"weight_{k}" for k in WEIGHTS]
        + ["total"]
    )
    with output_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")  # bit-exact across OSes
        writer.writerow(headers)
        for row in rows:
            writer.writerow(
                [row.player_key]
                + [f"{row.subscores.get(k, 0.0):.6f}" for k in WEIGHTS]
                + [f"{WEIGHTS[k]:.6f}" for k in WEIGHTS]
                + [f"{row.total:.6f}"]
            )


def emit_provenance(
    output_dir: Path,
    raw_csv: Path,
    output_csv: Path,
) -> None:
    """Write `scoring-{slug}.provenance.json` with hashes for audit."""
    provenance = {
        "schema_version": "scoring-provenance.v1",
        "script_path": str(Path(__file__).name),
        "python_version_min": "3.11",
        "weights": WEIGHTS,
        "log_normalized_fields": list(LOG_NORMALIZED_FIELDS),
        "subscore_baselines": {k: {"field": v[0], "baseline_max": v[1]} for k, v in SUBSCORE_BASELINES.items()},
        "inputs": {
            "raw_csv": str(raw_csv.name),
            "raw_csv_sha256": _sha256(raw_csv),
        },
        "outputs": {
            "scoring_csv": str(output_csv.name),
            "scoring_csv_sha256": _sha256(output_csv),
        },
    }
    provenance_path = output_dir / f"{output_csv.stem}.provenance.json"
    provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


# ────────────────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reproducible composite scoring (Story RA-F.1 AC-3).",
    )
    parser.add_argument(
        "run_dir",
        help="Path to docs/research/{date}-{slug}/ OR docs/bench/{date}-{slug}/",
    )
    parser.add_argument(
        "--raw-csv",
        default="scoring-inputs.csv",
        help="Filename of raw inputs inside run_dir (default: scoring-inputs.csv)",
    )
    parser.add_argument(
        "--output-csv",
        default=None,
        help="Output filename (default: scoring-{slug}.csv where slug=basename of run_dir)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Bit-exact verify against existing output (exit 2 on divergence)",
    )
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"ERROR: run dir not found: {run_dir}", file=sys.stderr)
        return 3

    raw_csv = run_dir / args.raw_csv
    slug = run_dir.name
    output_name = args.output_csv or f"scoring-{slug}.csv"
    output_csv = run_dir / output_name

    rows = load_players(raw_csv)
    for row in rows:
        compute_subscores(row)
        compute_total(row)

    if args.check:
        if not output_csv.exists():
            print(f"ERROR: --check requires existing {output_csv}", file=sys.stderr)
            return 1
        existing_hash = _sha256(output_csv)
        tmp_csv = output_csv.with_suffix(".tmp.csv")
        emit_scoring_csv(rows, tmp_csv)
        new_hash = _sha256(tmp_csv)
        tmp_csv.unlink()
        if existing_hash != new_hash:
            print(
                f"DIVERGENCE: existing {existing_hash} vs new {new_hash}",
                file=sys.stderr,
            )
            return 2
        print(f"OK: scoring CSV reproduces bit-exact ({existing_hash[:12]})")
        return 0

    emit_scoring_csv(rows, output_csv)
    emit_provenance(run_dir, raw_csv, output_csv)
    print(json.dumps({"status": "ok", "rows": len(rows), "output": str(output_csv.relative_to(run_dir))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
