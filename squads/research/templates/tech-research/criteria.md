# Criteria — {SUBJECT_OR_TOPIC}

> **Emitted by:** `/tech-research` Phase M7/P5 (Document Final Artifacts)
> **Trigger:** `comparison_pattern: multi_player` AND `dimensions_count >= 5`
> **Schema:** `research-criteria.v1`
> **Companion atoms:** `matrices.yaml` (scores) + `scripts/scoring-{SLUG}.py` (reproducibility, when composite scoring)
>
> This atom declares the EVALUATION FRAMEWORK BEFORE any score is assigned. Auditors and downstream consumers can interrogate the choice of axes independently from the choice of values per cell.

---

## Meta

```yaml
schema_version: "research-criteria.v1"
slug: "{SLUG}"
date: "{YYYY-MM-DD}"
comparison_pattern: "{multi_player|single_subject|paired}"
players_count: {N}
dimensions_count: {M}                     # MUST be >= 5 to trigger this atom
emitted_by: "/tech-research"
phase: "M7/P5 — Document Final Artifacts"
paired_artifacts:
  matrix: "matrices.yaml"
  scoring_script: "scripts/scoring-{SLUG}.py"   # only when composite multi-weighted scoring (>=3 sub-scores)
```

---

## Scoring Calibration (AC-2)

Declare the nature of the scores produced under this criteria set. Every numeric score in `matrices.yaml` MUST be interpretable through this calibration block. The same block is mirrored in the YAML frontmatter / `meta.scoring_calibration` of every atom that contains numeric `score`, `rank_score`, `dimension_score`, `feature_depth_score`, or similar fields.

```yaml
scoring_calibration:
  type: "{interpretive|empirical|hybrid}"
  # interpretive — analytical judgment by the agent based on declared evidence
  # empirical    — observed measurement from an instrument (benchmark run, citation count, runtime, etc.)
  # hybrid       — mostly interpretive but anchored to one empirical baseline

  scale: "{1-5|0-10|0-100|other}"
  scale_description: "{e.g. 1=poor, 3=adequate, 5=excellent}"

  baseline: "{path/url/description of the empirical anchor, REQUIRED when type=hybrid|empirical}"

  calibrated_by: "{agent_id} single-pass | n={X} human raters | n={X} runs at temperature={T}"

  disclaimer: |
    Scores are {analytical|empirical|hybrid}. They are NOT controlled measurements
    unless explicitly stated above. Inter-rater agreement was not measured unless
    documented in `validation-report.yaml`.

  reproducibility: "{low|medium|high}"
  # low    — same agent re-running likely produces different scores
  # medium — same agent re-running converges; different agents may diverge
  # high   — bit-exact reproducible via scoring script (see `scripts/scoring-{SLUG}.py`)
```

---

## Dimensions (Axes Chosen)

Each dimension below MUST appear in `matrices.yaml#dimensions[]`. Adding a dimension here without scoring it in the matrix is a contract violation. Scoring a dimension in the matrix without declaring it here is also a violation.

### Dimension 1 — {DIMENSION_ID}

```yaml
id: "{snake_case_dimension_id}"
label: "{Human-readable label}"
operational_definition: |
  {What exactly does a high score in this dimension mean? Anchor the definition
   to observable signals (file paths, API endpoints, doc sections, runtime traces)
   so two reviewers would converge on the same score given the same evidence.}

evidence_signals:
  - "{signal_1 — e.g. presence of <X> in repo or docs}"
  - "{signal_2}"
  - "{signal_3}"

scale_anchors:
  1: "{what a score of 1 looks like}"
  3: "{what a score of 3 looks like}"
  5: "{what a score of 5 looks like}"

weight: {0.00..1.00}        # only when composite scoring; sum across all dimensions = 1.0
weight_rationale: "{why this weight, in 1 sentence}"

justification: |
  {Why is this dimension relevant for the decision/comparison being made?
   Cite the source (research-report §X.Y, action-plan goal Z, founder directive).}
```

### Dimension 2 — {DIMENSION_ID}

(repeat block per dimension; minimum 5 to trigger this atom)

---

## Rejected Dimensions (Auditability)

Dimensions that were considered and explicitly excluded, with rationale. Keeping a written record prevents future reviewers from re-proposing the same axes without context.

| Rejected Axis | Considered Because | Excluded Because | Linked Evidence |
|---------------|--------------------|--------------------|------------------|
| {axis_1}      | {reason}           | {anti-reason}      | {citation/path}  |
| {axis_2}      | {reason}           | {anti-reason}      | {citation/path}  |

---

## Caps & Field-Name Conventions (AC-4)

When the data underlying a score comes from an API with a known limit, the corresponding raw field MUST encode the cap in its name. This prevents downstream consumers from misinterpreting truncated data as ground truth.

| Raw Field (CSV/JSON)              | Cap | Source |
|-----------------------------------|-----|--------|
| `contributors_api_capped_100`     | GitHub API contributors endpoint cap = 100 | github.com/{owner}/{repo}/contributors |
| `commits_90d_capped_N`            | API pagination limit, where N is the observed pagination ceiling | github.com paginated commits |
| `search_results_per_query_capped_50` | Search engine result-page limit | Google/Bing/DDG SERP cap |
| `snapshot_at_{YYYY-MM-DD}`        | Time-bounded snapshot — values frozen at the listed date | data extraction run |

Add rows as needed. If no API caps apply to this comparison, write `N/A — no API-derived fields`.

---

## Decision Trail

```yaml
authoring_record:
  authored_by: "{agent_id}"           # e.g. "tech-research M7/P5 inline"
  authored_at: "{ISO-8601}"
  reviewed_by: "{reviewer_or_null}"
  source_references:
    - "00-query-original.md"
    - "02-research-report.md §{X.Y}"
    - "{any prior bench in docs/bench/}"
  open_questions:
    - "{questions left in curiosity_queue.yaml about this criteria set}"
```

---

## Anti-Patterns Avoided

- Adding a dimension that ONLY one player satisfies by construction (structural self-favoring).
- Inflating composite weights to mirror a desired ranking ("weight tuning until the chosen player wins").
- Using `interpretive` scores at scale `1-5` without anchor descriptions (becomes guesswork).
- Reporting raw counts from an API endpoint without acknowledging the cap (e.g. silent `contributors=100` from GitHub when the project has 250 contributors).

---

*Template `criteria.md` v1.0 — tech-research | Story RA-F.1 | Founder mandate 2026-05-19: criteria separate from scoring, calibration declared explicitly, reproducibility anchored to scripts.*
