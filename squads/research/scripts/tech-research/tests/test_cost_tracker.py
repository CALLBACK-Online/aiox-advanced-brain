#!/usr/bin/env python3
"""Smoke tests for cost_tracker.py — STORY-RA-0.1.

Run:
    python3 squads/research/scripts/tech-research/tests/test_cost_tracker.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from cost_tracker import (  # noqa: E402
    build_cost_record,
    record_phase,
    aggregate,
    _determine_confidence,
    _estimate_cost,
)


class TestCostRecord(unittest.TestCase):
    """Tests for build_cost_record and helpers."""

    def test_exact_confidence_from_sdk(self):
        rec = build_cost_record("P3", tokens_in=1000, tokens_out=500, wallclock_sec=5.0, from_sdk=True)
        self.assertEqual(rec["cost_confidence"], "exact")
        self.assertIsNotNone(rec["cost_usd_estimate"])
        self.assertGreater(rec["cost_usd_estimate"], 0)

    def test_approximate_confidence_from_tiktoken(self):
        rec = build_cost_record("P4", tokens_in=800, tokens_out=200, wallclock_sec=3.2, from_sdk=False)
        self.assertEqual(rec["cost_confidence"], "approximate")
        self.assertIsNotNone(rec["cost_usd_estimate"])

    def test_unavailable_when_no_tokens(self):
        """AC-1: cost_confidence: unavailable when no method works. NEVER 0."""
        rec = build_cost_record("P5", tokens_in=None, tokens_out=None, wallclock_sec=1.0, from_sdk=False)
        self.assertEqual(rec["cost_confidence"], "unavailable")
        self.assertIsNone(rec["cost_usd_estimate"])  # Must be None, not 0

    def test_no_zero_fallback(self):
        """Regression: cost_usd_estimate must be None when unavailable, not 0."""
        rec = build_cost_record("P3.5", tokens_in=None, tokens_out=None, wallclock_sec=0.5, from_sdk=False)
        self.assertNotEqual(rec["cost_usd_estimate"], 0)

    def test_schema_fields_present(self):
        rec = build_cost_record("P1", tokens_in=100, tokens_out=50, wallclock_sec=2.0, from_sdk=True)
        required = {"phase_id", "tokens_in", "tokens_out", "cost_usd_estimate", "cost_confidence", "wallclock_sec", "recorded_at"}
        self.assertTrue(required.issubset(rec.keys()), f"Missing fields: {required - set(rec.keys())}")


class TestRecordPhase(unittest.TestCase):
    """Tests for pipeline-state.yaml persistence."""

    def test_appends_to_pipeline_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_phase(out, "P3", tokens_in=500, tokens_out=200, wallclock_sec=4.0, from_sdk=True)
            record_phase(out, "P4", tokens_in=300, tokens_out=150, wallclock_sec=2.0, from_sdk=False)

            import yaml
            state = yaml.safe_load((out / "pipeline-state.yaml").read_text())
            self.assertEqual(len(state["cost_per_phase"]), 2)
            self.assertEqual(state["cost_per_phase"][0]["phase_id"], "P3")
            self.assertEqual(state["cost_per_phase"][1]["phase_id"], "P4")

    def test_creates_file_if_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertFalse((out / "pipeline-state.yaml").exists())
            record_phase(out, "P0", tokens_in=100, tokens_out=50, wallclock_sec=1.0, from_sdk=False)
            self.assertTrue((out / "pipeline-state.yaml").exists())

    def test_unavailable_phase_recorded(self):
        """Mock SDK failure: tokens None → cost_confidence unavailable."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_phase(out, "P3.5", tokens_in=None, tokens_out=None, wallclock_sec=0.5, from_sdk=False)

            import yaml
            state = yaml.safe_load((out / "pipeline-state.yaml").read_text())
            rec = state["cost_per_phase"][0]
            self.assertEqual(rec["cost_confidence"], "unavailable")
            self.assertIsNone(rec["cost_usd_estimate"])


class TestAggregate(unittest.TestCase):
    """Tests for cost-latency.yaml emission."""

    def test_aggregate_produces_valid_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_phase(out, "P1", tokens_in=1000, tokens_out=400, wallclock_sec=3.0, from_sdk=True)
            record_phase(out, "P3", tokens_in=2000, tokens_out=800, wallclock_sec=8.0, from_sdk=True)

            out_path = out / "cost-latency.yaml"
            result = aggregate(out, out_path, run_id="test-run")

            required = {"run_id", "total_cost_usd", "cost_confidence_aggregate",
                        "total_wallclock_sec", "total_tokens", "phases", "tool_calls"}
            self.assertTrue(required.issubset(result.keys()))
            self.assertTrue(out_path.exists())
            self.assertEqual(result["run_id"], "test-run")
            self.assertEqual(result["cost_confidence_aggregate"], "exact")

    def test_aggregate_unavailable_when_any_phase_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_phase(out, "P1", tokens_in=1000, tokens_out=400, wallclock_sec=3.0, from_sdk=True)
            record_phase(out, "P3", tokens_in=None, tokens_out=None, wallclock_sec=5.0, from_sdk=False)

            result = aggregate(out, out / "cost-latency.yaml")
            self.assertEqual(result["cost_confidence_aggregate"], "unavailable")

    def test_aggregate_with_no_phases(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = aggregate(out, out / "cost-latency.yaml")
            self.assertEqual(result["cost_confidence_aggregate"], "unavailable")
            self.assertIsNone(result["total_cost_usd"])


class TestDetermineConfidence(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(_determine_confidence(100, 50, True), "exact")

    def test_approximate(self):
        self.assertEqual(_determine_confidence(100, 50, False), "approximate")

    def test_unavailable_none_in(self):
        self.assertEqual(_determine_confidence(None, 50, True), "unavailable")

    def test_unavailable_none_out(self):
        self.assertEqual(_determine_confidence(100, None, False), "unavailable")

    def test_unavailable_both_none(self):
        self.assertEqual(_determine_confidence(None, None, False), "unavailable")


class TestCLIRecord(unittest.TestCase):
    """Smoke test for CLI record subcommand."""

    def test_cli_record_with_explicit_tokens(self):
        from cost_tracker import main
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["record", "--phase", "P3", "--tokens-in", "1000",
                        "--tokens-out", "400", "--wallclock", "5.0", "--dir", tmp])
            self.assertEqual(ret, 0)

    def test_cli_record_anthropic_usage(self):
        from cost_tracker import main
        usage = json.dumps({"input_tokens": 2000, "output_tokens": 600})
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["record", "--phase", "P4", "--anthropic-usage", usage,
                        "--wallclock", "3.5", "--dir", tmp])
            self.assertEqual(ret, 0)

    def test_cli_aggregate(self):
        from cost_tracker import main
        with tempfile.TemporaryDirectory() as tmp:
            main(["record", "--phase", "P3", "--tokens-in", "1000",
                  "--tokens-out", "500", "--wallclock", "4.0", "--dir", tmp])
            ret = main(["aggregate", "--dir", tmp, "--run-id", "smoke-test"])
            self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
