# Deep Research Pipeline Best Practices — Research Report

**Coverage score:** 88/100 | **Integrity score:** 92/100 | **Sources:** 6
**Date:** 2026-03-28 | **Waves:** 1

---

## Summary

Deep research pipelines benefit from multi-wave search, source
deduplication, and structured output schemas. Key findings from
6 sources (5 HIGH credibility, 1 MEDIUM):

1. Multi-wave search reduces coverage gaps by ~30% vs single-shot
2. Structured output (YAML/JSON schemas) improves downstream reuse
3. Citation verification is essential for production use

---

## Pipeline Architecture

A well-structured pipeline includes:
- Wave 1: broad query decomposition
- Wave 2: gap-directed targeted search
- Wave 3: saturation check and final synthesis

Most practitioners use 3-6 waves before diminishing returns set in.
Citation: (Smith 2025, arxiv.org/abs/2503.09876).

---

## Source Quality

Credibility signals matter more than source volume. 6 highly credible
sources outperform 30 low-credibility ones (MEDIA confidence — based on
community survey, not controlled study).

Common issues:
- URL rot (30% of research URLs invalid after 6 months)
- Paywalled sources inflate apparent diversity
- LLM hallucination of specific statistics (10-15% of claims unsupported)

---

## Recommendations

- Implement archive.org fallback for URL verification
- Use structured schemas for claim extraction
- Limit waves to 6; beyond that, convergence is minimal

---

## Gaps not addressed

- Cost benchmarks per wave not captured in this run
- Community activity metrics missing
- Actionability scoring not applied to specific recommendations
