# Task: Squad Design — Architecture & Scaffold

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-squad-design` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-squad-design
name: "Squad Design & Scaffold"
category: squad-creation
agent: squad-chief
elicit: true
autonomous: false
description: "Define tier structure, plan agent relationships and handoffs, design quality gates, then create the physical directory structure and initial files."
accountability:
  human: squad-operator
  scope: full
domain: Strategic
merged_from:
  - create-squad-architecture v1.0.0
  - create-squad-scaffold v1.0.0

```


<!-- SINKRA_CONTRACT -->
Domain: `Strategic`
atomic_layer: Atom
Input: request::create_squad_design
Output: artifact::create_squad_design
pre_condition: create-squad-discover completed AND agent roster com tier suggestions AND write permissions em squads/
post_condition: architecture blueprint com tier assignments, handoff maps e quality gates definidos AND directory structure materializada
performance: < 15 min (Hybrid — architecture elicitation + scaffold creation), escalate em conflito de tier
Completion Criteria: architecture_score >= 8.0 AND directory structure criada AND config.yaml gerado com entry_agent
error_handling: escalate to squad-chief on failure, persist error context
## Purpose

Transform the agent roster from discovery into a complete architectural blueprint with tier assignments, handoff maps, agent synergies/conflicts, and quality gates -- then materialize that architecture into the physical directory structure and initial files. The scaffold is the direct expression of the architecture; separating them was artificial.

## SINKRA Creation Contract

Every squad created by this task must have an explicit SINKRA contract before files are generated. Do not postpone these fields to validation; architecture owns the decision.

```yaml
sinkra_creation_contract:
  required:
    - squad_io_contract:
        source: "squads/squad-creator/squad-io.yaml"
        output_path: "squads/{squad_name}/squad-io.yaml"
        minimum_sections: [inputs, outputs, triggers, dependencies, artifact_contracts, data_sources, integrations, observability]
    - artifact_contracts:
        min_items: 1
        required_fields: [artifact_id, template_path, lifecycle_states]
        lifecycle_states: [draft, pending_validation, validated, approved, rejected, consumed, superseded, archived]
    - bu_mapping:
        default: "hub-framework"
        required: true
    - supported_modes:
        allowed: [CRIAR, RESOLVER, GERENCIAR, ENTENDER, VALIDAR, CONFIGURAR, PLANEJAR, EXPLORAR]
        min_items: 1
    - workspace_integration:
        required_field: level
        allowed_levels: [none, read_only, controlled_runtime_consumer, workspace_first]
  blocking_rule:
    - "If any required field is unknown, stop and elicit it before Step 3.1"
    - "If workspace_integration writes to workspace/, require explicit COO/c-level handoff"
```

## Prerequisites

- [ ] `create-squad-discover` completed successfully (discover output available)
- [ ] Agent roster with tier suggestions defined
- [ ] `data/tier-system-framework.md` loaded
- [ ] `data/decision-heuristics-framework.md` loaded
- [ ] Write permissions for `squads/` directory
- [ ] Templates available: `templates/config-tmpl.yaml`

## Inputs

```yaml
inputs:
  discover_output:
    type: object
    required: true
    description: "Output from create-squad-discover"
    fields: [viability_score, decision, squad_name, entry_agent, slash_prefix, pattern_prefix, mode, squad_type, template_approach, agent_roster, total_agents_planned]
  squad_name:
    type: string
    required: true
  pack_title:
    type: string
    required: true
  entry_agent:
    type: string
    required: true
  version:
    type: string
    required: true
    default: "1.0.0"
  author:
    type: string
    required: true
  mode:
    type: enum
    required: true
    description: '"incremental" or "yolo"'
```

## Workflow / Steps

### Step 2.1: Define Tier Structure

**Apply: tier-system-framework.md**

```yaml
tier_structure_design:
  orchestrator:
    purpose: "Coordinates all tiers, routes requests"
    agent_id: "{squad_name}-chief"

  tier_0_diagnosis:
    purpose: "First contact, analysis, classification"
    agents: "From roster where tier == 0"
    required: true

  tier_1_masters:
    purpose: "Primary experts with core execution capability"
    agents: "From roster where tier == 1"

  tier_2_systematizers:
    purpose: "Framework creators and methodology agents"
    agents: "From roster where tier == 2"

  tier_3_specialists:
    purpose: "Specific format/channel experts"
    agents: "From roster where tier == 3"

  tools:
    purpose: "Validation, checklists, calculators"
    examples: ["quality-checker", "compliance-validator"]
```

