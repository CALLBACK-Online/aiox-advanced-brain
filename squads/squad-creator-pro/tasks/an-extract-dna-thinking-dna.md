<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: an-extract-dna-thinking-dna
  task_name: Extract DNA -- Thinking DNA
  status: pending
  responsible_executor: '@oalanicolas'
  execution_type: Agent
  estimated_time: 10m
  domain: Operational
  action_items:
    - Extract Primary Framework
    - Map Heuristics and Vetoes
    - Document Decision Architecture
  acceptance_criteria:
    - primary framework é explicitado
    - heuristics e veto conditions são documentadas
    - decision architecture fica action-oriented
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: review_only
  escalation_priority: medium
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Tactical
  atomic_layer: Atom
  executor: Agent
  pre_condition: "dna_layers e contexto de decisão já consolidados."
  post_condition: "thinking_dna documentado com framework mestre e heurísticas."
  performance: "bloquear output vago sem pipeline de decisão explícito."
```
<!-- AIOX_CONTRACT:END -->

# Task: Extract DNA -- Thinking DNA

## Purpose

Transformar modelos mentais implícitos em arquitetura de decisão reutilizável pelo clone.

## Output Contract

```yaml
output:
  thinking_dna:
    primary_framework: ""
    secondary_frameworks: []
    heuristics: []
    veto_conditions: []
    decision_architecture: {}
```
