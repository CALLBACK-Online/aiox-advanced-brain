---
task-id: promote-heuristic
name: "Promote Heuristic"
version: 1.0.0
execution_type: Agent
model: Opus
model_rationale: "Promotion requires semantic validation of eligibility, backlink generation, and target placement."
haiku_eligible: false
estimated-time: 15 min
complexity: medium

inputs:
  required:
    - heuristic_id: "ID of heuristic to promote"
  optional:
    - source: "skill_execution — promote from learning entries"
    - skill: "specific skill to filter learning entries"

outputs:
  primary:
    - promotion_result: "Promotion outcome with backlinks, target location, and updated files"

elicit: true
---
<!-- SINKRA_TASK_METADATA:START -->
```yaml
sinkra_task_metadata:
  task_id: promote-heuristic
  task_name: Promote Heuristic
  status: pending
  responsible_executor: '@heuristic-ops'
  execution_type: Agent
  estimated_time: 15m
  domain: Tactical
  input:
  - heuristic_id
  - source (optional)
  - skill (optional)
  output:
  - promotion_result
  action_items:
  - Check eligibility (promotion_score >= 3.5 for Pattern/Anti-Pattern, >= 4.0 for Rule/Veto)
  - Execute promotion (create L2 card + L3 doc in minds/)
  - For Rules/Vetos, inline to target SKILL.md sections
  - Maintain bidirectional backlinks (INV-05)
  - Mark promoted entries status promoted in .aiox/learning/entries/
  acceptance_criteria:
  - Promotion eligibility verified against threshold
  - Bidirectional backlinks created (source → target AND target → source)
  - Human approval obtained before execution (INV-02)
  - Learning entries marked as promoted if --source skill_execution
  output_persistence: transient_output
  accountable_id: Human:Squad_Operator
  accountability_scope: approval_required
  escalation_priority: medium
  coherence_threshold: 0.90
  error_behavior: raise
```
<!-- SINKRA_TASK_METADATA:END -->

<!-- SINKRA_CONTRACT:START -->
```yaml
sinkra_contract:
  Domain: Tactical
  atomic_layer: Atom
  executor: Agent
  pre_condition: "heuristic_id resolves to an existing heuristic. Human approval obtained."
  post_condition: "heuristic promoted with bidirectional backlinks. Learning entries marked if applicable."
  performance: "executar dentro do SLA declarado, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- SINKRA_CONTRACT:END -->


# Task: Promote Heuristic

## Purpose

Check eligibility, execute promotion, and maintain bidirectional backlinks for heuristic promotion.

## Promotion Flow

1. **Check eligibility:** `promotion_score >= 3.5` (Pattern/Anti-Pattern) or `>= 4.0` (Rule/Veto)
2. **Human gate:** Present candidate to operator for approval (INV-02)
3. **Execute promotion:** Create L2 decision card + L3 documentation in `minds/{owner}/heuristics/`
4. **Inline to skills:** For Rules/Vetos, add to target `SKILL.md` ## Rules or ## Vetos sections
5. **Backlinks:** Create bidirectional references (INV-05)
6. **Mark promoted:** If `--source skill_execution`, update `.aiox/learning/entries/` status

## Governance

- INV-02: Human gate — no promotion without explicit approval
- INV-05: Backlinks bidirectional obrigatórios em TODO promotion path
- RT-LEARNING-001: No Learning Entry promoted without explicit RECORD
