---
task-id: detect-conflicts
name: "Detect Heuristic Conflicts"
version: 1.0.0
execution_type: Agent
model: Opus
model_rationale: "Semantic conflict detection requires deep comprehension of contradictory guidance."
haiku_eligible: false
estimated-time: 20 min
complexity: high

inputs:
  required:
    - minds_path: "Path to minds/ directory"
  optional:
    - scope: "intra_owner | inter_owner | constitution_risk (default: all)"

outputs:
  primary:
    - conflict_report: "Structured conflict scan with pairs, severity, and resolution suggestions"

elicit: true
---
<!-- SINKRA_TASK_METADATA:START -->
```yaml
sinkra_task_metadata:
  task_id: detect-conflicts
  task_name: Detect Heuristic Conflicts
  status: pending
  responsible_executor: '@heuristic-ops'
  execution_type: Agent
  estimated_time: 20m
  domain: Operational
  input:
  - minds_path
  - scope (optional)
  output:
  - conflict_report
  action_items:
  - Scan intra-owner conflicts (same owner, contradictory heuristics)
  - Scan inter-owner conflicts (cross-owner contradictions)
  - Scan constitution_risk (heuristic contradicts .aiox-core/constitution.md)
  - Score severity (LOW/MEDIUM/HIGH/CRITICAL)
  - Suggest resolution for each conflict
  acceptance_criteria:
  - All heuristic pairs with contradictory guidance are identified
  - Each conflict includes exact file references and contradictory excerpts
  - Constitution risk conflicts are flagged as CRITICAL
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: approval_required
  escalation_priority: high
  coherence_threshold: 0.90
  error_behavior: raise
```
<!-- SINKRA_TASK_METADATA:END -->

<!-- SINKRA_CONTRACT:START -->
```yaml
sinkra_contract:
  Domain: Operational
  atomic_layer: Atom
  executor: Agent
  pre_condition: "minds/ directory exists with heuristic files from at least 1 owner."
  post_condition: "conflict_report generated with all detected conflicts, severity scores, and resolution suggestions."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- SINKRA_CONTRACT:END -->


# Task: Detect Heuristic Conflicts

## Purpose

Scan heuristic files for three types of conflicts: intra-owner, inter-owner, and constitution risk.

## Conflict Types

1. **Intra-owner:** Same owner has two heuristics giving contradictory advice on the same topic.
2. **Inter-owner:** Different owners have heuristics that contradict each other (preserve both — use canonical_ref per INV-03).
3. **Constitution risk:** A heuristic contradicts a rule in `.aiox-core/constitution.md` (CRITICAL — must resolve).

## Output Format

```yaml
conflicts:
  - id: CONF-NNN
    type: intra_owner|inter_owner|constitution_risk
    severity: LOW|MEDIUM|HIGH|CRITICAL
    heuristic_a: { owner, file, id, stance }
    heuristic_b: { owner, file, id, stance }
    contradiction: "description of what contradicts"
    suggested_resolution: "..."
```