### Step 2.2: Plan Agent Relationships

```yaml
agent_relationships:
  handoff_map:
    - from: "orchestrator"
      to: "tier_0_agents"
      when: "New request arrives"

    - from: "tier_0_agents"
      to: "tier_1_agents"
      when: "Diagnosis complete, execution needed"

  synergies:
    - agents: ["diagnosis-agent", "master-agent"]
      pattern: "Diagnosis feeds master context"

  conflicts:
    - agents: ["aggressive-style", "conservative-style"]
      reason: "Contradictory approaches"
```

### Step 2.3: Design Quality Gates

```yaml
quality_gates_design:
  gates:
    - id: "QG-001"
      name: "Request Classification"
      transition: "Input -> Tier 0"
      type: "routing"
      criteria: "Request type identified"

    - id: "QG-002"
      name: "Diagnosis Complete"
      transition: "Tier 0 -> Tier 1"
      type: "blocking"
      criteria: "Analysis approved, requirements clear"

    - id: "QG-003"
      name: "Draft Review"
      transition: "Execution -> Output"
      type: "blocking"
      criteria: "Quality checklist passed"

  escalation_paths:
    - on_failure: "Return to previous tier with feedback"
    - on_repeated_failure: "Escalate to human review"
```

### Step 3.0: Verify No Existing Directory

```yaml
verify_no_collision:
  check: "squads/{squad_name}/ does NOT exist"
  on_exists:
    action: "HALT -- trigger VETO-SQD-001"
    prompt: "Squad directory already exists. Overwrite? (yes/no)"
    on_confirm: "Remove existing and proceed"
    on_deny: "Abort scaffold"
```

### Step 3.1: Create Directory Structure

```yaml
create_directories:
  base: "squads/{squad_name}/"
  subdirectories:
    - agents/
    - tasks/
    - workflows/
    - templates/
    - checklists/
    - data/
    - docs/
```

### Step 3.1b: Annotate reasoning_tier (C3 — EPIC-109 Wave 1)

When `model_strategy.enabled = true` in the squad config being created,
annotate each planned workflow phase with `reasoning_tier` based on the
verb-pattern heuristic:

```yaml
reasoning_tier_annotation:
  enabled_when: "config.yaml model_strategy.enabled == true"
  classification_rule:
    planning:
      verbs: [discover, research, design, plan, analyze]
      model: gemini-3.1-pro-preview
    implementation:
      verbs: [generate, create, build, render, scaffold]
      model: claude-sonnet-4
    verification:
      verbs: [validate, check, verify, qa, test]
      model: claude-haiku-4
    default: implementation
  apply_to: "Each phase in planned workflows — match phase name verb to tier"
  output: "Annotate phase definitions with reasoning_tier field"
  constraint: "NEVER set default model to gemini-flash (PV_BS_001)"
```

### Step 3.2: Create Initial Files

```yaml
create_initial_files:
  config_yaml:
    source: "templates/config-tmpl.yaml"
    target: "squads/{squad_name}/config.yaml"
    interpolate:
      - pack.name: "{squad_name}"
      - pack.version: "{version}"
      - pack.description: "{purpose}"
      - pack.icon: "determined from domain"
      - entry_agent: "{entry_agent}"
      - agents: "from tier_structure"
      - capabilities: "from use_cases"
      - activation.shortcuts: "/{squad_name}:{entry_agent}"
      - artifact_contracts: "from sinkra_creation_contract"
      - bu_mapping: "from sinkra_creation_contract"
      - supported_modes: "from sinkra_creation_contract"
      - workspace_integration: "from sinkra_creation_contract"

  squad_io_yaml:
    source: "squads/squad-creator/squad-io.yaml"
    target: "squads/{squad_name}/squad-io.yaml"
    interpolate:
      - inputs: "from discover_output + architecture blueprint"
      - outputs: "from artifact_contracts"
      - triggers: "from activation model"
      - dependencies: "from integration plan"
      - artifact_contracts: "from sinkra_creation_contract"

  readme_md:
    target: "squads/{squad_name}/README.md"
    content: "Placeholder -- will be completed in create-squad-build"
    sections:
      - "# {pack_title}"
      - "## Overview"
      - "## Agents"
      - "## Workflows"
      - "## Tasks"
      - "## Usage"
```

