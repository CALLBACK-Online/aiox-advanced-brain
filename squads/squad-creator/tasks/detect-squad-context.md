# Task: Detect Squad Context

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `detect-squad-context` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Core Principle

```
Wrong context selection creates wrong architecture.
Detect first, then build.
```

---


<!-- AIOX_CONTRACT -->
Domain: `Tactical`
atomic_layer: Atom
agent: squad-chief
Input: request::detect_squad_context
Output: artifact::detect_squad_context
pre_condition: domain fornecido AND squad_name ou intent opcionalmente fornecidos
post_condition: context type detectado (greenfield/brownfield/upgrade) com rota de criação selecionada
performance: < 15 min (Hybrid — script detection + Agent para ambiguity), elicitation apenas se sinais conflitantes
Completion Criteria: context type classificado AND rota de criação/upgrade selecionada AND sem ambiguidade residual
error_handling: fail-loud, persist error context, escalate to squad-chief
## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `domain` | string | Yes | Domain to create/upgrade |
| `squad_name` | string | No | Existing or desired squad slug |
| `intent` | enum | No | `create`, `upgrade`, `unsure` |

---

## Accountability

```yaml
accountability:
  human: squad-operator
  scope: full
```

## Context Categories

```yaml
contexts:
  greenfield_pure:
    signal: "No existing squad and no prior artifacts"
    action: "Run greenfield creation workflow"

  pre_existing_brief:
    signal: "PRD/brief exists but squad folder is missing or partial"
    action: "Create using brief as source of truth"

  legacy_assets:
    signal: "Squad exists with assets but missing current standards"
    action: "Route to brownfield upgrade workflow"

  partial_squad:
    signal: "Squad exists with incomplete structure"
    action: "Resume creation with gap fill"
```

**Output Schema:** `squads/squad-creator/config/workflow-yaml-schema.yaml`

## Veto Conditions

```yaml
veto_conditions:
  - id: "VETO-CTX-001"
    condition: "Target path is not a valid squad directory (missing canonical markers)"
    trigger: "Before assigning context category"
    block_behavior: "BLOCK detection result; require valid squad path or explicit greenfield intent"

  - id: "VETO-CTX-002"
    condition: "Confidence below 0.70 with conflicting evidence"
    trigger: "After confidence scoring"
    block_behavior: "BLOCK autonomous routing; require user confirmation from offered options"
```

---

## Detection Flow

1. Check `squads/{squad_name}/` existence.
2. Check presence of `config.yaml`, `agents/`, `tasks/`, `workflows/`.
3. Scan for PRD/brief references in `docs/` and `.aiox/squad-runtime/`.
4. Build confidence score per context.
5. If confidence < 0.70, ask user with 3 options.

---

## Outputs

```yaml
context_detection:
  detected_context: greenfield_pure | pre_existing_brief | legacy_assets | partial_squad
  confidence: 0.0-1.0
  recommended_workflow: wf-context-aware-create-squad | wf-brownfield-upgrade-squad
  evidence:
    - file_or_signal: "..."
      impact: "..."
  next_action: "..."
```

---

## Validation

- Context assigned with confidence >= 0.70, or user-confirmed.
- Recommended workflow exists and is executable.
- Decision evidence saved in logs.
