---
tags: [layer/squad, squad/skill-creator-ops]
---

# Skill Creator Ops — Skill Lifecycle Operations

**Command:** `/skill-creator-ops`
**Version:** 2.0.0
**Icon:** 🔧
**Tier:** Core
**Entry Agent:** skill-ops-chief

> Skill lifecycle ops — create, validate (schema + 4.7 prompt quality), test, migrate, package, deprecate, retire. Linked to `/skill-creator` (authoring) and `/prompt-47-migrator` (tooling). Empirically calibrated against Claude Opus 4.7 production patterns.

Main pipeline: INIT → DEVELOP → VALIDATE (schema) → PROMPT_QUALITY (4.7) → TEST → PACKAGE → REGISTER.
Auxiliary flows: migrate-to-47, deprecate, retire, lifecycle-audit.

---

## Agents (3)

| ID | Specialty |
|----|-----------|
| skill-ops-chief | Orchestrates the full skill lifecycle and auxiliary flows |
| skill-validator | Schema validation (CHK-01-12) + prompt-quality validation (CHK-13-16) |
| skill-tester | Sandbox execution testing (golden inputs/outputs pattern) |

## Capabilities

- Skill creation and scaffolding
- Schema validation (12 checks)
- Prompt-quality validation (4 checks, weighted, 4.7-calibrated)
- End-to-end sandbox testing
- Migration of legacy skills to 4.7 conventions (preview-first)
- Lifecycle governance: active / deprecated / retired
- Packaging and distribution
- Registry governance and monthly lifecycle audit

## Artifact Contracts

- `skill-validation-report` — templates/validation-report-tmpl.yaml (schema + prompt_quality sections)
- `skill-test-result` — templates/test-result-tmpl.yaml
- `skill-package` — bundled artifact
- `skill-prompt-quality-report` — extends validation-report with prompt_quality section
- `skill-migration-preview` — preview-first migration output (4 deliverables from /prompt-47-migrator)
- `skill-lifecycle-log` — append-only lifecycle events log

## Linked Skills

- `/skill-creator` — skills/skill-creator/SKILL.md (operational owner relationship)
- `/prompt-47-migrator` — skills/prompt-47-migrator/SKILL.md (tooling consumer)

## Reference Data

- `data/anthropic-patterns.yaml` — empirical reference catalog of patterns observed in Claude Opus 4.7 production system prompt. Canonical shapes for decision trees, severity calibration, triggering tiers, cost framing, self-check loops, triplet examples, arrow notation, priority-numbered tool lists, section tagging, and internalized-no-scaffolding absences.
- `data/validation-schema.yaml` — schema and prompt-quality check definitions, scoring formulas, lifecycle state requirements.

## AIOX

- **BU Mapping:** hub-framework
- **Tier:** Core
- **Modes:** CRIAR, VALIDAR, CONFIGURAR
- **Evidence hierarchy:** source code of Anthropic's production prompt is ground truth; documentation is narrative about it. When the two disagree, the system prompt wins.

## Vault (Obsidian)

- Ponte: [[cursos/entradas/squad-skill-creator-ops|entrada · skill-creator-ops]]

Camada leve para o Graph — não altera a execução do squad.

- Aula: [[cursos/AIOX-Advanced-Squads/aulas/22-skill-creator-ops|22-skill-creator-ops]]
- Skill: [[skills/skill-creator-ops/SKILL|skill-creator-ops]]
- Mapa: [[cursos/MOC-Squads|MOC · Squads]]
- Home: [[00-HOME]]
