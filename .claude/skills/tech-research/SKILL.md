---
name: tech-research
description: "Deep technical research pipeline (7 molecules, 11 atoms) with multi-wave search, coverage scoring, multi-LLM cross-reference, citation verification, and incremental learning log. Phase 3 routes academic queries to scholarly databases (arXiv, PubMed, Semantic Scholar via research-adapters) before generic WebSearch. Produces evidence-graded research dossiers under docs/research/. Optional product-discovery mode feeds the research-chief validate-product-idea molecule."
version: "2.1.0"
workflow_version: "3.2.0"
user-invocable: true
argument-hint: "<query> [--product-discovery|--pd] [--deep] [--yolo|--interactive] [--budget-preset economy|standard|deep] [--cost-max $X]"
depends_on: []
invokes: ["/research-chief"]
---

# Tech Research — SINKRA-Native Deep Research Pipeline v2.0.0

Orchestrates the complete tech-research EXPLORAR-mode pipeline from Auto-Clarify through
Document using **inline persona-fidelity** (each phase loads a persona + workflow YAML
and executes in main context). Visual task tracking via TeamCreate + TaskCreate.
Checkpoint gates (COVERAGE_GATE, CITATION_GATE) are real — VETO halts, REVIEW requires
explicit caveat documentation.

Source of truth: `squads/research/workflows/tech-research/tech-research-pipeline.yaml`
Pattern: aligned with `/sinkra-map-process`, `/sinkra-validate-squad`, `/full-sdc`.

## Usage

```
/tech-research "como melhorar performance de queries SQL"
/tech-research "comparar Postgres vs MySQL vs MongoDB" --deep
/tech-research "validar ideia: plataforma de PromptOps empresarial" --product-discovery
/tech-research "validar JTBD para meeting AI" --pd
/tech-research "follow-up: como o pgvector se compara com pinecone" --yolo
/tech-research "análise de pgvector" --budget-preset economy
/tech-research "landscape de ferramentas de observabilidade" --budget-preset deep
/tech-research "comparar Redis vs Dragonfly" --cost-max 1.50
```

### Budget Presets (RA-A.2)

Controls cost/time hard stops via the `budget` block in `pipeline-state.yaml`.
Flag `--budget-preset {economy|standard|deep}` or `--cost-max $X` (custom cap).

| Preset | cost_usd_max | token_max | wallclock_max_sec | Use when |
|---|---|---|---|---|
| `economy` | $0.50 | 100 000 | 300s | Quick answer, constrained budget |
| `standard` | $2.50 | 250 000 | 600s | Default — most research queries |
| `deep` | $10.00 | 800 000 | 1800s | Full landscape, multi-wave dossier |
| `--cost-max $X` | user-supplied | (standard caps) | (standard caps) | Fine-grained cost ceiling |

Budget signals evaluated by heartbeat (source: `heartbeat-policy.yaml`):
- Priority 2: `token_budget` — fires at 85% token_max
- Priority 3: `cost_usd` — fires when cost_usd_used > cost_usd_max (IGNORED if cost_confidence=unavailable)
- Priority 4: `wallclock` — fires when wallclock_used > wallclock_max_sec

Cost confidence levels: `exact` (SDK data) | `approximate` (tiktoken estimate) | `unavailable` (SDK+tiktoken failure → signal ignored, run continues).

### Product Discovery Mode

When `--product-discovery` (alias `--pd`) is set, OR auto-clarify detects the
`product_validation` pattern (JTBD, Mom Test, smoke test, MVP keywords), Phase 1.5
decomposition uses **product-validation sub-queries** (JTBD framing + Villain OSINT +
WTP signals + blue ocean + validation case studies). Output dossier feeds the
`/research-chief` validate-product-idea molecule (Wave 0). See
`squads/research/data/product-discovery-framework.md`.

Cross-link: this skill is the **research helper**; the spy molecule is the
**decision engine** (GO/NO-GO gates).

---

## Execution Model — Inline Persona-Fidelity + Visual Tracking

This skill does **NOT** spawn specialist subagents per phase (unlike `/sinkra-map-process`
which spawns `@process-discoverer`, `@architecture-designer`, etc.). Instead, each phase
loads:

1. The corresponding **workflow YAML** (`workflows/phase-*.yaml`) for protocol
2. The corresponding **prompt** (`prompts/*.md`) when present
3. The **persona name** declared in `squads/research/workflows/tech-research/tech-research-pipeline.yaml`

and executes inline in main context with persona fidelity. `TeamCreate` is used for
**visual progress tracking only** (the team has a single team-lead participant).

### Why inline (not spawn)?

The research personas (decomposer, executor, evaluator, synthesizer, citation-verifier,
documenter) are **roles**, not full SINKRA agents. Each is ~5-10 specific behaviors
loaded from the corresponding workflow file. Spawning subagents per phase would:
- Pay context-cold cost 7+ times (high token waste)
- Require 6+ new files in `squads/{owner}/agents/`
- Add coordination overhead with zero specialization gain

The full-spawn pattern is reserved for skills where each phase has truly distinct
expert protocols (e.g. `sinkra-map-process` spawns 7 specialists across 60-120 minutes).
tech-research's 7 molecules complete in ~5-15 minutes inline.

### When inline fallback applies (from sinkra-map-process)

N/A here — inline IS the canonical execution. No fallback needed.

---

## NON-NEGOTIABLE RULES (read BEFORE any phase)

**RULE 1: Guardrails first.** Phase 00 MUST `Read("squads/research/checklists/tech-research/guardrails.yaml")` and confirm `veto_conditions`, `constraints`, `implementation_redirect`, `security`, `scope_boundaries` are loaded. Apply vetoes immediately. Skipping guardrails = INADMISSIBLE.

**RULE 2: Checkpoints are absolute.** `COVERAGE_GATE` VETO (coverage<50 after 3 waves) halts. `CITATION_GATE` VETO (verified_ratio<0.85 after 2 fix attempts) halts. REVIEW requires explicit caveat documentation in the final report. No override.
Coverage target threshold (APPROVE band): see `squads/research/data/tech-research/_skill-config.yaml#search_waves.coverage_threshold` (canonical SOT — do NOT hardcode here).

**RULE 2b: Stop decisions are policy-driven (RA-A.1).** Phase 3.5 MUST load `squads/research/data/heartbeat-policy.yaml` and evaluate signals in priority order. Single-signal `coverage >= 70` is now signal #5 of 7. Policy file is governed by `quality-gates.yaml` (macro SOT). See §Stop Signals below.

**RULE 3: Incremental learning log.** Write `.aiox/learning/logs/tech-research/{slug}-{timestamp}.yaml` at Phase 00c with all phases as `status: pending`, update on EVERY phase start (in_progress) AND completion (completed/halted/failed). Post-hoc single-write at end is forbidden — see `.claude/rules/incremental-learning-log.md`.

**RULE 4: Prior-art before absence.** Any claim of "this technology does not exist", "no library does X", "no benchmark available" requires documented WebSearch/grep with verdict. See `.claude/rules/prior-art-search.md`. Findings without evidence = REVIEW caveat.

**RULE 5: NO implementation.** Recommendations are research outputs, not production code. If the user request is "implement X" → redirect to `@aiox-pm` or `@aiox-dev`. Writing code/agents/skills/deploy artifacts = VETO. See `squads/research/checklists/tech-research/guardrails.yaml#implementation_redirect`.

**RULE 6: Outputs only under `docs/research/{date}-{slug}/`.** Plus the learning log under `.aiox/learning/logs/tech-research/`. Writing anywhere else = VETO.

**RULE 7: Follow-up reuses existing folder.** When the request continues an existing topic (mentions previous findings, uses terms like `mais sobre`, `continue`, `aprofunde`, `também`, technology names from active folder) → reuse the same `docs/research/{date}-{slug}/` folder and resolve next file number via `squads/research/scripts/tech-research/next_followup_number.py {output_dir}` before writing `04-*`, `05-*`, etc. Do NOT create a new folder.

**RULE 8: No partial reads — ACTIVE SELF-CHECK.** If you ARE ABOUT TO say or have just said you will read a file "in parts" / "parcialmente" / "in chunks" / "first part" — STOP your current turn before any tool call. Do not narrate the partial read. Either read the file fully or HALT with `Missing tech-research operational file: {path}`. Partial reads corrupt phase contracts.

**RULE 9: Sequential by default; waves are bounded.** Phases run sequentially. Phase 3 search waves bounded at `max_waves: 3`. Wave 2+ MUST read `evolving_report.md` + `wave-*-summary.md` instead of carrying all raw results forward. Citation Gate fix loop bounded at 2 attempts.

**RULE 10: CLI next-command suggestion.** At completion (not on VETO/halt), suggest the next logical command per `.claude/rules/cli-next-command-flow.md`. Skip if `--yolo` was passed.

**RULE 11: Phase 0 Prior-Art Audit (MANDATORY).** BEFORE any guardrail or wave execution, Phase 0 MUST run `node ./scripts/research/prior-art-check.js --query "<query>" --artifact-type research --skill tech-research --markdown`. Verdict ∈ {`SKIP`, `SYNTH_ONLY`, `FOCUSED_FOLLOWUP`, `NEW_QUERY`} drives next step:
- `SKIP` (≥80% overlap) → HALT, point to existing dossier
- `SYNTH_ONLY` (≥2 MEDIUM matches, 40-79%) → HALT, redirect to inline synthesis
- `FOCUSED_FOLLOWUP` (1 MEDIUM match) → reuse folder via `next_followup_number.py` (current RULE 7 path)
- `NEW_QUERY` (no match or all LOW <40%) → proceed to Phase 00 guardrails

Operator can override any verdict, but override MUST register reason in `docs/research/_audit-log.yaml` through `./scripts/research/prior-art-check.js --append-log`. See `.claude/rules/prior-art-search.md` § Research Outputs as Prior Art. Founding incident: 2026-05-26 (`/research-chief` recomendou 6 queries cobertas 85-100% por dossiês existentes).

