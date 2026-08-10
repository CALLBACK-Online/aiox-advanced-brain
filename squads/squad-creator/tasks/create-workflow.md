# Task: Create Squad Workflow (Composed)

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-workflow` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Composed` |

---


<!-- SINKRA_CONTRACT -->
Domain: `Tactical`
atomic_layer: Molecule
agent: squad-chief
Input: request::create_workflow
Output: artifact::create_workflow
pre_condition: workflow_purpose e squad_name fornecidos AND squad target existe com config.yaml válido
post_condition: workflow .yaml validado por SC_WFL_001, salvo em squads/{squad_name}/workflows/ e registrado em config.yaml
performance: Composed (3 sub-tasks), < 15 min total com elicitation, veto em quality gate bloqueia pipeline
Completion Criteria: workflow .yaml gerado com 3+ phases AND SC_WFL_001 PASS AND registrado em config.yaml e README
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief
## Execution Sequence

```
INPUT (workflow_purpose + squad_name)
    |
[1. CLASSIFY]     create-workflow-classify.md
    |              Workflow vs Task, identity, scope
    |
[2. DESIGN]       create-workflow-design.md
    |              Phases, tiers, agents, task_refs, handoffs,
    |              checkpoints, veto conditions, error handling
    |
[3. GENERATE]     create-workflow-generate.md
    |              YAML from template, SC_WFL_001, contract validation,
    |              config.yaml, README, handoff summary
    |
OUTPUT: Validated workflow file (.yaml) + registered in squad
```

## Sub-Task Reference

| # | Task ID | Phase | Responsibility | Executor |
|---|---------|-------|----------------|----------|
| 1 | `create-workflow-classify` | Classification | Workflow vs Task, identity, scope | Hybrid |
| 2 | `create-workflow-design` | Design | Phases, tiers, agents, task_refs, handoffs, gates, error handling | Hybrid |
| 3 | `create-workflow-generate` | Generation + Registration | YAML from template, validation, config.yaml, README, summary | Agent |

## Frameworks Used

- `data/tier-system-framework.md` -- Phase tier classification (Sub-task 2)
- `data/executor-matrix-framework.md` -- Agent assignment (Sub-task 2)
- `data/decision-heuristics-framework.md` -- Checkpoint logic (Sub-task 2)

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `workflow_purpose` | string | Yes | What the workflow should accomplish |
| `squad_name` | string | Yes | Target squad |

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Workflow File | `squads/{squad_name}/workflows/wf-{workflow_id}.yaml` | Complete workflow |
| Updated README | `squads/{squad_name}/README.md` | Workflow added |
| Updated Config | `squads/{squad_name}/config.yaml` | Workflow registered |

## Heuristics Reference

| Heuristic ID | Name | Sub-Task | Blocking |
|--------------|------|----------|----------|
| SC_WFL_PRE | Workflow Pre-Check | create-workflow-classify | Yes |
| SC_PHS_001 | Phases Defined | create-workflow-design | Yes |
| SC_AGN_001 | Agents Assigned | create-workflow-design | Yes |
| SC_CKP_001 | Checkpoints Complete | create-workflow-design | Yes |
| SC_WFL_001 | Workflow Quality Gate | create-workflow-generate | Yes |

## Error Handling

| Error | Sub-Task | Action |
|-------|----------|--------|
| Should be Task | classify | Redirect to `*create-task` |
| Fewer than 3 phases | design | Suggest combining or use task |
| Agent not in squad | design | Create agent or reassign |
| Validation fails | generate | Fix and re-validate (max 2 iterations) |

## Alternate Entry Point

**`create-workflow-from-sop.md`** -- SOP-to-workflow conversion. Separate entry point that feeds into this pipeline at the design phase.

## Veto Conditions

- Target squad directory does not exist or `config.yaml` is absent -> BLOCK
- A blocking sub-task in the execution sequence emits FAIL or ABORT -> BLOCK
- Workflow id already exists in `squads/{squad}/workflows/` (name collision) -> BLOCK

---

_Task Version: 4.0 (de-atomized)_
_Last Updated: 2026-03-27_
_Sub-tasks: 3 tasks (classify, design, generate)_
**Output Schema:** `squads/squad-creator/config/workflow-yaml-schema.yaml`

