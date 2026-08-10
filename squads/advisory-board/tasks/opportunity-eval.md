# Opportunity Evaluation Task

**Command:** `/advisory-board:opportunity-eval`
**Agent:** board-chair + selected advisors
**Purpose:** Avaliar oportunidade específica (partnership, investment, project, market)

---

## Overview

Framework estruturado para avaliar oportunidades de negócio. Combina análise de risco, fit estratégico, e múltiplas perspectivas dos conselheiros.

---

## Input Requirements

```yaml
required:
  - opportunity: string       # Descrição da oportunidade
  - type: enum               # partnership | investment | project | market | acquisition

optional:
  - timeline: string         # Prazo para decisão
  - investment_required: string  # Recursos necessários
  - expected_return: string      # Retorno esperado
  - alternatives: list           # Outras opções consideradas
```

---

## Evaluation Framework

### Phase 1: Opportunity Brief

```markdown
## OPPORTUNITY BRIEF

### The Opportunity
{descrição clara e concisa}

### Type
{partnership | investment | project | market | acquisition}

### Why Now?
{por que essa oportunidade existe agora}

### Investment Required
- Financial: {amount}
- Time: {hours/days/months}
- Opportunity cost: {what we're not doing}

### Expected Return
- Financial: {projected return}
- Strategic: {non-financial benefits}
- Timeline: {when returns expected}
```

### Phase 2: Multi-Lens Analysis

#### Munger Lens (Risk Assessment)

```markdown
## MUNGER: RISK ASSESSMENT

### Inversão - How This Fails
1. {failure_mode_1} - Probability: {H/M/L}
2. {failure_mode_2} - Probability: {H/M/L}
3. {failure_mode_3} - Probability: {H/M/L}

### Worst Case Scenario
If everything goes wrong: {description}
Is this survivable? {yes/no}

### Margin of Safety
What buffer do we have if 50% wrong?
{analysis}

### Circle of Competence
- Inside circle: {what we know}
- Outside circle: {what we don't know}
- Risk of unknowns: {assessment}
```

#### Thiel Lens (Monopoly Potential)

```markdown
## THIEL: MONOPOLY POTENTIAL

### Zero to One Check
- [ ] Creates something new (0→1)?
- [ ] Or copies existing (1→N)?

### Competition Analysis
- Current competition: {who}
- Future competition: {who might enter}
- Why we win: {defensibility}

### Contrarian Angle
- What do we believe that others don't?
- Why are others not pursuing this?

### Secret
- What do we know that others don't?
- Is this insight proprietary?
```

#### Naval Lens (Freedom & Leverage)

```markdown
## NAVAL: FREEDOM & LEVERAGE

### Leverage Type
| Type | Present | Notes |
|------|---------|-------|
| Code | {✓/✗} | {notes} |
| Media | {✓/✗} | {notes} |
| Capital | {✓/✗} | {notes} |
| Labor | {✓/✗} | {notes} |

### Freedom Impact
- Short-term: {more/less} freedom
- Long-term: {more/less} freedom
- Creates asset or sells time?

### Compounding
- Does this compound over time?
- Long-term game with long-term people?
```

#### Hoffman Lens (Network & Scale)

```markdown
## HOFFMAN: NETWORK & SCALE

### Network Effects
- Direct network effects: {present? how?}
- Indirect network effects: {present? how?}
- Data network effects: {present? how?}

### Scale Potential
- What works at 10x?
- What breaks at 100x?
- Winner-take-all market?

### Speed Requirement
- First-mover advantage important?
- Last-mover advantage possible?
- Timing criticality: {H/M/L}
```

#### Sivers Lens (Simplicity Check)

```markdown
## SIVERS: SIMPLICITY CHECK

### Hell Yeah Test
Is this a "HELL YEAH!" or just "interesting"?
{honest_answer}

### Opposite True
What if not pursuing this is the right answer?
{consideration}

### One Person Test
If we did this for ONE person perfectly, would it spread?
{analysis}

### Complexity Warning
Are we overcomplicating?
{assessment}
```

### Phase 3: Advisor Perspectives

```markdown
## ADVISOR PERSPECTIVES

### Bullish Voices
{Advisors who would recommend pursuing}

**{Advisor Name}:**
- Why pursue: {reasons}
- Best case: {scenario}

### Bearish Voices
{Advisors who would recommend passing}

**{Advisor Name}:**
- Why pass: {reasons}
- Risk highlighted: {concern}

### Key Debate
The central tension: {description}
```

### Phase 4: Decision Matrix

```markdown
## DECISION MATRIX

### Scoring (1-10)

| Criterion | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Strategic Fit | 25% | {score} | {weighted} |
| Risk/Return | 25% | {score} | {weighted} |
| Execution Ability | 20% | {score} | {weighted} |
| Freedom Impact | 15% | {score} | {weighted} |
| Timing | 15% | {score} | {weighted} |
| **TOTAL** | 100% | — | **{total}** |

### Interpretation
- 8.0+: Strong yes
- 6.5-8.0: Conditional yes
- 5.0-6.5: Needs more validation
- <5.0: Pass
```

### Phase 5: Recommendation

```markdown
## BOARD RECOMMENDATION

### Verdict
{PURSUE | PASS | CONDITIONAL | NEED MORE INFO}

### Rationale
{clear reasoning}

### If Pursuing - Key Conditions
1. {condition_1}
2. {condition_2}
3. {condition_3}

### If Passing - What Would Change Mind
1. {factor_1}
2. {factor_2}

### Next Steps
1. {action_1} - Owner: {name} - By: {date}
2. {action_2} - Owner: {name} - By: {date}
```

---

## Output

```yaml
outputs:
  - opportunity_brief: summary document
  - multi_lens_analysis: detailed analysis per framework
  - decision_matrix: scored evaluation
  - recommendation: final verdict with conditions
```

---

## Metadata

```yaml
task_id: opportunity-eval
category: evaluation
complexity: medium-high
duration: 30-45min
requires: board-chair + 3-5 advisors
version: "1.0"
```
