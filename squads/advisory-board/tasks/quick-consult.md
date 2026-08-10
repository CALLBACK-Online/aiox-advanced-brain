# Quick Consult Task

**Command:** `/advisory-board:quick-consult`
**Agent:** single advisor or board-chair
**Purpose:** Consulta rápida com conselheiro específico sobre questão pontual

---

## Overview

Para situações onde você precisa de uma perspectiva específica rapidamente, sem uma sessão completa do board. Ideal para:
- Decisões menores que precisam de um segundo olhar
- Quando você sabe qual perspectiva precisa
- Validação rápida de raciocínio
- Coaching moment específico

---

## Input Requirements

```yaml
required:
  - question: string     # A pergunta ou situação

optional:
  - advisor: string      # Conselheiro específico (auto-select se omitido)
  - context: string      # Contexto adicional
  - urgency: enum        # low | medium | high
```

---

## Advisor Quick-Select Guide

| Situação | Conselheiro | Porquê |
|----------|-------------|--------|
| "Devo entrar nesse mercado competitivo?" | **Thiel** | Monopoly vs competition thinking |
| "Como lidar com conflito na equipe?" | **Lencioni** | Team dynamics expert |
| "Isso vai me dar mais ou menos liberdade?" | **Naval** | Freedom & leverage focus |
| "Qual é o risco que não estou vendo?" | **Munger** | Inversão and risk |
| "Estou complicando demais?" | **Sivers** | Simplicity advocate |
| "Devo escalar ou manter pequeno?" | **Hoffman** vs **Sivers** | Opposing views |
| "Como falar sobre algo difícil?" | **Brown** | Vulnerability & courage |
| "Qual é o propósito aqui?" | **Sinek** | Purpose champion |
| "Devo comprometer meus valores?" | **Chouinard** | Values guardian |
| "Qual princípio deveria guiar isso?" | **Dalio** | Principled decision-making |

---

## Quick Consult Format

### Request

```markdown
## QUICK CONSULT REQUEST

**To:** {advisor_name}
**From:** Alan
**Urgency:** {low/medium/high}

### Situation
{brief description}

### My Current Thinking
{what I'm leaning towards}

### What I Need
{type of input: validation, challenge, alternative perspective, etc.}
```

### Response

```markdown
## {ADVISOR_NAME} RESPONSE

### My Take
{direct answer using advisor's framework}

### Key Question for You
{one probing question}

### If I Were You
{specific actionable suggestion}

### Watch Out For
{risk or blind spot from this advisor's perspective}
```

---

## Common Quick Consult Patterns

### The Validation Ask
"I'm thinking X, am I missing something?"
→ Get confirmation or challenge

### The Tiebreaker
"I'm torn between A and B"
→ Get a perspective that breaks the tie

### The Sanity Check
"This feels off but I can't articulate why"
→ Help surface the discomfort

### The Courage Boost
"I know what I should do but..."
→ Get the push to act

### The Risk Check
"What could go wrong here?"
→ Get the inversão analysis

---

## Example Invocations

```
/advisory-board:quick-consult
question: "Should I hire my first employee or keep solo?"
advisor: naval
```

```
/advisory-board:quick-consult
question: "My co-founder and I disagree on pricing strategy"
# Auto-selects based on topic
```

```
/advisory-board:quick-consult
question: "I'm avoiding a difficult conversation"
advisor: brown
urgency: high
```

---

## Quick Consult vs Full Session

| Use Quick Consult When | Use Full Session When |
|------------------------|----------------------|
| Single perspective needed | Multiple viewpoints needed |
| Time-constrained | Can invest 30-60 min |
| Lower stakes decision | High stakes decision |
| Clear which advisor helps | Unsure who to consult |
| Validation/sanity check | Deep analysis needed |

---

## Output

```yaml
outputs:
  - advisor_response: targeted advice
  - key_question: follow-up to consider
  - suggested_action: specific next step
```

---

## Metadata

```yaml
task_id: quick-consult
category: consultation
complexity: low
duration: 5-10min
requires: single advisor
version: "1.0"
```
