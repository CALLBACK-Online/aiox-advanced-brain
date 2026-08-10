---
task-id: build-reverse-index
name: "Build Reverse Index"
version: 1.0.0
execution_type: Agent
model: Sonnet
model_rationale: "Reverse index construction is pattern-matching across files — Sonnet sufficient."
haiku_eligible: true
estimated-time: 10 min
complexity: medium

inputs:
  required:
    - minds_path: "Path to minds/ directory"
  optional:
    - scope: "rules | tokens | vetos | all (default: all)"

outputs:
  primary:
    - reverse_index: "Mapping of rules/tokens/vetos to their dependent heuristics"

elicit: false
---
<!-- SINKRA_TASK_METADATA:START -->
```yaml
sinkra_task_metadata:
  task_id: build-reverse-index
  task_name: Build Reverse Index
  status: pending
  responsible_executor: '@heuristic-ops'
  execution_type: Agent
  estimated_time: 10m
  domain: Operational
  input:
  - minds_path
  - scope (optional)
  output:
  - reverse_index
  action_items:
  - Scan all heuristic files for references to rules, tokens, and vetos
  - Build reverse mapping (rule/token/veto → list of heuristics that reference it)
  - Identify orphan rules (declared but no heuristic references)
  - Identify heuristics with broken references (cite non-existent rules)
  acceptance_criteria:
  - Reverse index covers 100% of heuristic files
  - Each entry includes exact file path and line number
  - Orphan rules and broken references flagged
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: review_only
  escalation_priority: low
  coherence_threshold: 0.95
  error_behavior: raise
```
<!-- SINKRA_TASK_METADATA:END -->

<!-- SINKRA_CONTRACT:START -->
```yaml
sinkra_contract:
  Domain: Operational
  atomic_layer: Atom
  executor: Agent
  pre_condition: "minds/ directory exists with heuristic files."
  post_condition: "reverse_index generated mapping all rules/tokens/vetos to their dependent heuristics."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- SINKRA_CONTRACT:END -->


# Task: Build Reverse Index

## Purpose

Map which rules, tokens, and vetos depend on which heuristics. Enables impact analysis when modifying or archiving heuristics.

## Output Format

```yaml
reverse_index:
  rules:
    - rule_id: "INV-01"
      referenced_by:
        - { file: "minds/alan_nicolas/heuristics/AN_KE_085.md", line: 42 }
  tokens:
    - token_id: "TKF-001"
      referenced_by: [...]
  vetos:
    - veto_id: "V1"
      referenced_by: [...]

orphans:
  rules_not_referenced: [...]
  broken_references: [...]
```