---

## Stop Signals — Multi-Signal Heartbeat Policy (RA-A.1)

Source of truth: `squads/research/data/heartbeat-policy.yaml`
Governed by: `squads/research/data/quality-gates.yaml` (macro SOT; QG wins on conflict)

Phase 3.5 evaluates 7 stop signals in priority order at each heartbeat tick.
First match wins → STOP. If none fires → evaluate 3 replan signals → CONTINUE.

### Stop Signals (priority order, first match wins)

| Priority | Signal ID | Condition | Category | stop_reason_category |
|---|---|---|---|---|
| 1 | `wave_max_with_low_coverage` | wave_num == 3 AND coverage_score < 50 | hard_stop | max_waves |
| 2 | `token_budget` | token_budget_used > 0.85 | hard_stop | budget_limit |
| 3 | `cost_usd` | cost_usd_used > cost_max | hard_stop | budget_limit |
| 4 | `wallclock` | wallclock_used > timeout_sec | hard_stop | budget_limit |
| 5 | `coverage_score` | coverage_score >= 70 | soft_stop | decision_sufficiency |
| 6 | `gap_convergence` | gap_set.is_empty() | soft_stop | saturation |
| 7 | `new_information_ratio` | new_information_ratio < 0.05 | soft_stop | saturation |

Signal `gap_convergence` is now active (RA-B.1 delivers `gaps.yaml` from P3.4). Returns true when all gaps are closed or abandoned.

### Gap-Driven Decompose — Wave 2+ (RA-B.2)

**Rule:** Wave 2+ sub-query decomposition MUST consume `gaps.yaml` (produced by P3.4 `gap_detector.py`) as the primary input.

**Protocol:**
1. Before decompose, read `gaps.yaml` from output_dir and extract open gaps.
2. Generate sub-queries that target open gaps — each sub-query carries `targets_gaps: [G001, ...]`.
3. Fallback queries (no specific gap) are allowed at ≤ 40% of total queries.
4. After Wave 2 execution, run `gap_alignment_check.py` as part of phase finalize.

**Alignment Check:**
```bash
python3 squads/research/scripts/tech-research/gap_alignment_check.py \
  --output-dir {output_dir} \
  --wave {wave_num} \
  --sub-queries-file {output_dir}/sub-queries-wave{N}.json \
  --mode {mode}
```
Returns `{alignment_ratio, threshold: 0.60, status: PASS|FAIL}`.

**Alignment semantics (STORY-RA-B.2 D1):**
- PASS (alignment_ratio >= 0.60): log and continue.
- FAIL (alignment_ratio < 0.60): emit WARNING in wave summary — not a veto in v1.
  Threshold may become BLOCKING after 10 historical runs with calibrated baseline.
- EXEMPT: Wave 1 (targets_gaps optional; gaps.yaml not yet populated at decompose time).

**Product-discovery mode (AC-5 / D3):** same `gap_alignment_check.py`, same threshold.
Only the decomposition framing changes (JTBD/Villain/WTP instead of scope angles).

**Metrics update:** write `alignment_ratio` to `metrics.yaml` `gap_loop.wave_{N}_alignment_ratio`.

**Sub-query template:** `squads/research/templates/tech-research/sub-queries.yaml`

### Replan Signals (all-matching, evaluated only when no stop fires)

| Signal ID | Condition | Action |
|---|---|---|
| `source_contradiction_detected` | == true | inject_contradiction_resolution_subquery |
| `wave_returned_low_signal` | == true | pivot_query_phrasing |
| `unsupported_claim_top_tier` | > 20% | inject_citation_recovery_subquery |

Replan signals do NOT stop the run. They modify next-wave sub-queries.

### Metrics Sources

| Metric | Source |
|---|---|
| token_budget_used, cost_usd_used, wallclock_used | `cost_tracker.py` (RA-0.1) |
| coverage_score, new_information_ratio | `coverage_calculator.py` |
| cost_max, timeout_sec | `pipeline-state.yaml` or env var |
| unsupported_claim_top_tier_ratio | `citation_verifier.py` (RA-D.1) |

### Validator

`squads/research/scripts/tech-research/output_validator.py` hook `check_heartbeat_policy()`
validates the schema of `heartbeat-policy.yaml`. Severity: default WARNING; ERROR under
`--enforcement block`. 30d warn → block promotion window (same as F.1/F.2/F.3/C.1 hooks).

---

## WHEN CALLED BY ANOTHER SKILL

This skill is invoked by:

- **`/research-chief`** — `validate-product-idea` Wave 0 (atoms 3 Villain + 4 WTP)
- **`/skill-creator`** — optional prior-art evidence before scaffolding
- **`/aiox-architect`** — optional research-before-decision
- **`/research-bench`** — multi-player benchmarks (codebase/llm/product/company/technology). When query implies multi-player comparison or absorption analysis, **redirect to `/research-bench`** instead of executing in research-mode. Bench produces `docs/bench/{date}-{slug}/`, not `docs/research/{date}-{slug}/`.

The pipeline MUST execute identically when called from another skill — full 7 molecules,
both checkpoints, incremental learning log. Do NOT "simplify" or "estimate" because
you are inside another skill's context. The 7 molecules take ~5-15 minutes inline.
There is no faster alternative.

**Caller receives:**
- Path to `docs/research/{date}-{slug}/` directory (all atoms inside)
- `README.md` (TL;DR + index)
- `quick-wins.md` (≥3 items with hub targets) OR documented gap block
- Learning log path: `.aiox/learning/logs/tech-research/{slug}-{timestamp}.yaml`
- COVERAGE_GATE + CITATION_GATE verdicts (APPROVE is required for caller to proceed)

## Bench-Mode Redirect (Auto-Detection)

When `/tech-research` is invoked with a query that pattern-matches `compare X vs Y vs Z`, `X vs Y`, `top open-source projects for X`, `landscape of X`, `absorption analysis`, or similar **multi-subject comparison**, Auto-Clarify (Phase M1 / P0) MUST:

1. Tag `comparison_pattern: multi_player` in inferred_context
2. Emit suggestion to user: "Esta query parece ser multi-player comparison. Recomendação: redirecionar para `/research-bench` que produz `docs/bench/{date}-{slug}/` com Gold contract (16 YAMLs + microdim matrix + N-choose-2 duels)."
3. If user confirms → HALT tech-research, escalate to `/research-bench`
4. If user wants single-topic deep research anyway (e.g. "deep dive on X" not "compare X with Y") → continue tech-research normally

This prevents the failure mode observed 2026-05-18 where research-mode and bench-mode artifacts were mixed.

See `.claude/rules/research-bench-gold.md` Rule 10 for unified extractor mode.

---

## Phase 00: Parse Args + Initialize (team-lead, inline)

### 0.0 — SKILL-VERSION Print + Cache-Staleness Check (AC8)

```
# Read workflow_version from this SKILL.md frontmatter (the field declared above).
# This is the SINGLE SOURCE OF TRUTH for versioning (AC7).
skill_workflow_version = frontmatter.workflow_version   # e.g. "3.2.0"

# Print the version banner BEFORE any other action:
print("SKILL-VERSION: v{skill_workflow_version}")

# Cache-staleness check: if the model loaded a cached version of SKILL.md
# that has a DIFFERENT workflow_version than the on-disk file, halt.
# In practice: read the first 20 lines of .claude/skills/tech-research/SKILL.md
# and extract the workflow_version field. Compare with what was loaded.
on_disk_version = Read(".claude/skills/tech-research/SKILL.md", limit=20)
                  → extract `workflow_version:` value

IF skill_workflow_version != on_disk_version:
  HALT with:
    "Cache-staleness detected: loaded workflow_version={skill_workflow_version}
     but on-disk workflow_version={on_disk_version}.
     Reload the skill and retry."
```

### 0.1 — Capture Start Time + Extract Arguments

```
start_epoch = Bash("date +%s")   # used for elapsed_minutes in learning log

query                = arguments[0]                    # required
product_discovery    = arg has --product-discovery | --pd
deep_mode            = arg has --deep
mode                 = "yolo" if --yolo else "interactive"   # default: interactive
slug                 = kebab-case(query[:60])
date                 = Bash("date +%Y-%m-%d")
output_dir           = docs/research/{date}-{slug}/
learning_log_dir     = .aiox/learning/logs/tech-research/
learning_log_path    = {learning_log_dir}/{slug}-{Bash('date +%Y%m%d-%H%M%S')}.yaml
```

### 0.2 — Pre-Flight Guardrails (RULE 1)

```
Read("squads/research/checklists/tech-research/guardrails.yaml")
Verify sections present: veto_conditions, constraints, implementation_redirect, security, scope_boundaries
Apply vetoes immediately:
  - request is "implement X" → REDIRECT to @aiox-pm or @aiox-dev, HALT
  - write outside docs/research/** → BLOCK
  - no results expected (impossible query) → HALT with explicit no-result message
```

### 0.25 — Prior-Art Audit (RULE 11, MANDATORY before any execution)

```bash
node ./scripts/research/prior-art-check.js \
  --query "<query>" \
  --artifact-type research \
  --skill tech-research \
  --markdown
```

Apply verdict:
- `SKIP` -> HALT with reference to top match dossier.
- `SYNTH_ONLY` -> HALT and synthesize existing matches before spending new budget.
- `FOCUSED_FOLLOWUP` -> set `mode=follow_up`, reuse the closest folder, and call `python squads/research/scripts/tech-research/next_followup_number.py {output_dir}`.
- `NEW_QUERY` -> proceed to 0.3.

Append the operator decision only through the CLI:

