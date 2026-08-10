# Scope Extraction Report — {scope}, Window {window}

**Scope:** {session|project|global}
**Owner:** {heuristic_owner_slug} ({heuristic_owner_handle})
**Extractor:** /extract-session-heuristics {version}
**Date:** {YYYY-MM-DD}
**Source Corpus:** {session_context_or_paths}

---

## Source Corpus

| File / Artifact | Date | Type | Candidate IDs |
|---|---:|---|---|
| {source} | {date} | {type} | {ids} |

## Raw Candidates

| # | Candidate | Category | Source |
|---:|---|---|---|
| 1 | {candidate} | {pivot_decision|bug_incident|avoided_antipattern|validated_pattern|research_insight} | {source} |

## GAH Summary

| Candidate | Verdict | Destination / Rewrite |
|---|---|---|
| {candidate} | {ADMIT|ADMIT_WITH_REWRITE_LIGHT|REWRITE_REQUIRED|REJECT} | {destination} |

## Pareto ao Cubo

| Zone | Count | Cards |
|---|---:|---|
| genialidade | {n} | {ids} |
| excelencia | {n} | {ids} |
| impacto | {n} | {ids} |
| descartadas | {n} | {ids_or_reasons} |

## Overlap / Dedup

| Candidate | Existing Match | Action |
|---|---|---|
| {candidate} | {existing_card_or_none} | {CREATE|UPDATE|DISCARD|RECLASSIFY} |

## Formalized Heuristics

| ID | Name | Zone | Source |
|---|---|---|---|
| {ID} | {name} | {zone} | {source} |

## Calibration

| Session | Candidates | Matches | Match Rate |
|---|---:|---:|---:|
| {session} | {n} | {matches} | {rate} |

## Drift / Follow-Up

- {drift_or_followup}

## Outcome

- Raw candidates: {n}
- Formalized: {n}
- Updated existing: {n}
- Reclassified/discarded: {n}
- Gate verdict: {PASS|WARN|FAIL}
