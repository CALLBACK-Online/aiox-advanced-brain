#!/usr/bin/env python3
"""Per-claim citation verification with archive.org fallback, rewrite-claim, and classification.

Worker atoms: atm_verify_citations (per-claim), atm_archive_fallback, atm_rewrite_claim
Story: STORY-RA-D.1

ACs implemented:
  AC-1 — archive.org snapshot fallback for dead URLs
  AC-2 — Per-claim classification: supported | unsupported | unknown | ambiguous
  AC-3 — Rewrite-claim with audit trail for ambiguous claims
  AC-4 — Veto threshold: unsupported_top_tier > 20%
  AC-5 — Sackett evidence_grade integration (optional, graceful fallback)

Usage:
    python citation_verifier.py verify --claims claims.json --sources sources.json
    python citation_verifier.py verify --claims claims.json --sources sources.json --sackett sackett.json
    python citation_verifier.py archive-check --url https://example.com/dead-page
    python citation_verifier.py aggregate --claims-out claims_verified.json
"""

from __future__ import annotations

import json
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ARCHIVE_API = "https://archive.org/wayback/available?url={url}"
ARCHIVE_RETRY_DELAYS = [1, 2, 4]  # exponential backoff seconds

# Veto thresholds (AC-4)
APPROVE_CLEAN_THRESHOLD = 0.05        # < 5% unsupported → APPROVE
APPROVE_WITH_CONFIDENCE_THRESHOLD = 0.20  # 5-20% unsupported → APPROVE_WITH_CONFIDENCE
# > 20% unsupported_top_tier → VETO

# Claim-source match threshold (reuse from claim_extractor logic)
MATCH_SCORE_THRESHOLD = 1.5

# Sackett evidence grades considered "top-tier" (grades 1a, 1b, 2a)
TOP_TIER_GRADES = {"1a", "1b", "2a"}


# ---------------------------------------------------------------------------
# archive.org fallback (AC-1)
# ---------------------------------------------------------------------------

