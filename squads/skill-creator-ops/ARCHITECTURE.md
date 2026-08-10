# Skill-Creator-Ops Squad — Architecture

## Overview

O squad `skill-creator-ops` orquestra o lifecycle completo de Claude Code skills: init → develop → validate → test → package → register. Vinculado à skill `/skill-creator` como superfície de ativação, mas o squad é a infraestrutura operacional.

## Agent Hierarchy

```
skill-ops-chief (Orchestrator)
│
├── skill-validator     # Programmatic validation vs schemas & standards
└── skill-tester        # Golden inputs/outputs testing
```

Single-tier, enxuto: cada agente tem responsabilidade atômica no pipeline.

## Skill Lifecycle Pipeline

```
MAIN PIPELINE
═════════════

[1] INIT
  skill-ops-chief scaffolds directory structure
  └── Templates from skill-creator.init_skill.py
      ├── SKILL.md with frontmatter template
      ├── scripts/ (Tier 3)
      ├── references/ (Tier 2+)
      └── assets/ (Tier 2+)

[2] DEVELOP
  User / agent authors content
  └── Following Tier rules (Tier 1 / 2 / 3)
  └── Reference: data/anthropic-patterns.yaml for canonical shapes

[3] VALIDATE (schema, blocking)
  skill-validator runs programmatic checks (CHK-01-12)
  ├── Frontmatter (6 checks)
  ├── Structure (4 checks)
  └── Registry (2 checks)

[4] PROMPT_QUALITY (4.7 calibration, advisory by default)
  skill-validator runs cognitive checks (CHK-13-16)
  ├── CHK-13 Description routing quality (weight 30)
  ├── CHK-14 Severity calibration (weight 25)
  ├── CHK-15 Scaffolding density (weight 25)
  └── CHK-16 Canonical pattern adoption (weight 20)
  └── Weighted total: 0.30*CHK13 + 0.25*CHK14 + 0.25*CHK15 + 0.20*CHK16

[5] TEST
  skill-tester runs golden inputs / outputs
  ├── Sandbox isolated execution
  ├── Compare actual vs expected
  └── Edge case coverage

[6] PACKAGE
  skill-ops-chief packages for distribution
  └── Version bump (semver per change type)

[7] REGISTER
  Update .claude/skills/skill-registry.yaml
  └── total_skills count + last_updated
```

## Auxiliary Flows

```
MIGRATION FLOW (on demand)
══════════════════════════

[M1] migrate-skill-to-47
  skill-ops-chief invokes tasks/migrate-skill-to-47.md
  └── Wraps /prompt-47-migrator with approval gate
  └── NEVER mutates source without explicit "yes"
  └── Produces 4 preview artifacts in outputs/
  └── Cross-checks against data/anthropic-patterns.yaml
  └── On approval: apply + bump version + changelog + re-validate


LIFECYCLE FLOW (on demand)
══════════════════════════

[L1] deprecate
  Transition: active → deprecated
  Requires: migration_target
  Effect: router deprioritizes, description prefixed with [DEPRECATED]

[L2] retire
  Transition: deprecated → retired
  Requires: migration_story_ref + zero-invocation audit (or force+signoff)
  Effect: skill archived to outputs/skill-creator-ops/retired/, removed from registry

[L3] revert-deprecation (emergency only)
  Transition: deprecated → active
  Requires: revert_rationale with ADR reference


AUDIT FLOW (scheduled monthly)
══════════════════════════════

[A1] lifecycle-audit
  Surfaces candidates:
  ├── Zero invocations in last 90d → deprecation candidate
  ├── Stale version 90d+ → review candidate
  ├── Overlap > 80% with another skill → consolidation candidate
  └── Deprecated with zero invocations since → retirement candidate
  └── Consumes cc-session-analyze output
```

## SINKRA Tier Definitions

| Tier | Requirements | Example |
|------|--------------|---------|
| **Tier 1** (Basic) | SKILL.md + frontmatter | `tech-search`, `coderabbit-review` |
| **Tier 2** (Standard) | Tier 1 + config.yaml + process_id + SINKRA mode | `service-*` skills |
| **Tier 3** (Full) | Tier 2 + templates/ + checklists/ + data/ + artifact_contracts | `handoff`, `roundtable`, `wave-execute` |

## Required Frontmatter Schema

```yaml
---
name: skill-name
description: "Clear, concise — used by Claude for matching"
version: "1.0.0"
owner_squad: squad-name
sinkra_tier: Tier1|Tier2|Tier3
context: inline|fork|conversation
agent: general-purpose|specific
user-invocable: true|false
---
```

## Context Selection Rules (NON-NEGOTIABLE)

| Skill Type | Context | Example |
|-----------|---------|---------|
| SDC skills (story lifecycle) | `inline` | develop-story, review-story |
| Operational skills (deploy, verify) | `fork` | deploy-story, verify-deploy |
| Agent Teams skills | `conversation` | roundtable, wave-execute |

## Scripts (Extended from /skill-creator)

```yaml
- quick-validate      # Extended for optional fields check
- init-skill          # Extended with full frontmatter template
- package-skill       # Used as-is from /skill-creator
```

## Registry Governance

| File | Purpose |
|------|---------|
| `.claude/skills/skill-registry.yaml` | Canonical catalog (source of truth) |
| `.claude/skills/{name}/SKILL.md` | Entry point per skill |
| `squads/infra-ops-squad/data/service-catalog.yaml` | Service-level tracking |

## Integration Points

| Connected to | How |
|--------------|-----|
| `/skill-creator` skill | Operational owner relationship |
| `/validate-skill` skill | Used in validation phase |
| `.claude/skills/` directory | Direct filesystem ops |
| Registry governance | Pre-push check integration |

## Outputs Location

Todas as skills instaladas vivem em `.claude/skills/` (80+ skills active). Validation reports e test results gerados sob demanda.

## Boundary

- **In scope:** Skill lifecycle (init → develop → validate → test → package → register), Tier governance, frontmatter compliance
- **Out of scope:** Creating new squads (@squad-creator), framework evolution (@aiox-master), agent definitions (@squad-creator creates agents)

## Tasks Canônicas (6 total)

Skill creation, validation, testing, packaging, registry update, tier migration.