```bash
node ./scripts/research/prior-art-check.js \
  --query "<query>" \
  --artifact-type research \
  --skill tech-research \
  --append-log \
  --operator-decision confirm
```

Override path:

```bash
node ./scripts/research/prior-art-check.js \
  --query "<query>" \
  --artifact-type research \
  --skill tech-research \
  --append-log \
  --force-rerun "reason: <operator justification>"
```

### 0.3 — Follow-Up Detection (RULE 7, fallback path)

This runs ONLY if Phase 0.25 verdict was `NEW_QUERY` — preserved for explicit follow-up signals the operator may include:

```
IF query mentions "continue|mais sobre|aprofunde|follow-up|também|e sobre" OR
   query references a slug from existing_folders OR
   query references technology name from a recent active folder:
   → mode = "follow_up"
   → output_dir = existing folder (most recent matching)
   → next_followup_num = Bash("python squads/research/scripts/tech-research/next_followup_number.py {output_dir}")
ELSE:
   → mode = "new_research"
   → Bash("mkdir -p {output_dir}")
```

### 0.4 — Display Banner

```
╔══════════════════════════════════════════════════════════╗
║  /tech-research — {query[:50]}                            ║
╠══════════════════════════════════════════════════════════╣
║  Slug:           {slug}                                   ║
║  Mode:           {new_research|follow_up}                 ║
║  Product Disc.:  {yes|no}                                 ║
║  Deep:           {yes|no}                                 ║
║  Interactive:    {yes|no}                                 ║
║  Output Dir:     docs/research/{date}-{slug}/             ║
║  Learning Log:   {learning_log_path}                      ║
╠══════════════════════════════════════════════════════════╣
║  Pipeline (7 molecules, 11 atoms + Phase 0 audit):        ║
║    P0.25. PRIOR-ART AUDIT (RULE 11, MANDATORY)            ║
║          → SKIP | SYNTH_ONLY | FOCUSED_FOLLOWUP | NEW_QUERY ║
║    P00. Parse + Init (team-lead)                          ║
║    P00b. TeamCreate + TaskCreate                          ║
║    P00c. Init Incremental Learning Log                    ║
║    M1 P0.     Auto-infer context (SEED)                   ║
║    M1 P1.     Strategic Brief Builder (always)            ║
║    M2 P1.5.   Decompose (2-3 per SCOPE angle, 5-18)       ║
║    M3 P2.     Generate Deep Research Prompt               ║
║    M4 P3-3.7. Execute Research (waves+evaluate+compress)  ║
║               [COVERAGE_GATE @ P3.5]                      ║
║    M5 P4.     Synthesize + Extract Quick Wins             ║
║    M6 P4.5.   Verify Citations [CITATION_GATE]            ║
║    M7 P5.     Document final artifacts                    ║
║    P5b. Finalize Log + Suggest Next Command               ║
╚══════════════════════════════════════════════════════════╝
```

Proceed directly. Only HALT conditions (guardrail veto, missing query, VETO without resolution) surface to user before P00b.

---

## Phase 00b: Create Team + Tasks (visual tracking)

```
TeamCreate(
  team_name: "trr-{slug}",
  description: "Tech Research — {query[:60]}"
)

TaskCreate(title: "P00c: Initialize Learning Log")
TaskCreate(title: "M1: Auto-Clarify")
TaskCreate(title: "M2: Decompose (2-3 per SCOPE angle, 5-18)")
TaskCreate(title: "M3: Generate Deep Research Prompt")
TaskCreate(title: "M4: Execute Research (waves + evaluate) [COVERAGE_GATE]")
TaskCreate(title: "M5: Synthesize + Quick Wins")
TaskCreate(title: "M6: Verify Citations [CITATION_GATE]")
TaskCreate(title: "M7: Document final artifacts")
TaskCreate(title: "P5b: Finalize Log + Suggest Next Command")
```

`TaskUpdate(in_progress)` on phase entry, `TaskUpdate(completed)` on phase exit.

---

## Phase 00c: Initialize Incremental Learning Log (RULE 3)

Write the log file BEFORE any research action. Pre-populate phase registry with all
phases as `status: pending`. This is the **provenance contract** — if the pipeline
crashes mid-way, the log preserves what was attempted.

```yaml
# Write to: .aiox/learning/logs/tech-research/{slug}-{timestamp}.yaml
schema_version: "1.0"
skill_id: "tech-research"
run_id: "{slug}-{YYYYMMDD-HHmmss}"
timestamp_started: "{ISO-8601 now}"
timestamp_updated: "{ISO-8601 now}"
timestamp_completed: null
outcome: in_progress

inputs:
  query: "{query}"
  product_discovery: {bool}
  deep_mode: {bool}
  follow_up: {bool}
  output_dir: "{output_dir}"

phases:
  p00_init:                { status: completed, started_at: "{start}", completed_at: "{now}" }
  p00b_team:               { status: completed }
  p00c_log_init:           { status: in_progress, started_at: "{now}" }
  p0_auto_clarify:         { status: pending }
  p1_strategic_brief:      { status: pending }
  p15_decompose:           { status: pending }
  p2_generate_prompt:      { status: pending }
  p3_execute_research:     { status: pending, waves: [] }
  p35_evaluate_coverage:   { status: pending, checkpoint: COVERAGE_GATE }
  p36_compress_wave:       { status: pending }
  p37_multi_llm:           { status: pending, conditional: true }
  p4_synthesize:           { status: pending }
  p45_verify_citations:    { status: pending, checkpoint: CITATION_GATE }
  p5_document:             { status: pending }
  p5b_finalize:            { status: pending }

artifacts:
  required: []   # populated as files are written
  optional: []
```

After write: `TaskUpdate(p00c_log_init, completed)` and update log:
`phases.p00c_log_init.status = completed`.

**Write protocol (per RULE 3):** Each phase transition does a FULL-FILE overwrite of
the YAML (no append, no diff). Update `timestamp_updated` on every write. Persist on
halt/error.

---

## Phase M1 / P0: Auto-Clarify (research-decomposer inline)

**TaskUpdate(M1, in_progress)** → **learning log: `p0_auto_clarify.status = in_progress`**

### Load

```
Read("squads/research/data/tech-research/auto-clarification.yaml")
Read("squads/research/workflows/tech-research/phase-0-auto-clarify.yaml")
```

Confirm markers:
```
LOADED: squads/research/data/tech-research/auto-clarification.yaml ({line_count} lines)
LOADED: squads/research/workflows/tech-research/phase-0-auto-clarify.yaml ({line_count} lines)
```

### Persona — Research Decomposer

You infer context to SEED the brief. Detect:
- **research focus**: technical | comparison | general
- **temporal intent**: recent/current vs evergreen
- **technology/domain**: match aliases from `squads/research/data/tech-research/auto-clarification.yaml`
- **product-validation pattern**: JTBD, Mom Test, smoke test, MVP keywords → set `product_discovery=true`

### Execute

Follow `phase-0-auto-clarify.yaml` protocol. There is **no skip gate** — strong
inference only pre-fills more of the brief; it never bypasses Phase P1.

### Outputs

- `inferred_context`: {focus, technology, temporal_intent, product_validation} — **SEED** for P1

### Transitions

- ALWAYS → Phase P1 (Strategic Brief Builder)

**TaskUpdate(M1, completed)** → **learning log: `p0_auto_clarify.status = completed`**, add `inferred_context` summary.

---

## Phase P1: Strategic Brief Builder (ALWAYS runs)

**Learning log: `p1_strategic_brief.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-1-clarify.yaml")
Read("squads/research/data/tech-research/auto-clarification.yaml")  # strategic_brief_builder
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-1-clarify.yaml ({line_count} lines)
LOADED: squads/research/data/tech-research/auto-clarification.yaml ({line_count} lines)
```

### Persona — Research-Prompt Strategist

You convert a simple question into a strategic Deep Research brief. **Expand the
scope, never narrow it.** Bias toward actionable insight over generic summary.

### Execute

Apply `strategic_brief_builder` from `auto-clarification.yaml`:

0. **Read `few_shot_examples.cases` first — they are DEPTH ANCHORS.** Match
   that level of strategic reframing: turn the naive question into a research
   *territory*, expand scope, add a time horizon, make SCOPE angles specific.
   A skeletal brief that just restates the query is a FAIL.
1. Use `inferred_context` (SEED) per `seed_usage` to pre-fill the brief.
2. Fill the `template`: **TOPIC** (strategic title + time horizon) → **CONTEXT**
   (purpose, why now) → **SCOPE** (4-6 angles: trends/cases, quant data,
   implementable, risks, comparison) → **REQUIREMENTS** (3-4 params) →
   **RECOMMENDED SOURCES** (3-4 source types) → **EXPECTED OUTCOMES** (3-5 deliverables).
3. **Emit the brief inside ONE fenced code block** — copy-pasteable to an
   external Deep Research tool AND consumed by P1.5 Decompose.
4. **Emit 2-3 clarifying questions AFTER and OUTSIDE the code block.** They are
   skippable — the brief stands alone.
5. Language: the BRIEF (incl. section headers) is **ALWAYS ENGLISH** (pasted
   into Deep Research, drives English search). The CLARIFYING QUESTIONS use the
   operator language (PT-BR default for AIOX operators).
6. If `product_discovery=true`, reshape the brief around JTBD / villain OSINT /
   WTP / blue ocean / validation case studies.

### Outputs

- `strategic_brief`: structured brief (in a code block)
- `clarifying_questions`: 2-3 questions (outside the block)

### Transitions

- ALWAYS → Phase P1.5 (Decompose), consuming `strategic_brief`. If the user
  answers the clarifying questions, fold the answers into the brief first.

**Learning log: `p1_strategic_brief.status = completed`**, record brief topic.

---

## Phase M2 / P1.5: Decompose Query (research-decomposer inline)

