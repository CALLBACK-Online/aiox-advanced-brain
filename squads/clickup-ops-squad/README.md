---
tags: [layer/squad, squad/clickup-ops-squad]
---

# ClickUp Ops — Mission Materializer

**Command:** `/clickup-ops`
**Version:** 0.1.0
**Icon:** 📋
**Status:** Pilot
**Entry Agent:** clickup-chief

> Squad responsável por materializar Missions mapeadas pelo aiox-squad no ClickUp. Recebe mission-clickup-handoff.yaml e cria a estrutura de Space/Folder/Lists/Views no ClickUp.

---

## Agents (4)

| ID | Tipo | Specialty |
|----|------|-----------|
| clickup-chief | Agent | Mission materialization orchestration |
| mission-lead | Human | Go/no-go, accountability, exception handling |
| clickup-runner | Worker | Deterministic API and automation execution |
| mission-quality-clone | Clone | Preflight coherence and readiness review |

## Capabilities

- Receive mission-clickup-handoff.yaml from aiox-squad
- Create ClickUp Space/Folder/Lists structure
- Configure DAG View, Board, Dashboard views

## Upstream

- **aiox-squad** — Phase 7 completion (mode=mission)

## AIOX

- **Modes:** CRIAR, RESOLVER, GERENCIAR, ENTENDER, VALIDAR, CONFIGURAR, PLANEJAR, EXPLORAR
- **Composition:** Full AIOX hierarchy (Tokens → Atoms → Molecules → Organisms → Instances)

## Vault (Obsidian)

- Ponte: [[cursos/entradas/squad-clickup-ops-squad|entrada · clickup-ops-squad]]

Camada leve para o Graph — não altera a execução do squad.

- Aula: [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad|12-clickup-ops-squad]]
- Skill: [[skills/clickup-ops-squad/SKILL|clickup-ops-squad]]
- Mapa: [[cursos/MOC-Squads|MOC · Squads]]
- Home: [[00-HOME]]
