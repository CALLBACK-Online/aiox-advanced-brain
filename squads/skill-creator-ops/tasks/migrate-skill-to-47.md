# Task: Migrate Skill to 4.7

## Purpose

Orchestrate the migration of an existing skill's prompt content to Claude Opus 4.7 conventions. This task is a thin wrapper around the `/prompt-47-migrator` slash skill, adapted for skill-creator-ops lifecycle.

This task does NOT modify the source file without explicit operator approval. It honors the preview-first contract inherited from `/prompt-47-migrator`.

## Inputs

- `skill_path` (required) — path to the skill directory, e.g. `.claude/skills/tech-search/`
- `mode` (optional, default `preview`) — `preview` | `apply` | `scan-only`
- `apply_scope` (optional, default `SKILL.md`) — `SKILL.md` | `full-skill` (whole directory, recursive)

## Executor

skill-ops-chief

## Steps

### 1. Pre-flight

- Verify `skill_path` exists and contains SKILL.md.
- Verify the skill has a `version` field in frontmatter.
- Read `data/anthropic-patterns.yaml` and hold it as the target reference.
- Record baseline metrics: line count, aggressive-language hit count, scaffolding hit count.

### 2. Invoke prompt-47-migrator

- Call `/prompt-47-migrator <skill_path>/SKILL.md` (or each prompt file if `apply_scope=full-skill`).
- The migrator runs in preview mode by default and produces four deliverables in `outputs/prompt-47-migrator/<timestamp>/`:
  - `<filename>.migrated.md`
  - `<filename>.diff.patch`
  - `<filename>.rationale.yaml`
  - `<filename>.summary.md`

### 3. Cross-check against anthropic-patterns.yaml

For each change the migrator proposes, verify the new content aligns with the canonical shape in `data/anthropic-patterns.yaml`:

- Decision-tree changes → match `decision-tree-stop-at-first-match` shape
- Severity-language changes → pass four-criterion test
- Removed scaffolding → map to an `internalized-no-scaffolding` absence
- New example blocks → use `triplet-user-response-rationale`

Flag any change that deviates from the canonical shape as `human-review-required` in the rationale file.

### 4. Present for approval

Present the migration summary to the operator with:

- Baseline → after line count
- Pattern hit counts before and after
- Severity-calibration outcomes (legitimate hits preserved; attitudinal hits removed)
- Human-review flags (low-confidence changes)
- Full diff

Ask explicitly: **"Apply these changes to `<skill_path>/SKILL.md`? (yes / no / modify)"**

### 5. Apply (only on explicit approval)

If operator replies `yes`:

- Move the candidate migrated file over SKILL.md.
- Bump `version` in the skill's frontmatter (patch-level bump for content migration).
- Add a changelog entry: `v<new> — migrated to 4.7 conventions via skill-creator-ops:migrate-skill-to-47 (<date>)`.
- Run `skill-validator` on the migrated skill to confirm schema still passes.
- Run `validate-skill-prompt-quality` to confirm score improved.
- Archive the preview artifacts to `outputs/skill-creator-ops/migrations/<skill-name>/<timestamp>/`.

If operator replies `no`: stop. Preview artifacts remain in scratch for record.

If operator replies `modify <instruction>`: re-run step 2 with the adjusted scope.

## Batch mode

When invoked by skill-ops-chief for multiple skills, respect these guards:

- Process skills serially, not in parallel (human review gate per skill).
- Stop after N skills (configurable, default 5) for consolidated PR review before continuing.
- Maintain a session-level manifest at `outputs/skill-creator-ops/migrations/<session-timestamp>/manifest.yaml` listing each skill, verdict, and actions taken.

## Veto conditions

- `skill_path` does not exist → ABORT
- SKILL.md missing → ABORT
- Skill is in `deprecated` or `retired` lifecycle state → ABORT (do not migrate what is about to be removed)
- `/prompt-47-migrator` slash skill not available → ABORT with actionable error (`ide-sync sync`)

## Output

- Four preview deliverables from `/prompt-47-migrator`
- If applied: updated SKILL.md, bumped version, changelog entry, validation report, archived migration artifacts
- Session manifest (batch mode only)

## Completion criteria

- Preview generated for every skill in scope
- Human approval gate presented (unless `scan-only` mode)
- On approval: apply + re-validate + bump version + archive
- On rejection: stop cleanly, preserve artifacts

## Integration

- Invoked by skill-ops-chief command `*migrate-skill <skill-name>` or `*migrate-batch <scope>`
- Results feed skill registry metadata (`last_migrated_at`, `migration_version`)
- Chains with `validate-skill.md` and `validate-skill-prompt-quality.md` for post-migration verification

## Safety

- NEVER mutates the source file before operator approval
- NEVER runs in batch mode without pre-authorized `--yes` at session level
- NEVER migrates skills in `approved` state without a parallel changelog entry
