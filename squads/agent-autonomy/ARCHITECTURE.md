# Architecture — Agent Autonomy Squad

## Tier System

```text
                    autonomy-chief
                   [Orchestrator]
                   Triage + Routing
                        |
          ┌─────────────┤
          |              |
   autonomy-auditor      |
      [Tier 0]           |
   Diagnosis + Scoring   |
   (3 Pillars + L1-L5)   |
          |              |
    ┌─────┴──────┐       |
    |            |       |
agent-architect  reasoning-engineer
   [Tier 1]        [Tier 1]
 Design + ACI    ReAct/Reflexion/ToT
    |            |
    ┌────┴───────┘
    |
 ┌──┴──────────┐
 |             |
tool-smith   ecosystem-scout
 [Tier 2]     [Tier 2]
Build Tools   Research OSS
```

## Handoff Flows

### Routing Matrix (autonomy-chief)

| User Request | Route To | Quality Gate |
|-------------|----------|-------------|
| Audit agent | autonomy-auditor | QG-002 |
| Create agent | agent-architect | QG-003 |
| Diagnose failure | autonomy-auditor | QG-002 |
| Optimize agent | agent-architect + reasoning-engineer | QG-003 + QG-004 |
| Build tools | tool-smith | QG-005 |
| Find libraries | ecosystem-scout | QG-SCOUT |
| Teach reasoning | reasoning-engineer | QG-004 |

### Audit-Optimize Cycle (wf: audit-optimize-cycle)

```text
┌─► autonomy-auditor ──► autonomy-chief ──► specialist ──► autonomy-auditor ─┐
│      (audit)            (triage)          (optimize)      (re-audit)        │
│                                                                             │
└──────────── loop until target level OR max 3 iterations ───────────────────┘
```

**Triage routing by gap area:**

| Gap Area | Specialist | Task |
|----------|-----------|------|
| Planning (P1-P3) | reasoning-engineer | teach-reasoning.md |
| Memory (M1-M3) | agent-architect | optimize-agent.md |
| Tool Use (T1-T3) | ecosystem-scout + tool-smith | search-ecosystem.md + suggest-tools.md |
| Failure Modes | autonomy-auditor | diagnose-autonomy-failure.md |
| Multiple areas | agent-architect | optimize-agent.md (redesign) |

### Create Agent Flow (wf: create-agent-flow)

```text
autonomy-chief ──► agent-architect ──► tool-smith ──► autonomy-auditor
  (scope)          (design)           (tools)        (validate L3+)
```

## Quality Gates

| ID | Name | Owner | Type | Transition |
|----|------|-------|------|-----------|
| QG-001 | Request Classification | autonomy-chief | routing | Input → Specialist |
| QG-002 | Diagnosis Complete | autonomy-auditor | blocking | Audit → Optimize |
| QG-003 | Architecture Review | agent-architect | blocking | Design → Build |
| QG-004 | Reasoning Validated | reasoning-engineer | blocking | Pattern → Apply |
| QG-005 | Tool Quality | tool-smith | blocking | Build → Deliver |
| QG-006 | Final Validation | autonomy-chief | blocking | Deliver → Done |
| QG-SCOUT | Research Quality | ecosystem-scout | advisory | Research → Recommend |

## Diagnostic Framework (3 Pillars + 4 FM)

```text
┌─────────────────────────────────────────────┐
│              AUTONOMY SCORE                  │
│                                              │
│  Planning (0.35)    Memory (0.30)    Tool Use (0.35)  │
│  ├─ P1: Decompose   ├─ M1: Working   ├─ T1: Coverage  │
│  ├─ P2: Reflect      ├─ M2: Long-Term ├─ T2: Quality   │
│  └─ P3: Persist      └─ M3: Cross     └─ T3: Recovery  │
│                                              │
│  Failure Modes                               │
│  ├─ FM-1: Context Saturation                 │
│  ├─ FM-2: Tool Brittleness                   │
│  ├─ FM-3: Reasoning Drift                    │
│  └─ FM-4: Evaluator Absence                  │
│                                              │
│  Levels: L1 (Operator) → L5 (Full Autonomy)  │
│  Threshold: L3+ = 13/18, L4+ = 15/18        │
└─────────────────────────────────────────────┘
```
