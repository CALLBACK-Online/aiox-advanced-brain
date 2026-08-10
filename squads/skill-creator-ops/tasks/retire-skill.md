# Task: Retire Skill

## Purpose

Govern the lifecycle exit of a skill — transition from `active` through `deprecated` to `retired`. Without this task, skills accumulate in `.claude/skills/` and in the registry indefinitely, creating ghost entries with zero invocations and stale content.

## Lifecycle states

```
active → deprecated → retired
```

- **active** — skill is fully available and recommended.
- **deprecated** — skill remains invocable but carries a warning. Router deprioritizes it. Not recommended for new use. Must have a migration target declared.
- **retired** — skill is removed from the registry and from `.claude/skills/`. Its directory is archived under `outputs/skill-creator-ops/retired/<skill-name>/<timestamp>/` for audit.

Transitions are non-reversible in normal flow. Un-retiring a skill requires re-initialization via `init-skill.md` as a fresh artifact.

## Inputs

- `skill_name` (required) — name of the skill to act on
- `action` (required) — `deprecate` | `retire` | `revert-deprecation`
- `migration_target` (required for `deprecate`) — skill name or path that consumers should move to
- `migration_story_ref` (required for `retire`) — story ID in `docs/stories/` explaining why retirement is happening
- `force` (optional, default false) — bypass usage check (requires @architect sign-off in rationale)

## Executor

skill-ops-chief

## Steps

### A. Action = `deprecate`

1. Locate skill directory. Verify `status: active` in frontmatter or registry.
2. Update skill's frontmatter: set `status: deprecated`, add `deprecated_at: <ISO-8601>`, `migration_target: <target>`.
3. Update `.claude/skills/skill-registry.yaml`: mark skill as deprecated, add the migration_target.
4. Edit the skill's `description` to prepend: `[DEPRECATED — use <migration_target>]`.
5. Log entry in `outputs/skill-creator-ops/lifecycle-log.yaml` with timestamp, action, rationale.

### B. Action = `retire`

1. Verify skill is currently `status: deprecated`. If `active`, abort with message `Must deprecate before retiring`.
2. Run usage audit — call `cc-session-analyze` to count invocations of this skill over the last 90 days.
   - If invocation count > 0 AND `force` is not true → abort with the invocation list.
   - If `force: true` → proceed, require `forced_by` and `forced_rationale` fields in the lifecycle log.
3. Verify `migration_story_ref` points to a valid story in `docs/stories/`.
4. Archive the skill directory to `outputs/skill-creator-ops/retired/<skill-name>/<timestamp>/`.
5. Remove the skill directory from `.claude/skills/`.
6. Remove entry from `.claude/skills/skill-registry.yaml`. Add it to the `retired` section of the registry with: `retired_at`, `migration_target`, `migration_story_ref`, `archive_path`.
7. Log entry in `outputs/skill-creator-ops/lifecycle-log.yaml`.

### C. Action = `revert-deprecation`

Only for emergencies where deprecation was in error (e.g. migration_target turned out to be worse).

1. Verify skill is `status: deprecated`. If `retired`, abort (cannot revive).
2. Require `revert_rationale` field. Must reference a decision record or ADR.
3. Update frontmatter: `status: active`, remove `deprecated_at` and `migration_target`, restore `description` (remove the `[DEPRECATED]` prefix).
4. Update registry accordingly.
5. Log entry in `outputs/skill-creator-ops/lifecycle-log.yaml`.

## Veto conditions

- Skill in `approved` state with no migration_target → ABORT (deprecate requires target)
- `retire` on an `active` skill → ABORT (must go through `deprecated` first)
- `retire` with invocations > 0 and no `force: true` → ABORT
- `retire` without `migration_story_ref` → ABORT
- `revert-deprecation` on a `retired` skill → ABORT (no Lazarus recovery)

## Outputs

- Updated frontmatter on the skill file
- Updated `.claude/skills/skill-registry.yaml`
- Archive under `outputs/skill-creator-ops/retired/` (for retirement only)
- Lifecycle log entry

## Integration

- Invoked by skill-ops-chief command `*deprecate <skill>` or `*retire <skill>`
- Runs pre-check against `cc-session-analyze` output to find zero-invocation skills as candidates
- Feeds the monthly `skill-lifecycle-audit.md` report

## Canonical hit-list for deprecation

Skills that match any of these deserve a deprecation candidate evaluation (not automatic, but flagged):

- Zero invocations in last 90 days
- Version string older than 90 days AND zero updates in `git log`
- Description contains `Migrated legacy slash command` without a refactor since
- Frontmatter missing required fields that have become required after the skill was created
- Overlap > 80% with another skill (based on description similarity)

## Completion criteria

- Action executed
- Registry updated
- Lifecycle log updated
- Archive created (for retirement)
- Consumer audit completed (for retirement)
