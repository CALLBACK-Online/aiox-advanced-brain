# Task: Squad Overview — Write

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `squad-overview-write` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: squad-overview-write
name: "Squad Overview — Write"
category: documentation
agent: squad-chief
elicit: false
autonomous: true
description: "Escreve o SQUAD-OVERVIEW.md, aplica checklist de saída e reporta o score final."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::squad_overview_write
Output: artifact::squad_overview_write
pre_condition: squad-overview-generate completed com markdown final disponível
post_condition: SQUAD-OVERVIEW.md escrito no root do squad com checklist de saída aplicado e score final reportado
performance: deterministic Worker, < 30s, fail-loud em write error ou checklist failure
Completion Criteria: SQUAD-OVERVIEW.md persistido AND checklist de saída PASS AND score final reportado
error_handling: fail-loud, persist evidence, escalate if unrecoverable
## Purpose

Persistir o overview no root do squad e aplicar as validações finais de
existência, completude e qualidade mínima.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_path` | string | Yes | Path do squad |
| `overview_document` | object | Yes | Saída de `squad-overview-generate` |
| `format` | string | No | `detailed` ou `compact` |

## Workflow

### Step 1: Gravar o arquivo

- Escrever `{squad_path}/SQUAD-OVERVIEW.md`
- Confirmar criação e tamanho final

### Step 2: Aplicar validação de saída

Checar:

- arquivo existe
- seções essenciais presentes
- sem placeholders
- comprimento adequado ao formato

### Step 3: Emitir relatório final

Responder com:

- path do arquivo
- linhas geradas
- score do checklist
- próximos passos sugeridos

## Output

```yaml
overview_report:
  output_path: ""
  line_count: 0
  quality_score: 0
  verdict: "PASS|CONDITIONAL|FAIL"
  next_action: ""
```


## Veto Conditions

- Generated overview from `squad-overview-generate` is missing -> BLOCK
- Write target path is not writable -> BLOCK
- Written file size is 0 bytes -> BLOCK (empty output)

## Acceptance Criteria

- [ ] `SQUAD-OVERVIEW.md` gravado no root do squad
- [ ] Checklist de saída aplicado
- [ ] Relatório final emitido com score e veredicto

## Related Documents

- `squad-overview.md` -- Task composta
- `checklists/squad-overview-checklist.md` -- Checklist de saída

---

_Task Version: 1.0.0_
