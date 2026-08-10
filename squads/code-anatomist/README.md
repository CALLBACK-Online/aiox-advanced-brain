# Domain Decoder Squad

Squad especializado em **decodificação de domínio a partir de código brownfield** — extrai regras de negócio, taxonomia e modelo de negócio de sistemas legados, atuais e open-source.

## Scope

**code-anatomist = business model extraction from brownfield code, NOT DNS/domain intelligence.**

The real scope is extracting business model logic from codebases:
- Bounded contexts and ubiquitous language (DDD)
- Business rules taxonomy and classification (Ross taxonomy)
- Decision models and DMN formalization
- Traceability: code -> rule -> decision table -> RuleSpeak
- Legacy characterization and seam mapping

Out of scope: DNS/WHOIS/reputation toolchains, domain registration, network intelligence.

## Internal-First Policy

### Fully Covered Internally
| Capability | Method |
|------------|--------|
| DDD bounded context mapping | `map-domain` task + `codebase-mapper` script |
| Ross taxonomy classification | `classify-rules` task + `pattern-extractor` script |
| Legacy characterization / seam mapping | `characterize-legacy` task + `framework-analyzer` + `dependency-analyzer` |
| Decision modeling (DMN formalization) | `model-decisions` task |
| RuleSpeak / SBVR-oriented expression | `express-rules` task |
| Codebase and dependency inventory | AIOX infrastructure scripts |

### Requires External Tools (Gap-Only)
| Capability | Why External | Recommended Tool |
|------------|-------------|-----------------|
| AST queries at scale (structural rule mining) | Volume and precision beyond regex/grep | `ast-grep`, `Semgrep` |
| Semantic pattern matching (rule candidate detection) | Cross-function taint analysis | `Semgrep`, `CodeQL` |
| Code property graphs (deep rule flow) | Combines AST + CFG + PDG for complex legacy | `Joern` |

See `docs/tool-integration-plan.md` and `docs/tool-discovery-report.md` for full details.

## Problema que Resolve

Sistemas contêm décadas de conhecimento de negócio embutido em código, stored procedures, planilhas e conhecimento tribal. Este conhecimento inclui:
- **Regras de negócio** não documentadas ou mal documentadas
- **Taxonomias implícitas** em enums, types, hierarchies e tabelas
- **Modelos de negócio** codificados em fluxos de dados, transações e integrações
- Lógica espalhada por múltiplos sistemas e inconsistente entre eles

O Domain Decoder squad **decodifica, classifica, modela, formaliza e padroniza** todo esse conhecimento de domínio em documentação que tanto negócio quanto tecnologia conseguem ler e validar.

## Time (por Tier)

### Orchestrator
| Agent | Comando | Função |
|-------|---------|--------|
| **Decoder Chief** | `@decoder-chief` | Orquestra o squad, roteia para agente correto |

### Tier 0 - Diagnóstico (sempre primeiro)
| Agent | Comando | Especialidade |
|-------|---------|---------------|
| **Ronald G. Ross** | `@ronald-ross` | Taxonomia e classificação de regras (RuleSpeak, SBVR) |
| **Eric Evans** | `@eric-evans` | Mapeamento de domínios (DDD, Ubiquitous Language, Bounded Context) |

### Tier 1 - Masters (extração e modelagem)
| Agent | Comando | Especialidade |
|-------|---------|---------------|
| **Michael Feathers** | `@michael-feathers` | Entrada em código legado (Characterization Tests, Seam Model) |
| **Barbara von Halle** | `@barbara-von-halle` | Modelagem de lógica de negócio (The Decision Model) |

### Tier 2 - Systematizers (formalização)
| Agent | Comando | Especialidade |
|-------|---------|---------------|
| **James Taylor** | `@james-taylor` | Formalização em DMN (Decision Tables, FEEL, DRD) |
| **Martin Fowler** | `@martin-fowler` | Padrões de arquitetura (PoEAA, Refactoring, Specification Pattern) |

### Tier 3 - Specialist (expressão)
| Agent | Comando | Especialidade |
|-------|---------|---------------|
| **Graham Witt** | `@graham-witt` | Expressão de regras em linguagem natural sem ambiguidade |

### Tool (validação)
| Ferramenta | Comando | Função |
|------------|---------|--------|
| **SBVR Checklist** | `*sbvr-check` | Validação contra standard OMG SBVR 1.5 |

## Workflow de Extração

