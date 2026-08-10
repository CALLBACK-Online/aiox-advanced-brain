# Task: Next Squad — Signals

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `next-squad-signals` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: next-squad-signals
name: "Next Squad — Signals"
category: planning
agent: squad-chief
elicit: false
autonomous: true
description: "Coleta sinais adicionais de demanda em modo deep ou emite skip explícito em modo quick."
accountability:
  human: squad-operator
  scope: full
domain: Tactical

```


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Atom
Input: request::next_squad_signals
Output: artifact::next_squad_signals
pre_condition: next-squad-registry completed com buckets CREATE/IMPROVE/FIX AND mode (quick/deep) definido
post_condition: sinais de demanda coletados (deep) ou skip_reason emitido (quick), evidências separadas do scoring
performance: < 15 min (Hybrid — deep scan) ou < 30s (quick skip), escalate se sinais conflitantes
Completion Criteria: modo quick com skip explícito OR modo deep com sinais de outputs/git/runtime coletados
error_handling: escalate to squad-chief on failure, persist error context

## Inputs

- request::next_squad_signals## Purpose

Adicionar contexto de demanda real sem acoplar o fluxo rápido a scans pesados.


## Veto Conditions

- `ecosystem-registry.yaml` is inaccessible or unparseable -> BLOCK
- No active stories or epics found to extract demand signals from -> WARN (proceed with ecosystem-only signals)

## Acceptance Criteria

- [ ] Modo `quick` produz skip explícito
- [ ] Modo `deep` coleta sinais de local_docs, git e runtime
- [ ] Evidências ficam separadas do scoring

## Related Documents

- `next-squad.md`
- `next-squad-scoring.md`

---

_Task Version: 1.0.0_
