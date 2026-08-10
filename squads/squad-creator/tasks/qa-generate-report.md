# Task: QA Generate Report

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `qa-generate-report` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: qa-generate-report
name: QA Generate Report
category: qa-validation
agent: squad-chief
elicit: false
autonomous: true
description: >
  Aggregate results from all QA check tasks, calculate final score,
  determine overall verdict, generate formatted report, and take
  appropriate action (PASS/CONDITIONAL/FAIL).
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::qa_generate_report
Output: artifact::qa_generate_report
pre_condition: todos 5 QA checks (structure, schema, references, completeness, compatibility) completados com resultados disponíveis
post_condition: qa_report.md gerado com final_score, verdict (PASS/CONDITIONAL/FAIL) e recommendations acionáveis
performance: Agent, < 5 min, structured output com score breakdown por dimensão
Completion Criteria: report gerado com verdict explícito AND score breakdown per check AND recommendations priorizadas
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Consolidate all QA check results into a single report with a final score, overall verdict, and actionable recommendations. This is the terminal task in the qa-after-creation pipeline -- it produces the deliverable that the user sees.

## Prerequisites

- [ ] qa-check-structure has completed
- [ ] qa-check-schema has completed
- [ ] qa-check-references has completed
- [ ] qa-check-completeness has completed
- [ ] qa-check-compatibility has completed

## Inputs

```yaml
inputs:
  - name: created_component
    type: string
    required: true
    description: "Path to created component"

  - name: component_type
    type: enum
    required: true
    values: ["squad", "agent", "task", "workflow", "template"]
    description: "Type of component created"

  - name: creation_task
    type: string
    required: false
    description: "Task that triggered this QA"

  - name: structure_result
    type: object
    required: true
    source: qa-check-structure

  - name: schema_result
    type: object
    required: true
    source: qa-check-schema

  - name: references_result
    type: object
    required: true
    source: qa-check-references

  - name: completeness_result
    type: object
    required: true
    source: qa-check-completeness

  - name: compatibility_result
    type: object
    required: true
    source: qa-check-compatibility
```

## Workflow

### Step 1: Determine Overall Verdict

Apply verdict logic in priority order:

1. If any input has `verdict: "ABORT"` --> overall verdict is **FAIL**
2. If `compatibility_result.security.high_severity > 0` --> overall verdict is **FAIL**
3. If `completeness_result.final_score < 5.0` --> overall verdict is **FAIL**
4. If `completeness_result.final_score >= 5.0 and < 7.0` --> overall verdict is **CONDITIONAL**
5. If all checks pass and `completeness_result.final_score >= 7.0` --> overall verdict is **PASS**

### Step 2: Aggregate Issues

Collect all issues from every check into two categories:

**Blocking issues** (must fix before delivery):
- Structure ABORTs
- Schema FAILs
- Broken references
- HIGH security findings
- Veto conditions triggered

**Warnings** (should fix, not blocking):
- Markdown formatting issues
- Missing recommended governance framework fields
- Orphan files
- MEDIUM security findings
- Score below 7.0 but above 5.0

### Step 3: Generate Report

Report sections: `header` (component, type, created_by, qa_date), `summary` (result, score, issues_found, security_issues), per-check sections (structure, schema, references, completeness, compatibility), `issues` (blocking[] and warnings[] with issue/location/fix), `recommendation` (action: PROCEED|FIX_REQUIRED|REVIEW, message).

### Step 4: Take Action Based on Verdict

**On PASS (score >= 7.0, 0 HIGH security):**
- Log success
- Mark component as validated
- Output: "QA PASSED: {component} (Score: {score})"
- Create validation badge at `{component}/docs/VALIDATED.md`

**On CONDITIONAL (score >= 5.0 and < 7.0, 0 HIGH security):**
- Log warnings
- Output: "QA CONDITIONAL: {component} (Score: {score})"
- List issues to fix
- Present: "Proceed anyway? Issues found: {count}"

**On FAIL (score < 5.0 OR HIGH security):**
- Log failure
- Output: "QA FAILED: {component}"
- List blocking issues
- Block: "Cannot proceed. Fix {count} blocking issues."
- Offer: "*fix-issues {component}"

### Step 5: Generate Machine-Readable JSON Report (C4 — EPIC-109 Wave 1)

In addition to the markdown report, produce a JSON twin validated against
`schemas/validation-report.schema.json`.

**JSON report structure:**
```json
{
  "squad_name": "{component_name}",
  "version": "{detected_from_config_yaml}",
  "timestamp": "{ISO8601_now}",
  "total_checks": "{total}",
  "passed": "{passed_count}",
  "failed": "{failed_count}",
  "skipped": "{skipped_count}",
  "blocking_passed": "{true|false}",
  "final_score": "{score}",
  "verdict": "{PASS|CONDITIONAL|FAIL}",
  "dimensions": { "{per_dimension_breakdown}" },
  "checks": [ "{per_check_results}" ],
  "recommended_actions": [ "{action_1}", "{action_2}" ],
  "doom_loop_check": "{injected_from_wf_state_if_available}"
}
```

**Validation gate:** Validate the JSON against `schemas/validation-report.schema.json`
before writing. If validation fails, log a WARNING and write the report anyway
(do NOT block the overall QA result — the JSON report is supplementary).

### Step 6: Save Report Files

Write markdown report to: `{component}/docs/qa-report-{date}.md`
Write JSON report to: `{component}/docs/qa-report-{date}.json`

## Output

```yaml
output:
  name: qa_report
  type: object
  description: "Complete QA report with verdict, score, and recommendations"
  locations:
    - console: "Immediate feedback summary"
    - file_md: "{component}/docs/qa-report-{date}.md"
    - file_json: "{component}/docs/qa-report-{date}.json"
    - badge: "{component}/docs/VALIDATED.md (if PASS)"

outputs:
  - name: qa_report_md
    type: file
    format: markdown
    path: "{component}/docs/qa-report-{date}.md"
  - name: qa_report_json
    type: file
    format: json
    path: "{component}/docs/qa-report-{date}.json"
    schema: "squads/squad-creator/schemas/validation-report.schema.json"
    validated: true
```

## Acceptance Criteria

- [ ] All 5 check results aggregated correctly
- [ ] Verdict priority logic applied (FAIL > CONDITIONAL > PASS)
- [ ] Blocking issues separated from warnings
- [ ] Report file saved to component docs directory
- [ ] Validation badge created on PASS
- [ ] CONDITIONAL verdict presents user choice to proceed
- [ ] FAIL verdict blocks with actionable fix list
- [ ] Console output shows summary with score

## Veto Conditions

| Condition | Action |
|-----------|--------|
| Any input check has ABORT/FAIL verdict | Overall FAIL, no override |
| HIGH security finding present | Overall FAIL, no override |
| Score < 5.0 | Overall FAIL |

## Related Documents

| Document | Purpose |
|----------|---------|
| `qa-after-creation.md` | Parent orchestrator task |
| `qa-check-structure.md` | Provides structure_result |
| `qa-check-schema.md` | Provides schema_result |
| `qa-check-references.md` | Provides references_result |
| `qa-check-completeness.md` | Provides completeness_result |
| `qa-check-compatibility.md` | Provides compatibility_result |
| `fix-issues` | Offered on FAIL verdict |