**TaskUpdate(M2, in_progress)** → **learning log: `p15_decompose.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-1-5-decompose.yaml")
Read("squads/research/prompts/tech-research/decompose.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-1-5-decompose.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/decompose.md ({line_count} lines)
```

### Persona — Research Decomposer

Decompose the **strategic_brief** (from P1). Generate **2-3 orthogonal
sub-queries per SCOPE angle** (and its sub-bullets) — do NOT collapse a rich
brief into 5-7. Floor 5, ceiling 18 (M4 runs one search wave per sub-query —
cost is linear). Honor REQUIREMENTS as search constraints. Coverage MUST include:
- every SCOPE angle of the brief (≥2 sub-queries each)
- definitions/fundamentals + implementation + tradeoffs/comparison + real-world
- at least one devil's-advocate query
- at least one expert-level query

**If `product_discovery=true`:** use product-validation decomposition instead:
- JTBD framing
- Villain OSINT (3 competitors min)
- WTP signals (willingness-to-pay evidence)
- Blue ocean angle
- Validation case studies (Mom Test interviews, smoke tests)

Skip only for tiny follow-ups where a single targeted query is clearly enough.

### Mandatory Sources Matrix Consultation (STORY-RA-F.3 AC-A2)

After base decomposition, consult `squads/research/data/mandatory-sources.yaml`:

```
Read("squads/research/data/mandatory-sources.yaml")

For each mandatory_coverage entry:
  IF entry.when_domain_includes intersects with inferred_context.technology
     OR with strategic_brief topic keywords:
       For each literature in entry.must_cover_literatures:
         IF literature.id NOT already covered by base sub-queries:
           ADD sub-query: "{literature.id} — {first canonical_ref}, evidence base"
           CAP additions at max_mandatory_additions_per_run (default 3) per run

Log to learning log: phases.p15_decompose.mandatory_additions = [list of injected sub-queries]
```

**Cap rationale:** Bounded at 3 additions per run to prevent decompose count
inflation (Regression Risk R2). The matrix is **additive**, never gating —
if owner did not declare a literature angle, mandatory matrix surfaces it as
WARNING in caveats, not as a hard block (anti-pattern §1).

If `mandatory_additions` is empty (no domain matched), log explicitly:
`mandatory_additions: []  # no domain matched mandatory-sources.yaml`

### Outputs

- `decomposition_result`: N sub-queries with rationale (N = 2-3 per SCOPE angle, 5-18; PD mode 5-7)
- `mandatory_additions`: list of sub-queries injected from mandatory-sources matrix (may be empty)

**TaskUpdate(M2, completed)** → **learning log: `p15_decompose.status = completed`**, add sub-query count + `mandatory_additions`.

---

## Phase M3 / P2: Generate Deep Research Prompt (research-prompter inline)

**TaskUpdate(M3, in_progress)** → **learning log: `p2_generate_prompt.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-2-generate-prompt.yaml")
Read("squads/research/templates/tech-research/deep-research-prompt-template.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-2-generate-prompt.yaml ({line_count} lines)
LOADED: squads/research/templates/tech-research/deep-research-prompt-template.md ({line_count} lines)
```

### Persona — Research Prompter

Combine into the prompt template:
- original query
- strategic_brief (from P1) + any clarifying-question answers
- decomposition result
- temporal freshness requirements (if detected)
- explicit output expectations

### Output

- Write `docs/research/{date}-{slug}/01-deep-research-prompt.md` (atom: `research-prompt`)

**TaskUpdate(M3, completed)** → **learning log: `p2_generate_prompt.status = completed`**, record artifact path.

---

## Phase M4 / P3-P3.7: Execute Research (research-executor + coverage-evaluator inline)

**TaskUpdate(M4, in_progress)** → **learning log: `p3_execute_research.status = in_progress`**

The Execute Research molecule contains a wave loop with up to 3 iterations,
gated by COVERAGE_GATE at the end of each wave.

### Wave Loop Structure

```
FOR wave_num in [1, 2, 3]:
  P3:    Execute search (research-executor)
  P3.2:  Deep-read top sources (research-executor, conditional)
  P3.5:  Evaluate coverage [COVERAGE_GATE] (coverage-evaluator)
  P3.6:  Compress wave (coverage-evaluator)
  IF stop_decision OR wave_num == 3: break
```

### Phase P3 — Execute Search (per wave)

#### Load

```
Read("squads/research/workflows/tech-research/phase-3-execute-research.yaml")
Read("squads/research/data/tech-research/dependencies.yaml")
Read("squads/research/prompts/tech-research/tool-strategy.md")
Read("squads/research/prompts/tech-research/executor-matrix.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-3-execute-research.yaml ({line_count} lines)
LOADED: squads/research/data/tech-research/dependencies.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/tool-strategy.md ({line_count} lines)
LOADED: squads/research/prompts/tech-research/executor-matrix.md ({line_count} lines)
```

#### Persona — Research Executor

- Check Context7 and Exa availability before depending on them
- Use official docs first when a library/framework is detected (Context7)
- Use Exa for high-quality neural search when available
- Use WebSearch fallback when MCPs fail
- Use `squads/research/scripts/tech-research/url_detector.py` before routing special content (PDF, YouTube, arXiv)
- Execute sub-queries in main context by default
- Write `wave-{N}-progress.jsonl` after each sub-query result set (timeout recovery)

Carry forward source URLs, titles, snippets, tool used, credibility, extraction stats.

#### Output

- `wave-{N}-progress.jsonl`
- `search_results` (carried in context to P3.2/P3.5)

### Phase P3.2 — Deep Read (conditional, supplemental)

When snippets are insufficient for credibility/decision:

#### Load

```
Read("squads/research/workflows/tech-research/phase-3-2-deep-read.yaml")
Read("squads/research/prompts/tech-research/page-extract.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-3-2-deep-read.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/page-extract.md ({line_count} lines)
```

#### Execution

Use ETL first (YouTube transcript / PDF / blog fetch via `services/etl`), WebFetch fallback. Select top sources by credibility × relevance × density. Do NOT deep-read low-quality sources to fill quota.

### Phase P3.5 — Evaluate Coverage [COVERAGE_GATE]

#### Load

```
Read("squads/research/workflows/tech-research/phase-3-5-evaluate-coverage.yaml")
Read("squads/research/prompts/tech-research/evaluate.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-3-5-evaluate-coverage.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/evaluate.md ({line_count} lines)
```

#### Persona — Coverage Evaluator

Use `squads/research/scripts/tech-research/coverage_calculator.py` and `squads/research/scripts/tech-research/credibility_scorer.py` when available. Calculate:
- coverage_score (0-100)
- coverage_breakdown per sub-query
- source_quality (mean credibility)
- new_information_ratio (vs previous wave)
- remaining_gaps
- decision: `stop | continue | escalate-multi-llm`

#### COVERAGE_GATE Verdict

| coverage_score | wave_num | Verdict | Action |
|---|---|---|---|
| ≥ 70 | any | **APPROVE** | Stop search loop, proceed to P3.7 if `--deep` else P4 |
| 50-69 | < 3 | **REVIEW** | Continue to next wave |
| 50-69 | == 3 | **REVIEW** | Trigger P3.7 (multi-LLM escape valve) |
| < 50 | == 3 | **VETO** | HALT — escalate to user. Learning log: `outcome=halted`, reason=coverage_veto |

REVIEW band requires documenting the coverage caveat in the final report.

### Phase P3.6 — Compress Wave

#### Load

```
Read("squads/research/workflows/tech-research/phase-3-6-compress-wave.yaml")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-3-6-compress-wave.yaml ({line_count} lines)
```

#### Execution

Write `wave-{N}-summary.md`:
- coverage_score + decision
- key findings with source citations
- best source list
- remaining gaps

Update `evolving_report.md` cumulatively.

**Wave summaries are the memory bridge.** Wave 2+ MUST read summaries instead of carrying all raw data forward.

**Learning log per wave:** Append to `p3_execute_research.waves[]`: `{wave: N, coverage: X, decision: Y, sources_count: Z}`.

### Phase P3.7 — Multi-LLM Deep Research (conditional escape valve)

Triggered when:
- `--deep` flag was set, OR
- COVERAGE_GATE returned REVIEW band at wave 3, OR
- Manual keyword trigger ("multiple perspectives", "compare LLM views")

#### Load

```
Read("squads/research/workflows/tech-research/phase-3-7-playwright-deep-research.yaml")
Read("squads/research/prompts/tech-research/playwright-deep-research.md")
Read("squads/research/data/tech-research/_skill-config.yaml")    # for playwright_deep_research.* section
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-3-7-playwright-deep-research.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/playwright-deep-research.md ({line_count} lines)
LOADED: squads/research/data/tech-research/_skill-config.yaml ({line_count} lines)
```

#### Persona — Research Executor (multi-LLM mode)

Use Playwright MCP to query Grok / Claude.ai / Gemini per `config.yaml#playwright_deep_research.llms`. Graceful degradation: 1 successful LLM is enough.

If Playwright MCP unavailable AND `--deep` was explicit:
- HALT and escalate ("Multi-LLM deep research requires Playwright MCP. Run `@devops *mcp-setup playwright`.")
- IF `--deep` NOT explicit: skip P3.7 silently, document missing capability in `evolving_report.md`

#### Output

- `docs/research/{date}-{slug}/XX-llm-deep-research.md` (atom: `llm-deep-research`)
- Screenshots per `config.yaml#playwright_deep_research.screenshots`

**TaskUpdate(M4, completed)** → **learning log: `p3_execute_research.status = completed`**, add waves array, COVERAGE_GATE verdict.

### Phase P4.0 — Per-Candidate Parallel Analysis (Story RA-F.2 AC-3, conditional)

**Conditional fire:** runs ONLY when `inferred_context.comparison_pattern == "multi_player"` AND `candidates_count >= 3` AND every candidate requires the SAME structured analysis (same dimensions/features). When fewer than 3 candidates or heterogeneous analysis required, skip this phase — synthesis proceeds inline in P4 as usual.

