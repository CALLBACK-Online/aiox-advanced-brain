#!/usr/bin/env python3
"""Smoke tests for claim_extractor.py RA-D.1 per-claim metadata additions.

Run:
    python3 squads/research/scripts/tech-research/tests/test_claim_extractor_rad1.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from claim_extractor import extract_claims, match_claims_to_sources  # noqa: E402


SAMPLE_TEXT = """
Research shows 73% of developers prefer Python for data tasks.
The market reached $4.2B in Q1 2024, representing significant growth.
GPT-4 outperforms all competitors on MMLU benchmark with 86.4% accuracy.
#1 in open-source LLM adoption for enterprise deployments.
Over 500 models available on the HuggingFace platform.
"""

SAMPLE_SOURCES = [
    {
        "url": "https://example.com/devsurvey",
        "title": "Developer Survey 2024",
        "snippet": "73% of developers prefer Python",
    },
    {
        "url": "https://example.com/market",
        "title": "AI Market Report",
        "snippet": "$4.2B market valuation in Q1 2024",
    },
]


class TestClaimExtractorRadD1(unittest.TestCase):
    """RA-D.1: per-claim metadata emitted by extract_claims."""

    def test_claims_have_claim_id(self):
        claims = extract_claims(SAMPLE_TEXT)
        self.assertGreater(len(claims), 0)
        for c in claims:
            self.assertIn("claim_id", c, f"Missing claim_id in claim: {c}")

    def test_claim_ids_are_sequential(self):
        claims = extract_claims(SAMPLE_TEXT)
        for i, c in enumerate(claims):
            expected = f"C{(i + 1):03d}"
            self.assertEqual(c["claim_id"], expected, f"Expected {expected}, got {c['claim_id']}")

    def test_claims_have_per_claim_metadata_fields(self):
        required = {"claim_id", "text", "type", "has_confidence_tag",
                    "status", "rewritten", "original_claim", "confidence", "evidence_grade"}
        claims = extract_claims(SAMPLE_TEXT)
        for c in claims:
            missing = required - set(c.keys())
            self.assertFalse(missing, f"Missing fields {missing} in claim: {c}")

    def test_rewritten_defaults_to_false(self):
        claims = extract_claims(SAMPLE_TEXT)
        for c in claims:
            self.assertFalse(c["rewritten"])

    def test_original_claim_defaults_to_none(self):
        claims = extract_claims(SAMPLE_TEXT)
        for c in claims:
            self.assertIsNone(c["original_claim"])

    def test_confidence_defaults_to_none(self):
        claims = extract_claims(SAMPLE_TEXT)
        for c in claims:
            self.assertIsNone(c["confidence"])

    def test_evidence_grade_defaults_to_none(self):
        claims = extract_claims(SAMPLE_TEXT)
        for c in claims:
            self.assertIsNone(c["evidence_grade"])

    def test_no_duplicate_claim_ids(self):
        claims = extract_claims(SAMPLE_TEXT)
        ids = [c["claim_id"] for c in claims]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate claim_ids found")


class TestMatchClaimsRadD1(unittest.TestCase):
    """RA-D.1: match output includes per-claim metadata passthrough."""

    def test_match_output_includes_claim_id(self):
        claims = extract_claims(SAMPLE_TEXT)
        results = match_claims_to_sources(claims, SAMPLE_SOURCES)
        for r in results:
            self.assertIn("claim_id", r)

    def test_match_output_includes_text_field(self):
        """RA-D.1: text field added for citation_verifier compatibility."""
        claims = extract_claims(SAMPLE_TEXT)
        results = match_claims_to_sources(claims, SAMPLE_SOURCES)
        for r in results:
            self.assertIn("text", r)
            self.assertEqual(r["text"], r["claim"])

    def test_match_output_preserves_rewritten_false(self):
        claims = extract_claims(SAMPLE_TEXT)
        results = match_claims_to_sources(claims, SAMPLE_SOURCES)
        for r in results:
            self.assertFalse(r["rewritten"])

    def test_matched_status_correct(self):
        claims = extract_claims(SAMPLE_TEXT)
        results = match_claims_to_sources(claims, SAMPLE_SOURCES)
        statuses = {r["status"] for r in results}
        self.assertTrue(statuses.issubset({"MATCHED", "UNSOURCED"}))


if __name__ == "__main__":
    unittest.main()
