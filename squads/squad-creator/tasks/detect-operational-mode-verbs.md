# Task: Detect Operational Mode — Verb Signal

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `detect-operational-mode-verbs` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: detect-operational-mode-verbs
name: "Detect Operational Mode — Verb Signal"
category: discovery
agent: squad-chief
elicit: false
autonomous: true
description: "Extrai verbos operacionais e textuais do briefing e produz o sinal lexical inicial."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::detect_operational_mode_verbs
Output: artifact::detect_operational_mode_verbs
pre_condition: briefing bruto do squad fornecido como input text
post_condition: verb_signal com lista de verbos operacionais vs textuais extraídos e ratio calculado
performance: deterministic Worker, < 30s, regex-based extraction sem LLM
Completion Criteria: verbos classificados em operacionais/textuais AND ratio calculado AND sinal lexical emitido
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Identificar, no texto do briefing, os verbos que sugerem execução real em sistemas
externos versus verbos que sugerem apenas análise, recomendação ou documentação.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `briefing` | string | Yes | Briefing bruto do squad |

## Workflow

### Step 1: Extrair verbos operacionais

Escanear o briefing por verbos e padrões como `create`, `send`, `post`,
`update`, `sync`, `trigger`, `publish`, `schedule`, `upload` e equivalentes em
PT-BR.

### Step 2: Extrair verbos textuais

Escanear o briefing por padrões como `recommend`, `analyze`, `suggest`,
`review`, `evaluate`, `assess`, `draft`, `outline` e equivalentes em PT-BR.

### Step 3: Emitir sinal lexical

Calcular contagens, listar evidências e produzir o sinal primário.

## Output

```yaml
verb_signal:
  operational_verbs: []
  textual_verbs: []
  operational_verb_count: 0
  textual_verb_count: 0
  primary_mode_signal: "OPERATIONAL|TEXTUAL|NONE"
```


## Veto Conditions

- Briefing text is empty or contains fewer than 10 words (insufficient signal) -> BLOCK
- No verbs extracted from the briefing (zero operational signals) -> BLOCK

## Acceptance Criteria

- [ ] Verbos operacionais extraídos do briefing
- [ ] Verbos textuais extraídos do briefing
- [ ] Contagens calculadas
- [ ] Sinal primário emitido

## Related Documents

- `detect-operational-mode.md` -- Task composta
- `detect-operational-mode-systems.md` -- Próxima fonte de sinal

---

_Task Version: 1.0.0_
