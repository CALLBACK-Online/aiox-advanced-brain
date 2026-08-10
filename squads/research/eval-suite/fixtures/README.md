# eval-suite/fixtures — Selection Criteria

Story: STORY-RA-0.2 | Sprint 0 skeleton

## Purpose

Three synthetic fixtures representing the quality spectrum of research squad
output. They enable `llm_judge.py` to produce meaningful scores for A/B
comparison (RA-EXP.1) and regression detection (regression_runner.sh).

Fixtures are **synthetic** (not copies of real runs) to avoid drift when
real research evolves. Shape modeled after existing runs in `docs/research/`.

## Fixtures

### high-quality/

**Baseline score:** 82/100
**Modeled after:** `docs/research/2026-05-18-gold-bench-profile-fixture/` —
6 waves, 13 sources, citation_verified=true, coverage_score=96.

**Selection criteria:**
- Comprehensive coverage (5+ sub-questions addressed)
- 80%+ claims sourced with verifiable URLs and pub_date
- Explicit confidence markers (HIGH/MEDIUM/LOW)
- Logical narrative arc (hypothesis → evidence → conclusion)
- Prioritized actionable recommendations with owners and timelines

### medium-quality/

**Baseline score:** 58/100
**Modeled after:** `docs/research/2026-03-28-deep-research-pipeline-best-practices/` —
1 wave, 6 sources, citation_verified=false, coverage_score=88.

**Selection criteria:**
- Decent breadth, notable gaps (cost benchmarks, community metrics missing)
- ~50% of claims sourced, limited source diversity
- Some qualification ("MEDIA confidence") but core claims unverified
- Loose narrative; sections present but not well-connected
- Vague recommendations without owners or prioritization

### low-quality/

**Baseline score:** 20/100
**Modeled after:** `docs/research/2026-05-19-research-core-launcher-smoke/` —
mock engine, 1 source, smoke/validation purpose, not a real research output.

**Selection criteria:**
- Query was a system smoke test, not a research question
- Minimal content: no analysis, no recommendations, no narrative
- 1 source, 2 mock claims, 1 invalid citation
- Not intended to answer a research question — score expected to be low

## Baseline score semantics

Each fixture has a `.baseline_score` file (integer 0-100). The regression
runner uses this as the reference: score >= (baseline - 5) = PASS.

The baselines here are intentionally conservative relative to what a real
LLM judge will score. They define the minimum acceptable floor, not the
expected score.

## Anti-overengineering note

These are Sprint 0 fixtures. Full Gartner-grade fixture curation — with
real run selection, multi-judge consensus scoring, and drift monitoring —
is out of scope for this story. See AC-5 / README.md for scope boundaries.
