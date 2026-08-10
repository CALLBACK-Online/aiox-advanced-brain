# ClickUp Ops — Mission Materializer

**Command:** `/clickup-ops`
**Version:** 0.1.0
**Icon:** 📋
**Status:** Pilot
**Entry Agent:** clickup-chief

> Squad responsável por materializar Missions mapeadas pelo sinkra-squad no ClickUp. Recebe mission-clickup-handoff.yaml e cria a estrutura de Space/Folder/Lists/Views no ClickUp.

---

## Agents (4)

| ID | Tipo | Specialty |
|----|------|-----------|
| clickup-chief | Agent | Mission materialization orchestration |
| mission-lead | Human | Go/no-go, accountability, exception handling |
| clickup-runner | Worker | Deterministic API and automation execution |
| mission-quality-clone | Clone | Preflight coherence and readiness review |

## Capabilities

- Receive mission-clickup-handoff.yaml from sinkra-squad
- Create ClickUp Space/Folder/Lists structure
- Configure DAG View, Board, Dashboard views

## Upstream

- **sinkra-squad** — Phase 7 completion (mode=mission)

## SINKRA

- **Modes:** CRIAR, RESOLVER, GERENCIAR, ENTENDER, VALIDAR, CONFIGURAR, PLANEJAR, EXPLORAR
- **Composition:** Full SINKRA hierarchy (Tokens → Atoms → Molecules → Organisms → Instances)
