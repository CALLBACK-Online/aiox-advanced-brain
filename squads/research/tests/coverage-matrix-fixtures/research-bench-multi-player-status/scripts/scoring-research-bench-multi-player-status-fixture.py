#!/usr/bin/env python3
"""Fixture scoring stub for tech-research-multi-player-status.

Trigger anchor for STORY-RA-F.1 AC-3 (>=3 weighted sub-scores → script presence
required). This stub does NOT compute bit-exact reproducibility — see
`squads/research/templates/scoring-script-template.py` for the canonical
reference impl.

For STORY-RA-F.2, the relevant detail is that each cell's `status` field
maps to `score` via coverage_matrix_helper.status_to_score(...) — that
mapping is the bit-exact contract.
"""

WEIGHTS = {
    "agentic_planning": 0.30,
    "tool_runtime": 0.25,
    "multi_agent": 0.20,
    "evidence_fidelity": 0.15,
    "ux_control": 0.10,
}


def main() -> int:
    total = sum(WEIGHTS.values())
    if abs(total - 1.0) > 1e-9:
        print(f"WEIGHTS sum {total} != 1.0")
        return 1
    print(f"WEIGHTS sum: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