**Coordination with RA-C.2 dispatcher (RUNTIME DETECT, not temporal):** Story RA-C.2 owns `dispatcher.py` for spawn-by-PHASE (P3 / P4 / P4.5 parallelism). F.2 spawn is by-CANDIDATE (1 sub-agent per candidate, all running the SAME phase). Both patterns are orthogonal and MUST coexist without duplication.

The branch is decided at RUNTIME by file presence, NOT by tracking which story merged first:

```python
# pseudocode for P4.0 spawn dispatch (NOT temporal — runtime probe)
DISPATCHER_PATH = "squads/research/scripts/tech-research/dispatcher.py"
if os.path.exists(DISPATCHER_PATH):
    # RA-C.2 helper is present → delegate by-candidate spawn through it.
    from dispatcher import spawn_by_candidate  # type: ignore
    handles = spawn_by_candidate(candidates=candidates, prompt_template=PROMPT, schema=SCHEMA)
else:
    # RA-C.2 not landed yet → emit thin subagent_spawn[] envelope inline.
    # Records the handshake contract so refactor on RA-C.2 merge is mechanical.
    handles = inline_subagent_spawn(candidates=candidates, prompt_template=PROMPT, schema=SCHEMA)
log_event("spawn_init", spawn_mode="parallel", dispatcher_used=bool(...))
```

Why runtime detect:
- Deterministic in CI even if RA-C.2 merges out-of-order or gets reverted.
- Refactor is a one-line delete (remove the `else` branch) instead of a story coordination dance.
- Tests can cover BOTH branches by toggling `DISPATCHER_PATH` (mock-then-unmock) — see fixture coverage in §Validation in this session below.

**Spawn protocol:**

1. **Build the per-candidate prompt template** — identical across all sub-agents EXCEPT the candidate name. Each sub-agent receives:
   - `candidate_id` (e.g. `claude_code`, `aider`, `cline`, `openhands`, `cursor`)
   - `dimensions[]` (declared in `criteria.md` from Story RA-F.1)
   - `evidence_corpus` (subset of P3 search results relevant to the candidate)
   - REQUIRED OUTPUT SCHEMA (sub-agent-output.v1):

   ```json
   {
     "candidate_id": "string",
     "agent_id": "string",
     "started_at": "ISO-8601",
     "completed_at": "ISO-8601",
     "schema_version": "sub-agent-output.v1",
     "dimensions": [
       {
         "dimension_id": "string",
         "status": "confirmed | partial | uncertain | not_present",
         "score": 0.0,
         "confidence": "high | medium | low",
         "evidence_url": "string (optional)"
       }
     ]
   }
   ```

2. **Spawn N sub-agents in parallel** via the Agent tool with `subagent_type: general-purpose` (or specialist if discoverable in `.claude/agents/`). 1 sub-agent per candidate. Bounded by `max_candidates_parallel: 8` to prevent runaway fanout.

3. **Record spawn events to `execution-log.jsonl`**:
   ```json
   {"event": "spawn_init", "spawn_mode": "parallel", "candidates_count": N, "max_candidates_parallel": 8, "timestamp": "..."}
   {"event": "subagent_spawned", "agent_id": "general-purpose-{i}", "candidate_id": "...", "timestamp": "..."}
   {"event": "subagent_done", "agent_id": "...", "candidate_id": "...", "duration_s": N, "timestamp": "..."}
   {"event": "consolidation", "candidates_done": N, "merged_into": "matrices.yaml", "wallclock_s": N, "timestamp": "..."}
   ```

4. **Consolidate sub-agent outputs** via Python script that:
   - Validates each output against `sub-agent-output.v1` schema (reject misshapen output → re-spawn that candidate, max 1 retry)
   - Merges per-dimension status/score/confidence into the row × column matrix
   - Computes std deviation across candidates per dimension (sanity-check for AT-4 — if std dev > 0.5 in any dimension, log warning that rubric calibration may be off)

5. **Fallback sequential (AC-5):** when `--no-parallel` flag is passed OR Agent tool is unavailable, set `spawn_mode: sequential_fallback` and analyze each candidate inline. Output schema and merged matrix MUST be equivalent — only the wallclock differs.

**Validation in this session:** fixture `squads/research/tests/coverage-matrix-fixtures/parallel-spawn-fixture/` exercises:
- AT-3 (parallel speedup ≥ 2.5×): synthetic execution-log.jsonl shows parallel wallclock ÷ sequential wallclock = **4.55×** (measured 2026-05-19)
- AT-4 (sub-agent std dev < 0.5): 5 sub-agent outputs on identical input show max per-dimension std dev = **0.400**

Verify via:
```bash
python3 squads/research/tests/coverage-matrix-fixtures/parallel-spawn-fixture/verify_at3_at4.py
```

**Anti-patterns (Story §Anti-patterns):**
- NEVER spawn parallel when `candidates_count < 3` — Agent tool overhead does not pay off.
- NEVER let sub-agents output free-form text — the schema is fixed; reject misshapen output.
- NEVER spawn when analyses are heterogeneous (e.g. one candidate needs deep-read, others surface-scan) — that's a synthesis problem, not parallel-spawn problem.

**TaskUpdate(P4.0, completed)** → **learning log: `p4_0_per_candidate_parallel.status = completed`**, record `spawn_mode`, candidates_count, AT-3 + AT-4 measurements from execution-log.

---

## Phase M5 / P4: Synthesize + Extract Quick Wins (research-synthesizer inline)

**TaskUpdate(M5, in_progress)** → **learning log: `p4_synthesize.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-4-synthesize.yaml")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-4-synthesize.yaml ({line_count} lines)
```

### Persona — Research Synthesizer

Read all `wave-*-summary.md` files + `evolving_report.md` + `XX-llm-deep-research.md` (if present) + any enriched_results still in context.

**Preserve disagreement, uncertainty, source-specific nuance.** Do NOT flatten contradictions into fake consensus.

### Step 5.5 — Extract Quick Wins (mandatory)

Scan consolidated findings for items where:
- `value = high`
- `effort ∈ {XS, S}`
- `time_to_value ≤ 1 week`

Produce a Quick Wins set with **≥ 3 entries**. Each entry MUST:
- Map to a hub target (squad / app / skill / agent / runner / rule / workflow / ADR / doc)
- Cite a § of the report
- State the concrete next action

**If fewer than 3 candidates qualify:** write an explicit `## Quick Wins Não Encontrados` block documenting the gap. NEVER pad with low-quality items.

### Outputs

- `synthesis_draft` (held in context for P5)
- Write `docs/research/{date}-{slug}/quick-wins.md` (atom: `quick-wins`)

**TaskUpdate(M5, completed)** → **learning log: `p4_synthesize.status = completed`**, record quick_wins_count.

---

## Phase M6 / P4.5: Verify Citations [CITATION_GATE] (citation-verifier inline)

**TaskUpdate(M6, in_progress)** → **learning log: `p45_verify_citations.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-4-5-verify-citations.yaml")
Read("squads/research/prompts/tech-research/verify-citations.md")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-4-5-verify-citations.yaml ({line_count} lines)
LOADED: squads/research/prompts/tech-research/verify-citations.md ({line_count} lines)
```

### Persona — Citation Verifier

Every important claim needs a source. For each claim in `synthesis_draft`:
- Verify the citation URL exists (or that the source file still asserts the claim)
- Verify the quoted text matches the source (no paraphrase passing as quote)
- Verify the date is current relative to temporal intent

Use `squads/research/scripts/tech-research/claim_extractor.py` + `squads/research/scripts/tech-research/sources_extractor.py` if available.

### Fix Loop (bounded at 2 attempts)

```
attempt = 0
WHILE attempt < 2:
  unsupported = list of claims that failed verification
  IF len(unsupported) == 0: break
  FOR claim in unsupported:
    - Re-search for a backing source
    - IF found: update claim with verified citation
    - ELSE: mark claim for removal or downgrade to "speculation" tag
  attempt += 1
```

### CITATION_GATE Verdict

| verified_ratio | unsupported_count | Verdict | Action |
|---|---|---|---|
| ≥ 0.85 | 0 | **APPROVE** | Proceed to P5 |
| ≥ 0.85 | > 0 (residual) | **REVIEW** | Proceed to P5 with explicit caveat block listing unsupported claims |
| < 0.85 | any | **VETO** | HALT — escalate. Learning log: `outcome=halted`, reason=citation_veto |

**TaskUpdate(M6, completed)** → **learning log: `p45_verify_citations.status = completed`**, record `verified_ratio`, `unsupported_count`, gate verdict.

---

## Phase M7 / P5: Document Final Artifacts (research-documenter inline)

**TaskUpdate(M7, in_progress)** → **learning log: `p5_document.status = in_progress`**

### Load

```
Read("squads/research/workflows/tech-research/phase-5-document.yaml")
Read("squads/research/templates/tech-research/output-structure.md")
Read("squads/research/templates/tech-research/output-structure.yaml")
```

Confirm markers:
```
LOADED: squads/research/workflows/tech-research/phase-5-document.yaml ({line_count} lines)
LOADED: squads/research/templates/tech-research/output-structure.md ({line_count} lines)
LOADED: squads/research/templates/tech-research/output-structure.yaml ({line_count} lines)
```

### Persona — Research Documenter

Write the final artifacts under `docs/research/{date}-{slug}/`. Phase splits into two
steps: **5.0 Write Narrative Atoms** (Markdown, hand-authored) and **5.1 Run Extractor
Atoms** (YAML/JSON, deterministic scripts). Both are required for the `rich` render
tier in the Research Observatory (`apps/dash`).

#### 5.0 — Narrative Atoms (hand-authored Markdown)

