# Task: Design Workflow Structure

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `create-workflow-design` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: create-workflow-design
name: Design Workflow Structure
category: workflow-creation
agent: squad-chief
elicit: true
autonomous: false
description: >
  Design the complete workflow structure through interactive elicitation:
  phase architecture with tier classification, agent/task bindings with
  handoff points, and quality gates with veto conditions and error handling.
  Applies tier-system-framework.md, executor-matrix-framework.md, and
  decision-heuristics-framework.md.
accountability:
  human: squad-operator
  scope: full
domain: Operational

```


<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::create_workflow_design
Output: artifact::create_workflow_design
pre_condition: create-workflow-classify completed AND tier/executor/decision frameworks acessíveis AND squad agents conhecidos
post_condition: workflow design com phase architecture, agent/task bindings, handoffs e quality gates definidos
performance: < 15 min (Hybrid — interactive design session), escalate em conflito de agent assignment
Completion Criteria: phases com tier classification AND agent assignments com task_refs AND quality gates com veto conditions

## Purpose

Design the complete workflow structure in a single interactive session covering three dimensions: (1) phase architecture with tier classification and inline structures, (2) agent assignment with task_ref bindings and handoff points, and (3) quality gates with checkpoints, veto conditions, and error handling. These three dimensions form one cohesive design session -- the structural backbone that generation builds upon.

## Prerequisites

- [ ] Phase 0 classification complete (create-workflow-classify output)
- [ ] `data/tier-system-framework.md` is accessible
- [ ] `data/executor-matrix-framework.md` is accessible
- [ ] `data/decision-heuristics-framework.md` is accessible
- [ ] Target squad agents are known (from config.yaml)

## Inputs

```yaml
inputs:
  - name: phase_0_classification
    type: object
    required: true
    source: previous_task
    description: "Classification output from create-workflow-classify"

  - name: squad_name
    type: string
    required: true
    source: previous_task
    description: "Target squad identifier"

  - name: squad_config
    type: object
    required: true
    source: filesystem
    description: "Squad config.yaml with agent definitions"
```

## Workflow / Steps

### Step 1: Design Phase Structure

**Apply: tier-system-framework.md**

```yaml
tier_definitions:
  tier_0: "Foundation - Must complete before anything else"
  tier_1: "Core - Main execution phase"
  tier_2: "Advanced - Enhancement and optimization"
  tier_3: "Polish - Final quality assurance"

for_each_phase:
  - phase_number: "Sequential number (1, 2, 3...)"
  - phase_name: "Human-readable name"
  - phase_days: "Duration (e.g., 'Days 1-2')"
  - phase_tier: "0, 1, 2, or 3"
  - phase_description: "What this phase accomplishes"
  - phase_tasks: "List of tasks in this phase"
```

**Elicitation per phase:**

```yaml
elicit_phase:
  phase_identity:
    - "What is the name of Phase {N}?"
    - "What days does it span?"
    - "What tier is it? (0=foundation, 1=core, 2=advanced, 3=polish)"

  phase_content:
    - "What tasks belong to this phase?"
    - "Which agent executes each task?"
    - "What does this phase produce?"

  phase_checkpoint:
    - "What must be true to complete this phase?"
    - "Does it need human review?"
```

**Phase template:**

```yaml
phase_template:
  structure: |
    - id: PHASE-{phase_number}
      name: "{phase_name}"
      days: "{phase_days}"
      tier: {phase_tier}
      description: |
        {phase_description}

      tasks:
        - task_file: "{task_file}"
          agent: "{agent_id}"
          required: true
          description: "{task_description}"
          output: "{output_file}"

      checkpoint:
        criteria:
          - "{criterion_1}"
          - "{criterion_2}"
        human_review: true
        message: "{checkpoint_message}"
```

**Inline structures (add when needed):**

```yaml
inline_structure_criteria:
  add_when:
    - "Phase produces complex multi-part output"
    - "Detailed step-by-step guidance is needed"
    - "Timing/duration specifications are important"
    - "Domain-specific formatting required"

  examples:
    email_sequence:
      pattern: "SOS structure with cliffhangers"
    webinar_structure:
      pattern: "Introduction, content, close with durations"
    call_script:
      pattern: "Phased script with timing and elements"
