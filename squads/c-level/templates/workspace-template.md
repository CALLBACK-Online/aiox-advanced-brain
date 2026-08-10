# WorkspaceTemplate — Generic 5-Layer Workspace System

## Purpose
Template for the 5-layer workspace hierarchy that any spoke can instantiate with their own values.

## Layers (Abstract)
- **L0-identity** (TTL: 365d) — Company DNA, founder DNA, legal
- **L1-strategy** (TTL: 90d) — ICP, BMC, lean canvas, pricing, offerbook
- **L2-tactical** (TTL: 60d) — Brand, design, legal, acceleration
- **L3-product** (TTL: 30d) — Product specs, roadmaps
- **L4-operational** (TTL: 7d) — Campaigns, content, pitch decks

## Instantiation
Each spoke creates `workspace/{spoke-name}/` with their own documents following this template.
See `examples/{spoke}-override.yaml` for a reference implementation.

## Workspace Structure (Generic)

```
workspace/{spoke}/
├── document-registry.yaml               # Governance registry
│
├── L0-identity/                         # TTL: 365d — CEO + COO
│   ├── company-dna.yaml                 # Company profile (COO/CEO)
│   ├── founder-dna.yaml                 # Founder DNA (CEO)
│   ├── credentials.yaml                 # Authority credentials (CEO)
│   └── core-processes.yaml              # Core processes (COO)
│
├── L1-strategy/                         # TTL: 90d — CMO + CTO + CAIO
│   ├── icp.yaml                         # Ideal Customer Profile (CMO)
│   ├── diagnosis.yaml                   # Diagnosis (CMO)
│   ├── pricing-strategy.yaml            # Pricing strategy (CMO)
│   ├── bmc.yaml                         # Business Model Canvas (CMO)
│   ├── lean-canvas.yaml                 # Lean Canvas (CMO)
│   ├── offerbook.yaml                   # Offerbook (CMO)
│   ├── tech-strategy.yaml               # Tech strategy (CTO)
│   ├── tech-stack.yaml                  # Tech stack (CIO)
│   └── ai-strategy.yaml                 # AI strategy (CAIO)
│
├── L2-tactical/                         # TTL: 60d — CMO + Brand Squad
│   └── brand/
│       └── brandbook.yaml               # Brand guidelines (CMO -> brand-squad)
│
├── L3-product/                          # TTL: 30d — CMO + COO
│   └── {product-slug}/
│       └── offerbook.yaml
│
└── L4-operational/                      # TTL: 7d — COO
    ├── team-structure.yaml              # Team structure (COO)
    └── evidence/
        └── workspace-context-summary.yaml
```

## Golden Rule
L0 > L1 > L2 > L3 > L4 (higher layers override lower). Changes cascade downward ONLY.

## Document Lifecycle
PLACEHOLDER -> DRAFT -> POPULATED -> VALIDATED -> APPROVED -> STALE -> ARCHIVED
