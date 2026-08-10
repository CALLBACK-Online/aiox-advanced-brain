# Board Meeting Task

**Command:** `/advisory-board:board-meeting`
**Agent:** board-chair
**Purpose:** Facilitar sessão completa do Advisory Board

---

## Overview

Executa uma sessão completa do Advisory Board seguindo o modelo Vistage de Issue Processing. Inclui preload determinístico de contexto local, convocação de conselheiros relevantes, facilitação de debate, mecanismos anti-groupthink, e síntese de recomendações.

---

## Input Requirements

```yaml
required:
  - topic: string        # Tema central da sessão
  - type: enum           # strategic_review | issue_processing | opportunity_eval | crisis_advisory

optional:
  - advisors: list       # Conselheiros específicos (default: auto-select)
  - time_constraint: string  # Se há urgência
  - context: string      # Contexto adicional
  - prior_decisions: list    # Decisões anteriores relacionadas
```

---

## Execution Flow

### Phase 0: Local Context Preload (Board Chair)

Antes de qualquer conselho:

1. Executar `node squads/advisory-board/scripts/resolve-advisory-context.cjs --format=json`
2. Carregar `.aiox/advisory-board/alan-nicolas-profile.yaml` se `profile_path` existir
3. Carregar a ata mais recente em `docs/advisory/` se `latest_session_path` existir
4. Declarar `fresh_session_only` quando algum artefato necessário não estiver disponível

```json
{
  "advisory_context": {
    "status": "ready|partial|missing",
    "profile_path": ".aiox/advisory-board/alan-nicolas-profile.yaml",
    "latest_session_path": "docs/advisory/2026-03-10-....md",
    "missing_paths": []
  }
}
```

### Phase 1: Session Setup (Board Chair)

```markdown
## 📋 SESSION SETUP

**Topic:** {topic}
**Type:** {type}
**Date:** {current_date}

### Advisor Selection
Based on topic analysis, convening:

| Advisor | Rationale |
|---------|-----------|
| {advisor_1} | {why relevant} |
| {advisor_2} | {why relevant} |
| {advisor_3} | {why relevant} |

### Session Ground Rules
1. Radical candor expected
2. Best idea wins, not loudest voice
3. Devil's Advocate assigned: {advisor_name}
4. Divergence before convergence
```

### Phase 2: Issue Presentation (User/Chair)

```markdown
## 🎯 ISSUE PRESENTATION

### The Situation
{Descrição factual sem julgamento}

### What I've Tried
{Tentativas anteriores e resultados}

### What I Think the Options Are
{Opções que o apresentador vê}

### What I Want from This Session
{Outcome desejado}
```

### Phase 3: Clarifying Questions (All Advisors)

```markdown
## ❓ CLARIFYING QUESTIONS

**Rule:** Questions only. No advice yet.

{Advisor 1}: {question}
{Advisor 2}: {question}
{Advisor 3}: {question}
...

### Emerging Themes from Questions
- {theme_1}
- {theme_2}
```

### Phase 4: Perspective Sharing (Each Advisor)

```markdown
## 💡 ADVISOR PERSPECTIVES

### {Advisor Name} ({Role/Domain})

**Through my lens:**
{Perspective using their specific frameworks}

**Key insight:**
{Main takeaway}

**Challenge question:**
{Question that pushes thinking}

---
[Repeat for each advisor]
```

### Phase 5: Devil's Advocate Challenge

```markdown
## 😈 DEVIL'S ADVOCATE

**Assigned to:** {advisor_name}

### Challenges to Consensus

1. **On assumption X:** {challenge}
2. **On option Y:** {counterargument}
3. **What if we're all wrong about:** {blind spot}

### Reframe Requirement
Before concluding, we must address:
- {challenge_1}
- {challenge_2}
```

### Phase 6: Synthesis & Recommendation (Board Chair)

```markdown
## 🔮 SYNTHESIS

### Convergence Points
Where advisors agree:
1. {point_1}
2. {point_2}

### Productive Tensions
Where advisors disagree (and why both have merit):
1. {tension_1}: {advisor_a} vs {advisor_b}
2. {tension_2}: {advisor_c} vs {advisor_d}

### Board Recommendation
Based on combined wisdom:

**Primary recommendation:** {recommendation}

**Rationale:** {why}

**Risks acknowledged:** {risks}

**Implementation considerations:**
1. {consideration_1}
2. {consideration_2}

### Accountability
- **Decision owner:** {name}
- **Review checkpoint:** {date}
- **Success metrics:** {metrics}
```

---

## Advisor Selection Matrix

| Topic Type | Primary Advisors | Devil's Advocate |
|------------|------------------|------------------|
| Strategic Direction | Thiel, Naval, Dalio | Sivers |
| Scaling Decisions | Hoffman, Thiel | Chouinard |
| Team Dynamics | Lencioni, Sinek, Brown | Naval |
| Risk Assessment | Munger, Dalio | Hoffman |
| Values/Purpose | Chouinard, Sinek | Thiel |
| Personal Leadership | Brown, Sinek | Munger |
| Market Opportunity | Thiel, Hoffman | Sivers |

---

## Anti-Groupthink Interventions

| Trigger | Intervention |
|---------|--------------|
| Unanimous agreement too fast | "Let's steelman the opposite view" |
| One voice dominating | "We haven't heard from X yet" |
| Analysis paralysis | "What would we decide with 70% info?" |
| Comfort-seeking | "What's the bold version of this?" |
| Echo chamber forming | Activate Devil's Advocate |

---

## Output Artifacts

1. **Advisory Context Brief** -> `outputs/advisory-board/context/advisory-context-brief.json`
2. **Meeting Minutes** → `outputs/advisory-board/sessions/{date}-{topic}.md`
3. **Decision Record** → Append to decision log
4. **Follow-up Actions** → Task assignments with dates

---

## Example Invocation

```
/advisory-board:board-meeting
topic: "Should we raise external funding or bootstrap?"
type: strategic_review
context: "Currently profitable but growth constrained"
```

---

## Metadata

```yaml
task_id: board-meeting
category: session
complexity: high
duration: 30-60min
requires: board-chair + selected advisors
outputs:
  - meeting-minutes
  - decision-record
  - action-items
version: "1.0"
```