| Atom | Path | Contents |
|---|---|---|
| `research-readme` | `README.md` | Index + TL;DR + metadata (date, query, coverage_score, gate verdicts, file list, render_tier hint) |
| `original-query` | `00-query-original.md` | Original query + inferred context + flags |
| `research-report` | `02-research-report.md` | Full findings with source citations, confidence tags, disagreement preserved |
| `recommendations` | `03-recommendations.md` | Actionable recommendations (NO production code) + caveat blocks for CITATION_GATE REVIEW |
| `criteria` (conditional) | `criteria.md` | **Required** when `comparison_pattern=multi_player` AND `dimensions_count >= 5` (Story RA-F.1 AC-1). `dimensions_count` is computed at the START of Phase M7/P5 (immediately after P4 synthesis), from the axes that will be emitted to `matrices.yaml` by `comparison_matrix_extractor.py`. The file `criteria.md` MUST be authored BEFORE `comparison_matrix_extractor.py` runs in step 5.1 — the extractor produces the matrix; this atom produces the framework that interprets it. Template: `squads/research/templates/tech-research/criteria.md`. |
| `recommendations-by-use-case` (conditional) | `recommendations-by-use-case.md` | **Required** when `comparison_pattern=multi_player` AND `candidates_count >= 3` (Story RA-F.2 AC-4). Translates the bench ranking into prescriptive decisions PER USE CASE. Minimum 5 distinct use cases; each contains primary candidate, secondary candidate, decisive dimension, and gap to mitigate. Cross-table at the end shows candidate × use_case best-fit markers. NOT a summary of `02-research-report.md` — independent prescriptive atom. Template: `squads/research/templates/recommendations-by-use-case.md`. |
| `curiosity-queue` | `curiosity_queue.yaml` | Open questions, gaps, follow-up candidates — schema: `items: [{question, status: open\|resolved\|discarded, owner}]` (validated by `output_validator.py`) |
| `metrics.yaml` | `metrics.yaml` | coverage_score, gate verdicts, source counts, elapsed_minutes, token usage if tracked |
| `pipeline-state.yaml` | `pipeline-state.yaml` | Phase completion map (mirrors learning log) |

#### 5.0a — Criteria + Scoring Calibration (Story RA-F.1, AC-1/AC-2/AC-3)

When this research run produces ANY numeric score (`matrices.yaml`, `scorecard.json`, or any atom carrying `score`, `rank_score`, `dimension_score`, `feature_depth_score`):

1. **AC-1 — Emit `criteria.md` BEFORE the matrix** when both triggers fire:
   - `inferred_context.comparison_pattern == "multi_player"`, AND
   - `dimensions_count >= 5` (count of axes that will appear in `matrices.yaml`)

   Author `criteria.md` from `squads/research/templates/tech-research/criteria.md`. Declare axes, operational definitions, scale anchors, weights, rejected dimensions, and API caps (AC-4) BEFORE running `comparison_matrix_extractor.py`.

2. **AC-2 — Every scored atom MUST carry a `scoring_calibration` block** at root (YAML frontmatter) OR under `meta.scoring_calibration` (JSON). Required keys: `type` (interpretive | empirical | hybrid), `scale`, `calibrated_by`, `disclaimer`, `reproducibility`. When `type=hybrid|empirical`, also include `baseline`.

3. **AC-3 — Composite multi-weighted scoring (>=3 sub-scores) requires `scripts/scoring-{slug}.py`** copied from `squads/research/templates/scoring-script-template.py`. Weights MUST be declared IN CODE (not prose). Running `python scripts/scoring-{slug}.py {output_dir}` MUST re-produce the scoring CSV bit-exact (AT-3 reproducibility).

4. **AC-4 — Caps in field names** for any raw CSV/JSON column backed by an API with a known cap (e.g. `contributors_api_capped_100`, `commits_90d_capped_N`, `search_results_per_query_capped_50`, `snapshot_at_{YYYY-MM-DD}`). The cap is part of the data.

5. **AC-5 — Validator enforcement**: `output_validator.py --skill tech-research --enforcement {warn|block}` checks all four above. Defaults to `--enforcement warn` for 30d post-merge per Story RA-F.1 Regression Risk row 1; promote to `block` after a clean window.

#### 5.0b — Status Code 4-Níveis + Recommendations-by-Use-Case (Story RA-F.2)

When this research run produces a multi-player coverage matrix:

1. **AC-1 — Status code 4-níveis padronizado**: every cell in `matrices.yaml#rows[].cells[player]` MUST carry a `status` field from the canonical 4-level enum:

   | Status | Score | Symbol | Meaning |
   |---|:---:|:---:|---|
   | `confirmed` | 2.0 | ✅ | Public evidence confirms presence |
   | `partial` | 1.0 | ◐ | Evidence shows partial / qualified presence |
   | `uncertain` | 0.5 | ? | Evidence was sought but does NOT confirm |
   | `not_present` | 0.0 | — | Confirmed absence |

   PT-BR aliases (`sim`/`parcial`/`incerto`/`não`) and legacy binary (`tem`/`não tem`/`yes`/`no`) are accepted on input; the helper normalizes them to the canonical enum on read.

   **Anti-pattern (forbidden):** using `uncertain` as fallback for "not evaluated". Cells that were not evaluated MUST be exposed as gaps (e.g. `curiosity_queue.yaml`), NEVER as `uncertain` status. The helper rejects empty/None inputs explicitly to prevent silent fallback.

   ASCII degradation: set `RESEARCH_OUTPUT_ASCII=true` to render `[X]/[~]/[?]/[ ]` instead of the Unicode glyphs (Story §R2).

2. **AC-2 — Helper utility canonical**: import `coverage_matrix_helper.py` (singleton at `squads/research/scripts/tech-research/coverage_matrix_helper.py`). Public API: `normalize_status(raw)`, `status_to_score(s)`, `status_to_symbol(s)`, `validate_matrix(m)`. Do NOT duplicate this logic in other scripts; consume the helper.

3. **AC-3 — Parallel sub-agent spawn (≥3 candidates with homogeneous analysis)** — see §Phase P4.0 — Per-Candidate Parallel Analysis below.

4. **AC-4 — `recommendations-by-use-case.md` MANDATORY** when `comparison_pattern=multi_player` AND `candidates_count >= 3`. Author from `squads/research/templates/recommendations-by-use-case.md` (flat path). Minimum 5 distinct use cases, each with `primary`/`secondary`/`decisive_dimension`/`gap_to_mitigate`. Cross-table at the end. NOT a summary of `02-research-report.md`.

5. **AC-5 — Optional `--no-parallel` flag + sequential fallback**: if the run is invoked with `--no-parallel` OR Agent tool is unavailable, the per-candidate analysis runs sequentially inline. Record `spawn_mode: parallel | sequential_fallback` in `execution-log.jsonl`. Output equivalence is guaranteed (same matrix, same recommendations atom) — only the wallclock differs.

6. **AC-6 — Validator enforcement (extension hook)**: `output_validator.py` runs `check_status_code_compliance()` after `check_criteria_calibration()`. The hook is GENERIC across both skills (no `if skill == 'tech-research'` branches per PO Condition 2). Findings honor `--enforcement {warn|block}`:
   - `warn` (default for 30d post-merge per Story §Regression Risk): findings appear in `warnings[]`; exit code stays 0 unless legacy V1/V3 baseline fails.
   - `block`: findings cause `valid: false` + exit non-zero. Promote after 30d clean window (same canonical mechanics as Story RA-F.1 — see §Validator below).

#### 5.0c — Gap Analysis Atomo + Extraction Schema Enrichment (Story RA-F.3)

When this research run is multi-player comparison:

1. **AC-C1 — `gap-analysis.md` MANDATORY when `comparison_pattern=multi_player`**. Author the standalone atom from `squads/research/templates/gap-analysis-tmpl.md` (flat path consistent with F.1/F.2 templates). The atom contains: (a) summary table of structural gaps with risk level, (b) per-dimension analysis showing what each competitor has that subject lacks, (c) 5-stage maturity roadmap (Clareza → Repetibilidade → Mensuração → Ensino → Escala), (d) risks if gaps not corrected, (e) prioritized action items. The atom is SEPARATE from `02-research-report.md` — NOT embedded in §Caveats. Caveats remains for **conceptual caveats** (analytical limits); `gap-analysis.md` carries **structural competitive gaps** (subject vs competitors).

2. **AC-C2 — Cross-link MANDATORY**: when `gap-analysis.md` is emitted, `02-research-report.md` MUST include the line `Ver análise dedicada de lacunas: [./gap-analysis.md](./gap-analysis.md)` in the appropriate section (typically near §Caveats or §Recomendações). Additionally, `dashboard-manifest.yaml` registers `gap-analysis.md` in the `Ações` tab.

3. **AC-B2 — Source extraction schema enrichment (additive)**: when running `sources_extractor.py`, optional `extraction_metadata` dict may be provided (keyed by URL). Each entry merges `extraction_*` fields into the source record:
   - `extraction_method`: one of `websearch_snippet | webfetch | etl | playwright | manual_paste | extraction_blocked`
   - `extraction_quality`: one of `full | snippet_only | blocked_fallback_used`
   - `extraction_attempts`: integer count
   - `extraction_ladder_steps_tried`: list of step names when ladder was activated
   - `extraction_notes`: optional string explaining failure + fallback used

   Fields are OMITTED entirely when data is absent — never filled with universal defaults (per `.claude/rules/extraction-no-fallbacks.md`). `schema_version` remains `"1.0"` (additive, no breaking changes).

