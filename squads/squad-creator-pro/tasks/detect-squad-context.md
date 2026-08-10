---
task-id: detect-squad-context
name: "Detect Squad Context"
version: 1.0.0
execution_type: Agent
model: Sonnet
model_rationale: "Context detection is pattern-matching against known squad structures — Sonnet sufficient."
haiku_eligible: true
estimated-time: 5 min
complexity: low

inputs:
  required:
    - squad_path: "Path to the target squad directory"
  optional:
    - depth: "shallow | deep (default: shallow)"

outputs:
  primary:
    - context_report: "Squad context assessment: existing artifacts, state, version, dependencies"

elicit: false
---
<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: detect-squad-context
  task_name: Detect Squad Context
  status: pending
  responsible_executor: '@squad-chief'
  execution_type: Agent
  estimated_time: 5m
  domain: Tactical
  input:
  - squad_path
  - depth (optional)
  output:
  - context_report
  action_items:
  - Read config.yaml to detect squad version, type, and status
  - Inventory agents, tasks, workflows, templates, data, checklists, scripts
  - Detect brownfield vs greenfield state
  - Identify dependencies and cross-squad references
  - Assess AIOX compliance level (Tier 1/2/3)
  acceptance_criteria:
  - Context report accurately reflects current squad state
  - Brownfield/greenfield classification is correct
  - All cross-squad dependencies identified
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: review_only
  escalation_priority: low
  coherence_threshold: 0.95
  error_behavior: raise
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Tactical
  atomic_layer: Atom
  executor: Agent
  pre_condition: "squad_path exists and contains config.yaml."
  post_condition: "context_report generated with complete squad state assessment."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- AIOX_CONTRACT:END -->


# Task: Detect Squad Context

## Purpose

Preflight task for squad creation and upgrade workflows. Detects existing squad state to determine whether to proceed as brownfield (upgrade) or greenfield (create).

## Used By

- `workflows/modules/module-discovery.yaml` — discovery-context phase
- `workflows/wf-create-squad.yaml` — preflight_task
- `workflows/wf-brownfield-upgrade-squad.yaml` — via module-discovery import

## Steps

1. Read `{squad_path}/config.yaml` — extract version, type, status
2. Glob agents, tasks, workflows, templates, data, checklists, scripts
3. Classify: brownfield (config exists + tasks > 0) vs greenfield
4. Detect dependencies from `composition_mapping` and `squad-io.yaml`
5. Assess AIOX tier from structure completeness
