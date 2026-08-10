# Bench Criteria — {ANCHOR} vs {N} players

> **Emitted by:** `/research-bench` BEFORE dimension scoring (i.e. before `comparison-matrix.json` is built).
> **Trigger:** `comparison_pattern: multi_player` AND `dimensions_count >= 5` (always satisfied for `profile: gold_absorption` per `.claude/rules/research-bench-gold.md` Rule 3 — minimum 60 microdims).
> **Schema:** `bench-criteria.v1`
> **Companion atoms:** `comparison-matrix.json` (scores) + `bench-weights.yaml` (group weights, MUST sum 100) + `scripts/scoring-{SLUG}.py` (reproducibility when composite multi-weighted).
>
> This atom is the AUDIT-FRIENDLY pre-declaration of axes, weights, and calibration. It is the source of truth for "why these dimensions and not others" and must be authored BEFORE any score is assigned. Aligns with `.claude/rules/bench-weight-calibration.md` framework-agnostic mandate (no `aiox_fit`, no anchor-only-satisfiable axes).

---

## Meta

```yaml
schema_version: "bench-criteria.v1"
slug: "{YYYY-MM-DD}-{slug}"               # MUST start with YYYY-MM-DD (new benches)
date: "{YYYY-MM-DD}"
profile: "{standard|gold_absorption}"
anchor: "{anchor_player_key}"             # MUST be present in players[] (rule 10.5)
players: ["{player_key_1}", "{player_key_2}", "..."]   # all keys; anchor first by convention
players_count: {N}                        # MUST be >= 5 for gold_absorption (auto-fires per Rule 1)
macro_dimensions_count: {M}               # macro atoms (groups)
microdimensions_count: {M*3}              # 3 microdims per macro (Rule 3); min 60 for Gold
weights_file: "bench-weights.yaml"        # MANDATORY authority for normalized group weights
paired_artifacts:
  matrix: "comparison-matrix.json"
  weights: "bench-weights.yaml"
  scoring_script: "scripts/scoring-{slug}.py"   # only when composite multi-weighted
```

---

## Scoring Calibration (AC-2)

This block is MIRRORED in `comparison-matrix.json#meta.scoring_calibration` and in every atom that contains numeric `score`, `rank_score`, `dimension_score`, `feature_depth_score`, or `microdim_score`. Single source of truth for "what kind of measurement is this?"

```yaml
scoring_calibration:
  type: "{interpretive|empirical|hybrid}"
  # interpretive — analytical judgment by bench-analyst based on declared evidence/inventory
  # empirical    — observed measurement (LOC, stars, build-time, citations, runtime, throughput)
  # hybrid       — mostly interpretive anchored to one empirical baseline per dimension

  scale: "{1-5|0-10|0-100|other}"
  scale_description: "{e.g. 1=absent, 3=present-partial, 5=present-strong-with-evidence}"

  baseline: "{path/url/description of the empirical anchor when type=hybrid|empirical}"
  # e.g. "Deep Research Bench v1.2 reference scores" or "GitHub API snapshot 2026-05-19"

  calibrated_by: "{agent_id} single-pass | n={X} human raters | n={X} runs at temperature={T}"

  disclaimer: |
    Scores are {analytical|empirical|hybrid}. They are NOT controlled measurements
    unless explicitly stated. Inter-rater agreement is recorded in
    `validation-report.yaml#inter_rater_agreement` when applicable.

  reproducibility: "{low|medium|high}"
  # high requires `scripts/scoring-{slug}.py` to re-produce CSV bit-exact (AC-3, AT-3)
```

---

## Framework-Agnosticism Pledge (NON-NEGOTIABLE)

Per `.claude/rules/bench-weight-calibration.md`, the bench MUST be framework-agnostic. Confirm before authoring dimensions:

- [ ] NO `aiox_fit` dimension (removed from schema 2026-05-18 — not even at weight 0).
- [ ] NO weight on `dogfood_presence` of the anchor.
- [ ] NO governance-alignment scoring using AIOX-specific vocabulary (`Mandamentos`, `Ponto A→B`, `tokenization`).
- [ ] NO dimension that ONLY the anchor satisfies by construction.
- [ ] Use universal capability dimensions (Coverage Gate, Citation verification, Cost-per-task, Wall-time) or external benchmark frameworks (Deep Research Bench, RACE/FACT, LiveDRBench) where possible.

---

## Critical Groups (Founder Mandate 2026-05-18)

These three macro groups MUST be explicitly acknowledged. Excluding any one requires `_rationale` in `bench-weights.yaml`.

| Group ID | Why Critical | Acknowledged? |
|---|---|:---:|
| `research_depth_synthesis` | Differentiates surface scrapers from deep researchers | [ ] |
| `tool_runtime_integration` | Differentiates wrappers from real research stacks | [ ] |
| `multi_agent_orchestration` | Differentiates monolithic loops from teams | [ ] |

---

## Macro Dimensions (Groups)

Each macro group below corresponds to a section of `comparison-matrix.json#dimensions[]`. Each macro will decompose into **3 microdimensions** per Rule 3 (rule of thirds: `microdim.weight = macro.weight / 3`).

