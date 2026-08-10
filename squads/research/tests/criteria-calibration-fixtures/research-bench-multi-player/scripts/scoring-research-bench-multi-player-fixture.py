#!/usr/bin/env python3
"""scoring-research-bench-multi-player-fixture.py — Story RA-F.1 AC-3 stub."""

WEIGHTS = {
    "agentic_planning_control": 18,
    "tool_runtime_integration": 18,
    "research_depth_synthesis": 14,
    "multi_agent_orchestration": 12,
    "evidence_fidelity_evaluation": 10,
}

assert sum(WEIGHTS.values()) == 72  # not 100 — there are more groups in the full bench


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(0)
