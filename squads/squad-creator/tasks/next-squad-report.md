# Task: Next Squad — Report

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `next-squad-report` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: next-squad-report
name: "Next Squad — Report"
category: planning
agent: squad-chief
elicit: false
autonomous: true
description: "Emite o relatório final com top 3, quick wins e trilha de execução sugerida."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::next_squad_report
Output: artifact::next_squad_report
pre_condition: next-squad-ranking completed com candidatos priorizados e comandos sugeridos
post_condition: relatório final com top 3, quick wins e trilha de execução sugerida, opcionalmente persistido
performance: Agent, < 5 min, structured output com recomendação acionável
Completion Criteria: top 3 apresentado com rationale AND quick wins listados AND opção de persistir scores suportada
error_handling: fail-loud, persist error context, escalate to squad-chief

## Inputs

- request::next_squad_report## Purpose

Entregar uma recomendação acionável e legível, com possibilidade de salvar o
snapshot de scores quando solicitado.


## Veto Conditions

- Ranking output from `next-squad-ranking` is missing -> BLOCK
- Report generated with zero recommended candidates -> BLOCK (empty recommendation is not actionable)

## Acceptance Criteria

- [ ] Top 3 apresentado com rationale
- [ ] Quick wins listados quando existirem
- [ ] Opção de persistir scores suportada

## Related Documents

- `next-squad.md`
- `.aiox/squad-runtime/next-squad/`

---

_Task Version: 1.0.0_