### Step 3.3: Initialize Runtime State

```yaml
init_runtime:
  state_file: ".aiox/squad-runtime/create-squad/{squad_name}/state.json"
  initial_state:
    squad_name: "{squad_name}"
    phase: "design_complete"
    created_at: "{timestamp}"
    mode: "{mode}"
    phases_completed: ["discover", "design"]
    phases_remaining: ["build", "validate", "publish"]
```

## Output

```yaml
design_output:
  # Architecture outputs
  tier_structure:
    orchestrator: "{squad}-chief"
    tier_0: ["{diagnosis-agent-1}", "{diagnosis-agent-2}"]
    tier_1: ["{master-agent-1}", "{master-agent-2}"]
    tier_2: ["{systematizer-1}", "{systematizer-2}"]
    tier_3: ["{specialist-1}", "{specialist-2}"]
    tools: ["{tool-1}", "{tool-2}"]
  quality_gates: "{N}"
  handoffs: "{N}"
  architecture_score: "{score}/10"
  # Scaffold outputs
  base_path: "squads/{squad_name}/"
  directories_created: 7
  files_created:
    - "squads/{squad_name}/config.yaml"
    - "squads/{squad_name}/squad-io.yaml"
    - "squads/{squad_name}/README.md"
  sinkra_creation_contract:
    squad_io_contract: "present"
    artifact_contracts_count: "{N}"
    bu_mapping: "{bu_mapping}"
    supported_modes: ["{mode}"]
    workspace_integration_level: "{level}"
  runtime_state: ".aiox/squad-runtime/create-squad/{squad_name}/state.json"
  artifact_produced:
    artifact_id: squad-config-base
    artifact_template: squads/squad-creator/templates/config-tmpl.yaml
    lifecycle_state: draft
  status: "PASS"
```

## Acceptance Criteria

- [ ] Tier 0 defined with at least one agent
- [ ] Orchestrator agent defined as `{squad_name}-chief`
- [ ] Quality gates >= 3
- [ ] Handoff map complete (all tier transitions covered)
- [ ] Agent synergies and conflicts documented
- [ ] In incremental mode: human approval obtained for architecture
- [ ] Directory `squads/{squad_name}/` exists with all 7 subdirectories
- [ ] `config.yaml` is valid YAML with `entry_agent` field populated
- [ ] `config.yaml` declares `artifact_contracts[]` with at least 1 contract
- [ ] `config.yaml` declares `bu_mapping`
- [ ] `config.yaml` declares `supported_modes[]`
- [ ] `config.yaml` defines `workspace_integration.level` (VETO-SQD-004)
- [ ] `squad-io.yaml` exists with inputs, outputs, triggers, dependencies, artifact_contracts, data_sources, integrations, and observability
- [ ] `README.md` placeholder created
- [ ] Runtime state file initialized
- [ ] No pre-existing directory was overwritten without confirmation

## Veto Conditions

- **VETO-SQD-001:** Squad directory already exists without user confirmation to overwrite
- **VETO-SQD-004:** `config.yaml` missing `workspace_integration.level` field
- **VETO-SQD-008:** SINKRA creation contract missing `artifact_contracts`, `bu_mapping`, `supported_modes`, or `squad-io.yaml`
- Missing Tier 0 definition
- Missing orchestrator definition
- Fewer than 3 quality gates
- Incomplete handoff map (orphan agents with no incoming/outgoing handoffs)

## Related Documents

- `create-squad.md` (parent composed task)
- `create-squad-discover.md` (previous step)
- `create-squad-build.md` (next step)
- `data/tier-system-framework.md`
- `data/decision-heuristics-framework.md`
- `templates/config-tmpl.yaml`

---

_Task Version: 1.0.0 (merged from: create-squad-architecture v1.0.0 + create-squad-scaffold v1.0.0)_
_Last Updated: 2026-03-27_
