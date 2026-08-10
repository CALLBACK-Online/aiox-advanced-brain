# CC Format Specification — Squad Protocol v2.0 (EPIC-109 Wave 4)

> Source: Squad Protocol v2.0.0 by @gutomec (adopted as-is, SINKRA extensions are additive).
> Evidence: Squad Format Analysis (squads.sh, April 2026) — 418 real agents, ~18% token waste.
> Story: STORY-109.4 | Epic: EPIC-109

---

## Design Principle

```
Frontmatter = what the HARNESS needs (routing, config, runtime)
Body .md    = what the AGENT needs (instructions, persona, heuristics, commands)
config.yaml = what the ECOSYSTEM needs (metadata, composition, UI, marketplace)
```

The LLM never sees frontmatter. The harness never parses the body as config.
Total separation of concerns.

---

## Agent Format

### Frontmatter Fields

**Required:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent identifier (kebab-case) |
| `description` | string | 1-2 sentences — when to use this agent |

**Optional:**

| Field | Type | Description |
|-------|------|-------------|
| `model` | string | Model override (e.g., `claude-sonnet-4`). NEVER `gemini-flash`. |
| `tools` | array | Tool whitelist. Omit = all tools. |
| `effort` | string | `high` for decision agents (chiefs, architects, QA) |
| `maxTurns` | integer | Max turns for forked agents |
| `permissionMode` | string | Permission mode override |
| `skills` | array | Skills pre-loaded |
| `memory` | boolean | Enable persistent memory |
| `isolation` | string | `none` (inline) or other values — **NEVER** `worktree` (causes 500 errors) |
| `mcpServers` | array | MCP server config |

### Body Sections (Markdown)

```markdown
# {Name} — {Title}

{1-2 sentence identity statement. Who you are, what you do, your primary style.}

## Scope

{What this agent is responsible for. Use bullet list for clarity.}

## Heuristics

{Decision rules the agent applies. Bullet list. These are the core intelligence.}

## Vocabulary (if Expert agent)

Use: {term1}, {term2}, {term3}.
Never say: {avoid1}, {avoid2}.
Tone: {tone description}.

## Commands

- `*command-name` — Brief description of what it does
- `*another-command` — Brief description

## Collaboration

{Who this agent hands off to, and when. Brief prose.}

## Anti-Patterns

{What this agent must NEVER do. Bullet list.}
```

### Token Budget

| Agent Type | Max Body Tokens | Rationale |
|-----------|----------------|-----------|
| Orchestrators (chiefs) | 3000 | Need context for routing decisions |
| Pipeline agents | 4000 | Need detailed execution instructions |
| Hard ceiling | 5000 | Beyond this, use external task files |

---

## Task Format

### Frontmatter Fields

**Required:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Task identifier (kebab-case) |
| `description` | string | 1 sentence — what this task does |

**Optional:**

| Field | Type | Description |
|-------|------|-------------|
| `allowed-tools` | string | Space-separated tool list |
| `context` | string | `fork` for isolated sub-agent, omit for inline |

**Removed from tasks (SINKRA AD-3):**

`owner` / `responsavel` fields are removed from tasks. The workflow decides who
executes each task via `steps[].agent`. This enforces Task-First Architecture (P6).

### Body Sections (Markdown)

```markdown
# {Task Name}

{Brief description of what this task accomplishes and why.}

## Input

- `{field_name}` ({type}, required|optional) — Description of what this field contains

## Steps

1. {Concrete action step}
2. {Concrete action step}
3. {Apply pattern/heuristic if relevant}

## Output

- `{field_name}` ({type}, {destination}) — What this output contains

## Acceptance Criteria

- {Measurable criterion 1}
- {Measurable criterion 2}

## Error Handling (optional)

- {Error type}: {Recovery action}
```

### I/O Contract Convention

Fields use the format `- name (type, required) — description` which is both
human-readable and parseable by the validator.