```
Phase 0: DISCOVERY (Tier 0)
  Evans: Mapear bounded contexts e vocabulário
  Ross: Classificar tipos de regras esperados
    |
Phase 1: CHARACTERIZATION (Tier 1 + Tier 2)
  Feathers: Entrar no código legado com safety nets
  Fowler: Identificar padrões de arquitetura
    |
Phase 2: EXTRACTION (Tier 0 + Tier 1)
  Ross: Extrair e classificar regras
  Feathers: Extrair de código com rastreabilidade
    |
Phase 3: MODELING (Tier 1 + Tier 2)
  Von Halle: Criar Decision Model (rule families)
  Taylor: Formalizar em DMN (decision tables)
    |
Phase 4: EXPRESSION (Tier 3 + Tier 0)
  Witt: Escrever regras em linguagem natural
  Ross: Validar expressão RuleSpeak
    |
Phase 5: VALIDATION (Tool)
  SBVR Checklist: Validar documentação final
  Entrega: Rule Catalog padronizado
```

## Quick Start

```bash
# Ativar o squad
/code-anatomist "nome do sistema ou projeto"

# Iniciar diagnóstico
*diagnose

# Extração completa (todas as fases)
*decode-full

# Validar documentação final
*sbvr-check
```

## Comandos Principais

| Comando | Fase | Descrição |
|---------|------|-----------|
| `*diagnose` | 0 | Diagnóstico completo (classificação + domínios) |
| `*map-domains` | 0 | Evans: mapear bounded contexts |
| `*classify-system` | 0 | Ross: classificar tipos de regras |
| `*characterize` | 1 | Feathers: characterization tests no legado |
| `*identify-patterns` | 1 | Fowler: identificar padrões de arquitetura |
| `*model-logic` | 3 | Von Halle: modelar com Decision Model |
| `*formalize-dmn` | 3 | Taylor: criar decision tables DMN |
| `*express-rules` | 4 | Witt: expressar em linguagem natural |
| `*sbvr-check` | 5 | Validar contra SBVR |
| `*extract-full` | ALL | Workflow completo de extração |
| `*export` | 5 | Exportar rule catalog padronizado |

## Estrutura do Squad

```
squads/code-anatomist/
├── agents/
│   ├── decoder-chief.md        # Orchestrator
│   ├── ronald-ross.md          # Tier 0 - Taxonomia
│   ├── eric-evans.md           # Tier 0 - Domínios
│   ├── michael-feathers.md     # Tier 1 - Código legado
│   ├── barbara-von-halle.md    # Tier 1 - Decision Model
│   ├── james-taylor.md         # Tier 2 - DMN
│   ├── martin-fowler.md        # Tier 2 - Padrões
│   └── graham-witt.md          # Tier 3 - Expressão
├── workflows/
│   ├── wf-extract-rules.yaml   # Workflow completo de extração
│   └── wf-standardize-rules.yaml
├── tasks/
│   ├── classify-rules.md
│   ├── map-domain.md
│   ├── characterize-legacy.md
│   ├── model-decisions.md
│   └── express-rules.md
├── templates/
│   └── rule-catalog-tmpl.md    # Template do catálogo final
├── checklists/
│   ├── sbvr-validation.md      # Checklist SBVR (35 itens)
│   └── extraction-quality.md   # Qualidade do processo
├── data/
├── docs/
├── config.yaml
└── README.md
```

## Output Final

O deliverable principal é o **Rule Catalog** contendo:

1. **Glossário de Termos** - Todos os termos de negócio definidos
2. **Regras Estruturais** - Definições, fatos, derivações
3. **Regras Comportamentais** - Constraints, enablers, computações
4. **Regras de Decisão** - Decision tables com hit policies
5. **Decision Requirements Diagrams** - Visualização de dependências
6. **Matriz de Rastreabilidade** - Regra → código fonte → política
7. **Score SBVR** - Validação contra standard OMG

## Standards Utilizados

| Standard | Versão | Uso |
|----------|--------|-----|
| **SBVR** | 1.5 (OMG) | Vocabulário e regras de negócio |
| **DMN** | 1.4 (OMG) | Modelagem de decisões |
| **FEEL** | (parte do DMN) | Expressões de regras |
| **DDD** | (Evans, 2003) | Bounded contexts e ubiquitous language |

## Fontes das Metodologias

| Expert | Obra Principal | Framework |
|--------|---------------|-----------|
| Ronald G. Ross | "Building Business Solutions" | RuleSpeak, DecisionSpeak, Q-Charts |
| Eric Evans | "Domain-Driven Design" (2003) | Ubiquitous Language, Bounded Context |
| Michael Feathers | "Working Effectively with Legacy Code" (2004) | Characterization Tests, Seam Model |
| Barbara von Halle | "The Decision Model" (2009) | TDM, Rule Families |
| James Taylor | "Real-World Decision Modeling with DMN" | DMN, Decision Tables, FEEL |
| Martin Fowler | "PoEAA" (2002), "Refactoring" (2018) | Domain Logic Patterns, Specification Pattern |
| Graham Witt | "Writing Effective Business Rules" (2012) | Structured Natural Language, Ambiguity Elimination |

---

*Domain Decoder Squad v2.0.0*
*Created: 2026-02-18*
*Squad Creator: AIOX Squad Architect*