4. **AC-B3 — Extraction escalator**: when web extraction fails or yields low-quality snippet, callers can invoke `squads/research/scripts/tech-research/extraction_escalator.py` which runs the 5-step ladder declared in `squads/research/data/extraction-policy.yaml`:
   1. `websearch_snippet` (always first)
   2. `webfetch` (full-page)
   3. `etl_adapter` (structured types: youtube/pdf/arxiv/pubmed)
   4. `playwright` (JS-rendered, when MCP available)
   5. `mark_blocked` (terminal: register in caveats)

   The escalator NEVER silences failures — every attempt is logged with reason. Returns `ExtractionResult` with `to_sources_fields()` ready to merge into sources.yaml.

5. **AC-A2 — Mandatory sources matrix consultation** — see Phase M2/P1.5 above for the consumption protocol. Log `mandatory_additions: [list]` in learning log.

6. **Validator enforcement (extension hooks F.3)**: `output_validator.py` runs three new hooks after F.1/F.2 hooks:
   - `check_extraction_ladder()` — validates sources.yaml schema enrichment when present; flags invalid method/quality values and blocked entries without log notes
   - `check_mandatory_sources_coverage()` — WARN if `mandatory_additions` key is absent from pipeline-state/metrics/learning log (advisory only — matrix is additive)
   - `check_gap_analysis_presence()` — WARN/ERROR if `gap-analysis.md` is absent when `comparison_pattern=multi_player` is detected; advisory check on cross-link in 02-research-report.md

   All three hooks honor `--enforcement {warn|block}` (default `warn`, same canonical promotion mechanics as F.1/F.2).

#### 5.1 — Extractor Atoms (deterministic scripts, MANDATORY for `rich` render tier)

All scripts already exist in `squads/research/scripts/tech-research/`. They parse the
narrative atoms from 5.0 + wave summaries and emit structured YAML/JSON consumed by
`apps/dash` Research Observatory tabs.

Run in this order (each tolerates absent inputs gracefully):

```
Bash("python3 squads/research/scripts/tech-research/sources_extractor.py {output_dir}")           # → sources.yaml
Bash("python3 squads/research/scripts/tech-research/players_extractor.py {output_dir}")           # → players.yaml
Bash("python3 squads/research/scripts/tech-research/ux_patterns_extractor.py {output_dir}")       # → ux-patterns.yaml
Bash("python3 squads/research/scripts/tech-research/comparison_matrix_extractor.py {output_dir}") # → matrices.yaml
Bash("python3 squads/research/scripts/tech-research/logger.py consolidate {output_dir}")          # → execution-log.jsonl (final consolidated timeline)
Bash("python3 squads/research/scripts/tech-research/action_assets_extractor.py {output_dir}")     # → action-plan.yaml, claims.yaml, risk-register.yaml, decision-ledger.yaml
Bash("python3 squads/research/scripts/tech-research/research_graph.py {output_dir}")              # → research-graph.json (DEPENDS on sources + action assets — run AFTER both)
Bash("python3 squads/research/scripts/tech-research/dashboard_manifest.py {output_dir}")          # → dashboard-manifest.yaml, validation-report.yaml
```

| Atom | Path | Extractor | Observatory Tab |
|---|---|---|---|
| `sources` | `sources.yaml` | `sources_extractor.py` | Evidências / Fontes (URLs + credibility + flags) |
| `players` | `players.yaml` | `players_extractor.py` | Players (tools/companies/people referenced) |
| `ux-patterns` | `ux-patterns.yaml` | `ux_patterns_extractor.py` | Map (UX/product patterns, when research is UX-themed) |
| `matrices` | `matrices.yaml` | `comparison_matrix_extractor.py` | Map (every Markdown table under a heading becomes a matrix) |
| `execution-log` | `execution-log.jsonl` | `logger.py consolidate` | Waves (timeline of events — consolidates `wave-*-progress.jsonl`) — schema validated by `output_validator.py` |
| `action-plan` | `action-plan.yaml` | `action_assets_extractor.py` | Ações / Map (decision, actions, roadmap) |
| `claims` | `claims.yaml` | `action_assets_extractor.py` | Evidências (claims verificáveis) |
| `risk-register` | `risk-register.yaml` | `action_assets_extractor.py` | Ações (riscos e mitigação) |
| `decision-ledger` | `decision-ledger.yaml` | `action_assets_extractor.py` | Ações (decisões e consequências) |
| `research-graph` | `research-graph.json` | `research_graph.py` | Evidências (nodes: query/waves/sources/report/decisions; links: cite/derives_from) |
| `dashboard-manifest` | `dashboard-manifest.yaml` | `dashboard_manifest.py` | Map (readiness por aba + quality bars) |
| `validation-report` | `validation-report.yaml` | `dashboard_manifest.py` | Evidências (checks estruturais) |

**Tolerance rule:** if an extractor returns 0 entries because the research has no
matching content (e.g. `ux-patterns.yaml` when research is pure backend), the empty
YAML/JSON is STILL written with `items: []`. Empty extractor output is NOT a failure.

**Apps/research render tier mapping**:
- `gold` — has `rich` assets plus `action-plan.yaml`, `claims.yaml`, `risk-register.yaml`, `decision-ledger.yaml`
- `rich`  — has core narrative + `metrics.yaml` + `sources.yaml` + `research-graph.json` + `recommendations`
- `partial` — has narrative + some YAML/JSON (missing graph or sources)
- `legacy` — Markdown-only (no extractors run)

**Target after 5.1: `gold` tier.** If any extractor fails (script error, not empty
output), log warning to `execution-log.jsonl` and continue — Observatory will fall
back to `partial` tier render. Do NOT halt the pipeline.

### Validator (mandatory)

```
Bash("python squads/research/scripts/tech-research/output_validator.py --skill tech-research --enforcement warn {output_dir}")
```

The validator now runs TWO generic extension hooks back-to-back:

1. `check_criteria_calibration()` — Story RA-F.1 AC-5 (criteria.md presence, scoring_calibration block, scoring script presence)
2. `check_status_code_compliance()` — Story RA-F.2 AC-6 (recommendations-by-use-case.md presence, 4-level enum compliance, symbol consistency)

Both hooks honor the same `--enforcement {warn|block}` flag (single canonical 30-day window — promote one with the other).

**HALT logic (consistent with --enforcement semantics):**

| Outcome | Cause | Action |
|---|---|---|
| exit 0, `valid: true`, `warnings: []` | clean run | Mark M7 completed |
| exit 0, `valid: true`, `warnings: [...]` | legacy V1/V3 baseline OK, but criteria-calibration AND/OR status-code findings present (under `--enforcement warn`) | Mark M7 completed; surface `warnings[]` to user; record in learning log under `p5_document.criteria_calibration_findings` AND `p5_document.status_code_findings` |
| exit 1, `valid: false` (legacy V1/V3 check failed) | always HALT — REQUIRED_FILES missing, README sections missing, confidence tags absent, etc. | HALT, report errors. Do NOT mark M7 completed. |
| exit 1, `valid: false` AND `--enforcement block` | criteria-calibration findings (AC-1/AC-2/AC-3) OR status-code findings (AC-1/AC-4/symbol-consistency) under block mode | HALT, report errors. Do NOT mark M7 completed. |

**Story RA-F.1 30-day warn → block promotion mechanics (canonical):**

- **t0 (canonical):** Story RA-F.1 merge commit date in `main`. Recorded in `docs/stories/epic-research-intelligence/STORY-RA-F.1-CRITERIA-CALIBRATION-SCORING-SCRIPT.md#Change Log` when @devops merges the PR.
- **t0 → t0+30d:** validator invoked with `--enforcement warn`. Criteria-calibration findings (AC-1/AC-2/AC-3) appear in `warnings[]`; exit code stays 0 unless legacy V1/V3 baseline fails. M7 is marked completed.
- **t0+30d:** if zero regression incidents are documented in `outputs/qa/` over the window, @aiox-devops promotes the default by editing this SKILL.md and `.claude/skills/research-bench/SKILL.md` to swap `--enforcement warn` → `--enforcement block`. The flip date is recorded in the same Change Log.
- **Owner:** @aiox-devops drives the flip; @aiox-qa monitors `warnings[]` accumulation during the window.
- **Rollback (Regression Risk row 1 of the story):** if ≥10% of post-flip runs fail validation, revert to `warn` via the same Change Log mechanism and re-extend the window 30d.

### Quality Gates Enforced by Validator

- Original query + inferred context present
- Generated research prompt present (`01-deep-research-prompt.md`)
- Source list with URLs + titles + dates + credibility
- Coverage score + breakdown
- Binary rubrics (information recall / analysis / presentation)
- Confidence tags on findings
- Explicit gaps/caveats if coverage below excellent
- Citation verification completed before final report
- Recommendations contain no production code
- Stop reason explaining why research stopped
- Curiosity queue with status per item (schema: `items: [{question, status, owner?}]`)
- `quick-wins.md` with ≥3 selected entries OR `## Quick Wins Não Encontrados` block
- `execution-log.jsonl` present and valid JSONL (one JSON object per line)
- Extractor atoms attempted (warnings allowed; absence triggers `partial` render tier)

**TaskUpdate(M7, completed)** → **learning log: `p5_document.status = completed`**, list all artifact paths.

---

## Phase P5b: Finalize Learning Log + Suggest Next Command

**TaskUpdate(P5b, in_progress)** → **learning log: `p5b_finalize.status = in_progress`**

### Finalize Learning Log

```yaml
# Overwrite .aiox/learning/logs/tech-research/{slug}-{timestamp}.yaml
outcome: completed
timestamp_completed: "{ISO-8601 now}"
elapsed_minutes: {(Bash("date +%s") - start_epoch) / 60}

summary:
  coverage_gate_verdict: {APPROVE|REVIEW}
  citation_gate_verdict: {APPROVE|REVIEW}
  waves_executed: {1|2|3}
  multi_llm_triggered: {bool}
  quick_wins_count: {N}
  sources_consulted: {N}
  artifacts_written: [list of paths]
  output_dir: "{output_dir}"
```

### Suggest Next Command (RULE 10 — skip if --yolo)

