# Agent Naming Convention

## Rule: Chief Pattern

Every squad MUST have exactly ONE chief agent. The chief follows the pattern:

```
{squad-short-name}-chief.md
```

Examples:
- `squads/copy/agents/copy-chief.md`
- `squads/design-system/agents/design-chief.md`
- `squads/aiox-sop/agents/sop-chief.md`
- `squads/squad-creator/agents/squad-chief.md`

## Rule: Reserved Word "chief"

The word "chief" is RESERVED for squad orchestrators only. Sub-agents MUST NOT use "chief" in their name.

| Role | Allowed | Forbidden |
|---|---|---|
| Squad orchestrator | `{squad}-chief` | `{squad}-orchestrator`, `{squad}-lead` |
| Sub-agent specialist | `{role}-strategist`, `{role}-architect`, `{role}-engineer`, `{role}-analyst` | `{role}-chief` |

## Rule: Consistency for Sync

Agent file names MUST match across:
- `squads/{squad}/agents/{name}.md` (source of truth)
- `.claude/agents/{name}.md` (Claude Code native)
- `skills/{squad}/{name}/SKILL.md` (slash skills)
- `skills/{skill}/SKILL.md` (Codex + Grok; `skills` é symlink)

When renaming an agent, ALL locations must be updated in the same commit.

## Rule: IDE Mirror Naming

IDE mirror directories use PascalCase without the `aiox-` prefix:

| Squad slug | Mirror dir name |
|---|---|
| `aiox-copy` | `Copy` |
| `aiox-design` | `Design` |
| `aiox-sop` | `Sop` |
| `squad-creator` | `SquadCreator` |
| `squad-creator-pro` | `SquadCreatorPro` |