```

### Step 1b: Auto-Classify reasoning_tier via Verb Pattern (C3 — EPIC-109 Wave 1)

When the parent squad has `model_strategy.enabled = true`, automatically
classify each phase with `reasoning_tier` using the verb-pattern heuristic:

```yaml
verb_pattern_heuristic:
  enabled_when: "squad config.yaml model_strategy.enabled == true"
  classification:
    planning:
      verbs: [discover, research, design, plan, analyze]
      model_hint: gemini-3.1-pro-preview
      rationale: "High-reasoning tasks benefit from most capable model"
    implementation:
      verbs: [generate, create, build, render, scaffold]
      model_hint: claude-sonnet-4
      rationale: "Generation tasks need balanced capability/speed"
    verification:
      verbs: [validate, check, verify, qa, test]
      model_hint: claude-haiku-4
      rationale: "Deterministic checks are fast and low-complexity"
    default: implementation
  matching_rule: >
    Extract the leading verb from the phase name (e.g., 'Generate Agents' → 'generate').
    Match against the verbs list above. If no match, use default tier (implementation).
  constraint: >
    NEVER assign gemini-flash as a model hint (PV_BS_001).
    gemini-3.1-pro-preview is the high-capability default, not gemini-flash.
  output: >
    Add reasoning_tier field to each phase definition before generation.
    Example: reasoning_tier: planning
```

### Step 2: Assign Agents to Phases

**Apply: executor-matrix-framework.md**

```yaml
agent_assignment:
  template: |
    agents_by_phase:
      PHASE-{N}:
        primary:
          - "{primary_agent_1}"
          - "{primary_agent_2}"
        secondary:
          - "{secondary_agent_1}"

  criteria:
    primary_agent: "Main executor for the phase"
    secondary_agent: "Supports or validates primary"
```

**Elicitation:**

```yaml
elicit_agents:
  for_each_phase:
    - "Which agent is PRIMARY for Phase {N}?"
    - "Which agents SUPPORT this phase?"
    - "Are these agents defined in the squad?"
```

**Resolve task_ref bindings** for each task listed in each phase:

```yaml
resolve_task_ref:
  for_each_task_in_phase:
    check_existing:
      - path: "squads/{squad_name}/tasks/{task_file}"
      - exists: true | false

    if_exists:
      action: "Bind task_ref to existing file"

    if_not_exists:
      options:
        - "Create task via *create-task (recommended)"
        - "Mark as placeholder with TODO"
        - "Reference a task from another squad"

    binding_format: "task_ref, agent, required, description, output"
```

### Step 3: Define Handoff Points

```yaml
handoff_points:
  template: |
    handoffs:
      - from_phase: PHASE-{N}
        to_phase: PHASE-{N+1}
        from_agent: "{agent_1}"
        to_agent: "{agent_2}"
        context_passed:
          - "{context_item_1}"
          - "{context_item_2}"
        validation: "{handoff_validation}"

  criteria:
    - "Clear sender and receiver"
    - "Context preserved between phases"
    - "Validation at handoff"
```

Document agent synergies (which agents work well together) and conflicts (which should not share phases).

### Step 4: Define Checkpoints Per Phase

**Apply: decision-heuristics-framework.md**

```yaml
checkpoint_design:
  every_phase_must_have:
    - criteria: "List of specific validation items"
    - human_review: "true for important decisions"
    - message: "Context for the reviewer"

  checkpoint_template: |
    checkpoint:
      criteria:
        - "{criterion_1}"
        - "{criterion_2}"
        - "{criterion_3}"
      human_review: {true|false}
      message: "{reviewer_context}"
```

**Elicitation:**

```yaml
elicit_checkpoint:
  for_each_phase:
    - "What must be true to complete Phase {N}?"
    - "List 2-4 specific criteria"
    - "Does this checkpoint need human review?"
    - "What context should the reviewer have?"
```

### Step 5: Set Veto Conditions and Error Handling

**Veto conditions:**

```yaml
veto_conditions:
  purpose: "Define conditions that BLOCK progress"

  template: |
    checkpoint_config:
      - phase: PHASE-{N}
        heuristic: "{heuristic_id}"
        criteria: "{criteria}"
        veto_condition: "{veto_condition}"

  examples:
    - veto: "Vision unclear (<0.7 clarity score)"
    - veto: "Missing required outputs"
    - veto: "Quality score below 7.0"
    - veto: "Security validation failed"
    - veto: "Human review rejected"
