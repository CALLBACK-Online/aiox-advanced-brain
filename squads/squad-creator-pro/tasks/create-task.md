<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: create-task
  task_name: Create Squad Task (Extension Wrapper)
  status: pending
  responsible_executor: '@squad-chief'
  execution_type: Worker
  estimated_time: 15m
  domain: Operational
  action_items:
    - Normalize Target Squad
    - Build Base Payload
    - Delegate to Base Workflow
    - Reconcile Outputs for Pro Callers
  acceptance_criteria:
    - "squads/squad-creator/workflows/wf-create-task.yaml existe"
    - "pack_name e squad_name são reconciliados corretamente"
    - "o wrapper não define pipeline paralelo"
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: review_only
  escalation_priority: medium
  coherence_threshold: 0.95
  error_behavior: raise
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Strategic
  atomic_layer: Atom
  executor: Worker
  pre_condition: "inputs, dependências e artefatos prévios resolvidos antes de iniciar a execução."
  post_condition: "output principal gerado, validado e pronto para handoff da próxima fase."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- AIOX_CONTRACT:END -->

# Task: Create Squad Task (Extension Wrapper)

**Task ID:** create-task
**Version:** 3.2.0
**Purpose:** manter compatibilidade do `squad-creator-pro` delegando a criação real de tasks ao pipeline atômico do `squad-creator`. A partir da v3.2.0 o wrapper aceita também um `task_object` V5 estruturado (seam do `aiox-squad-creator-gerar` / ADR §D-G), sem forkar os atomics.

## Canonical Owner

- `squads/squad-creator/workflows/wf-create-task.yaml`
- `squads/squad-creator/tasks/create-task-{classify,anatomy,executor,generate,validate,register}.md`

## Inputs

- `task_purpose` e `task_name` são obrigatórios (forma flat — chamadores legados)
- `squad_name` é preferido; `pack_name` é aceito como alias legado
- `source_framework`, `source_artifacts` e `integration_notes` apenas enriquecem a delegação
- `task_object` (OPCIONAL, V5 — seam do `aiox-squad-creator-gerar`): objeto V5 estruturado
  (`executor`, `inputs[]`, `outputs[]`, `depends_on[]`, `how_to`, `ac[]`, `artifact_template`).
  Quando presente, o wrapper deriva `task_purpose`/`task_name`/`squad_name` dele e delega ao MESMO
  workflow base — sem forkar atomics nem o quality gate (ver `v5_adapter` no Execution Contract).

## Preconditions

- [ ] `squads/squad-creator/workflows/wf-create-task.yaml` existe
- [ ] o alvo resolve para `squads/{squad_name}/`
- [ ] o chamador entende que o wrapper não possui pipeline próprio

## Execution Contract

```yaml
normalize_target:
  rules:
    - if: "squad_name vazio e pack_name presente"
      then: "set squad_name = pack_name"
    - if: "squad_name e pack_name divergem"
      then: "block and reconcile"

build_base_payload:
  required_fields: [task_purpose, task_name, squad_name]
  optional_context: [source_framework, source_artifacts, integration_notes, task_object]

v5_adapter:
  # STORY-181.W3.4 — accept a V5 task_object as input (ADR §D-G seam). The adapter only MAPS
  # the V5 fields onto the base payload; it never forks the create-task-* atomics nor the gate.
  when: "task_object is present"
  derive:
    - "task_name    <- task_object.id | task_object.name"
    - "task_purpose <- task_object.purpose | task_object.name + description"
    - "squad_name   <- caller-provided squad_name (unchanged)"
  pass_through_to_base:
    # the base anatomy/generate consume these pre-resolved V5 fields (skipped phases per D-G):
    - "executor          <- task_object.executor (slug; classify Step3 / anatomy Step3 skipped)"
    - "inputs            <- task_object.inputs[]  (anatomy Step4 skipped)"
    - "outputs           <- task_object.outputs[] (anatomy Step6 skipped)"
    - "depends_on        <- task_object.depends_on[]"
    - "steps             <- task_object.how_to (anatomy Step5 — HOW-TO nucleus, PRESERVED)"
    - "acceptance        <- task_object.ac[]"
    - "artifact_template <- task_object.artifact_template"
  contract:
    - use_base_classification   # classify Step1 skipped by the V5→input adapter; base still owns the phase shell
    - use_base_anatomy          # base anatomy fills only the non-pre-resolved fields
    - use_base_executor_design
    - use_base_generation
    - use_base_validation       # SC_TSK_001 (create-task-validate.md) — REUSED, never forked
    - use_base_registration
  prohibition:
    - "Do NOT recreate create-task-* atomics inside squad-creator-pro"
    - "Do NOT fork quality gates locally"

delegate_to_base:
  workflow: "squads/squad-creator/workflows/wf-create-task.yaml"
  contract:
    - use_base_classification
    - use_base_anatomy
    - use_base_executor_design
    - use_base_generation
    - use_base_validation
    - use_base_registration
  prohibition:
    - "Do NOT recreate create-task-* atomics inside squad-creator-pro"
    - "Do NOT fork quality gates locally"

reconcile_outputs:
  task_file: "squads/{squad_name}/tasks/{task_id}.md"
  delegated_workflow: "squads/squad-creator/workflows/wf-create-task.yaml"
  execution_mode: "base-delegated"
```

## Output

```yaml
output:
  task_file: "squads/{squad_name}/tasks/{task_id}.md"
  delegated_workflow: "squads/squad-creator/workflows/wf-create-task.yaml"
  normalized_squad_name: "{squad_name}"
  status: "delegated"
```

## Acceptance Criteria

- [ ] `pack_name` e `squad_name` são reconciliados corretamente
- [ ] a criação real da task é delegada ao workflow base
- [ ] nenhuma fase paralela de create-task existe no pro
- [ ] chamadores do pro continuam compatíveis
- [ ] quando `task_object` V5 é fornecido, `v5_adapter` deriva o payload e delega ao MESMO workflow base, sem forkar atomics nem o gate (SC_TSK_001 REUSADO)

## Veto Conditions

- `squad_name` e `pack_name` apontam para squads diferentes
- `wf-create-task.yaml` não existe no base
- algum chamador exige fase inventada fora do base

## Related Documents

- `squads/squad-creator/workflows/wf-create-task.yaml`
- `squads/squad-creator/tasks/create-task.md`
- `workflows/wf-context-aware-create-squad.yaml`
- `workflows/wf-research-then-create-agent.yaml`