### Group 1 — {GROUP_ID}

```yaml
id: "{snake_case_group_id}"
label: "{Human-readable label}"
operational_definition: |
  {Universal capability — what does a high score in this group mean? Anchor to
   observable signals (file paths, API endpoints, runtime traces, docs sections,
   external benchmarks) so two reviewers converge on the same score per cell.}

evidence_signals:
  - "{signal_1}"
  - "{signal_2}"
  - "{signal_3}"

scale_anchors:
  1: "{what a score of 1 looks like in this group}"
  3: "{what a score of 3 looks like}"
  5: "{what a score of 5 looks like with verifiable evidence}"

weight_normalized: {0..100}        # from bench-weights.yaml#normalized_weights[]
weight_rationale: "{why this weight, 1 sentence — operator-calibrated, NOT AI-chosen}"

microdimensions:
  - id: "{group_id}__micro_1"
    label: "{label}"
    question: "{operational YES/NO/partial question}"
    weight: {weight_normalized / 3}
  - id: "{group_id}__micro_2"
    label: "{label}"
    question: "{operational question}"
    weight: {weight_normalized / 3}
  - id: "{group_id}__micro_3"
    label: "{label}"
    question: "{operational question}"
    weight: {weight_normalized / 3}

justification: |
  {Why is this group relevant for the comparison? Cite metadata.json,
   bench-weights.yaml#_rationale, or founder directive log.}
```

### Group 2 — {GROUP_ID}

(repeat block per macro group; minimum 5 dimensions; gold_absorption requires 15-group canonical taxonomy per `.claude/rules/bench-weight-calibration.md`.)

---

## Rejected Dimensions (Auditability)

Dimensions explicitly excluded WITH rationale. Required to prevent future reviewers from re-proposing the same axes blindly.

| Rejected Axis | Considered Because | Excluded Because | Evidence |
|---|---|---|---|
| `{axis_1}` | {reason} | {anti-reason — e.g. anchor-only-satisfiable, opaque scale, non-reproducible} | {citation} |
| `aiox_fit` (canonical) | Legacy from pre-2026-05-18 schema | Framework-agnostic mandate; anchor's own methodology cannot be a comparison dimension | `.claude/rules/bench-weight-calibration.md` |

---

## Caps & Field-Name Conventions (AC-4)

Encode API caps directly in field names so downstream consumers don't misread truncated data.

| Raw Field (CSV/JSON) | Cap | Source |
|---|---|---|
| `contributors_api_capped_100` | GitHub contributors endpoint = 100 | github.com/{owner}/{repo}/contributors |
| `commits_90d_capped_N` | API pagination limit; N observed | github.com/{owner}/{repo}/commits |
| `stargazers_api_snapshot_at_{date}` | Snapshot value at extraction time | github.com/{owner}/{repo} |
| `citations_semantic_scholar_capped_1000` | Semantic Scholar API page-size limit | api.semanticscholar.org |
| `search_results_per_query_capped_50` | Search engine SERP cap | Google/Bing/DDG |

Add rows as needed. If no API caps apply, write `N/A — all data is locally computed or human-rated`.

---

## All-Pairs Duels Contract (Rule 4)

Per `.claude/rules/research-bench-gold.md` Rule 4, the matrix produces **N choose 2** duels. The dimensions declared here are the SAME axes used for every duel — duels do NOT introduce new axes mid-flight.

```yaml
duels:
  pair_count: {N * (N-1) / 2}             # e.g. 10 players → 45 duels
  axes_used: [{list of group_ids declared above}]
  tiebreak_rule: "highest weighted sum on critical groups wins ties"
```

---

## Decision Trail

```yaml
authoring_record:
  authored_by: "{agent_id}"                # e.g. "research-bench inline | bench-analyst spawned"
  authored_at: "{ISO-8601}"
  reviewed_by: "{operator_handle_or_null}"
  source_references:
    - "metadata.json"
    - "bench-weights.yaml"
    - "{any prior bench in docs/bench/ used as template}"
  founder_directives_applied:
    - "2026-05-18: no aiox_fit (framework-agnostic mandate)"
    - "2026-05-18: 3 critical groups acknowledged"
  open_questions:
    - "{questions left in curiosity-queue.yaml about this criteria set}"
```

---

## Anti-Patterns Avoided

- `aiox_fit` reintroduced at any weight (forbidden).
- Anchor-only-satisfiable axes (e.g. "uses AIOX tokenization").
- Adding axes mid-scoring to favor the anchor.
- Reporting raw GitHub counts without API caps in field names.
- Composite scoring `total_normalized != 100.0`.
- Skipping `bench-weights.yaml` and letting AI invent weights.

---

*Template `research-bench-criteria.md` v1.0 — research-bench | Story RA-F.1 | Aligned to `.claude/rules/research-bench-gold.md` Rules 1-10 + `.claude/rules/bench-weight-calibration.md` (founder mandate 2026-05-18).*