```

**Error handling:**

```yaml
error_handling:
  template: |
    error_handling:
      on_phase_failure:
        - log_error: true
        - notify_stakeholders: true
        - create_remediation_task: true
        - halt_workflow: {true|false}

      on_checkpoint_failure:
        - log_failure_reason: true
        - return_to_previous_phase: {true|false}
        - max_retries: {count}

      on_veto_triggered:
        - halt_immediately: true
        - escalate_to: "{escalation_target}"
        - document_reason: true
```

**Circuit breakers:**

Max 3 retries per checkpoint. Escalation path: phase owner, then squad-chief, then @master. Configurable timeout per phase; on timeout: halt and escalate.

### Step 6: Validate Complete Design

**Checkpoint SC_PHS_001:**

```yaml
heuristic_id: SC_PHS_001
name: "Phases Defined"
blocking: true
criteria:
  - phases_count >= 3
  - all_phases_have_tier
  - all_phases_have_tasks
  - tier_0_exists  # Foundation phase required
```

**Checkpoint SC_AGN_001:**

```yaml
heuristic_id: SC_AGN_001
name: "Agents Assigned"
blocking: true
criteria:
  - all_phases_have_primary_agent
  - all_task_refs_resolved_or_marked
  - handoff_points_defined
  - agents_exist_in_squad_config
```

**Checkpoint SC_CKP_001:**

```yaml
heuristic_id: SC_CKP_001
name: "Checkpoints Complete"
blocking: true
criteria:
  - all_phases_have_checkpoint
  - all_checkpoints_have_criteria
  - veto_conditions_defined
  - error_handling_defined
```

All three checkpoints must PASS before proceeding to generation.

## Output

```yaml
output:
  name: workflow_design
  format: yaml
  structure:
    phases: []              # Array of phase definitions with tiers
    phase_count: "{N}"
    inline_structures: "{count}"
    agents_by_phase: {}     # Phase -> agent mapping
    task_refs: []           # Resolved task_ref per step
    handoff_points: []      # Phase-to-phase handoffs
    synergies: []           # Agent synergy patterns
    conflicts: []           # Agent conflict patterns
    unresolved_tasks: []    # Tasks that need creation
    checkpoints: []         # Per-phase checkpoint definitions
    veto_conditions: []     # Blocking conditions
    error_handling: {}      # Failure procedures
    circuit_breakers: {}    # Escalation and timeout config
    checkpoint_SC_PHS_001: "PASS | FAIL"
    checkpoint_SC_AGN_001: "PASS | FAIL"
    checkpoint_SC_CKP_001: "PASS | FAIL"
```

## Acceptance Criteria

- [ ] At least 3 phases designed with id, name, days, tier, description
- [ ] Every phase has at least 1 task assigned
- [ ] Tier 0 (foundation) phase exists
- [ ] Tiers assigned via tier-system-framework.md
- [ ] Inline structures added where domain guidance is needed
- [ ] Every phase has at least one primary agent assigned
- [ ] All task_ref values resolved to existing files or marked as TODO
- [ ] Handoff points defined for each phase transition
- [ ] Agents referenced exist in squad config.yaml
- [ ] Synergies and conflicts documented
- [ ] Every phase has a checkpoint with 2+ criteria
- [ ] Human review flag set for each checkpoint
- [ ] Veto conditions defined (at least 1 per critical phase)
- [ ] Error handling covers phase failure, checkpoint failure, veto triggered
- [ ] Circuit breakers defined with escalation path
- [ ] Checkpoints SC_PHS_001, SC_AGN_001, SC_CKP_001 all pass

## Veto Conditions

- Fewer than 3 phases defined
- No tier 0 (foundation) phase
- Any phase missing tasks
- Tier assignment skipped (not using framework)
- Phase has no agent assigned
- task_ref references non-existent file without acknowledgment
- Agent not defined in squad config
- No handoff points between consecutive phases
- Any phase without a checkpoint
- No veto conditions defined for the workflow
- Error handling section missing
- No escalation path defined

## Related Documents

- `data/tier-system-framework.md` -- Phase tier classification
- `data/executor-matrix-framework.md` -- Agent assignment framework
- `data/decision-heuristics-framework.md` -- Checkpoint logic framework
- `create-workflow-classify.md` -- Preceding task (classification)
- `create-workflow-generate.md` -- Next task (generation and registration)
- `create-workflow.md` -- Parent composed task

---

_Task Version: 1.0.0_
_Merged from: create-workflow-phases.md + create-workflow-task-refs.md + create-workflow-gates.md_