Based on output content + flags:

| Condition | Suggestion |
|---|---|
| `--product-discovery` was set | "Próximo: `/research-chief` validate-product-idea para gerar GO/NO-GO sobre `{output_dir}`" |
| Architecture recommendation present | "Próximo: `/aiox-architect` para decisão arquitetural baseada em `{output_dir}/03-recommendations.md`" |
| Story implementation candidate | "Próximo: `/aiox-pm` para criar epic/story a partir de `{output_dir}/quick-wins.md`" |
| Citation Gate REVIEW (caveats present) | "Atenção: caveats não-resolvidos em `{output_dir}/02-research-report.md#caveats`. Revisar antes de decidir." |
| Coverage Gate REVIEW | "Cobertura intermediária. Considere `/tech-research \"{query}\" --deep` para multi-LLM cross-reference" |
| `--yolo` was passed | (skip suggestion silently) |

### Display Final Banner

```
╔══════════════════════════════════════════════════════════╗
║  /tech-research — COMPLETE                                ║
╠══════════════════════════════════════════════════════════╣
║  Output:     docs/research/{date}-{slug}/                 ║
║  Coverage:   {score}/100 ({APPROVE|REVIEW})               ║
║  Citations:  {ratio} ({APPROVE|REVIEW})                   ║
║  Quick Wins: {N} selected                                 ║
║  Sources:    {N} consulted                                ║
║  Elapsed:    {N} minutes                                  ║
║  Log:        {learning_log_path}                          ║
╠══════════════════════════════════════════════════════════╣
║  Próximo: {suggestion}                                    ║
╚══════════════════════════════════════════════════════════╝
```

**TaskUpdate(P5b, completed)** → **learning log: final write**. DONE.

---

## Halt Protocol (any VETO or unrecoverable error)

When triggered:
1. Set `learning_log.outcome = halted | failed | escalated`
2. Set `learning_log.timestamp_completed = now`
3. Append `learning_log.halt_reason = "{reason}"` (e.g. `coverage_veto`, `citation_veto`, `guardrail_redirect`, `partial_read_failure`, `user_abort`)
4. Persist the log immediately (full file overwrite)
5. `TaskUpdate(current_phase, completed)` with description=halted reason
6. Emit halt report to user:
   ```
   HALT: tech-research pipeline stopped at phase {phase_id}
   Reason: {reason}
   Partial artifacts: {list of files written so far}
   Learning log: {path}
   Remediation: {hint based on reason}
   ```

Halt does NOT skip the learning log. The log IS the provenance.

---

## Stream Timeout Recovery

When the runtime emits `Stream idle timeout` / `partial response received`, or the user types "continue" after >5 minutes of silence during Phase M4 (P3 wave loop):

1. Read `wave-{N}-progress.jsonl` from `{output_dir}/` (last written wave file)
2. Parse completed sub-query entries (`status == "completed"`)
3. Emit status line: `Resuming wave {N} at sub-query {M}/{total}` (where M = first uncompleted index)
4. Skip sub-queries that appear in the completed set
5. Execute remaining sub-queries from where interrupted
6. Continue normal wave completion → P3.5 (Evaluate Coverage)

**If `wave-{N}-progress.jsonl` is missing or unreadable:** restart the entire wave from sub-query 1 with a warning logged to `execution-log.jsonl`.

**Trigger conditions (any of):**

| Signal | Detection |
|---|---|
| `Stream idle timeout` | Runtime error message contains this string |
| `partial response received` | Runtime error message contains this string |
| User "continue" | User types "continue" / "continuar" / "prosseguir" after >5 min silence |
| Agent stalls mid-wave | No progress JSONL appended in >5 min while sub-queries remain |

The `atm_resume_from_checkpoint` atom in `squads/research/workflows/tech-research/phase-3-execute-research.yaml` implements this protocol.

---

## Context Discipline

- Load each phase YAML / prompt / template **fully** when its phase starts (RULE 8)
- Do not read every workflow file at startup — only on phase entry
- Emit marker after every operational file load: `LOADED: {relative/path} ({line_count} lines)`
- Keep raw source extractions out of long-term context after wave compression (P3.6)
- Preserve exact code snippets, version numbers, benchmark numbers, citations, publication dates
- Do not paraphrase source claims before citation verification (P4.5)

---

## Skill File Structure

> **Note (v2.1.0, 2026-05-16):** This skill was absorbed into `squads/research/` as part
> of the spy→research squad rename. The `/tech-research` slash entry point remains here
> (`.claude/skills/tech-research/SKILL.md`) as a stable alias; the implementation
> (workflows, scripts, templates, prompts, data, checklists) lives under
> `squads/research/{section}/tech-research/`.

```
.claude/skills/tech-research/
└── SKILL.md                          # slash entry (this file) — alias preserved

squads/research/
├── agents/
│   └── tech-research-agent.md        # canonical agent file (v2.1.0)
├── docs/
│   └── tech-research-README.md       # quick reference
├── checklists/tech-research/
│   └── guardrails.yaml               # vetoes, constraints, security, scope
├── data/tech-research/
│   ├── _skill-config.yaml            # SINKRA-native + operational config
│   ├── auto-clarification.yaml
│   ├── commands.yaml
│   └── dependencies.yaml
├── workflows/tech-research/
│   ├── tech-research-pipeline.yaml   # aggregate manifest (process_mapping target)
│   ├── phase-0-auto-clarify.yaml
│   ├── phase-1-clarify.yaml
│   ├── phase-1-5-decompose.yaml
│   ├── phase-2-generate-prompt.yaml
│   ├── phase-3-execute-research.yaml
│   ├── phase-3-2-deep-read.yaml
│   ├── phase-3-5-evaluate-coverage.yaml
│   ├── phase-3-6-compress-wave.yaml
│   ├── phase-3-7-playwright-deep-research.yaml
│   ├── phase-4-synthesize.yaml
│   ├── phase-4-5-verify-citations.yaml
│   └── phase-5-document.yaml
├── prompts/tech-research/
│   ├── decompose.md
│   ├── evaluate.md
│   ├── executor-matrix.md
│   ├── page-extract.md
│   ├── playwright-deep-research.md
│   ├── tech-discovery.md
│   ├── tool-strategy.md
│   └── verify-citations.md
├── scripts/tech-research/
│   ├── claim_extractor.py
│   ├── compare-run-artifacts.sh
│   ├── comparison_matrix_extractor.py
│   ├── coverage_calculator.py
│   ├── credibility_scorer.py
│   ├── logger.py
│   ├── metrics_collector.py
│   ├── next_followup_number.py
│   ├── output_validator.py
│   ├── players_extractor.py
│   ├── research_graph.py
│   ├── research_kb_index.py
│   ├── scaffold.py
│   ├── sources_extractor.py
│   ├── url_detector.py
│   └── ux_patterns_extractor.py
└── templates/tech-research/
    ├── deep-research-prompt-template.md
    ├── meta-prompt-template.yaml
    ├── output-structure.md
    └── output-structure.yaml
```

---

## Output Structure (final, under `docs/research/{date}-{slug}/`)

```
docs/research/{YYYY-MM-DD}-{slug}/
├── README.md                    # Índice + TL;DR + metadata (atom: research-readme)
├── 00-query-original.md         # Query + flags + inferred context (atom: original-query)
├── 01-deep-research-prompt.md   # Generated prompt (atom: research-prompt)
├── 02-research-report.md        # Full findings (atom: research-report)
├── 03-recommendations.md        # Recommendations, no code (atom: recommendations)
├── quick-wins.md                # ≥3 selected QW OR gap block (atom: quick-wins)
├── curiosity_queue.yaml         # Open questions (atom: curiosity-queue)
├── evolving_report.md           # Cumulative state per wave (atom: evolving-report)
├── wave-1-summary.md            # Per-wave checkpoint (atom: wave-summary, cardinality: many)
├── wave-2-summary.md            # (if executed)
├── wave-3-summary.md            # (if executed)
├── XX-llm-deep-research.md      # Multi-LLM dossier (atom: llm-deep-research, conditional)
├── metrics.yaml                 # coverage, gates, counts, elapsed
├── pipeline-state.yaml          # phase completion map
│
│   # Extractor atoms — apps/dash Research Observatory (rich render tier)
├── sources.yaml                 # Fontes com URL + credibility + flags (atom: sources)
├── players.yaml                 # Ferramentas/companies/people citados (atom: players)
├── ux-patterns.yaml             # Padrões UX reutilizáveis (atom: ux-patterns)
├── matrices.yaml                # Tabelas extraídas dos Markdown (atom: matrices)
├── execution-log.jsonl          # Timeline consolidada de eventos (atom: execution-log)
├── research-graph.json          # Grafo nós/links query→waves→sources→report (atom: research-graph)
│
└── 04-*.md, 05-*.md, ...        # Follow-up files (RULE 7)

.aiox/learning/logs/tech-research/{slug}-{timestamp}.yaml   # incremental log (RULE 3)
```

**Observatory tab → atom dependency** (from `apps/dash/HANDOFF-research-compatibility.md`):

| Aba | Atoms consumidos |
|---|---|
| `Doc` | `README.md`, `02-research-report.md`, `03-recommendations.md` |
| `Map` | `metrics.yaml`, `pipeline-state.yaml`, `matrices.yaml`, `ux-patterns.yaml`, `curiosity_queue.yaml`, `research-graph.json` |
| `Evidências` | `sources.yaml`, `research-graph.json`, `metrics.yaml` |
| `Waves` | `execution-log.jsonl`, `wave-*-summary.md` |
| `Fontes` | `sources.yaml` |
| `Players` | `players.yaml` |
| `Ações` | `03-recommendations.md`, `quick-wins.md`, `curiosity_queue.yaml` |
| `Perguntas` | `curiosity_queue.yaml` |

---