def fetch_archive_snapshot(url: str, timeout: int = 8) -> Optional[str]:
    """Query archive.org Wayback Machine for the latest snapshot of url.

    Returns snapshot URL string if found, None otherwise.
    Applies exponential backoff: 1s/2s/4s between retries.
    Results are NOT cached here — callers handle caching if needed.
    """
    api_url = ARCHIVE_API.format(url=urllib.parse.quote(url, safe=":/?=&"))
    last_exc: Optional[Exception] = None

    for attempt, delay in enumerate([0] + ARCHIVE_RETRY_DELAYS):
        if delay:
            time.sleep(delay)
        try:
            req = urllib.request.Request(
                api_url,
                headers={"User-Agent": "aiox-citation-verifier/1.0 (research pipeline)"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
                snapshot = data.get("archived_snapshots", {}).get("closest", {})
                if snapshot.get("available") and snapshot.get("url"):
                    return snapshot["url"]
                return None
        except urllib.error.HTTPError as exc:
            if exc.code == 429:  # rate limited — keep retrying with backoff
                last_exc = exc
                continue
            return None
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            last_exc = exc
            continue

    # All retries exhausted
    _ = last_exc  # suppress unused warning
    return None


def check_url_liveness(url: str, timeout: int = 6) -> bool:
    """Return True if URL responds with 2xx/3xx, False on 4xx/5xx/timeout."""
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "aiox-citation-verifier/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status < 400
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Per-claim classification (AC-2)
# ---------------------------------------------------------------------------

def classify_claim(
    claim: dict,
    sources: list[dict],
    sackett_graded: Optional[dict] = None,
) -> dict:
    """Classify a single claim as supported/unsupported/unknown/ambiguous.

    Args:
        claim: dict with keys: text, type, matched_sources (optional), status (optional)
        sources: full sources list [{url, title, snippet, ...}]
        sackett_graded: optional dict keyed by claim_id with evidence_grade

    Returns extended claim dict with:
        status: supported | unsupported | unknown | ambiguous
        archive_url: str | None (if archive fallback used)
        evidence_grade: str | None (Sackett grade 1a-5 if available)
        confidence: high | medium | low | none
    """
    claim_id = claim.get("claim_id", "")
    matched_sources = claim.get("matched_sources", [])
    original_status = claim.get("status", "UNSOURCED")

    # Build source lookup
    source_map: dict[str, dict] = {s.get("url", ""): s for s in sources}

    archive_url: Optional[str] = None
    live_sources = []
    dead_urls = []

    for ms in matched_sources:
        url = ms.get("url", "")
        if not url:
            continue
        if check_url_liveness(url):
            live_sources.append(ms)
        else:
            dead_urls.append(url)

    # Try archive.org for dead URLs (AC-1)
    archive_sources = []
    for url in dead_urls:
        snapshot = fetch_archive_snapshot(url)
        if snapshot:
            archive_url = snapshot
            archive_sources.append({"url": snapshot, "original_url": url, "via": "archive.org"})

    all_sources = live_sources + archive_sources

    # --- Classification logic (AC-2) ---
    if original_status == "UNSOURCED" and not all_sources:
        status = "unsupported"
        confidence = "none"
    elif not all_sources and dead_urls and not archive_sources:
        # URL existed but is now dead + no snapshot
        status = "unsupported"
        confidence = "none"
    elif not all_sources:
        # No sources matched at all (never had a match)
        status = "unknown"
        confidence = "none"
    else:
        # We have at least one live or archived source — semantic check
        claim_text_lower = claim.get("text", "").lower()
        # Simple heuristic: check if source content (title+snippet) overlaps enough
        # "ambiguous" = source diverges partially (some overlap but not confirming fully)
        # "supported" = good overlap or match_score high
        best_score = max((ms.get("match_score", 0) for ms in all_sources), default=0)

        if best_score >= 3.0:
            status = "supported"
            confidence = "high"
        elif best_score >= 1.5:
            # Check for divergence signals
            source_texts = []
            for ms in all_sources:
                s = source_map.get(ms.get("url", ""), {})
                source_texts.append(
                    f"{s.get('title', '')} {s.get('snippet', '')}".lower()
                )

            # Heuristic: if claim has strong quantitative assertion but source text
            # is hedged (contains "approximately", "may", "could", "reportedly")
            hedge_words = {"approximately", "may", "could", "reportedly", "suggests", "seems"}
            source_full = " ".join(source_texts)
            has_hedge = any(w in source_full for w in hedge_words)

            if has_hedge:
                status = "ambiguous"
                confidence = "medium"
            else:
                status = "supported"
                confidence = "medium"
        else:
            status = "unknown"
            confidence = "low"

    # Sackett evidence grade integration (AC-5)
    evidence_grade: Optional[str] = None
    if sackett_graded and claim_id in sackett_graded:
        evidence_grade = sackett_graded[claim_id].get("evidence_grade")

    result = dict(claim)
    result.update({
        "status": status,
        "confidence": confidence,
        "archive_url": archive_url,
        "evidence_grade": evidence_grade,
        "live_sources": live_sources,
        "archive_sources": archive_sources,
    })
    return result


# ---------------------------------------------------------------------------
# Rewrite-claim (AC-3)
# ---------------------------------------------------------------------------

def rewrite_claim(claim: dict, sources: list[dict]) -> dict:
    """Attempt rewrite for ambiguous claim. Only called on status==ambiguous.

    Produces:
        text: rewritten text
        original_claim: original text
        rewritten: True
        rewrite_rationale: explanation
        status: supported (after rewrite)

    Strategy: if source snippet provides a more hedged version of the claim,
    use it. Otherwise soften the claim with "reportedly" prefix.
    """
    original_text = claim.get("text", "")
    source_map: dict[str, dict] = {s.get("url", ""): s for s in sources}

    # Look for source snippet to base rewrite on
    best_snippet = ""
    for ms in claim.get("live_sources", []) + claim.get("archive_sources", []):
        url = ms.get("url", ms.get("original_url", ""))
        s = source_map.get(url, {})
        snippet = s.get("snippet", "")
        if snippet and len(snippet) > len(best_snippet):
            best_snippet = snippet

    if best_snippet:
        # Produce a rewrite that qualifies the claim based on source language
        rewritten_text = f"{original_text.rstrip('.')} (per source: {best_snippet[:120].rstrip()}...)."
        rationale = f"Source provides hedged/partial confirmation. Rewrite incorporates source language to avoid overclaiming."
    else:
        # Fallback: soften the claim
        rewritten_text = f"Reportedly, {original_text[0].lower()}{original_text[1:]}"
        rationale = "Source diverges partially from original claim. Softened with 'reportedly' qualifier."

    result = dict(claim)
    result.update({
        "text": rewritten_text,
        "original_claim": original_text,
        "rewritten": True,
        "rewrite_rationale": rationale,
        "status": "supported",
    })
    return result


# ---------------------------------------------------------------------------
# Aggregation & veto logic (AC-4)
# ---------------------------------------------------------------------------

def aggregate_claims(claims: list[dict]) -> dict:
    """Compute per-claim distribution and veto decision.

    Returns:
        verdict: APPROVE | APPROVE_WITH_CONFIDENCE | VETO
        unsupported_ratio: float
        unsupported_top_tier_ratio: float
        confidence_distribution: dict
        total: int
        counts: dict
    """
    total = len(claims)
    if total == 0:
        return {
            "verdict": "APPROVE",
            "unsupported_ratio": 0.0,
            "unsupported_top_tier_ratio": 0.0,
            "confidence_distribution": {},
            "total": 0,
            "counts": {},
        }

    counts: dict[str, int] = {"supported": 0, "unsupported": 0, "unknown": 0, "ambiguous": 0}
    confidence_dist: dict[str, int] = {"high": 0, "medium": 0, "low": 0, "none": 0}
    unsupported_top_tier = 0

    for c in claims:
        s = c.get("status", "unknown")
        counts[s] = counts.get(s, 0) + 1
        conf = c.get("confidence", "none")
        confidence_dist[conf] = confidence_dist.get(conf, 0) + 1

        # top-tier unsupported: unsupported + Sackett grade top-tier
        if s == "unsupported":
            grade = c.get("evidence_grade")
            if grade and grade in TOP_TIER_GRADES:
                unsupported_top_tier += 1

    unsupported_ratio = counts.get("unsupported", 0) / total
    unsupported_top_tier_ratio = unsupported_top_tier / total

    # AC-4 veto logic
    if unsupported_top_tier_ratio > APPROVE_WITH_CONFIDENCE_THRESHOLD:
        verdict = "VETO"
    elif unsupported_ratio > APPROVE_CLEAN_THRESHOLD:
        verdict = "APPROVE_WITH_CONFIDENCE"
    else:
        verdict = "APPROVE"

    return {
        "verdict": verdict,
        "unsupported_ratio": round(unsupported_ratio, 3),
        "unsupported_top_tier_ratio": round(unsupported_top_tier_ratio, 3),
        "confidence_distribution": confidence_dist,
        "total": total,
        "counts": counts,
    }


# ---------------------------------------------------------------------------
# Sackett input parser (AC-5)
# ---------------------------------------------------------------------------

def load_sackett_grades(sackett_path: str) -> dict:
    """Load Sackett output file and return {claim_id: {evidence_grade, ...}}.

    Sackett output format (from RA-E.2 frontmatter schema):
      graded_claims:
        - claim_id: C001
          evidence_grade: 1a
          rationale: ...
    Returns {} on parse failure (graceful fallback per D3).
    """
    try:
        path = Path(sackett_path)
        if not path.exists():
            return {}
        text = path.read_text(encoding="utf-8")
        # Support YAML frontmatter in sackett.md
        if text.startswith("---"):
            import re
            fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            if fm_match:
                try:
                    import yaml
                    data = yaml.safe_load(fm_match.group(1))
                except ImportError:
                    data = {}
            else:
                data = {}
        else:
            data = json.loads(text)

        graded = data.get("graded_claims", [])
        return {
            g["claim_id"]: g
            for g in graded
            if "claim_id" in g and "evidence_grade" in g
        }
    except Exception:
        # Graceful fallback: Sackett is enhancement, not dependency (D3)
        return {}


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("Usage: citation_verifier.py <verify|archive-check|aggregate> [args]", file=sys.stderr)
        return 3

    command = argv[0]

    if command == "verify":
        # Parse args
        args = argv[1:]
        claims_path = None
        sources_path = None
        sackett_path = None

        i = 0
        while i < len(args):
            if args[i] == "--claims" and i + 1 < len(args):
                claims_path = args[i + 1]; i += 2
            elif args[i] == "--sources" and i + 1 < len(args):
                sources_path = args[i + 1]; i += 2
            elif args[i] == "--sackett" and i + 1 < len(args):
                sackett_path = args[i + 1]; i += 2
            else:
                i += 1

        if not claims_path or not sources_path:
            print("Error: --claims and --sources required", file=sys.stderr)
            return 3

        with open(claims_path) as f:
            claims_data = json.load(f)
        with open(sources_path) as f:
            sources_data = json.load(f)

        claims = claims_data if isinstance(claims_data, list) else claims_data.get("claims", [])
        sources = sources_data if isinstance(sources_data, list) else sources_data.get("sources", [])

        # Assign claim IDs if missing
        for idx, c in enumerate(claims):
            if "claim_id" not in c:
                c["claim_id"] = f"C{idx + 1:03d}"

        sackett_graded = load_sackett_grades(sackett_path) if sackett_path else {}

        verified = []
        for claim in claims:
            result = classify_claim(claim, sources, sackett_graded or None)
            if result["status"] == "ambiguous":
                result = rewrite_claim(result, sources)
            verified.append(result)

        agg = aggregate_claims(verified)
        print(json.dumps({"claims": verified, "aggregation": agg}, indent=2))
        return 0

    elif command == "archive-check":
        args = argv[1:]
        url = None
        i = 0
        while i < len(args):
            if args[i] == "--url" and i + 1 < len(args):
                url = args[i + 1]; i += 2
            else:
                i += 1
        if not url:
            print("Error: --url required", file=sys.stderr)
            return 3
        snapshot = fetch_archive_snapshot(url)
        result = {"url": url, "snapshot": snapshot, "found": snapshot is not None}
        print(json.dumps(result, indent=2))
        return 0

    elif command == "aggregate":
        args = argv[1:]
        claims_path = None
        i = 0
        while i < len(args):
            if args[i] == "--claims-out" and i + 1 < len(args):
                claims_path = args[i + 1]; i += 2
            else:
                i += 1
        if not claims_path:
            data = json.loads(sys.stdin.read())
            claims = data.get("claims", [])
        else:
            with open(claims_path) as f:
                data = json.load(f)
            claims = data.get("claims", [])

        agg = aggregate_claims(claims)
        print(json.dumps(agg, indent=2))
        return 0

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
