# Evidence Grading for LLM-Generated Clinical Summaries

**Run:** treatment/run-1 | **Fixture:** F1 (academic/citation-heavy) | **Arm:** spawn-adhoc
**Specialists spawned:** Sackett (evidence grading) + Klein (pre-mortem) via Task tool in P4/P4.5

## Executive Summary

With Sackett specialist spawned ad-hoc as a Task subagent during evidence grading phase,
citation_quality and claim_verifiability show modest improvement over inline persona.
However, spawn coordination overhead introduced 2.4x token cost vs control.

## Key Findings (Sackett specialist output merged)

### Evidence Grade Assignments

Sackett specialist provided explicit evidence level assignments for each cited study:
- Topol et al. (2023, Nature Medicine): Level 5 (expert opinion — no primary data)
- Brown et al. (2024, preprint): Level 3 (non-randomized pilot; pre-print, not peer reviewed)
- Guyatt GRADE framework (2008, BMJ): Level 1 (systematic framework, widely adopted)

### GRADE Application

With Sackett specialist active: GRADE certainty for LLM clinical summaries classified as
VERY LOW (HIGH risk of bias, imprecision, indirectness). Specialist added explicit GRADE
domain-specific reasoning: undisclosed training data = HIGH risk of bias.

### Inline findings (unchanged)

Same core findings as control arm. Sackett spawn did not surface new primary literature;
it re-graded existing citations with more explicit evidence hierarchy.

## Spawn Overhead

- Sackett subagent: +3,800 input tokens (system prompt + context transfer)
- Klein subagent (pre-mortem phase, F1 not primary target): +2,100 input tokens
- Total spawn overhead: +5,900 tokens = 2.4x control

## Recommendations

Same as control. Sackett spawn added granularity to evidence levels but no new recommendations.
