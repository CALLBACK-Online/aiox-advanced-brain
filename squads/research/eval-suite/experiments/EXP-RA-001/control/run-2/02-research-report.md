# Jobs-to-be-Done Analysis for AI Research Assistants

**Run:** control/run-2 | **Fixture:** F2 (product-discovery/JTBD) | **Arm:** persona-inline

## Executive Summary

Knowledge workers using AI research assistants in 2025-2026 are primarily hiring these tools
for speed-of-synthesis, not depth. Pre-mortem analysis identifies trust erosion as the #1
failure mode within 6 months of deployment.

## Primary JTBD

1. **Rapid synthesis** — summarize 50+ papers in under 10 minutes
2. **Citation validation** — verify claims without reading full papers
3. **Competitive landscape mapping** — track emerging players and papers weekly
4. **Pre-mortem anticipation** — identify risks before committing to a research direction

## Pre-Mortem: Top 5 Failure Modes

1. **Hallucination cascades** — one fabricated citation is cited in 3 follow-up queries
2. **Staleness blindness** — tool does not flag its knowledge cutoff prominently
3. **Over-trust lock-in** — teams stop verifying because tool "is usually right"
4. **Breadth vs depth tradeoff** — good at overview, poor at edge-case depth
5. **Context collapse** — long research threads lose earlier context; conclusions contradict

## Recommendations

Consider deploying with mandatory citation verification step. Assign a human reviewer
for any claim rated MEDIUM or LOW confidence.
