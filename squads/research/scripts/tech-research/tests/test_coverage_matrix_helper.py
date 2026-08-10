#!/usr/bin/env python3
"""Unit tests for coverage_matrix_helper.py.

Origin: STORY-RA-F.2 AC-1, AC-2.

Run: python3 squads/research/scripts/tech-research/tests/test_coverage_matrix_helper.py
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from coverage_matrix_helper import (  # noqa: E402
    PT_BR_ALIASES,
    LEGACY_ALIASES,
    SCORE_MAP,
    STATUS_ENUM,
    SYMBOL_MAP_ASCII,
    SYMBOL_MAP_UNICODE,
    StatusValueError,
    normalize_status,
    status_to_score,
    status_to_symbol,
    validate_matrix,
)


class TestNormalizeStatus(unittest.TestCase):
    def test_canonical_identity(self):
        for status in STATUS_ENUM:
            self.assertEqual(normalize_status(status), status)

    def test_canonical_uppercase(self):
        self.assertEqual(normalize_status("CONFIRMED"), "confirmed")
        self.assertEqual(normalize_status("Partial"), "partial")

    def test_pt_br_aliases(self):
        self.assertEqual(normalize_status("sim"), "confirmed")
        self.assertEqual(normalize_status("parcial"), "partial")
        self.assertEqual(normalize_status("incerto"), "uncertain")
        self.assertEqual(normalize_status("não"), "not_present")
        self.assertEqual(normalize_status("nao"), "not_present")  # accent-stripped

    def test_pt_br_case_insensitive(self):
        self.assertEqual(normalize_status("SIM"), "confirmed")
        self.assertEqual(normalize_status("Parcial"), "partial")

    def test_legacy_aliases(self):
        self.assertEqual(normalize_status("tem"), "confirmed")
        self.assertEqual(normalize_status("yes"), "confirmed")
        self.assertEqual(normalize_status("ausente"), "not_present")
        self.assertEqual(normalize_status("no"), "not_present")

    def test_rejects_unknown(self):
        with self.assertRaises(StatusValueError):
            normalize_status("yolo")

    def test_rejects_none(self):
        with self.assertRaises(StatusValueError):
            normalize_status(None)

    def test_rejects_empty(self):
        with self.assertRaises(StatusValueError):
            normalize_status("")
        with self.assertRaises(StatusValueError):
            normalize_status("   ")

    def test_rejects_non_string(self):
        with self.assertRaises(StatusValueError):
            normalize_status(42)
        with self.assertRaises(StatusValueError):
            normalize_status(["confirmed"])

    def test_no_silent_uncertain_fallback(self):
        """Story §Anti-patterns: NEVER fall back to uncertain on missing."""
        for empty in (None, "", "  "):
            with self.assertRaises(StatusValueError):
                normalize_status(empty)


class TestStatusToScore(unittest.TestCase):
    def test_canonical(self):
        self.assertEqual(status_to_score("confirmed"), 2.0)
        self.assertEqual(status_to_score("partial"), 1.0)
        self.assertEqual(status_to_score("uncertain"), 0.5)
        self.assertEqual(status_to_score("not_present"), 0.0)

    def test_pt_br_round_trip(self):
        self.assertEqual(status_to_score("sim"), 2.0)
        self.assertEqual(status_to_score("não"), 0.0)

    def test_score_map_total_consistency(self):
        for status, score in SCORE_MAP.items():
            self.assertEqual(status_to_score(status), score)


class TestStatusToSymbol(unittest.TestCase):
    def setUp(self):
        os.environ.pop("RESEARCH_OUTPUT_ASCII", None)

    def tearDown(self):
        os.environ.pop("RESEARCH_OUTPUT_ASCII", None)

    def test_unicode_default(self):
        self.assertEqual(status_to_symbol("confirmed"), "✅")
        self.assertEqual(status_to_symbol("partial"), "◐")
        self.assertEqual(status_to_symbol("uncertain"), "?")
        self.assertEqual(status_to_symbol("not_present"), "—")

    def test_ascii_fallback(self):
        os.environ["RESEARCH_OUTPUT_ASCII"] = "true"
        self.assertEqual(status_to_symbol("confirmed"), "[X]")
        self.assertEqual(status_to_symbol("partial"), "[~]")
        self.assertEqual(status_to_symbol("uncertain"), "[?]")
        self.assertEqual(status_to_symbol("not_present"), "[ ]")

    def test_ascii_case_insensitive(self):
        os.environ["RESEARCH_OUTPUT_ASCII"] = "TRUE"
        self.assertEqual(status_to_symbol("confirmed"), "[X]")

    def test_unrelated_env_value_unicode(self):
        os.environ["RESEARCH_OUTPUT_ASCII"] = "false"
        self.assertEqual(status_to_symbol("confirmed"), "✅")

    def test_no_creative_emojis_in_maps(self):
        """Anti-pattern guard: confirm helper only ships canonical glyphs."""
        forbidden = {"🟢", "🟡", "🔴", "🟠"}
        for value in SYMBOL_MAP_UNICODE.values():
            self.assertNotIn(value, forbidden)
        for value in SYMBOL_MAP_ASCII.values():
            self.assertNotIn(value, forbidden)


class TestValidateMatrix(unittest.TestCase):
    def test_valid_dict_with_rows(self):
        matrix = {
            "rows": [
                {
                    "dimension": "agentic_planning",
                    "cells": {
                        "claude_code": "confirmed",
                        "aider": "partial",
                        "cline": "uncertain",
                        "openhands": "not_present",
                    },
                }
            ]
        }
        result = validate_matrix(matrix)
        self.assertTrue(result.valid, msg=result.errors)
        self.assertEqual(result.cell_count, 4)
        self.assertEqual(result.errors, [])

    def test_rejects_invalid_status(self):
        matrix = {
            "rows": [{"dimension": "x", "cells": {"a": "yolo", "b": "confirmed"}}]
        }
        result = validate_matrix(matrix)
        self.assertFalse(result.valid)
        self.assertTrue(any("yolo" in e for e in result.errors))

    def test_rejects_empty_cell(self):
        matrix = {"rows": [{"dimension": "x", "cells": {"a": "", "b": "confirmed"}}]}
        result = validate_matrix(matrix)
        self.assertFalse(result.valid)

    def test_pt_br_aliases_valid(self):
        matrix = {
            "rows": [
                {
                    "dimension": "x",
                    "cells": {
                        "a": "sim",
                        "b": "parcial",
                        "c": "incerto",
                        "d": "não",
                    },
                }
            ]
        }
        result = validate_matrix(matrix)
        self.assertTrue(result.valid, msg=result.errors)

    def test_cells_as_dict_with_status_field(self):
        matrix = {
            "rows": [
                {
                    "dimension": "x",
                    "cells": {
                        "a": {"status": "confirmed", "score": 2.0},
                        "b": {"status": "partial", "score": 1.0},
                    },
                }
            ]
        }
        result = validate_matrix(matrix)
        self.assertTrue(result.valid, msg=result.errors)

    def test_cells_without_status_field_emits_warning(self):
        """F.1 backwards-compat: score-only cells produce warnings, not errors."""
        matrix = {
            "rows": [{"dimension": "x", "cells": {"a": {"score": 2.0}}}]
        }
        result = validate_matrix(matrix)
        self.assertTrue(result.valid, msg=result.errors)
        self.assertTrue(any("no `status` field" in w for w in result.warnings))

    def test_flat_list_shape(self):
        matrix = ["confirmed", "partial", "uncertain"]
        result = validate_matrix(matrix)
        self.assertTrue(result.valid, msg=result.errors)
        self.assertEqual(result.cell_count, 3)

    def test_unknown_shape_invalid(self):
        result = validate_matrix(42)
        self.assertFalse(result.valid)
        self.assertTrue(any("unrecognized matrix shape" in e for e in result.errors))


class TestAliasIntegrity(unittest.TestCase):
    """Guard: aliases must always resolve to a canonical enum value."""

    def test_all_pt_br_aliases_canonical(self):
        for alias, canonical in PT_BR_ALIASES.items():
            self.assertIn(canonical, STATUS_ENUM, f"{alias} → {canonical}")

    def test_all_legacy_aliases_canonical(self):
        for alias, canonical in LEGACY_ALIASES.items():
            self.assertIn(canonical, STATUS_ENUM, f"{alias} → {canonical}")

    def test_score_map_covers_all_enum_values(self):
        for status in STATUS_ENUM:
            self.assertIn(status, SCORE_MAP)

    def test_symbol_maps_cover_all_enum_values(self):
        for status in STATUS_ENUM:
            self.assertIn(status, SYMBOL_MAP_UNICODE)
            self.assertIn(status, SYMBOL_MAP_ASCII)


if __name__ == "__main__":
    unittest.main()
