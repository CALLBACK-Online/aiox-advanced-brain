# Devil's Advocate Task

**Command:** `/advisory-board:devils-advocate`
**Agent:** assigned advisor (rotates)
**Purpose:** Desafiar consenso emergente e testar robustez de decisões

---

## Overview

Ativação intencional do papel de Devil's Advocate para combater groupthink e testar a robustez de uma decisão ou direção. Pode ser usado standalone ou como parte de sessão maior.

---

## Input Requirements

```yaml
required:
  - position: string     # A posição/decisão a ser desafiada

optional:
  - context: string      # Contexto da discussão
  - consensus_level: enum  # emerging | strong | unanimous
  - advocate: string     # Quem assume o papel (default: auto-assign)
```

---

## Devil's Advocate Selection

Rotação baseada em quem naturalmente OPÕE o consenso:

| If Consensus Is | Devil's Advocate Should Be |
|-----------------|---------------------------|
| "Vamos escalar rápido" | Sivers, Chouinard, Munger |
| "Vamos manter pequeno" | Hoffman, Thiel |
| "Foco em sistemas/eficiência" | Sinek, Brown, Lencioni |
| "Foco em pessoas/cultura" | Naval, Thiel |
| "Vamos ser conservadores" | Thiel, Hoffman |
| "Vamos ser agressivos" | Munger, Dalio, Sivers |
| "Vamos seguir os dados" | Brown (feelings matter too) |
| "Vamos seguir intuição" | Dalio (where's the evidence?) |

---

## Devil's Advocate Protocol

### Phase 1: Steelman the Position

```markdown
## STEELMAN

Before attacking, I must understand.

**The Position Being Defended:**
{clear statement of the consensus}

**Why This Position Makes Sense:**
1. {strong argument for}
2. {strong argument for}
3. {strong argument for}

**Who Would Benefit:**
{stakeholders served by this position}
```

### Phase 2: Challenge Assumptions

```markdown
## CHALLENGING ASSUMPTIONS

### Hidden Assumptions
Assumptions baked into this position that might be wrong:

1. **Assumption:** {assumption}
   **Challenge:** {why it might not be true}
   **If wrong:** {consequence}

2. **Assumption:** {assumption}
   **Challenge:** {why it might not be true}
   **If wrong:** {consequence}

3. **Assumption:** {assumption}
   **Challenge:** {why it might not be true}
   **If wrong:** {consequence}
```

### Phase 3: Alternative Narrative

```markdown
## ALTERNATIVE NARRATIVE

**The Opposite Position:**
{clear statement of the contrarian view}

**Why This ALSO Makes Sense:**
1. {strong argument for opposite}
2. {strong argument for opposite}
3. {strong argument for opposite}

**Historical Precedent:**
{example where opposite was right}

**Who We Might Be Ignoring:**
{stakeholders not served by consensus}
```

### Phase 4: Stress Test

```markdown
## STRESS TEST

### Failure Scenarios
If we proceed with consensus and:

| Scenario | Probability | Impact | Mitigation |
|----------|-------------|--------|------------|
| {scenario_1} | {H/M/L} | {H/M/L} | {exists?} |
| {scenario_2} | {H/M/L} | {H/M/L} | {exists?} |
| {scenario_3} | {H/M/L} | {H/M/L} | {exists?} |

### Pre-Mortem
It's 12 months from now. This decision failed spectacularly.
Write the post-mortem:

"{post_mortem_narrative}"

### Disconfirming Evidence
What evidence would change our mind?
- {evidence_1}
- {evidence_2}
Have we actively looked for this? {yes/no}
```

### Phase 5: Reframe Requirement

```markdown
## REFRAME REQUIREMENT

Before finalizing, the group MUST address:

### Mandatory Responses
1. **Challenge:** {challenge_1}
   **Response required:** {what must be answered}

2. **Challenge:** {challenge_2}
   **Response required:** {what must be answered}

### Integration Question
How can we modify the decision to incorporate the valid concerns raised?

### Final Check
- [ ] We've genuinely considered the opposite
- [ ] We can articulate why we're NOT doing the opposite
- [ ] We've identified what would change our mind
- [ ] We've stress-tested key assumptions
```

---

## Devil's Advocate Rules

```
┌─────────────────────────────────────────────────────────┐
│           DEVIL'S ADVOCATE RULES                        │
├─────────────────────────────────────────────────────────┤
│ 1. STEELMAN FIRST                                       │
│    Must understand position before attacking            │
│                                                         │
│ 2. ATTACK IDEAS, NOT PEOPLE                            │
│    "This argument is weak because..." not              │
│    "You're wrong because..."                           │
│                                                         │
│ 3. PROVIDE ALTERNATIVES                                 │
│    Not just "this is bad" but "consider instead..."    │
│                                                         │
│ 4. BE GENUINE                                           │
│    Real challenges, not token opposition               │
│                                                         │
│ 5. ACCEPT DEFEAT GRACEFULLY                            │
│    If challenges are addressed, support the decision    │
└─────────────────────────────────────────────────────────┘
```

---

## When to Trigger Devil's Advocate

### Automatic Triggers
- Unanimous agreement reached in < 10 minutes
- No dissenting voice in discussion
- Decision matches what we "wanted" to decide
- High-stakes decision with low apparent risk

### Manual Triggers
- Someone says "everyone agrees"
- Important stakeholder is absent
- Decision reverses previous direction
- External pressure to decide quickly

---

## Output

```markdown
## DEVIL'S ADVOCATE SUMMARY

### Challenges Raised
1. {challenge}
2. {challenge}
3. {challenge}

### Responses Required
1. {what group must address}
2. {what group must address}

### Integration Opportunities
{how to improve decision with these concerns}

### Verdict
- [ ] Challenges adequately addressed → Proceed
- [ ] Challenges NOT addressed → Do not proceed
- [ ] Needs more discussion → Continue debate
```

---

## Metadata

```yaml
task_id: devils-advocate
category: quality-control
complexity: medium
duration: 10-15min
requires: single advisor in DA role
anti_pattern: groupthink
version: "1.0"
```
