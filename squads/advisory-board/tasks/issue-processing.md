# Issue Processing Task

**Command:** `/advisory-board:issue-processing`
**Agent:** board-chair + relevant advisors
**Purpose:** Resolver issue específico usando Vistage 5-Stage Model

---

## Overview

Aplica o framework Vistage de Issue Processing para resolver um problema específico. Estrutura rigorosa que força clareza, evita soluções prematuras, e gera recomendações acionáveis.

---

## Input Requirements

```yaml
required:
  - issue: string        # Descrição do problema/issue

optional:
  - owner: string        # Quem é responsável pela decisão
  - deadline: date       # Se há prazo
  - constraints: list    # Limitações conhecidas
  - prior_attempts: list # O que já foi tentado
```

---

## The Vistage 5-Stage Process

### Stage 1: Issue Presentation (5 min)

**Presenter provides:**

```markdown
## ISSUE PRESENTATION

### The Issue
{Descrição concisa - uma frase}

### Background
{Contexto relevante - máximo 3 parágrafos}

### What I've Tried
- {attempt_1} → {result}
- {attempt_2} → {result}

### My Current Thinking
{O que você acha que deveria fazer}

### What I Want from This Session
{Tipo de ajuda esperada}
```

**Board Chair ensures:**
- [ ] Issue is clearly stated
- [ ] No advice given yet
- [ ] Time respected

---

### Stage 2: Clarifying Questions (10 min)

**Rules:**
- Questions ONLY - no statements disguised as questions
- One question at a time
- Purpose: understand, not advise

```markdown
## CLARIFYING QUESTIONS

### From {Advisor}:
Q: {question}
A: {answer}

### From {Advisor}:
Q: {question}
A: {answer}

[Continue until understanding is complete]

### Summary of New Information Surfaced
1. {insight_1}
2. {insight_2}
```

**Red flags Board Chair watches for:**
- Leading questions (advice in disguise)
- Multiple questions at once
- Jumping to conclusions

---

### Stage 3: Content/Experience Sharing (15 min)

**Rules:**
- Share relevant experience, not solutions
- "When I faced something similar..."
- Each advisor gets equal time

```markdown
## EXPERIENCE SHARING

### {Advisor Name}
**Relevant experience:**
{story or example}

**What I learned:**
{lesson that might apply}

---

### {Advisor Name}
**Relevant experience:**
{story or example}

**What I learned:**
{lesson that might apply}

[Continue for each advisor]
```

---

### Stage 4: Suggestions & Recommendations (15 min)

**Rules:**
- Now advice is welcome
- Be specific and actionable
- Acknowledge tradeoffs

```markdown
## SUGGESTIONS & RECOMMENDATIONS

### From {Advisor Name}
**Suggestion:** {specific recommendation}
**Why:** {rationale}
**Tradeoff:** {what you'd be giving up}

### From {Advisor Name}
**Suggestion:** {specific recommendation}
**Why:** {rationale}
**Tradeoff:** {what you'd be giving up}

[Continue for each advisor]

### Devil's Advocate Challenge
{Assigned advisor}: "Before we conclude, I want to challenge..."
- {challenge_1}
- {challenge_2}
```

---

### Stage 5: Commitment & Action (5 min)

**Rules:**
- Presenter commits to specific actions
- NOT consensus - presenter decides
- Accountability established

```markdown
## COMMITMENT & ACTION

### What I'm Going to Do
Based on this session, I commit to:

1. **Action:** {specific action}
   **By when:** {date}

2. **Action:** {specific action}
   **By when:** {date}

3. **Action:** {specific action}
   **By when:** {date}

### What I'm NOT Going to Do
{Options I'm explicitly rejecting and why}

### Accountability
- **Check-in date:** {date}
- **With whom:** {board chair or specific advisor}
- **Success looks like:** {metrics}

### Presenter's Reflection
What was most valuable about this session:
{reflection}
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│              VISTAGE ISSUE PROCESSING                   │
├─────────────────────────────────────────────────────────┤
│ Stage 1: PRESENTATION (5 min)                           │
│   → Present issue clearly, no advice yet               │
│                                                         │
│ Stage 2: CLARIFYING QUESTIONS (10 min)                 │
│   → Questions only, understand fully                   │
│                                                         │
│ Stage 3: EXPERIENCE SHARING (15 min)                   │
│   → "When I faced similar..." - stories, not advice    │
│                                                         │
│ Stage 4: SUGGESTIONS (15 min)                          │
│   → Now advice welcome, be specific                    │
│                                                         │
│ Stage 5: COMMITMENT (5 min)                            │
│   → Presenter commits, accountability set              │
└─────────────────────────────────────────────────────────┘
```

---

## Output

```yaml
outputs:
  - issue_record: markdown document with full session
  - action_items: list of commitments with dates
  - follow_up: scheduled accountability check
```

---

## Metadata

```yaml
task_id: issue-processing
category: problem-solving
complexity: medium
duration: 45-60min
requires: board-chair + 3-5 advisors
model: Vistage Issue Processing
version: "1.0"
```
