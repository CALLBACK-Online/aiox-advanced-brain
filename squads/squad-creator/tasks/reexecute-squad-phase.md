# Task: Reexecute Squad Phase

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `reexecute-squad-phase` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Veto Conditions

```yaml
veto_conditions:
  - id: "VETO-REEXEC-001"
    condition: "Backup commit missing or not verifiable before cleanup"
    trigger: "Before deleting phase-scoped artifacts or rerunning phase steps"
    block_behavior: "BLOCK reexecution; require validated backup_ref (git commit SHA) first"

  - id: "VETO-REEXEC-002"
    condition: "Downstream impact summary not generated"
    trigger: "Before explicit user confirmation"
    block_behavior: "BLOCK reexecution; require impact report and explicit confirmation"
```

## Why

```
Brownfield improvements need safe retries.
Reexecution must preserve recoverability.
```

---


<!-- AIOX_CONTRACT -->
Domain: `Strategic`
atomic_layer: Atom
agent: squad-chief
Input: request::reexecute_squad_phase
Output: artifact::reexecute_squad_phase
pre_condition: squad_name e phase_id fornecidos AND backup commit verificável (VETO-REEXEC-001) AND impact report gerado
post_condition: phase re-executada com backup preservado, artifacts regenerados e impact summary emitido
performance: < 15 min (Hybrid — impact analysis + user confirmation + phase rerun), BLOCK sem backup verificável
Completion Criteria: backup validado AND phase re-executada AND downstream impact assessed AND artifacts regenerados
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief
## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Target squad |
| `workflow_id` | string | Yes | Workflow to reexecute |
| `phase_id` | string | Yes | Phase to rerun |
| `reason` | text | Yes | Why rerun is required |

---

## Safety Protocol

1. Snapshot phase inputs/outputs.
2. Commit backup with message: `backup: {squad_name} {workflow_id} {phase_id}`.
3. Show impacted downstream phases.
4. Require explicit confirmation.
5. Clean only phase-scoped artifacts.
6. Reexecute phase task list.
7. Run targeted validation.

---

## Output

```yaml
reexecution_report:
  squad_name: "..."
  workflow_id: "..."
  phase_id: "..."
  backup_ref: "git-commit-sha"
  cleaned_artifacts:
    - "..."
  rerun_status: success | fail
  downstream_impacts:
    - "..."
  rollback_instructions: "git checkout {sha} -- <paths>"
  schema_ref: squads/squad-creator/config/workflow-yaml-schema.yaml

```

---

## Validation

- Backup commit created before cleanup.
- No non-phase artifacts removed.
- Target phase completed with no blocking errors.
