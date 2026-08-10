# Task: Next Squad — Scoring

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `next-squad-scoring` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: next-squad-scoring
name: "Next Squad — Scoring"
category: planning
agent: squad-chief
elicit: false
autonomous: true
description: "Aplica as 5 dimensões de scoring aos candidatos usando evidência do registry e dos sinais coletados."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::next_squad_scoring
Output: artifact::next_squad_scoring
pre_condition: registry buckets e signals (ou skip) disponíveis com candidatos elegíveis
post_condition: candidatos pontuados nas 5 dimensões com fórmula composta explicitada e justificativa por score
performance: Agent, < 5 min, structured output com score breakdown por dimensão
Completion Criteria: 5 dimensões aplicadas AND fórmula composta explícita AND cada score com justificativa baseada em evidência
error_handling: fail-loud, persist error context, escalate to squad-chief

## Inputs

- request::next_squad_scoring## Purpose

Pontuar candidatos com uma lógica explícita e comparável, evitando ranking por
impressão.


## Veto Conditions

- Signal collection from `next-squad-signals` is missing or empty -> BLOCK
- Scoring formula references dimensions not present in collected signals -> BLOCK

## Acceptance Criteria

- [ ] 5 dimensões aplicadas aos candidatos elegíveis
- [ ] Fórmula composta explicitada
- [ ] Cada score tem justificativa baseada em evidência

## Related Documents

- `next-squad.md`
- `next-squad-ranking.md`

---

_Task Version: 1.0.0_
