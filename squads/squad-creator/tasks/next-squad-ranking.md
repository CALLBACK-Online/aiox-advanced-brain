# Task: Next Squad — Ranking

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `next-squad-ranking` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: next-squad-ranking
name: "Next Squad — Ranking"
category: planning
agent: squad-chief
elicit: false
autonomous: true
description: "Ordena candidatos, separa buckets de ação e escolhe a trilha de execução recomendada."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::next_squad_ranking
Output: artifact::next_squad_ranking
pre_condition: next-squad-scoring completed com scores calculados para todos candidatos
post_condition: candidatos ordenados por prioridade com buckets CREATE/IMPROVE/FIX preservados e comandos sugeridos
performance: Agent, < 5 min, deterministic ranking com tie-breaking rules
Completion Criteria: candidatos ranqueados AND buckets preservados AND top candidate com comando executável sugerido
error_handling: fail-loud, persist error context, escalate to squad-chief

## Inputs

- request::next_squad_ranking## Purpose

Transformar scores em uma fila priorizada de ação com comando executável.


## Veto Conditions

- Scored candidates from `next-squad-scoring` is missing -> BLOCK
- All candidates scored below minimum viability threshold -> BLOCK (no viable squad to recommend)

## Acceptance Criteria

- [ ] Candidatos ranqueados por prioridade
- [ ] Buckets CREATE, IMPROVE e FIX preservados
- [ ] Cada top candidate tem comando sugerido

## Related Documents

- `next-squad.md`
- `next-squad-report.md`

---

_Task Version: 1.0.0_
