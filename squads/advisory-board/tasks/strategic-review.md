# Strategic Review Task

**Command:** `/advisory-board:strategic-review`
**Agent:** board-chair + Tier 1 advisors
**Purpose:** Avaliação estratégica profunda de direção, posicionamento ou decisão major

---

## Overview

Sessão de alto nível para decisões estratégicas que afetam a direção do negócio. Envolve os conselheiros Tier 1 e usa múltiplos frameworks para análise abrangente.

---

## Input Requirements

```yaml
required:
  - strategic_question: string  # A pergunta central

optional:
  - options: list              # Opções já identificadas
  - timeline: string           # Horizonte da decisão
  - stakes: string             # O que está em jogo
  - constraints: list          # Limitações
```

---

## Framework Stack Applied

### 1. Munger Analysis (Risk & Mental Models)

```markdown
## MUNGER ANALYSIS

### Inversão
O que faria isso falhar espetacularmente?
- {failure_mode_1}
- {failure_mode_2}
- {failure_mode_3}

### Circle of Competence Check
- Onde temos expertise real: {areas}
- Onde estamos além do círculo: {areas}
- Gap analysis: {what we need to learn}

### Second-Order Effects
| First Order | Second Order | Third Order |
|-------------|--------------|-------------|
| {effect_1a} | {effect_1b}  | {effect_1c} |
| {effect_2a} | {effect_2b}  | {effect_2c} |

### Opportunity Cost
O que deixamos de fazer se escolhermos isso?
- {opportunity_1}
- {opportunity_2}
```

### 2. Thiel Analysis (Contrarian & Monopoly)

```markdown
## THIEL ANALYSIS

### The Contrarian Question
"O que você acredita sobre isso que a maioria discordaria?"
- {contrarian_insight}

### Zero to One Check
- [ ] Isso é genuinamente novo (0 to 1)?
- [ ] Ou apenas iteração (1 to N)?

### Monopoly Path
- Qual nicho pequeno podemos dominar completamente?
- Qual é a expansão natural a partir dele?
- Last mover advantage exists?

### Secret Identification
- Qual é o segredo que temos que outros não veem?
- Por que outros não viram isso?
```

### 3. Naval Analysis (Freedom & Leverage)

```markdown
## NAVAL ANALYSIS

### Leverage Check
| Type | Present? | How? |
|------|----------|------|
| Code | {yes/no} | {explanation} |
| Media | {yes/no} | {explanation} |
| Capital | {yes/no} | {explanation} |
| Labor | {yes/no} | {explanation} |

### Freedom Trajectory
- Em 1 ano: mais ou menos livre?
- Em 5 anos: mais ou menos livre?
- Isso cria asset ou vende tempo?

### Specific Knowledge
- Isso usa conhecimento único ou commodity?
- Parece "play" ou "work"?
```

### 4. Dalio Analysis (Principles & Systems)

```markdown
## DALIO ANALYSIS

### Principle Check
Qual princípio deveria guiar essa decisão?
- {principle_identified}

### The Machine View
- Estamos operando ou desenhando?
- Sistema atual suporta essa decisão?
- Que mudança sistêmica é necessária?

### Pain + Reflection
- Que dores passadas informam isso?
- Que princípio deveria ter existido antes?
```

---

## Synthesis Framework

```markdown
## STRATEGIC SYNTHESIS

### Convergence Map
| Framework | Recommends | Confidence |
|-----------|------------|------------|
| Munger    | {direction} | {H/M/L}   |
| Thiel     | {direction} | {H/M/L}   |
| Naval     | {direction} | {H/M/L}   |
| Dalio     | {direction} | {H/M/L}   |

### Key Tensions
Where frameworks conflict:
1. {tension_1}: {framework_a} vs {framework_b}
   Resolution: {how to think about this}

### Blind Spots Identified
What none of the frameworks adequately address:
- {blind_spot_1}
- {blind_spot_2}

### Final Strategic Recommendation

**Direction:** {recommendation}

**Confidence Level:** {high/medium/low}

**Key Assumptions:**
1. {assumption_1}
2. {assumption_2}

**Validation Needed:**
- {validation_1}
- {validation_2}

**Decision Criteria:**
If {condition}, then proceed
If {condition}, then reconsider
```

---

## Strategic Review Cadence

| Review Type | Frequency | Focus |
|-------------|-----------|-------|
| Direction Check | Quarterly | Are we on track? |
| Major Decision | As needed | Specific strategic choice |
| Annual Strategy | Yearly | Full strategic assessment |

---

## Output

```yaml
outputs:
  - strategic_analysis: multi-framework analysis document
  - recommendation: synthesized direction
  - validation_plan: what to test/learn
  - decision_record: for future reference
```

---

## Metadata

```yaml
task_id: strategic-review
category: strategy
complexity: high
duration: 60-90min
requires: board-chair + Tier 1 advisors
frameworks:
  - Munger Analysis
  - Thiel Contrarian
  - Naval Freedom Test
  - Dalio Principles
version: "1.0"
```
