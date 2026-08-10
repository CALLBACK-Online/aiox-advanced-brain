# Code Anatomist Squad — Architecture

## Overview

O squad `code-anatomist` (renomeado de `domain-decoder` por RT-DD-V2-001) executa engenharia reversa completa de software: extrai arquitetura (C4/Arc42), domínio (DDD/SBVR), dados (ER/schema), APIs (OpenAPI), dependências e infraestrutura de qualquer codebase, via pipeline de 9 fases com mapeamento para SINKRA Tokens.

## Agent Hierarchy

```
decoder-chief (Orchestrator — Pipeline de 9 Fases)
│
├── Tier 0 — Core Methodology
│   ├── ronald-ross        # Taxonomia Ross (5 tipos), classificação de regras
│   └── eric-evans         # DDD, ubiquitous language, bounded contexts
│
├── Tier 1 — Specialized Extraction
│   ├── michael-feathers   # Legacy code entry, characterization tests
│   ├── barbara-von-halle  # Decision Model, lógica de negócio
│   ├── simon-brown        # C4 model, architecture diagrams
│   └── data-specialist    # ER extraction, schema introspection
│
├── Tier 2 — Formalization & Pattern Recognition
│   ├── james-taylor       # DMN tables, decision formalization
│   ├── martin-fowler      # Architectural patterns, localization
│   └── rick-kazman        # Horseshoe Model, ATAM, architecture recovery
│
└── Tier 3 — Validation & Expression
    ├── graham-witt        # RuleSpeak, expressão sem ambiguidade
    ├── gail-murphy        # Reflexion Models, conformance checking
    └── sbvr-checklist     # SBVR 45-item validation (tool)
```

## 9-Phase Pipeline

```
Phase 0: Scoping          → Boundaries, goals, success criteria
Phase 1: Architecture     → C4 diagrams, module structure, dependencies
Phase 2: Domain           → DDD, entities, aggregates, bounded contexts
Phase 3: Data             → ER diagrams, schema, data flows
Phase 4: API              → OpenAPI/GraphQL/gRPC surface contracts
Phase 5: Rules            → Business rules extraction (SBVR taxonomy)
Phase 6: Decisions        → Decision Model + DMN formalization
Phase 7: Infrastructure   → Docker, CI/CD, deploy targets, env vars
Phase 8: Conformance      → Reflexion Model, drift detection
```

## Commands

| Command | Execução |
|---------|----------|
| `*extract-full` / `*extract-full-v2` | Pipeline completo (9 fases) |
| `*extract-arch` | Só arquitetura (C4, deps) |
| `*extract-deps` | Só dependências e módulos |
| `*scoping` | Phase 0 (boundaries) |
| `*domain-only` | Phase 2 (DDD) |
| `*classify-rules` | Ross taxonomy classification |
| `*map-domain` | Eric Evans bounded contexts |
| `*extract-rules` | SBVR rules extraction |
| `*model-decisions` | Barbara von Halle Decision Model |
| `*formalize-dmn` | James Taylor DMN tables |
| `*express-rules` | Graham Witt RuleSpeak |
| `*validate-sbvr` | SBVR 45-item checklist |
| `*characterize-legacy` | Michael Feathers characterization tests |
| `*standardize` | Normalização de regras pré-existentes |

## Workspace Integration

- **Level:** `read_only`
- **Read paths:** `outputs/decoded/{business}/` (baseline canônico)
- **Operations:** compare, audit, adopt (RT-ARCH-BRIDGE-001)
- **Self-extraction TTL:** 90 dias (re-extração obrigatória pós-Epic major)

## Integration Points

| Target | Output |
|--------|--------|
| SINKRA Tokens | Regras mapeadas para token-registry |
| Document Registry | Lifecycle PLACEHOLDER → APPROVED |
| ADRs | Decisões arquiteturais documentadas |

## Boundary

- **In scope:** Reverse engineering de codebases brownfield, extração de arquitetura/domínio/regras/dados/APIs, conformance checking, mapeamento para SINKRA
- **Out of scope:** Refactoring direto (@dev), novas features (@architect), escolha de novo stack (@architect)
