# Task: Rename Squad — Validate

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `rename-squad-validate` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: rename-squad-validate
name: "Rename Squad — Validate"
category: maintenance
agent: squad-chief
elicit: false
autonomous: true
description: "Executa grep residual, roda validate-squad no alvo renomeado e emite o relatório final do rename."
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::rename_squad_validate
Output: artifact::rename_squad_validate
pre_condition: rename-squad-propagate completed AND new_name squad directory pronto para validação
post_condition: grep residual zero refs, validate-squad PASS e relatório final do rename emitido
performance: < 15 min (Hybrid — grep residual + validate-squad + report), fail-loud se resíduos encontrados
Completion Criteria: grep residual == 0 relevant refs AND validate-squad --quick PASS AND rename report emitido
error_handling: fail-loud, persist evidence, escalate if unrecoverable

## Inputs

- request::rename_squad_validate## Purpose

Fechar o rename com verificação objetiva de resíduos, saúde estrutural e
preservação dos agent IDs internos.


## Veto Conditions

- Propagation from `rename-squad-propagate` did not complete -> BLOCK
- `validate-squad --quick` on the renamed squad returns FAIL -> BLOCK
- Residual grep for `old_name` returns > 0 references in critical paths -> BLOCK

## Acceptance Criteria

- [ ] Grep residual retorna zero refs relevantes
- [ ] `validate-squad {new_name} --quick` passa
- [ ] Relatório final do rename foi emitido

## Related Documents

- `rename-squad.md`
- `scripts/rename-squad.sh`

---

_Task Version: 1.0.0_