---

## Field Classification Tables

### Agent: Field-by-Field Migration

| Old Field (YAML frontmatter) | New Location | Notes |
|------------------------------|-------------|-------|
| `agent.name` | `frontmatter.name` | Direct mapping |
| `agent.id` | `frontmatter.name` | Same as name |
| `agent.whenToUse` | `frontmatter.description` | Rephrased |
| `agent.model` | `frontmatter.model` | Direct mapping |
| `agent.tools` | `frontmatter.tools` | Direct mapping |
| `agent.icon` | `config.yaml agents_metadata[].icon` | Ecosystem metadata |
| `agent.version` | `config.yaml agents_metadata[].version` | Ecosystem metadata |
| `agent.phase` | `config.yaml agents_metadata[].phase` | Ecosystem metadata |
| `agent.tier` | `config.yaml agents_metadata[].tier` | Ecosystem metadata |
| `persona.role` | `body — # Title + opening sentence` | Prose form |
| `persona.style` | `body — opening sentence/paragraph` | Prose form |
| `persona.focus` | `body — ## Scope` | Prose form |
| `persona.core_principles` | `body — ## Heuristics` | Bullet list |
| `voice_dna.*` | `body — ## Vocabulary + prose` | Natural language |
| `commands[]` | `body — ## Commands` | Bullet list with backtick names |
| `collaboration.hands_off_to` | `body — ## Collaboration` | Prose form |
| `persona_profile.archetype` | `config.yaml marketplace.archetype` | Ecosystem metadata |
| `greeting_levels` | `config.yaml marketplace.greeting_levels` | Ecosystem metadata |

### Task: Field-by-Field Migration

| Old Field (YAML frontmatter) | New Location | Notes |
|------------------------------|-------------|-------|
| `task` (function name) | `frontmatter.name` | kebab-case |
| `owner` / `responsavel` | `workflow steps[].agent` | Removed from tasks (AD-3) |
| `atomic_layer` | `config.yaml sinkra_extensions.composition_mapping` | SINKRA metadata |
| `Entrada[].campo` | `body ## Input - campo (tipo, req)` | Markdown prose |
| `Saida[].campo` | `body ## Output - campo (tipo, dest)` | Markdown prose |

---

## SINKRA Extensions (Additive — AD-2)

SINKRA composition metadata does NOT go in agent/task frontmatter or body.
It belongs in `config.yaml` under `sinkra_extensions`:

```yaml
sinkra_extensions:
  composition_mapping:
    tasks:
      - id: task-name
        atomic_layer: Atom   # Atom | Molecule | Organism
        domain: Operational  # Strategic | Tactical | Operational
        sinkra_primitive: atom
```

---

## Dual-Format Transition Period (AD-6)

| Period | Behavior |
|--------|---------|
| 0–180 days | WARNING for legacy format (not ERROR). Coexistence allowed. |
| 180+ days | ERROR for legacy format. Migration required. |

The validator (`validate-squad.sh`) auto-detects format:
- CC format: flat frontmatter with `name:` and `description:` at top level
- Legacy format: nested `agent:` key in frontmatter

---

## Compatibility

| Runtime | Status |
|---------|--------|
| Claude Code | Native (frontmatter parsed, body = system prompt) |
| Codex CLI | Compatible |
| Cursor | Compatible |
| Windsurf | Compatible |

Source: `loadAgentsDir.ts` line 713 — `const systemPrompt = content.trim()`

---

## Proof of Concept

PoC squad: **etl-ops** (chosen for moderate size: 8 tasks, 2 workflows, 3 agents).
Migration uses `scripts/migrate-to-cc-format.js --squad squads/etl-ops`.

---

*CC Format Specification v1.0*
*EPIC-109 Wave 4 — Protocolo Universal*
*Squad Protocol v2.0.0 adopted as-is, SINKRA extensions additive*
*Last Updated: 2026-04-13*
