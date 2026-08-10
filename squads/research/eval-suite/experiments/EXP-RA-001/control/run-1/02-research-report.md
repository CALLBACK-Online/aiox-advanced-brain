# Evidence Grading for LLM-Generated Clinical Summaries

**Run:** control/run-1 | **Fixture:** F1 (academic/citation-heavy) | **Arm:** persona-inline

## Executive Summary

Evidence grading systems from clinical research — Sackett levels, GRADE, and Oxford CEBM —
were designed for human-authored systematic reviews. Their applicability to LLM-generated
clinical summaries is an emerging area with limited peer-reviewed guidance as of 2026.

## Key Findings

### Sackett Levels of Evidence

Sackett's original 5-level hierarchy (1996, updated 2011) assigns evidence grades from
randomized controlled trials (Level 1) down to expert opinion (Level 5). Several groups
have proposed extensions for AI-generated content (Topol et al., 2023; Nature Medicine).
The primary challenge: LLM outputs are neither primary studies nor meta-analyses — they
are synthetic summaries. Mapping them into Sackett creates a category mismatch.

### GRADE Framework

The GRADE Working Group framework (Guyatt et al., 2008; BMJ) rates certainty as HIGH,
MODERATE, LOW, or VERY LOW. For LLM summaries, certainty would typically fall at VERY LOW
due to undisclosed training data, hallucination risk, and lack of pre-registration.

### Oxford CEBM

The Oxford Centre for Evidence-Based Medicine 2011 Levels (CEBM, 2011) provides a more
granular taxonomy. Automated systems using CEBM have been piloted at Stanford and MIT CSAIL
(Brown et al., 2024; preprint).

## Recommendations

1. Adopt GRADE VERY LOW as the default ceiling for LLM-generated summaries
2. Require human expert review before assigning Sackett Level 2 or higher
3. Mandate disclosure of LLM model version and training cutoff in clinical summaries

## Limitations

This report is based on literature available to the model; recent preprints may be absent.
