---
task-id: enhance-heuristic
name: "Enhance Heuristic"
version: 1.0.0
execution_type: Agent
model: Opus
model_rationale: "Identifying promotion candidates and threshold/gate bindings requires deep semantic analysis."
haiku_eligible: false
estimated-time: 15 min
complexity: medium

inputs:
  required:
    - heuristic_id: "ID of the heuristic to enhance (e.g., AN_KE_085)"
  optional:
    - target_family: "KE→BS or KE→PM migration target"

outputs:
  primary:
    - enhancement_plan: "Proposed changes to heuristic (threshold binding, gate integration, family migration)"

elicit: true
---
<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: enhance-heuristic
  task_name: Enhance Heuristic
  status: pending
  responsible_executor: '@heuristic-ops'
  execution_type: Agent
  estimated_time: 15m
  domain: Tactical
  input:
  - heuristic_id
  - target_family (optional)
  output:
  - enhancement_plan
  action_items:
  - Read target heuristic and assess current maturity
  - Identify candidates for threshold binding (can this become a numeric gate?)
  - Identify candidates for family migration (KE→BS if process, KE→PM if product)
  - Generate enhancement plan with before/after
  acceptance_criteria:
  - Enhancement plan includes specific threshold values if applicable
  - Family migration rationale is evidence-based
  - No breaking changes to existing consumers of the heuristic
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: approval_required
  escalation_priority: medium
  coherence_threshold: 0.90
  error_behavior: raise
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Tactical
  atomic_layer: Atom
  executor: Agent
  pre_condition: "heuristic_id resolves to an existing heuristic file in minds/."
  post_condition: "enhancement_plan generated with proposed changes and rationale."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- AIOX_CONTRACT:END -->


# Task: Enhance Heuristic

## Purpose

Identify enhancement opportunities for a specific heuristic: threshold/gate binding, family migration (KE→BS/PM), or formalization into a rule.

## Steps

1. Read the target heuristic file
2. Assess maturity: is it observation-only (KE) or ready for process enforcement (BS)?
3. Check if a numeric threshold can be derived
4. Check if it should migrate to a different family
5. Generate enhancement plan

## Governance

- INV-02: Human gate — Pedro Valério approves all enhancements
- Enhancements MUST preserve backward compatibility with existing consumers
