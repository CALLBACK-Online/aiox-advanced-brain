#!/usr/bin/env python3
"""extraction_escalator.py — Fallback ladder for source content extraction.

Implements the 5-step extraction ladder declared in:
  squads/research/data/extraction-policy.yaml

Story: STORY-RA-F.3 (Wave 14, Sprint F, 2026-05-19)
Evidence: Manus sessions 2/2 — explicit "visual navigation" fallback pattern.

Ladder steps (in order):
  1. websearch_snippet  — fast, cheap, always first
  2. webfetch           — full-page, medium cost
  3. etl_adapter        — structured types (YouTube/PDF/arXiv/PubMed)
  4. playwright         — JS-rendered pages, browser-based
  5. mark_blocked       — terminal: register in caveats, stop

Non-negotiable rules (per .claude/rules/extraction-no-fallbacks.md):
  - NEVER return a universal default value when extraction fails
  - NEVER silence failures — always return explicit log
  - Emit extraction_* fields ONLY when data is available
  - Omit fields when data is absent (do not fill with placeholder defaults)

Usage
-----
  # As a library:
  from extraction_escalator import escalate, ExtractionResult

  result = escalate(url="https://example.com", initial_method="websearch_snippet")
  print(result.method_used, result.quality, result.attempts_log)

  # CLI (for testing):
  python3 extraction_escalator.py https://example.com
  python3 extraction_escalator.py https://example.com --initial-method webfetch
  python3 extraction_escalator.py --test-ladder   # runs unit tests
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional

# ─────────────────────────────────────────────────────────────────────────────
# Constants from extraction-policy.yaml
# ─────────────────────────────────────────────────────────────────────────────

PER_STEP_TIMEOUT_SECONDS = 15
TOTAL_LADDER_TIMEOUT_SECONDS = 60
SNIPPET_QUALITY_THRESHOLD = 0.7
MIN_CHARS_FULL = 800
MIN_CHARS_SNIPPET = 150

ETL_SUPPORTED_TYPES = frozenset({"youtube", "pdf", "arxiv", "pubmed", "semantic_scholar"})


class ExtractionMethod(str, Enum):
    WEBSEARCH_SNIPPET = "websearch_snippet"
    WEBFETCH = "webfetch"
    ETL_ADAPTER = "etl"
    PLAYWRIGHT = "playwright"
    EXTRACTION_BLOCKED = "extraction_blocked"


class ExtractionQuality(str, Enum):
    FULL = "full"
    SNIPPET_ONLY = "snippet_only"
    BLOCKED_FALLBACK_USED = "blocked_fallback_used"


# ─────────────────────────────────────────────────────────────────────────────
# Result type
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class StepAttempt:
    step: int
    method: str
    started_at: float
    completed_at: Optional[float] = None
    success: bool = False
    reason: str = ""
    content_chars: int = 0

    def duration_ms(self) -> int:
        if self.completed_at is None:
            return 0
        return int((self.completed_at - self.started_at) * 1000)


@dataclass
class ExtractionResult:
    """Return value of escalate(). All fields are present; 'content' may be None on block."""

    url: str
    content: Optional[str]            # None when mark_blocked
    method_used: ExtractionMethod
    quality: ExtractionQuality
    attempts_count: int
    attempts_log: list[StepAttempt] = field(default_factory=list)

    # extraction_* fields emitted in sources.yaml when available
    extraction_method: str = ""        # populated from method_used.value
    extraction_quality: str = ""       # populated from quality.value
    extraction_attempts: int = 0       # same as attempts_count
    extraction_ladder_steps_tried: list[str] = field(default_factory=list)
    extraction_notes: Optional[str] = None   # omitted when None (no-fallback rule)

    def to_sources_fields(self) -> dict[str, Any]:
        """Return the extraction_* fields to append to a sources.yaml entry.

        Follows extraction-no-fallbacks.md: fields are OMITTED when data absent.
        The dict contains only fields that carry real signal.
        """
        out: dict[str, Any] = {
            "extraction_method": self.extraction_method,
            "extraction_quality": self.extraction_quality,
            "extraction_attempts": self.extraction_attempts,
        }
        if self.extraction_ladder_steps_tried:
            out["extraction_ladder_steps_tried"] = self.extraction_ladder_steps_tried
        if self.extraction_notes:
            out["extraction_notes"] = self.extraction_notes
        return out


# ─────────────────────────────────────────────────────────────────────────────
# Content-type inference helpers
# ─────────────────────────────────────────────────────────────────────────────

def _infer_content_type(url: str) -> str:
    """Heuristic content-type inference from URL pattern. Never raises."""
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    if url_lower.endswith(".pdf") or "/pdf/" in url_lower:
        return "pdf"
    if "arxiv.org" in url_lower:
        return "arxiv"
    if "pubmed.ncbi.nlm.nih.gov" in url_lower or "ncbi.nlm.nih.gov/pmc" in url_lower:
        return "pubmed"
    if "semanticscholar.org" in url_lower:
        return "semantic_scholar"
    return "web"


def _assess_quality(content: Optional[str]) -> ExtractionQuality:
    """Assess content quality based on char count thresholds from policy."""
    if content is None:
        return ExtractionQuality.BLOCKED_FALLBACK_USED
    length = len(content.strip())
    if length >= MIN_CHARS_FULL:
        return ExtractionQuality.FULL
    if length >= MIN_CHARS_SNIPPET:
        return ExtractionQuality.SNIPPET_ONLY
    return ExtractionQuality.BLOCKED_FALLBACK_USED


def _snippet_quality_ratio(content: Optional[str]) -> float:
    """Return quality ratio [0.0-1.0] for snippet-quality threshold comparison."""
    if not content:
        return 0.0
    length = len(content.strip())
    if length >= MIN_CHARS_FULL:
        return 1.0
    if length >= MIN_CHARS_SNIPPET:
        return length / MIN_CHARS_FULL  # partial score between threshold and full
    return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Step executor stubs
# In production, these would call the real MCP/ETL adapters.
# They accept an optional adapter_fn for injection in tests.
# ─────────────────────────────────────────────────────────────────────────────

def _execute_websearch_snippet(
    url: str,
    adapter_fn: Optional[Callable[[str], Optional[str]]] = None,
) -> Optional[str]:
    """Step 1: WebSearch snippet. Returns content string or None on failure."""
    if adapter_fn is not None:
        return adapter_fn(url)
    # Production: invoke WebSearch MCP tool.
    # This stub returns None to signal the escalator should try next steps.
    # Real implementation would call: WebSearch(query=f"site:{domain} {path}")
    return None


def _execute_webfetch(
    url: str,
    adapter_fn: Optional[Callable[[str], Optional[str]]] = None,
) -> Optional[str]:
    """Step 2: WebFetch full-page. Returns content or None on failure."""
    if adapter_fn is not None:
        return adapter_fn(url)
    # Production: invoke WebFetch MCP tool.
    # Real implementation: WebFetch(url=url)
    return None


def _execute_etl_adapter(
    url: str,
    content_type: str,
    adapter_fn: Optional[Callable[[str, str], Optional[str]]] = None,
) -> Optional[str]:
    """Step 3: ETL adapter for structured content types."""
    if adapter_fn is not None:
        return adapter_fn(url, content_type)
    # Production: route to services/etl/{content_type}_adapter
    # e.g. for arxiv: fetch abstract+body via arxiv API
    return None


def _execute_playwright(
    url: str,
    adapter_fn: Optional[Callable[[str], Optional[str]]] = None,
    playwright_available: bool = False,
) -> Optional[str]:
    """Step 4: Playwright browser rendering for JS-heavy pages."""
    if not playwright_available:
        return None
    if adapter_fn is not None:
        return adapter_fn(url)
    # Production: invoke Playwright MCP tool
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Core escalator
# ─────────────────────────────────────────────────────────────────────────────

def escalate(
    url: str,
    initial_method: str = "websearch_snippet",
    *,
    content_type: Optional[str] = None,
    playwright_available: bool = False,
    # Adapter injection for testing
    websearch_fn: Optional[Callable[[str], Optional[str]]] = None,
    webfetch_fn: Optional[Callable[[str], Optional[str]]] = None,
    etl_fn: Optional[Callable[[str, str], Optional[str]]] = None,
    playwright_fn: Optional[Callable[[str], Optional[str]]] = None,
) -> ExtractionResult:
    """Run the extraction ladder for a URL. Returns ExtractionResult.

    The function NEVER raises — all exceptions become blocked results.
    NEVER returns a universal default content string (extraction-no-fallbacks rule).

    Args:
        url: Target URL to extract content from.
        initial_method: Starting step in the ladder (default: websearch_snippet).
        content_type: Override auto-inferred content type.
        playwright_available: Whether Playwright MCP is available in this session.
        websearch_fn / webfetch_fn / etl_fn / playwright_fn: Optional adapter
            functions for testing. Production code leaves these as None.

    Returns:
        ExtractionResult with method_used, quality, attempts_log, and
        extraction_* fields ready to merge into sources.yaml.
    """
    inferred_type = content_type or _infer_content_type(url)
    start_time = time.monotonic()
    attempts_log: list[StepAttempt] = []
    steps_tried: list[str] = []

    # Determine starting step index
    method_order = [m.value for m in ExtractionMethod if m != ExtractionMethod.EXTRACTION_BLOCKED]
    try:
        start_idx = method_order.index(initial_method)
    except ValueError:
        start_idx = 0

    content: Optional[str] = None
    method_used = ExtractionMethod.EXTRACTION_BLOCKED

    # ── Step 1: websearch_snippet ─────────────────────────────────────────
    if start_idx <= 0:
        elapsed = time.monotonic() - start_time
        if elapsed < TOTAL_LADDER_TIMEOUT_SECONDS:
            attempt = StepAttempt(step=1, method="websearch_snippet", started_at=time.monotonic())
            steps_tried.append("websearch_snippet")
            try:
                result = _execute_websearch_snippet(url, adapter_fn=websearch_fn)
                attempt.completed_at = time.monotonic()
                if result and _snippet_quality_ratio(result) >= SNIPPET_QUALITY_THRESHOLD:
                    attempt.success = True
                    attempt.content_chars = len(result)
                    attempt.reason = f"quality_ratio={_snippet_quality_ratio(result):.2f} >= {SNIPPET_QUALITY_THRESHOLD}"
                    content = result
                    method_used = ExtractionMethod.WEBSEARCH_SNIPPET
                elif result:
                    # Got something but below quality threshold — record and continue
                    attempt.success = False
                    attempt.content_chars = len(result)
                    attempt.reason = f"low_quality: ratio={_snippet_quality_ratio(result):.2f} < {SNIPPET_QUALITY_THRESHOLD}"
                    content = result  # keep as fallback; may be upgraded by later steps
                else:
                    attempt.success = False
                    attempt.reason = "no_content_returned"
            except Exception as exc:
                attempt.completed_at = time.monotonic()
                attempt.success = False
                attempt.reason = f"exception: {type(exc).__name__}: {exc}"
            attempts_log.append(attempt)
            if attempt.success:
                return _build_result(url, content, method_used, attempts_log, steps_tried)

    # ── Step 2: webfetch ──────────────────────────────────────────────────
    if start_idx <= 1 and method_used == ExtractionMethod.EXTRACTION_BLOCKED:
        elapsed = time.monotonic() - start_time
        if elapsed < TOTAL_LADDER_TIMEOUT_SECONDS:
            # Skip if no URL available or already have acceptable quality
            if _snippet_quality_ratio(content) >= SNIPPET_QUALITY_THRESHOLD:
                pass  # skip — quality threshold already met by step 1
            else:
                attempt = StepAttempt(step=2, method="webfetch", started_at=time.monotonic())
                steps_tried.append("webfetch")
                try:
                    result = _execute_webfetch(url, adapter_fn=webfetch_fn)
                    attempt.completed_at = time.monotonic()
                    if result and len(result.strip()) >= MIN_CHARS_SNIPPET:
                        attempt.success = True
                        attempt.content_chars = len(result)
                        attempt.reason = f"content_chars={len(result)}"
                        content = result
                        method_used = ExtractionMethod.WEBFETCH
                    else:
                        attempt.success = False
                        attempt.reason = "insufficient_content" if result else "no_content_returned"
                except Exception as exc:
                    attempt.completed_at = time.monotonic()
                    attempt.success = False
                    attempt.reason = f"exception: {type(exc).__name__}: {exc}"
                attempts_log.append(attempt)
                if attempt.success:
                    return _build_result(url, content, method_used, attempts_log, steps_tried)

    # ── Step 3: etl_adapter ───────────────────────────────────────────────
    if start_idx <= 2 and method_used == ExtractionMethod.EXTRACTION_BLOCKED:
        elapsed = time.monotonic() - start_time
        if elapsed < TOTAL_LADDER_TIMEOUT_SECONDS and inferred_type in ETL_SUPPORTED_TYPES:
            attempt = StepAttempt(step=3, method="etl_adapter", started_at=time.monotonic())
            steps_tried.append("etl_adapter")
            try:
                result = _execute_etl_adapter(url, inferred_type, adapter_fn=etl_fn)
                attempt.completed_at = time.monotonic()
                if result and len(result.strip()) >= MIN_CHARS_SNIPPET:
                    attempt.success = True
                    attempt.content_chars = len(result)
                    attempt.reason = f"etl:{inferred_type}, chars={len(result)}"
                    content = result
                    method_used = ExtractionMethod.ETL_ADAPTER
                else:
                    attempt.success = False
                    attempt.reason = f"etl:{inferred_type}: " + ("insufficient_content" if result else "no_content")
            except Exception as exc:
                attempt.completed_at = time.monotonic()
                attempt.success = False
                attempt.reason = f"exception: {type(exc).__name__}: {exc}"
            attempts_log.append(attempt)
            if attempt.success:
                return _build_result(url, content, method_used, attempts_log, steps_tried)

    # ── Step 4: playwright ────────────────────────────────────────────────
    if start_idx <= 3 and method_used == ExtractionMethod.EXTRACTION_BLOCKED:
        elapsed = time.monotonic() - start_time
        if elapsed < TOTAL_LADDER_TIMEOUT_SECONDS and playwright_available:
            attempt = StepAttempt(step=4, method="playwright", started_at=time.monotonic())
            steps_tried.append("playwright")
            try:
                result = _execute_playwright(url, adapter_fn=playwright_fn, playwright_available=playwright_available)
                attempt.completed_at = time.monotonic()
                if result and len(result.strip()) >= MIN_CHARS_SNIPPET:
                    attempt.success = True
                    attempt.content_chars = len(result)
                    attempt.reason = f"playwright_rendered, chars={len(result)}"
                    content = result
                    method_used = ExtractionMethod.PLAYWRIGHT
                else:
                    attempt.success = False
                    attempt.reason = "playwright: " + ("insufficient_content" if result else "no_content")
            except Exception as exc:
                attempt.completed_at = time.monotonic()
                attempt.success = False
                attempt.reason = f"exception: {type(exc).__name__}: {exc}"
            attempts_log.append(attempt)
            if attempt.success:
                return _build_result(url, content, method_used, attempts_log, steps_tried)
        elif not playwright_available:
            steps_tried.append("playwright_skipped:unavailable")

    # ── Step 5: mark_blocked (terminal) ──────────────────────────────────
    steps_tried.append("mark_blocked")
    # Use best partial content if any was captured
    return _build_result(url, None, ExtractionMethod.EXTRACTION_BLOCKED, attempts_log, steps_tried, blocked=True)


def _build_result(
    url: str,
    content: Optional[str],
    method_used: ExtractionMethod,
    attempts_log: list[StepAttempt],
    steps_tried: list[str],
    blocked: bool = False,
) -> ExtractionResult:
    """Assemble ExtractionResult from ladder state."""
    quality = ExtractionQuality.BLOCKED_FALLBACK_USED if blocked else _assess_quality(content)

    notes: Optional[str] = None
    if blocked:
        tried = [s for s in steps_tried if s != "mark_blocked"]
        notes = f"All ladder steps exhausted ({', '.join(tried)}). Source URL inaccessible."

    result = ExtractionResult(
        url=url,
        content=content,
        method_used=method_used,
        quality=quality,
        attempts_count=len(attempts_log),
        attempts_log=attempts_log,
        extraction_method=method_used.value,
        extraction_quality=quality.value,
        extraction_attempts=len(attempts_log),
        extraction_ladder_steps_tried=steps_tried if len(steps_tried) > 1 else [],
        extraction_notes=notes,  # omit when None (single successful step needs no note)
    )
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Unit tests (runnable via --test-ladder flag)
# ─────────────────────────────────────────────────────────────────────────────

def _run_unit_tests() -> int:
    """Run unit tests covering each ladder step. Returns 0 on pass, 1 on fail."""
    failures: list[str] = []
    tests_run = 0

    def ok(name: str) -> None:
        pass

    def fail(name: str, msg: str) -> None:
        failures.append(f"FAIL [{name}]: {msg}")

    def assert_eq(name: str, got: Any, expected: Any) -> None:
        nonlocal tests_run
        tests_run += 1
        if got != expected:
            fail(name, f"expected {expected!r}, got {got!r}")
        else:
            ok(name)

    def assert_true(name: str, condition: bool, msg: str = "") -> None:
        nonlocal tests_run
        tests_run += 1
        if not condition:
            fail(name, msg or "condition is False")
        else:
            ok(name)

    # ── Test 1: Step 1 succeeds → returns websearch_snippet ──────────────
    def adapter_step1_full(url: str) -> str:
        return "A" * MIN_CHARS_FULL  # quality >= 0.7

    r = escalate("https://example.com/doc", websearch_fn=adapter_step1_full)
    assert_eq("T1.method_used", r.method_used, ExtractionMethod.WEBSEARCH_SNIPPET)
    assert_eq("T1.quality", r.quality, ExtractionQuality.FULL)
    assert_eq("T1.attempts", r.attempts_count, 1)
    assert_true("T1.content_not_none", r.content is not None, "content should not be None on success")

    # ── Test 2: Step 1 low quality → escalates to step 2 which succeeds ──
    def adapter_step1_low(url: str) -> str:
        return "B" * 100  # below MIN_CHARS_SNIPPET

    def adapter_step2_ok(url: str) -> str:
        return "C" * MIN_CHARS_FULL

    r = escalate("https://example.com/doc",
                 websearch_fn=adapter_step1_low,
                 webfetch_fn=adapter_step2_ok)
    assert_eq("T2.method_used", r.method_used, ExtractionMethod.WEBFETCH)
    assert_eq("T2.quality", r.quality, ExtractionQuality.FULL)
    assert_true("T2.steps_tried_includes_both",
                "websearch_snippet" in r.extraction_ladder_steps_tried and
                "webfetch" in r.extraction_ladder_steps_tried,
                f"steps={r.extraction_ladder_steps_tried}")

    # ── Test 3: Steps 1-2 fail → step 3 (ETL) for arxiv URL ─────────────
    def adapter_step1_none(url: str) -> Optional[str]:
        return None

    def adapter_step2_none(url: str) -> Optional[str]:
        return None

    def adapter_etl_ok(url: str, content_type: str) -> str:
        return "D" * MIN_CHARS_FULL

    r = escalate("https://arxiv.org/abs/2301.12345",
                 websearch_fn=adapter_step1_none,
                 webfetch_fn=adapter_step2_none,
                 etl_fn=adapter_etl_ok)
    assert_eq("T3.method_used", r.method_used, ExtractionMethod.ETL_ADAPTER)
    assert_eq("T3.quality", r.quality, ExtractionQuality.FULL)
    assert_true("T3.arxiv_type_detected",
                "etl_adapter" in r.extraction_ladder_steps_tried,
                f"steps={r.extraction_ladder_steps_tried}")

    # ── Test 4: All steps fail → mark_blocked ────────────────────────────
    r = escalate("https://blocked.example.com/paywall",
                 websearch_fn=adapter_step1_none,
                 webfetch_fn=adapter_step2_none,
                 playwright_available=False)
    assert_eq("T4.method_used", r.method_used, ExtractionMethod.EXTRACTION_BLOCKED)
    assert_eq("T4.quality", r.quality, ExtractionQuality.BLOCKED_FALLBACK_USED)
    assert_true("T4.content_is_none", r.content is None, "blocked result must have None content")
    assert_true("T4.notes_not_empty",
                bool(r.extraction_notes),
                "blocked result must have extraction_notes")

    # ── Test 5: Step 4 (playwright) when available ────────────────────────
    def adapter_playwright_ok(url: str) -> str:
        return "E" * MIN_CHARS_FULL

    r = escalate("https://spa.example.com/page",
                 websearch_fn=adapter_step1_none,
                 webfetch_fn=adapter_step2_none,
                 playwright_available=True,
                 playwright_fn=adapter_playwright_ok)
    assert_eq("T5.method_used", r.method_used, ExtractionMethod.PLAYWRIGHT)
    assert_eq("T5.quality", r.quality, ExtractionQuality.FULL)

    # ── Test 6: to_sources_fields omits None extraction_notes ────────────
    r = escalate("https://ok.example.com", websearch_fn=adapter_step1_full)
    fields = r.to_sources_fields()
    assert_true("T6.notes_absent_on_success",
                "extraction_notes" not in fields,
                f"extraction_notes should be omitted on success, got fields={fields}")
    assert_true("T6.method_present", "extraction_method" in fields)

    # ── Test 7: blocked URL → sources fields include extraction_notes ─────
    r = escalate("https://blocked.example.com",
                 websearch_fn=adapter_step1_none,
                 webfetch_fn=adapter_step2_none)
    fields = r.to_sources_fields()
    assert_true("T7.notes_present_on_block",
                "extraction_notes" in fields,
                "extraction_notes should be present when blocked")
    assert_eq("T7.blocked_method", fields.get("extraction_method"), "extraction_blocked")

    # ── Test 8: Non-ETL URL skips step 3 → mark_blocked without ETL ──────
    def adapter_step1_none_b(url: str) -> Optional[str]:
        return None

    def adapter_step2_none_b(url: str) -> Optional[str]:
        return None

    r = escalate("https://plain.example.com/page",  # not an ETL content type
                 websearch_fn=adapter_step1_none_b,
                 webfetch_fn=adapter_step2_none_b,
                 playwright_available=False)
    assert_eq("T8.method_used", r.method_used, ExtractionMethod.EXTRACTION_BLOCKED)
    assert_true("T8.etl_not_in_steps",
                "etl_adapter" not in r.extraction_ladder_steps_tried,
                f"etl should be skipped for web URLs, steps={r.extraction_ladder_steps_tried}")

    # ── Report ────────────────────────────────────────────────────────────
    total = tests_run
    passed = total - len(failures)
    print(f"\n[extraction_escalator] Tests: {passed}/{total} passed")
    if failures:
        for f in failures:
            print(f"  {f}")
        return 1
    print("  All tests PASSED")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extraction fallback ladder — tries websearch_snippet → webfetch → etl → playwright → mark_blocked"
    )
    parser.add_argument("url", nargs="?", help="URL to extract content from")
    parser.add_argument(
        "--initial-method",
        default="websearch_snippet",
        choices=["websearch_snippet", "webfetch", "etl", "playwright"],
        help="Starting step in the ladder (default: websearch_snippet)"
    )
    parser.add_argument(
        "--playwright",
        action="store_true",
        help="Signal that Playwright MCP is available in this session"
    )
    parser.add_argument(
        "--test-ladder",
        action="store_true",
        help="Run unit tests covering each ladder step"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON (for pipeline integration)"
    )
    args = parser.parse_args()

    if args.test_ladder:
        return _run_unit_tests()

    if not args.url:
        parser.print_help()
        return 3

    result = escalate(
        url=args.url,
        initial_method=args.initial_method,
        playwright_available=args.playwright,
    )

    if args.json:
        output = {
            "url": result.url,
            "method_used": result.method_used.value,
            "quality": result.quality.value,
            "attempts_count": result.attempts_count,
            "extraction_ladder_steps_tried": result.extraction_ladder_steps_tried,
        }
        if result.extraction_notes:
            output["extraction_notes"] = result.extraction_notes
        print(json.dumps(output, indent=2))
    else:
        print(f"URL:    {result.url}")
        print(f"Method: {result.method_used.value}")
        print(f"Quality: {result.quality.value}")
        print(f"Attempts: {result.attempts_count}")
        if result.extraction_ladder_steps_tried:
            print(f"Steps tried: {', '.join(result.extraction_ladder_steps_tried)}")
        if result.extraction_notes:
            print(f"Notes: {result.extraction_notes}")
        if result.content:
            preview = result.content[:200].replace("\n", " ")
            print(f"Content preview: {preview}...")

    return 0 if result.method_used != ExtractionMethod.EXTRACTION_BLOCKED else 1


if __name__ == "__main__":
    sys.exit(main())
