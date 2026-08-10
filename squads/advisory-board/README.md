# Advisory Board Squad

**Personal Board of Directors for Strategic Decisions**

Squad de conselheiros estratégicos pessoais baseado no DNA Mental™ de Alan Nicolas. Combina mentes alinhadas (validam direção) + mentes complementares (expandem perspectiva) para decisões robustas.

---

## Quick Start

```bash
# Consulta rápida com advisor específico
/Board:tasks:quick-consult

# Processar um problema/decisão (Vistage model)
/Board:tasks:issue-processing

# Reunião completa do board
/Board:tasks:board-meeting

# Avaliar oportunidade
/Board:tasks:opportunity-eval
```

Todas as sessões começam com preload determinístico do contexto local via `tasks/load-advisory-context.md` e `scripts/resolve-advisory-context.cjs`. Se o founder profile ou a ata mais recente não existirem, o board deve operar explicitamente em `fresh_session_only`.

---

## Board Composition

### Orchestrator
| Agent | Role |
|-------|------|
| **board-chair** | Facilita, sintetiza, gerencia tempo, garante anti-groupthink |

### Aligned Minds (4) — Validam e Amplificam
| Agent | Domain | Key Framework |
|-------|--------|---------------|
| **charlie-munger** | Mental Models | Latticework, Inversão |
| **naval-ravikant** | Liberdade + Leverage | Specific Knowledge |
| **ray-dalio** | Princípios + Sistemas | Radical Transparency |
| **derek-sivers** | Autenticidade | Hell Yeah or No |

### Complementary Minds (6) — Desafiam e Expandem
| Agent | Domain | Challenge Question |
|-------|--------|-------------------|
| **simon-sinek** | Liderança + Propósito | "Você está construindo sistemas OU cultivando pessoas?" |
| **patrick-lencioni** | Team Dynamics | "Automação está substituindo ou fortalecendo relações?" |
| **reid-hoffman** | Scaling + Network | "O que você perde por ser seletivo demais?" |
| **brene-brown** | Vulnerabilidade | "Clareza é armadura ou ponte?" |
| **peter-thiel** | Contrarian + Ação | "Está jogando para GANHAR ou para não perder?" |
| **yvon-chouinard** | Valores + Permanência | "É possível impacto massivo E manter integridade?" |

---

## When to Consult Each Advisor

| Situation | Primary | Challenger |
|-----------|---------|------------|
| **Decisão estratégica** | Munger, Dalio, Thiel | Sinek, Chouinard |
| **Pessoas/Equipe** | Lencioni, Sinek | Naval, Thiel |
| **Crescimento/Escala** | Hoffman, Thiel | Sivers, Chouinard |
| **Valores/Ética** | Chouinard, Sivers | Thiel, Hoffman |
| **Liderança pessoal** | Brown, Sinek | Munger, Naval |
| **Risco/Oportunidade** | Munger, Naval, Thiel | Brown, Chouinard |

---

## Session Types

### 1. Quick Consult (15-20 min)
Consulta rápida 1:1 com advisor específico.
```
/Board:tasks:quick-consult
```

### 2. Issue Processing (30-45 min)
Modelo Vistage para processar problemas:
1. Structure the Issue ("How do I...?")
2. Clarifying Questions
3. Reframe the Real Issue
4. Suggestions (advisors contribute)
5. Commitment to Action

```
/Board:tasks:issue-processing
```

### 3. Opportunity Evaluation (30-45 min)
Avaliar oportunidade de negócio/parceria/investimento.
```
/Board:tasks:opportunity-eval
```

### 4. Strategic Review (45-60 min)
Revisão estratégica de longo prazo.
```
/Board:tasks:strategic-review
```

### 5. Full Board Meeting (60-90 min)
Reunião completa com todos os advisors.
```
/Board:tasks:board-meeting
```

## Deterministic Local Context

Antes de aconselhar ou retomar uma discussão, o board deve:

1. Resolver `.aiox/advisory-board/alan-nicolas-profile.yaml`
2. Resolver a ata mais recente em `docs/advisory/`
3. Registrar `status`, `profile_path`, `latest_session_path` e `missing_paths`
4. Operar em `fresh_session_only` quando o contexto local estiver ausente

Isso preserva continuidade sem exigir que arquivos sensíveis sejam commitados.

### 6. Crisis Advisory (30-45 min)
Sessão de emergência para situações críticas.
```
/Board:tasks:crisis-advisory
```

---

## Anti-Groupthink Mechanics

O squad implementa mecânicas para evitar echo chamber:

1. **Devil's Advocate Rotation** — Sempre 2+ vozes desafiadoras
2. **Reframe Requirement** — Articular visão oposta antes de rejeitar
3. **Divergence Tracking** — Flag quando < 2 dissenting voices
4. **Aligned vs Complementary** — Estrutura garante perspectivas opostas

---

## Decision Quality Checklist

Antes de finalizar decisão:

- [ ] **MUNGER:** Por quais modelos mentais isso passou?
- [ ] **INVERSÃO:** O que pode dar errado?
- [ ] **NAVAL:** Isso aumenta ou diminui liberdade?
- [ ] **SIVERS:** É Hell Yeah?
- [ ] **SINEK:** Serve ao WHY?
- [ ] **LENCIONI:** Como afeta a equipe?
- [ ] **BROWN:** Estou blindado ou vulnerável?
- [ ] **THIEL:** Estou jogando para ganhar?
- [ ] **CHOUINARD:** Serve permanência?
- [ ] **HOFFMAN:** A velocidade importa aqui?

---

## Files Structure

```
squads/advisory-board/
├── config.yaml
├── README.md
├── agents/
│   ├── board-chair.md          # Orchestrator
│   ├── charlie-munger.md       # Aligned
│   ├── naval-ravikant.md       # Aligned
│   ├── ray-dalio.md            # Aligned
│   ├── derek-sivers.md         # Aligned
│   ├── simon-sinek.md          # Complementary
│   ├── patrick-lencioni.md     # Complementary
│   ├── reid-hoffman.md         # Complementary
│   ├── brene-brown.md          # Complementary
│   ├── peter-thiel.md          # Complementary
│   └── yvon-chouinard.md       # Complementary
├── tasks/
│   ├── load-advisory-context.md
│   ├── board-meeting.md
│   ├── issue-processing.md
│   ├── strategic-review.md
│   ├── opportunity-eval.md
│   ├── quick-consult.md
│   ├── crisis-advisory.md
│   └── devils-advocate.md
├── workflows/
│   ├── wf-board-meeting.yaml
│   └── wf-issue-processing.yaml
├── scripts/
│   └── resolve-advisory-context.cjs
├── checklists/
│   ├── pre-meeting-checklist.md
│   ├── decision-quality-checklist.md
│   └── anti-groupthink-checklist.md
├── templates/
│   ├── meeting-minutes-tmpl.md
│   ├── issue-brief-tmpl.md
│   └── opportunity-brief-tmpl.md
└── data/
    ├── board-kb.md
    └── advisor-frameworks.yaml
```

---

## Accountability Loop

Cada sessão gera:
1. **Action Items** com owner + deadline
2. **Decision Log** com rationale + dissenting views
3. **Follow-up Date** para revisar outcome

---

*Advisory Board Squad v1.0 | Based on DNA Mental™ alan_nicolas*
