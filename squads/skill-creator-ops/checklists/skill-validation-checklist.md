# Skill Validation Checklist

Two layers: schema checks (blocking) and prompt-quality checks (advisory by default, blocking once swept).

Reference: `data/validation-schema.yaml` for full field definitions and `data/anthropic-patterns.yaml` for canonical prompt patterns.

## Schema checks (12 — blocking)

### Frontmatter (6 checks)

- [ ] `name` present and kebab-case (lowercase, digits, hyphens only)
- [ ] `description` present, informative (>= 10 chars), no angle brackets
- [ ] `version` present and valid semver (X.Y.Z)
- [ ] `agent` present, defaults to `general-purpose`
- [ ] `user-invocable` present, boolean
- [ ] If `status` present, valid enum: `active | aiox-core-only | vendored | deprecated | retired`
  - If `status=deprecated`: `deprecated_at` and `migration_target` required
  - If `status=retired`: `retired_at` and `migration_story_ref` required

Notes on frontmatter purity: `owner_squad`, `sinkra_tier`, `context` are NOT required in the skill's own SKILL.md frontmatter — those fields live at the task/squad level per the Frontmatter Purity Rule. Treat their presence as informational, never as required schema.

### Structure (4 checks)

- [ ] SKILL.md exists in skill directory
- [ ] Directory name matches `name` field in frontmatter
- [ ] Tier-appropriate structure present:
  - Tier 1: SKILL.md only
  - Tier 2: SKILL.md + config.yaml
  - Tier 3: SKILL.md + config.yaml + templates/ + checklists/ + data/
- [ ] No forbidden files (.env, credentials, secrets, .DS_Store, node_modules, __pycache__)

### Registry (2 checks)

- [ ] Skill registered in `.claude/skills/skill-registry.yaml`
- [ ] Version in SKILL.md matches version in registry

## Prompt-quality checks (4 — advisory, weighted)

Executed by `tasks/validate-skill-prompt-quality.md`. Score formula: `0.30 * CHK13 + 0.25 * CHK14 + 0.25 * CHK15 + 0.20 * CHK16`.

### CHK-13 — Description routing quality (weight 30)

- [ ] Has `Use when...` or `TRIGGER when...` clause
- [ ] Has `SKIP when...` or `NOT FOR...` clause (optional for narrow skills)
- [ ] Names >= 5 concrete trigger nouns, verbs, or domain objects
- [ ] Length calibrated: Tier 1 >= 50 chars, Tier 2 >= 100, Tier 3 >= 150
- [ ] No filler (`stuff`, `things`, `helps with <nothing specific>`)

Reference: `data/anthropic-patterns.yaml#description-routing-format`.

### CHK-14 — Severity calibration (weight 25)

For every `NEVER`, `ALWAYS`, `CRITICAL`, `MUST NOT`, `SEVERE`, `NON-NEGOTIABLE` in the prompt, apply the four-criterion test:

- [ ] Specific concrete action / path / tool / format
- [ ] Binary — violation clearly defined
- [ ] High-frequency — applies across many interactions
- [ ] Real stakes OR output-breaking if violated

Legitimate hit = all four. Illegitimate hit = attitudinal or gradient. Score: `100 * legitimate / total`.

Reference: `data/anthropic-patterns.yaml#severity-for-workflow-preference` and `#severity-for-real-stakes`.

### CHK-15 — Scaffolding density (weight 25)

Scan for internalized-behavior scaffolding (4.7 no longer needs these). Each hit subtracts 5 from 100 (floor 0):

- [ ] Anti-laziness: `be thorough`, `be proactive`, `go above and beyond`, `default to using`, `if in doubt`, `ultrathink`, `think hard`, `be comprehensive`
- [ ] Search-first: `if unsure search`, `search when.*don't know`
- [ ] Apologetic humility: `be humble`, `acknowledge mistakes`, `don't apologize excessively`
- [ ] Conciseness: `be concise`, `be brief`, `keep it short`
- [ ] Progress forcing: `after every N tool calls`, `provide status update`, `interim summary`
- [ ] Clarification-first: `ask for clarification before`, `if unclear, ask`
- [ ] Blanket thinking-forcing: `think step by step` as blanket instruction

### CHK-16 — Canonical pattern adoption (weight 20)

Where applicable, use the canonical 4.7 shapes:

- [ ] Decision logic with > 3 conditions uses `decision-tree-stop-at-first-match` or `arrow-notation-decision-flow`
- [ ] Example blocks use `triplet-user-response-rationale`
- [ ] Tool list with > 3 tools uses `priority-numbered-tool-list` or `cost-framing`
- [ ] Multi-section agent/skill uses `section-tagged-structure`

Reference: all pattern IDs in `data/anthropic-patterns.yaml`.

## Scoring

### Schema layer

| Score | Verdict |
|-------|---------|
| >= 90% | PASS |
| 80-89% | CONCERNS (fixable) |
| < 80% | FAIL |

### Prompt-quality layer (weighted)

| Score | Verdict |
|-------|---------|
| >= 80 | PASS |
| 70-79 | CONCERNS |
| < 70 | FAIL (blocking mode only — advisory by default) |

## Verdict combination

- Schema FAIL → overall FAIL (blocking).
- Schema PASS + Prompt-quality FAIL → overall CONCERNS (advisory) OR FAIL (blocking mode).
- Schema PASS + Prompt-quality PASS → overall PASS.
- Schema PASS/CONCERNS + Prompt-quality PASS → overall PASS WITH CONCERNS.
