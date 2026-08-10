# Task: Detect Operational Mode — External Systems Signal

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `detect-operational-mode-systems` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: detect-operational-mode-systems
name: "Detect Operational Mode — External Systems Signal"
category: discovery
agent: squad-chief
elicit: false
autonomous: true
description: "Detecta referências a sistemas externos e deriva APIs ou conexões necessárias."
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::detect_operational_mode_systems
Output: artifact::detect_operational_mode_systems
pre_condition: briefing bruto AND skills_detected opcionalmente fornecidas
post_condition: system_signal com plataformas externas, webhooks e serviços detectados que exigem runtime
performance: deterministic Worker, < 30s, pattern-based detection de service references
Completion Criteria: plataformas e serviços externos identificados AND necessidade de runtime operacional avaliada
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Determinar se o briefing pressupõe integração com plataformas externas,
webhooks, automações ou serviços locais que exigem runtime operacional.

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `briefing` | string | Yes | Briefing bruto do squad |
| `skills_detected` | list | No | Skills já detectadas para o squad |

## Workflow

### Step 1: Detectar plataformas e serviços

Escanear o briefing por referências a Ads, CRM, planilhas, mensageria, social
media, pagamentos, automação, geração multimodal e serviços locais.

### Step 2: Derivar conexões requeridas

Traduzir cada sistema detectado em uma conexão ou família de APIs esperada.

### Step 3: Emitir sinal de sistemas

Registrar sistemas detectados, conexões exigidas e o modo inferido a partir
desse eixo.

## Output

```yaml
system_signal:
  systems_detected: []
  api_connections_required: []
  mode_from_systems: "OPERATIONAL|TEXTUAL"
```


## Veto Conditions

- `mode_report` input is missing or has no `primary_mode` field -> BLOCK
- System classification references tools not in `data/tool-discovery-sources.yaml` -> WARN

## Acceptance Criteria

- [ ] Sistemas externos detectados ou ausência confirmada
- [ ] Conexões requeridas derivadas de forma explícita
- [ ] Sinal de sistemas emitido

## Related Documents

- `detect-operational-mode.md` -- Task composta
- `detect-operational-mode-outputs.md` -- Próxima fonte de sinal

---

_Task Version: 1.0.0_
