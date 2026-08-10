# Task: Validate Final Artifacts

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `validate-final-artifacts` |
| **Version** | `2.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Cardinal Rule

```
Validate final deliverables, not process traces.
A squad passes only if final artifacts are production-ready.
```

---


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
agent: squad-chief
Input: request::validate_final_artifacts
Output: artifact::validate_final_artifacts
pre_condition: squad criado com todos required artifacts (config.yaml, agents/*.md, tasks/*.md, workflows/*.yaml, README.md)
post_condition: final artifact validation com structure gate, schema gate e semantic quality assessment
performance: < 15 min (Hybrid — deterministic gates + Agent semantic assessment), blocking quality gate
Completion Criteria: structure gate PASS AND all required files exist AND entry agent valid AND no broken path references
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief

## Inputs

- request::validate_final_artifacts## Final Targets

```yaml
required_artifacts:
  - config.yaml
  - agents/*.md
  - tasks/*.md
  - workflows/*.yaml
  - README.md
  - .claude/skills/*/{entry_agent}/SKILL.md
  - .agents/skills/{entry_agent}/SKILL.md

optional_but_scored:
  - checklists/*.md
  - templates/*
  - data/*
```

---

## Hard Gates

1. `Structure Gate` (blocking)
- All required files exist.
- Entry agent is valid and referenced.
- No broken internal path references.

2. `Execution Gate` (blocking)
- At least one runnable workflow exists.
- Task references resolve to existing files.
- No circular phase dependency in workflows.

3. `Quality Gate` (blocking)
- `validate-squad` score >= 7.0.
- No critical security findings.
- No veto condition triggered.

4. `Chief Activation Gate` (blocking)
- Chief slash skill exists in `.claude/skills/*/{entry_agent}/SKILL.md`.
- Chief Codex skill exists in `.agents/skills/{entry_agent}/SKILL.md`.

5. `Usability Gate` (warning)
- README includes activation and example commands.
- At least one end-to-end example path.

---

## Output

```yaml
final_artifact_report:
  result: PASS | CONDITIONAL | FAIL
  score: 0-10
  blocking_failures:
    - id: "..."
      reason: "..."
  warnings:
    - "..."
  recommended_fixes:
    - "..."
  schema_ref: squads/squad-creator/config/workflow-yaml-schema.yaml

```

## Veto Conditions

- Any blocking gate (Structure, Execution, Quality, Chief Activation) emits FAIL -> BLOCK
- Artifact paths referenced in the validation do not exist on the filesystem -> BLOCK
- Self-test scripts fail to execute (non-zero exit code on `--help` or basic invocation) -> BLOCK

---

## Success Criteria

- All blocking gates pass.
- Report generated at `.aiox/squad-runtime/squad-validation/{squad_name}/final-artifacts.yaml`.
