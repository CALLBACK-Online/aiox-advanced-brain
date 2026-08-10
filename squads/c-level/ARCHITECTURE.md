# C-Level Squad — Architecture

## Overview

O squad `c-level` estrutura o workspace da empresa via elicitação profunda e geração de documentos de referência canônicos. Orquestra decisões executivas cross-BU através do COO e opera como ponte entre direção estratégica (CEO/vision) e execução (especialistas C-level).

## Agent Hierarchy

```
workspace-chief (Tier 0 — Workspace Orchestrator)
└── coo-orchestrator (Tier 0 — Operations Orchestrator)
    │
    ├── vision-chief / vision-strategist (Strategic Direction)
    │
    ├── Tier 1 — Executive Specialists
    │   ├── cfo-architect       # Financial operations, FinOps
    │   ├── cmo-architect       # Marketing, brand, demand gen
    │   ├── cto-architect       # Tech direction, stack decisions
    │   ├── cio-engineer        # Information architecture
    │   ├── cso                 # Security, compliance, risk
    │   └── caio-architect      # AI strategy, agent governance
```

## Execution Flow

```
User request to establish workspace or make exec decision
                              ↓
                    workspace-chief (intake)
                              ↓
                    coo-orchestrator routes
                              ↓
       ┌──────────────────────┼──────────────────────┐
       v                      v                      v
   Deep elicitation      Reference doc         Cross-BU handoff
   (vision-chief)        generation            (COO delegates)
       ↓                      ↓                      ↓
       └──────────────────────┴──────────────────────┘
                              ↓
          Canonical docs in workspace/businesses/{biz}/L0-L4
```

## Operation Modes

| Mode | Trigger | Output |
|------|---------|--------|
| Bootstrap business | `*bootstrap` | L0-identity docs (company-dna, founder-dna, legal) |
| Setup business profile | `*setup-business-profile` | L1-strategy docs (ICP, pricing, offerbook) |
| Deep elicitation | `*deep-elicitation` | Strategic vision, priorities, North Star |
| Executive decision | `*decide` | Advisory board output, decision-log |
| Cross-BU handoff | Inter-BU work | Formal handoff with signoff |

## Workspace Integration

| Layer | TTL | Canonical docs owned |
|-------|-----|---------------------|
| L0-identity | 365d | company-dna, founder-dna, legal |
| L1-strategy | 90d | ICP, pricing-strategy, offerbook |
| L2-tactical | 60d | Brand, movement, design direction |
| L3-product | 30d | Product specs, offerbooks per product |
| L4-operational | 7d | Campaigns, content, operations |

## Boundary

- **In scope:** Executive decisions, workspace bootstrap, business profile setup, cross-BU orchestration, reference doc generation
- **Out of scope:** Implementation (dev/devops), story execution (sm/po), tactical copywriting (copy squad)

## Tasks Canônicas

40 tasks cobrindo bootstrap, setup, deep elicitation, strategic decisions, advisory board sessions, handoffs inter-BU, e governança de workspace/businesses/.
