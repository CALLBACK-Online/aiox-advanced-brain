# Task: Validate Skill Prompt Quality

## Purpose

Validate a skill's prompt content against Claude Opus 4.7 prompt-engineering principles. Complements `validate-skill.md` (schema-only) with cognitive quality checks: description routing quality, severity calibration, anti-laziness density, and canonical pattern adoption.

Advisory mode by default — reports metrics without blocking. Blocking mode is available once the ecosystem has been swept at least once.

## Inputs

- `skill_path` (required) — path to the skill directory, e.g. `.claude/skills/tech-search/`
- `mode` (optional, default `advisory`) — `advisory` | `blocking`
- `threshold` (optional, default 80) — minimum total score to pass in blocking mode

## Executor

skill-validator

## Steps

1. Verify `skill_path` exists and contains SKILL.md.
2. Invoke the `/prompt-47-migrator --scan <skill_path>` slash skill (read-only) and capture the per-pattern hit counts.
3. Run the four sub-checks below. Each produces a score (0-100) and a findings list.
4. Compute the weighted total: `0.30 * PQ01 + 0.25 * PQ02 + 0.25 * PQ03 + 0.20 * PQ04`.
5. Write the report using `templates/validation-report-tmpl.yaml` with a `prompt_quality` section.
6. Emit verdict: `PASS` (>= threshold), `CONCERNS` (threshold - 10 <= score < threshold), `FAIL` (< threshold - 10).

## Sub-checks

### PQ-01 — Description routing quality (weight 30)

Parse the `description` field from SKILL.md frontmatter. Score against this rubric:

- Has `Use when...` or `TRIGGER when...` clause → +20
- Has `SKIP when...` or `NOT FOR...` clause (optional for narrow skills) → +10
- Names >= 5 concrete trigger nouns, verbs, or domain objects → +30
- Length calibrated to tier (Tier 1: >= 50 chars; Tier 2: >= 100; Tier 3: >= 150) → +20
- No filler phrases ("stuff", "things", "helps with <nothing specific>") → +20

Reference: `data/anthropic-patterns.yaml#description-routing-format`.

### PQ-02 — Severity calibration (weight 25)

Scan the SKILL.md body for severity language: `CRITICAL:`, `NEVER`, `ALWAYS`, `MUST NOT`, `SEVERE`, `NON-NEGOTIABLE`.

For each hit, apply the four-criterion test:

1. Specific concrete action / path / tool / format?
2. Binary — violation clearly defined?
3. High-frequency — applies across many interactions?
4. Real stakes OR output-breaking if violated?

A hit is legitimate when all four criteria are met. A hit is illegitimate when applied to an attitudinal disposition ("ALWAYS be thorough") or to a gradient ("NEVER be verbose").

Score formula: `100 * legitimate_count / max(1, total_count)`. Zero hits → score 100 (neutral).

Findings list every illegitimate hit with the missing criterion.

Reference: `data/anthropic-patterns.yaml#severity-for-workflow-preference` and `#severity-for-real-stakes`.

### PQ-03 — Scaffolding density (weight 25)

Scan for internalized-behavior scaffolding that 4.7 no longer needs. Each match subtracts 5 points from 100 (floor 0):

- Anti-laziness: `be thorough`, `be proactive`, `go above and beyond`, `default to using`, `if in doubt`, `ultrathink`, `think hard`, `be comprehensive`
- Search-first: `if unsure search`, `search when.*don't know`
- Apologetic humility: `be humble`, `acknowledge mistakes`, `don't apologize excessively`
- Conciseness directives: `be concise`, `be brief`, `keep it short`
- Progress forcing: `after every N tool calls`, `provide status update`, `interim summary`
- Clarification-first: `ask for clarification before`, `if unclear, ask`

Reference: `data/anthropic-patterns.yaml#internalized-no-scaffolding` (implicit — patterns deliberately absent from Anthropic's 4.7 system prompt).

### PQ-04 — Canonical pattern adoption (weight 20)

Check whether the skill uses canonical 4.7 patterns where applicable. Each applicable sub-item scores 0-100:

- Decision logic with > 3 conditions? → should use `decision-tree-stop-at-first-match` (100) or `arrow-notation-decision-flow` (100). Prose conditionals score 50. Ambiguous logic scores 0.
- Example blocks present? → should use `triplet-user-response-rationale` (100). User+Response without rationale scores 50. Bare examples score 0.
- Tool list with > 3 tools? → should use `priority-numbered-tool-list` (100) or `cost-framing` (100). Unordered list scores 50. No guidance scores 0.
- Multi-section agent/skill? → should use `section-tagged-structure` (100). Markdown headers only score 50.

Score: weighted average across applicable sub-items. Items that do not apply are skipped (not scored zero).

## Veto conditions

- `skill_path` does not exist → ABORT
- SKILL.md missing → ABORT (defer to `validate-skill.md` for this case)
- `/prompt-47-migrator` slash skill not discoverable → ABORT with actionable error

## Output

Extend `templates/validation-report-tmpl.yaml` with a `prompt_quality` section:

```yaml
prompt_quality:
  total_score: 0-100
  verdict: PASS | CONCERNS | FAIL
  mode: advisory | blocking
  threshold_used: 80
  sub_scores:
    PQ_01_description_routing: 0-100
    PQ_02_severity_calibration: 0-100
    PQ_03_scaffolding_density: 0-100
    PQ_04_canonical_patterns: 0-100
  weighted_formula: "0.30 * PQ01 + 0.25 * PQ02 + 0.25 * PQ03 + 0.20 * PQ04"
  findings:
    - check: PQ-01 | PQ-02 | PQ-03 | PQ-04
      severity: blocker | concern | info
      location: "SKILL.md:line or frontmatter field"
      issue: "..."
      suggested_action: "..."
      pattern_ref: "anthropic-patterns.yaml#<pattern-id>"
```

## Example output

```
🔍 Prompt Quality — skill-ops-chief (mode: advisory)

  PQ-01 Description routing:      85 / 100
  PQ-02 Severity calibration:    100 / 100  (zero severity hits)
  PQ-03 Scaffolding density:      95 / 100  (1 hit: "be thorough" on SKILL.md:47)
  PQ-04 Canonical patterns:       70 / 100  (heuristics list, not decision tree)

  Weighted total: 87.0 / 100 → PASS (advisory)

  Recommended actions:
  - PQ-03: remove "be thorough" on line 47 (internalized in 4.7 base behavior)
  - PQ-04: convert HEURISTICS list to decision tree with stop-at-first-match
           (see anthropic-patterns.yaml#decision-tree-stop-at-first-match)
```

## Integration

- Invoked by `workflows/skill-lifecycle.yaml` in phase `prompt-quality` (between `validate` and `test`).
- Also runs as a recurring audit (monthly) over `.claude/skills/` to detect drift.
- Results feed `outputs/skill-creator-ops/prompt-quality-dashboard.md` for visibility.

## Completion criteria

- All four sub-checks executed
- Weighted score computed and recorded
- At least one actionable finding per sub-check scoring below 80
- Report written, verdict emitted, slash-skill output saved
