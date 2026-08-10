#!/usr/bin/env python3
"""Smoke tests for citation_verifier.py — STORY-RA-D.1.

Run:
    python3 squads/research/scripts/tech-research/tests/test_citation_verifier.py
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from citation_verifier import (  # noqa: E402
    aggregate_claims,
    fetch_archive_snapshot,
    classify_claim,
    rewrite_claim,
    load_sackett_grades,
    APPROVE_CLEAN_THRESHOLD,
    APPROVE_WITH_CONFIDENCE_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_claim(status="MATCHED", matched=None, text="73% of users prefer this approach."):
    return {
        "claim_id": "C001",
        "text": text,
        "type": "statistic",
        "status": status,
        "matched_sources": matched or [],
        "live_sources": [],
        "archive_sources": [],
        "confidence": None,
        "evidence_grade": None,
    }


def _make_source(url="https://example.com/src", title="Tech Report", snippet="73% of surveyed users prefer"):
    return {"url": url, "title": title, "snippet": snippet}


# ---------------------------------------------------------------------------
# AC-1 — archive.org fallback
# ---------------------------------------------------------------------------

class TestArchiveFallback(unittest.TestCase):
    """AC-1: archive.org snapshot fallback for dead URLs."""

    def test_returns_snapshot_url_when_available(self):
        mock_response = {
            "archived_snapshots": {
                "closest": {
                    "available": True,
                    "url": "https://web.archive.org/web/20240101/https://example.com/page",
                }
            }
        }
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_cm = mock_urlopen.return_value.__enter__.return_value
            mock_cm.read.return_value = json.dumps(mock_response).encode()
            mock_cm.status = 200
            result = fetch_archive_snapshot("https://example.com/page")
        self.assertIsNotNone(result)
        self.assertIn("archive.org", result)

    def test_returns_none_when_no_snapshot(self):
        mock_response = {"archived_snapshots": {}}
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_cm = mock_urlopen.return_value.__enter__.return_value
            mock_cm.read.return_value = json.dumps(mock_response).encode()
            mock_cm.status = 200
            result = fetch_archive_snapshot("https://totally-dead-url.example/page")
        self.assertIsNone(result)

    def test_returns_none_on_network_error(self):
        import urllib.error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("timeout")):
            result = fetch_archive_snapshot("https://example.com/page")
        self.assertIsNone(result)


# ---------------------------------------------------------------------------
# AC-2 — Per-claim classification
# ---------------------------------------------------------------------------

class TestClaimClassification(unittest.TestCase):
    """AC-2: supported | unsupported | unknown | ambiguous classification."""

    def test_unsupported_when_no_sources_and_unsourced(self):
        claim = _make_claim(status="UNSOURCED", matched=[])
        result = classify_claim(claim, sources=[])
        self.assertEqual(result["status"], "unsupported")

    def test_unknown_when_no_matched_sources(self):
        """Claim that was MATCHED but all URLs are dead and no archive."""
        claim = _make_claim(status="MATCHED", matched=[{"url": "https://dead.example.com/", "match_score": 2.0}])
        # Simulate: URL is dead, no archive snapshot
        with patch("citation_verifier.check_url_liveness", return_value=False), \
             patch("citation_verifier.fetch_archive_snapshot", return_value=None):
            result = classify_claim(claim, sources=[_make_source("https://dead.example.com/")])
        self.assertEqual(result["status"], "unsupported")

    def test_supported_when_live_source_high_score(self):
        claim = _make_claim(
            matched=[{"url": "https://example.com/src", "match_score": 3.5}]
        )
        with patch("citation_verifier.check_url_liveness", return_value=True):
            result = classify_claim(claim, sources=[_make_source()])
        self.assertEqual(result["status"], "supported")
        self.assertEqual(result["confidence"], "high")

    def test_ambiguous_when_source_is_hedged(self):
        claim = _make_claim(
            matched=[{"url": "https://example.com/src", "match_score": 2.0}]
        )
        hedged_source = _make_source(snippet="approximately 73% of users may prefer this approach")
        with patch("citation_verifier.check_url_liveness", return_value=True):
            result = classify_claim(claim, sources=[hedged_source])
        self.assertEqual(result["status"], "ambiguous")

    def test_archive_url_set_when_snapshot_found(self):
        claim = _make_claim(matched=[{"url": "https://dead.example.com/", "match_score": 2.0}])
        with patch("citation_verifier.check_url_liveness", return_value=False), \
             patch("citation_verifier.fetch_archive_snapshot",
                   return_value="https://web.archive.org/web/20240101/https://dead.example.com/"):
            result = classify_claim(claim, sources=[_make_source("https://dead.example.com/")])
        self.assertIsNotNone(result["archive_url"])
        self.assertIn("archive.org", result["archive_url"])


# ---------------------------------------------------------------------------
# AC-3 — Rewrite-claim with audit trail
# ---------------------------------------------------------------------------

class TestRewriteClaim(unittest.TestCase):
    """AC-3: rewrite-claim for ambiguous claims."""

    def test_rewrite_sets_original_claim(self):
        claim = _make_claim(status="ambiguous")
        claim["live_sources"] = [{"url": "https://example.com/src", "match_score": 2.0}]
        result = rewrite_claim(claim, sources=[_make_source()])
        self.assertEqual(result["original_claim"], claim["text"])
        self.assertTrue(result["rewritten"])
        self.assertIsNotNone(result["rewrite_rationale"])

    def test_rewrite_changes_status_to_supported(self):
        claim = _make_claim(status="ambiguous")
        claim["live_sources"] = []
        result = rewrite_claim(claim, sources=[])
        self.assertEqual(result["status"], "supported")

    def test_rewrite_fallback_softens_claim(self):
        claim = _make_claim(status="ambiguous")
        claim["live_sources"] = []
        result = rewrite_claim(claim, sources=[])
        # Fallback: should add softener (e.g. "reportedly" or similar)
        self.assertNotEqual(result["text"], result["original_claim"])

    def test_rewrite_text_different_from_original(self):
        claim = _make_claim(status="ambiguous")
        claim["live_sources"] = [{"url": "https://example.com/src", "match_score": 2.0}]
        result = rewrite_claim(claim, sources=[_make_source(snippet="studies suggest roughly 70% prefer")])
        self.assertNotEqual(result["text"], claim["text"])


# ---------------------------------------------------------------------------
# AC-4 — Veto threshold
# ---------------------------------------------------------------------------

class TestAggregation(unittest.TestCase):
    """AC-4: veto threshold unsupported_top_tier > 20%."""

    def test_approve_clean_when_low_unsupported(self):
        claims = [{"status": "supported", "confidence": "high", "evidence_grade": None}] * 20
        result = aggregate_claims(claims)
        self.assertEqual(result["verdict"], "APPROVE")
        self.assertLessEqual(result["unsupported_ratio"], APPROVE_CLEAN_THRESHOLD)

    def test_approve_with_confidence_when_moderate_unsupported(self):
        claims = (
            [{"status": "supported", "confidence": "high", "evidence_grade": None}] * 85 +
            [{"status": "unsupported", "confidence": "none", "evidence_grade": None}] * 10
        )
        result = aggregate_claims(claims)
        self.assertEqual(result["verdict"], "APPROVE_WITH_CONFIDENCE")

    def test_veto_when_top_tier_unsupported_exceeds_20_pct(self):
        claims = (
            [{"status": "supported", "confidence": "high", "evidence_grade": "2b"}] * 70 +
            [{"status": "unsupported", "confidence": "none", "evidence_grade": "1a"}] * 25
        )
        result = aggregate_claims(claims)
        self.assertEqual(result["verdict"], "VETO")
        self.assertGreater(result["unsupported_top_tier_ratio"], APPROVE_WITH_CONFIDENCE_THRESHOLD)

    def test_no_veto_if_unsupported_not_top_tier(self):
        """unsupported_ratio > 20% but evidence_grade=5 → not top-tier → APPROVE_WITH_CONFIDENCE."""
        claims = (
            [{"status": "supported", "confidence": "high", "evidence_grade": "1a"}] * 70 +
            [{"status": "unsupported", "confidence": "none", "evidence_grade": "5"}] * 30
        )
        result = aggregate_claims(claims)
        # unsupported_top_tier_ratio = 0 (grade 5 not top-tier)
        self.assertNotEqual(result["verdict"], "VETO")

    def test_empty_claims_returns_approve(self):
        result = aggregate_claims([])
        self.assertEqual(result["verdict"], "APPROVE")
        self.assertEqual(result["total"], 0)

    def test_confidence_distribution_populated(self):
        claims = [
            {"status": "supported", "confidence": "high", "evidence_grade": None},
            {"status": "unsupported", "confidence": "none", "evidence_grade": None},
            {"status": "unknown", "confidence": "low", "evidence_grade": None},
        ]
        result = aggregate_claims(claims)
        self.assertEqual(result["confidence_distribution"]["high"], 1)
        self.assertEqual(result["confidence_distribution"]["none"], 1)
        self.assertEqual(result["confidence_distribution"]["low"], 1)


# ---------------------------------------------------------------------------
# AC-5 — Sackett integration graceful fallback
# ---------------------------------------------------------------------------

class TestSackettIntegration(unittest.TestCase):
    """AC-5: Sackett grades integrated; graceful fallback if absent."""

    def test_sackett_grade_enriches_claim(self):
        sackett = {"C001": {"claim_id": "C001", "evidence_grade": "1a", "rationale": "RCT"}}
        claim = _make_claim(matched=[{"url": "https://example.com/src", "match_score": 3.5}])
        with patch("citation_verifier.check_url_liveness", return_value=True):
            result = classify_claim(claim, sources=[_make_source()], sackett_graded=sackett)
        self.assertEqual(result["evidence_grade"], "1a")

    def test_graceful_fallback_when_sackett_missing(self):
        claim = _make_claim(matched=[{"url": "https://example.com/src", "match_score": 3.5}])
        with patch("citation_verifier.check_url_liveness", return_value=True):
            result = classify_claim(claim, sources=[_make_source()], sackett_graded=None)
        self.assertIsNone(result["evidence_grade"])

    def test_load_sackett_grades_returns_empty_on_missing_file(self):
        result = load_sackett_grades("/tmp/nonexistent-sackett-12345.md")
        self.assertEqual(result, {})


# ---------------------------------------------------------------------------
# CLI smoke
# ---------------------------------------------------------------------------

class TestCLI(unittest.TestCase):
    """CLI smoke tests."""

    def test_archive_check_command(self):
        from citation_verifier import main
        import io, contextlib
        mock_response = {
            "archived_snapshots": {
                "closest": {"available": True, "url": "https://web.archive.org/web/20240101/x"}
            }
        }
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_cm = mock_urlopen.return_value.__enter__.return_value
            mock_cm.read.return_value = json.dumps(mock_response).encode()
            mock_cm.status = 200
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ret = main(["archive-check", "--url", "https://example.com/page"])
        self.assertEqual(ret, 0)
        data = json.loads(buf.getvalue())
        self.assertTrue(data["found"])

    def test_missing_command_returns_3(self):
        from citation_verifier import main
        ret = main([])
        self.assertEqual(ret, 3)

    def test_verify_missing_args_returns_3(self):
        from citation_verifier import main
        ret = main(["verify"])
        self.assertEqual(ret, 3)


if __name__ == "__main__":
    unittest.main()
