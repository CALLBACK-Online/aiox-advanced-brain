# Task: Create Squad Schemas

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-squad-schemas` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-squad-schemas
name: Create Squad Schemas
category: squad-creation
agent: squad-chief
elicit: false
autonomous: true
description: >
  Generate JSON Schema Draft-07 files for all cross-phase structured outputs
  produced by the squad being created. Schema generation is SCOPED to outputs
  that appear as inputs in at least one other task (cross-phase data flow).
  Markdown/text outputs are explicitly excluded.
accountability:
  human: squad-operator
  scope: review_only
domain: Operational
epic: EPIC-109
wave: 2
concept: C5 (Schema Generation)
```

<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_squad_schemas
Output: artifact::create_squad_schemas
pre_condition: squad creation pipeline is in schema_generation phase
post_condition: schemas/ directory populated with validated JSON Schema files
performance: registrar evidências, falhas e próximo passo sem erro silencioso
Completion Criteria: contrato mínimo AIOX explícito e saída rastreável produzida

## Purpose

Generate JSON Schema Draft-07 files for cross-phase structured outputs in the
squad being created. These schemas enable deterministic validation (via AJV in
Wave 3) as a complement to LLM-based quality checks. Coverage goal: >= 80% of
cross-phase structured outputs.

## Definition of "Cross-Phase"

A cross-phase output is an artifact produced by one task that appears as an
input in at least one other task within the same squad's workflow. Traced via
`data_flow`, `inject_as`, or `passed_to` fields in workflow and task definitions.

**Explicitly excluded from schema generation:**
- Markdown/text outputs (format: md, txt, prose)
- Internal-only outputs consumed only within the same task
- Human-review artifacts (no machine-readable structure)

## Prerequisites

- [ ] Squad creation pipeline at `schema_generation` phase
- [ ] `wf-create-squad.yaml` `creation` phase is complete
- [ ] Task definitions for the new squad are available
- [ ] `workflow-definition` output with data_flow annotations is available
- [ ] `schemas/` directory exists or can be created at `squads/{squad_name}/schemas/`

## Inputs

```yaml
inputs:
  - name: squad_name
    type: string
    required: true
    description: "Name of the squad being created"

  - name: workflow_definition
    type: object
    required: true
    source: wf-create-squad (creation phase)
    description: "Completed workflow with task definitions and data_flow annotations"

  - name: task_definitions
    type: array
    required: true
    source: wf-create-squad (creation phase)
    description: "Array of task .md definitions for the squad"
```

## Workflow / Steps

### Step 1: Discover Cross-Phase Outputs

Scan the `workflow_definition` and `task_definitions` to identify outputs that
are consumed as inputs in at least one other task:

```yaml
cross_phase_discovery:
  method: "Trace data_flow, inject_as, passed_to, source fields in task inputs"
  filter_in:
    - format: [json, yaml, object, array]
    - consumed_by: "at least 1 other task"
  filter_out:
    - format: [markdown, text, md, txt, prose, html]
    - consumed_by: "none (terminal outputs)"
    - scope: "internal to same task"
```

### Step 2: Generate Schema per Output

For each cross-phase structured output:

1. Infer the schema from the task's output definition fields (name, type, required, description)
2. Generate a JSON Schema Draft-07 file following the naming convention:
   `schemas/{output-name}.schema.json`
3. Include `$schema: http://json-schema.org/draft-07/schema#` header
4. Map types: `object → object`, `array → array`, `string → string`,
   `boolean → boolean`, `number → number`, `integer → integer`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "{output-name}.schema.json",
  "title": "{output_display_name}",
  "description": "Schema for {task_id} output: {output_name}",
  "type": "{inferred_type}",
  "required": ["{required_field_1}", "{required_field_2}"],
  "properties": {
    "{field_name}": {
      "type": "{field_type}",
      "description": "{field_description}"
    }
  }
}
```

### Step 3: Calculate Coverage

```yaml
coverage_calculation:
  formula: "schemas_generated / total_cross_phase_structured_outputs"
  target: ">= 0.80 (80%)"
  on_below_target: "Log gap list, continue — coverage is advisory not blocking"
```

### Step 4: Validate Generated Schemas

Each schema MUST be valid JSON Schema Draft-07. Validate by:
- Checking `$schema` field is present and correct
- Validating schema syntax with js-yaml or JSON.parse
- Running AJV meta-schema validation if AJV is available (graceful skip if not)

### Step 5: Write Schemas to Disk

Write all generated schemas to `squads/{squad_name}/schemas/`.

## Output

```yaml
output:
  name: squad_schemas
  type: object
  description: "Generated schema files and coverage report"
  fields:
    schemas_created:
      type: array
      items: { type: string }
      description: "Paths of schema files created"
    coverage:
      type: number
      description: "Fraction of cross-phase structured outputs covered (0.0–1.0)"
    uncovered_outputs:
      type: array
      items: { type: string }
      description: "Cross-phase outputs without a schema"
    schema_dir:
      type: string
      description: "Path to schemas/ directory"
```

## Acceptance Criteria

- [ ] Only cross-phase structured (json/yaml/object) outputs receive schemas
- [ ] Markdown/text outputs explicitly excluded
- [ ] Coverage >= 80% of cross-phase structured outputs
- [ ] All generated schemas are valid JSON Schema Draft-07
- [ ] `$schema` header present in every file
- [ ] Schema files named `{output-name}.schema.json` (kebab-case)
- [ ] Schemas written to `squads/{squad_name}/schemas/`

## Veto Conditions

| Condition | Action |
|-----------|--------|
| Schema generated for non-cross-phase output (violates PV_BS_001 scope) | VETO |
| Schema generated for markdown/text output | VETO |
| `$schema` header missing | VETO |
| Schema file is not valid JSON | VETO |

## Error Handling

| Error | Recovery |
|-------|---------|
| No cross-phase structured outputs found | Create empty `schemas/` dir, log INFO, coverage = N/A |
| Output type ambiguous | Default to `object` type, add comment in schema |
| Write permission denied | Log error, skip that schema, reduce coverage count |

## Related Documents

- `tasks/serialize-retry-state.md` — Wave 2 parallel task (C2)
- `workflows/wf-create-squad.yaml` — workflow that adds schema_generation phase
- `scripts/lib/ajv-validate.js` — Wave 3 (C6) will use these schemas
- `schemas/validation-report.schema.json` — reference example of expected format

---

_Task Version: 1.0.0_
_Epic: EPIC-109 Wave 2 — C5 Schema Generation_
_Last Updated: 2026-04-13_
