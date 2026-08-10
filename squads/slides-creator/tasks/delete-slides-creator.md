# Delete Slides Creator Squad

<!-- AIOX accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- AIOX Domain: Tactical -->

## AIOX Validation Metadata

```yaml
task: delete-slides-creator
atomic_layer: Atom
responsavel_type: Human
Domain: Tactical
Input:
  - name: task_context
    type: object
Output:
  - name: task_artifact
    type: object
Pre_conditions:
  - task_context provided
Post_conditions:
  - task_artifact emitted or explicit blocker recorded
Acceptance_criteria:
  - explicit deletion intent confirmed by approver
  - dependent artifacts inventoried (squads/slides-creator/, downstream decks, docs)
  - removal plan documented before any filesystem operation
  - rollback path available (git history + handoff record)
Performance:
  duration_target: bounded by active workflow SLA
Error_handling:
  strategy: fail fast with explicit handoff blocker
```

**Task ID:** `delete-slides-creator`
**Pattern:** `SC-TP-001`

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Delete Slides Creator Squad |
| **status** | `pending` |
| **responsible_executor** | @squad-chief |
| **execution_type** | `Human` |
| **input** | Explicit delete request with approval |
| **output** | Removal plan or approved deletion |
| **action_items** | 4 steps |
| **acceptance_criteria** | 3 criteria |

## Action Items

1. Confirm explicit deletion intent.
2. Inventory artifacts under `squads/slides-creator/`, docs, and runtime state.
3. Check dependencies on `ds` or downstream decks.
4. Remove only after approval.

## Acceptance Criteria

- [ ] Deletion was explicitly requested
- [ ] Dependent artifacts were inventoried
- [ ] Removal plan is clear before execution
