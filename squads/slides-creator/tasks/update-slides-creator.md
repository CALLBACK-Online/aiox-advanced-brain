# Update Slides Creator Squad

<!-- SINKRA accountability: producer owns output integrity; qa-inspector or human reviewer owns validation before release. -->

<!-- SINKRA Domain: Tactical -->

## SINKRA Validation Metadata

```yaml
task: update-slides-creator
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
  - all updated files are syntactically valid (YAML/Markdown)
  - CHANGELOG.md has a new entry with version delta
  - config.yaml version field reflects the update (semver bump)
  - npm run validate:yaml:changed passes for modified files
  - downstream consumers (ds delivery contract) unaffected or migration documented
Performance:
  duration_target: bounded by active workflow SLA
Error_handling:
  strategy: fail fast with explicit handoff blocker
```

**Task ID:** `update-slides-creator`
**Pattern:** `SC-TP-001`

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Update Slides Creator Squad |
| **status** | `pending` |
| **responsible_executor** | @squad-chief |
| **execution_type** | `Agent` |
| **input** | Change request, PRD delta, app surface change |
| **output** | Updated squad files, CHANGELOG entry, version bump |
| **action_items** | 5 steps |
| **acceptance_criteria** | 4 criteria |

## Action Items

1. Identify affected artifact scope.
2. Apply changes without breaking `ds` delivery contract.
3. Update docs and runtime artifacts if the contract changes.
4. Add CHANGELOG entry and version bump.
5. Re-run validation.

## Acceptance Criteria

- [ ] Updated files are syntactically valid
- [ ] CHANGELOG has a new entry
- [ ] `config.yaml` version reflects the update
- [ ] validation completed
