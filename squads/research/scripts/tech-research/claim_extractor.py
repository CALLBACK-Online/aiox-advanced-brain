#!/usr/bin/env python3
"""Factual claim extraction and source matching for citation verification.

Worker atoms: atm_extract_claims, atm_match_sources
Deterministic: regex-based extraction + string matching, no LLM needed.

Usage:
    python claim_extractor.py extract < report.md
    python claim_extractor.py match --claims claims.json --sources sources.json
"""

import re
import sys
import json

# Story: STORY-RA-D.1 — per-claim metadata emitted alongside extraction

CLAIM_PATTERNS = [
    {
        "type": "statistic",
        "pattern": r"(\d+(?:\.\d+)?%?\s*(?:of|dos|das|de)\s+[^.]+\.)",
    },
    {
        "type": "numeric",
        "pattern": r"(\$[\d,.]+(?:/[A-Z])?[^.]*\.)",
    },
    {
        "type": "comparison",
        "pattern": r"([A-Z][a-zA-Z\s]+(?:leads?|outperforms?|beats?|exceeds?|supera|lidera|atinge)[^.]+\.)",
    },
    {
        "type": "benchmark",
        "pattern": r"(\d+(?:\.\d+)?%\s+(?:on|em|no|na)\s+[A-Z][a-zA-Z-]+[^.]*\.)",
    },
    {
        "type": "ranking",
        "pattern": r"(#\d+\s+(?:on|em|no|na|in)\s+[^.]+\.)",
    },
    {
        "type": "market",
        "pattern": r"(\$[\d,.]+[BMK]?\s+(?:market|mercado|valuation|funding|revenue)[^.]*\.)",
    },
    {
        "type": "count",
        "pattern": r"(\d{2,}[\s+](?:models?|modelos?|tools?|sources?|fontes?|papers?|platforms?)[^.]*\.)",
    },
]


def extract_claims(text: str) -> list[dict]:
    """Extract factual claims from markdown text.

    RA-D.1: Each claim now emits per-claim metadata:
      - claim_id: stable C001..CNNN identifier
      - status: initial pre-verification status (MATCHED | UNSOURCED)
      - rewritten: False (default; citation_verifier sets True on rewrite)
      - original_claim: None (set by citation_verifier on rewrite)
      - confidence: None (set by citation_verifier after classification)
      - evidence_grade: None (set by Sackett integration if available)
    """
    claims = []
    seen = set()
    idx = 0

    for config in CLAIM_PATTERNS:
        matches = re.findall(config["pattern"], text, re.IGNORECASE)
        for match in matches:
            clean = match.strip()
            if clean not in seen and len(clean) > 20:
                seen.add(clean)
                idx += 1
                claims.append({
                    "claim_id": f"C{idx:03d}",
                    "text": clean,
                    "type": config["type"],
                    "has_confidence_tag": bool(re.search(r"\[(?:HIGH|MEDIA|LOW)\s*—", clean)),
                    # Per-claim metadata fields (RA-D.1)
                    "status": None,           # populated by citation_verifier
                    "rewritten": False,
                    "original_claim": None,   # set if rewrite_claim runs
                    "confidence": None,       # set by classify_claim
                    "evidence_grade": None,   # set if Sackett available
                })

    return claims


def match_claims_to_sources(claims: list[dict], sources: list[dict]) -> list[dict]:
    """Match extracted claims to source URLs via string matching."""
    results = []

    source_texts = {}
    for source in sources:
        url = source.get("url", "")
        combined = f"{source.get('title', '')} {source.get('snippet', '')}".lower()
        source_texts[url] = combined

    for claim in claims:
        claim_lower = claim["text"].lower()
        numbers = re.findall(r"\d+(?:\.\d+)?", claim_lower)

        matched_sources = []
        for url, text in source_texts.items():
            score = 0
            for num in numbers:
                if num in text:
                    score += 1
            words = [w for w in claim_lower.split() if len(w) > 4]
            for word in words[:5]:
                if word in text:
                    score += 0.5
            if score >= 1.5:
                matched_sources.append({"url": url, "match_score": round(score, 1)})

        matched_sources.sort(key=lambda x: x["match_score"], reverse=True)

        status = "UNSOURCED"
        if matched_sources:
            status = "MATCHED"

        results.append({
            "claim_id": claim.get("claim_id"),
            "claim": claim["text"],
            "text": claim["text"],        # RA-D.1: duplicate as text for citation_verifier compat
            "type": claim["type"],
            "status": status,
            "matched_sources": matched_sources[:3],
            "has_confidence_tag": claim.get("has_confidence_tag", False),
            # Per-claim metadata passthrough (RA-D.1)
            "rewritten": claim.get("rewritten", False),
            "original_claim": claim.get("original_claim"),
            "confidence": claim.get("confidence"),
            "evidence_grade": claim.get("evidence_grade"),
        })

    return results


def summarize_claims(matched_claims: list[dict]) -> dict:
    """Summarize claim matching results."""
    total = len(matched_claims)
    matched = sum(1 for c in matched_claims if c["status"] == "MATCHED")
    unsourced = sum(1 for c in matched_claims if c["status"] == "UNSOURCED")
    with_tags = sum(1 for c in matched_claims if c.get("has_confidence_tag"))

    return {
        "total_claims": total,
        "matched": matched,
        "unsourced": unsourced,
        "with_confidence_tags": with_tags,
        "match_ratio": round(matched / max(total, 1), 2),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: claim_extractor.py <extract|match> [args]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == "extract":
        text = sys.stdin.read()
        claims = extract_claims(text)
        print(json.dumps({"claims": claims, "total": len(claims)}, indent=2))

    elif command == "match":
        if "--claims" in sys.argv and "--sources" in sys.argv:
            claims_idx = sys.argv.index("--claims") + 1
            sources_idx = sys.argv.index("--sources") + 1
            with open(sys.argv[claims_idx]) as f:
                claims = json.load(f)
            with open(sys.argv[sources_idx]) as f:
                sources = json.load(f)
        else:
            data = json.loads(sys.stdin.read())
            claims = data.get("claims", [])
            sources = data.get("sources", [])

        if isinstance(claims, dict):
            claims = claims.get("claims", [])

        results = match_claims_to_sources(claims, sources)
        summary = summarize_claims(results)
        print(json.dumps({"results": results, "summary": summary}, indent=2))

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
