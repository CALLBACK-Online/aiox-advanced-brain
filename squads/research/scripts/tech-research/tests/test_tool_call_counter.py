#!/usr/bin/env python3
"""Smoke tests for tool_call_counter.py — STORY-RA-0.1.

Run:
    python3 squads/research/scripts/tech-research/tests/test_tool_call_counter.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from tool_call_counter import (  # noqa: E402
    build_tool_record,
    record_tool_call,
    record_batch,
    summarize,
)


class TestBuildToolRecord(unittest.TestCase):
    def test_schema_fields(self):
        rec = build_tool_record("P3", "WebSearch", count=2, total_latency_ms=1200, failures=0)
        required = {"phase_id", "tool_name", "count", "total_latency_ms", "failures", "recorded_at"}
        self.assertTrue(required.issubset(rec.keys()))

    def test_values_match(self):
        rec = build_tool_record("P4", "Read", count=5, total_latency_ms=350, failures=1)
        self.assertEqual(rec["phase_id"], "P4")
        self.assertEqual(rec["tool_name"], "Read")
        self.assertEqual(rec["count"], 5)
        self.assertEqual(rec["total_latency_ms"], 350)
        self.assertEqual(rec["failures"], 1)


class TestRecordToolCall(unittest.TestCase):
    def test_appends_new_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_tool_call(out, "P3", "WebSearch", 1, 850, 0)
            record_tool_call(out, "P3", "Read", 3, 120, 0)

            import yaml
            state = yaml.safe_load((out / "pipeline-state.yaml").read_text())
            records = state["tool_calls_per_phase"]
            self.assertEqual(len(records), 2)

    def test_merge_same_phase_tool(self):
        """Multiple calls to same (phase, tool) are merged into one row."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_tool_call(out, "P3", "WebSearch", 1, 800, 0, merge=True)
            record_tool_call(out, "P3", "WebSearch", 2, 1600, 1, merge=True)

            import yaml
            state = yaml.safe_load((out / "pipeline-state.yaml").read_text())
            records = state["tool_calls_per_phase"]
            # Should be merged into 1 row
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["count"], 3)
            self.assertEqual(records[0]["total_latency_ms"], 2400)
            self.assertEqual(records[0]["failures"], 1)

    def test_no_merge_creates_separate_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_tool_call(out, "P3", "WebSearch", 1, 800, 0, merge=False)
            record_tool_call(out, "P3", "WebSearch", 2, 1600, 0, merge=False)

            import yaml
            state = yaml.safe_load((out / "pipeline-state.yaml").read_text())
            self.assertEqual(len(state["tool_calls_per_phase"]), 2)

    def test_creates_pipeline_state_if_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertFalse((out / "pipeline-state.yaml").exists())
            record_tool_call(out, "P0", "Glob", 1, 20, 0)
            self.assertTrue((out / "pipeline-state.yaml").exists())


class TestRecordBatch(unittest.TestCase):
    def test_batch_records_multiple_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            events = [
                {"tool": "WebSearch", "count": 3, "latency_ms": 2100, "failures": 0},
                {"tool": "WebFetch", "count": 2, "latency_ms": 900, "failures": 1},
                {"tool": "Read", "count": 5, "latency_ms": 150, "failures": 0},
            ]
            results = record_batch(out, "P3", events)
            self.assertEqual(len(results), 3)

    def test_batch_uses_tool_name_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            events = [{"tool_name": "Grep", "count": 1, "latency_ms": 40, "failures": 0}]
            results = record_batch(out, "P5", events)
            self.assertEqual(results[0]["tool_name"], "Grep")


class TestSummarize(unittest.TestCase):
    def test_summary_aggregates_correctly(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            record_tool_call(out, "P3", "WebSearch", 3, 2100, 0)
            record_tool_call(out, "P3", "Read", 5, 150, 1)
            record_tool_call(out, "P4", "WebSearch", 2, 1000, 0)

            stats = summarize(out)
            self.assertEqual(stats["total_calls"], 10)
            self.assertEqual(stats["total_failures"], 1)
            self.assertIn("WebSearch", stats["by_tool"])
            self.assertEqual(stats["by_tool"]["WebSearch"]["count"], 5)
            self.assertIn("P3", stats["by_phase"])

    def test_summary_empty_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            stats = summarize(Path(tmp))
            self.assertEqual(stats["total_calls"], 0)
            self.assertEqual(stats["by_tool"], {})


class TestCLI(unittest.TestCase):
    def test_cli_record(self):
        from tool_call_counter import main
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["record", "--phase", "P3", "--tool", "WebSearch",
                        "--count", "2", "--latency-ms", "1500", "--failures", "0",
                        "--dir", tmp])
            self.assertEqual(ret, 0)

    def test_cli_record_batch(self):
        from tool_call_counter import main
        events = json.dumps([
            {"tool": "WebSearch", "count": 2, "latency_ms": 1000, "failures": 0},
            {"tool": "Read", "count": 1, "latency_ms": 50, "failures": 0},
        ])
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["record-batch", "--phase", "P3", "--dir", tmp, "--events", events])
            self.assertEqual(ret, 0)

    def test_cli_summary(self):
        from tool_call_counter import main
        with tempfile.TemporaryDirectory() as tmp:
            main(["record", "--phase", "P3", "--tool", "WebSearch",
                  "--count", "1", "--latency-ms", "800", "--dir", tmp])
            ret = main(["summary", "--dir", tmp])
            self.assertEqual(ret, 0)

    def test_cli_invalid_batch_json(self):
        from tool_call_counter import main
        with tempfile.TemporaryDirectory() as tmp:
            ret = main(["record-batch", "--phase", "P3", "--dir", tmp, "--events", "not-json"])
            self.assertEqual(ret, 3)


if __name__ == "__main__":
    unittest.main()
