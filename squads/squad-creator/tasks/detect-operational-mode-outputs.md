# Task: Detect Operational Mode — Output Signal

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `detect-operational-mode-outputs` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: detect-operational-mode-outputs
name: "Detect Operational Mode — Output Signal"
category: discovery
agent: squad-chief
elicit: false
autonomous: true
description: "Classifica os outputs esperados como operacionais, textuais ou mistos."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::detect_operational_mode_outputs
Output: artifact::detect_operational_mode_outputs
pre_condition: outputs_defined (lista de outputs esperados do squad) fornecida
post_condition: output_signal com outputs classificados como operacionais, textuais ou mistos
performance: deterministic Worker, < 30s, classification baseada em output types
Completion Criteria: cada output classificado AND signal type (operational/textual/mixed) emitido
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Usar os outputs definidos do squad como evidência objetiva do que ele precisa
produzir: artefatos textuais ou efeitos reais em sistemas.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `outputs_defined` | list | Yes | Lista de outputs esperados |

## Workflow

### Step 1: Classificar outputs operacionais

Marcar outputs que impliquem criação, modificação, sincronização, publicação,
notificação, upload, download ou geração real de arquivos/entidades.

### Step 2: Classificar outputs textuais

Marcar outputs que impliquem análise, recomendação, documentação, checklist,
framework, template ou relatório.

### Step 3: Emitir sinal de outputs

Aplicar a regra: qualquer output operacional torna o modo operacional por
default, salvo veto posterior.

## Output

```yaml
output_signal:
  operational_outputs: []
  textual_outputs: []
  operational_outputs_count: 0
  textual_outputs_count: 0
  mode_from_outputs: "OPERATIONAL|TEXTUAL"
```


## Veto Conditions

- `mode_report` input is missing or has no `primary_mode` field -> BLOCK
- Output path classification references directories outside `outputs/` and `workspace/` -> BLOCK

## Acceptance Criteria

- [ ] Outputs operacionais classificados
- [ ] Outputs textuais classificados
- [ ] Regra de predominância aplicada
- [ ] Sinal de outputs emitido

## Related Documents

- `detect-operational-mode.md` -- Task composta
- `detect-operational-mode-classify.md` -- Consolidação final

---

_Task Version: 1.0.0_
