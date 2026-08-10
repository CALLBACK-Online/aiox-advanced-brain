# Task: Next Squad — Registry Scan

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `next-squad-registry` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: next-squad-registry
name: "Next Squad — Registry Scan"
category: planning
agent: squad-chief
elicit: false
autonomous: true
description: "Lê o registry do ecossistema e produz os buckets CREATE, IMPROVE e FIX."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::next_squad_registry
Output: artifact::next_squad_registry
pre_condition: ecosystem-registry.yaml acessível e parseável
post_condition: registry scan com buckets CREATE, IMPROVE e FIX produzidos e cobertura de domínio resumida
performance: deterministic Worker, < 30s, fail-loud se registry indisponível ou malformado
Completion Criteria: registry carregado AND buckets CREATE/IMPROVE/FIX produzidos AND cobertura de domínio resumida
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::next_squad_registry## Purpose

Estabelecer a visão factual do ecossistema antes de pontuar prioridades.


## Veto Conditions

- `ecosystem-registry.yaml` is inaccessible or unparseable -> BLOCK
- Candidate squad name already exists in the registry (duplicate) -> BLOCK

## Acceptance Criteria

- [ ] Registry carregado ou bloqueio explícito emitido
- [ ] Buckets CREATE, IMPROVE e FIX produzidos
- [ ] Cobertura de domínio resumida

## Related Documents

- `next-squad.md`
- `next-squad-signals.md`

---

_Task Version: 1.0.0_
