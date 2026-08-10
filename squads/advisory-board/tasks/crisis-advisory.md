# Crisis Advisory Task

**Command:** `/advisory-board:crisis-advisory`
**Agent:** board-chair + rapid-response advisors
**Purpose:** Suporte em situação de crise que requer decisão rápida

---

## Overview

Protocolo de emergência para situações que requerem decisão rápida com input do board. Estrutura compacta que mantém rigor enquanto respeita urgência.

---

## Input Requirements

```yaml
required:
  - crisis: string       # O que está acontecendo
  - urgency: enum        # immediate | hours | day
  - decision_needed: string  # Que decisão precisa ser tomada

optional:
  - constraints: list    # Limitações conhecidas
  - options_identified: list  # Opções já pensadas
```

---

## Crisis Protocol

### Stage 1: Rapid Assessment (2 min)

```markdown
## 🚨 CRISIS ASSESSMENT

### The Situation
{One paragraph max}

### Urgency Level
{immediate | hours | day}

### Decision Deadline
{specific time}

### What's at Stake
- Best case if we act well: {outcome}
- Worst case if we act poorly: {outcome}
- Worst case if we don't act: {outcome}
```

### Stage 2: Rapid Triage - Who We Need

```markdown
## RAPID TRIAGE

### Crisis Type: {type}

**Convening:**
| Advisor | Why Needed |
|---------|------------|
| {name_1} | {rationale} |
| {name_2} | {rationale} |
| {name_3} | {rationale} |

**Not convening:** {who and why}
```

**Crisis Type → Advisor Match:**

| Crisis Type | Primary Advisors |
|-------------|------------------|
| Financial/Cash | Munger, Dalio |
| Team/People | Lencioni, Brown, Sinek |
| Strategic Pivot | Thiel, Naval, Hoffman |
| Reputation | Sinek, Brown |
| Legal/Compliance | Munger, Dalio |
| Opportunity (time-sensitive) | Thiel, Hoffman |
| Values Conflict | Chouinard, Sinek |

### Stage 3: Compressed Input (5 min total)

```markdown
## COMPRESSED ADVISOR INPUT

### {Advisor 1}: {One line headline}
- Key insight: {30 words max}
- Recommended action: {specific}
- Risk flagged: {one line}

### {Advisor 2}: {One line headline}
- Key insight: {30 words max}
- Recommended action: {specific}
- Risk flagged: {one line}

### {Advisor 3}: {One line headline}
- Key insight: {30 words max}
- Recommended action: {specific}
- Risk flagged: {one line}
```

### Stage 4: Decision Framework

```markdown
## CRISIS DECISION FRAMEWORK

### Options on the Table
| Option | Upside | Downside | Reversibility |
|--------|--------|----------|---------------|
| A: {option} | {upside} | {downside} | {H/M/L} |
| B: {option} | {upside} | {downside} | {H/M/L} |
| C: {option} | {upside} | {downside} | {H/M/L} |

### Munger Quick Check
- Worst case for each option: {analysis}
- Which worst case is most survivable?

### Reversibility Principle
**Prefer reversible decisions under time pressure.**

- Can we undo this if wrong? → Bias toward action
- Is this permanent? → Bias toward caution

### 70% Rule
We have {%} of information we'd ideally want.
Under crisis: 70% is enough. Decide.
```

### Stage 5: Crisis Decision

```markdown
## CRISIS DECISION

### Decision Made
{Clear statement of what we're doing}

### Rationale
{2-3 sentences max}

### Immediate Actions
1. {action_1} - Owner: {name} - By: {time}
2. {action_2} - Owner: {name} - By: {time}
3. {action_3} - Owner: {name} - By: {time}

### Communication Plan
- Who needs to know: {list}
- What they need to know: {key message}
- When: {timing}

### Review Checkpoint
Check results at: {specific time}
If {condition}, then {adjustment}
```

---

## Crisis Principles

```
┌─────────────────────────────────────────────────────────┐
│              CRISIS DECISION PRINCIPLES                 │
├─────────────────────────────────────────────────────────┤
│ 1. Reversible > Irreversible                            │
│    Prefer decisions you can undo                        │
│                                                         │
│ 2. 70% Information Rule                                 │
│    Perfect info won't come in time                      │
│                                                         │
│ 3. Worst Case Survivability                             │
│    Which failure can we recover from?                   │
│                                                         │
│ 4. Action Beats Paralysis                               │
│    Usually. But wrong action can be worse.              │
│                                                         │
│ 5. Communicate Early                                    │
│    Stakeholders prefer early incomplete to late         │
└─────────────────────────────────────────────────────────┘
```

---

## Post-Crisis Protocol

After immediate crisis is handled:

```markdown
## POST-CRISIS REVIEW

### What Happened
{factual description}

### Decision Made
{what we decided}

### Outcome
{what resulted}

### Lessons
1. What worked: {insight}
2. What didn't: {insight}
3. What we'd do differently: {insight}

### System Fix
- What principle/process would prevent this?
- What early warning did we miss?
```

---

## Output

```yaml
outputs:
  - crisis_assessment: situation summary
  - decision_record: what was decided and why
  - action_plan: immediate next steps
  - post_crisis_review: lessons learned (async)
```

---

## Metadata

```yaml
task_id: crisis-advisory
category: emergency
complexity: high (compressed)
duration: 10-15min
requires: board-chair + 2-3 advisors
version: "1.0"
```
