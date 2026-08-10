# Task: Serialize Retry State

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `serialize-retry-state` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Worker` |

## Metadata

```yaml
id: serialize-retry-state
name: Serialize Retry State
category: harness-engineering
agent: squad-chief
elicit: false
autonomous: true
description: >
  Capture the current pipeline step state into a serialized retry file under
  .aiox/squad-runtime/. Classifies the triggering error as transient/structural/unknown,
  integrates with doom-loop-detector to suppress retry when doom loop is active,
  and determines the appropriate recovery action.
accountability:
  human: squad-operator
  scope: review_only
domain: Operational
epic: EPIC-109
wave: 2
concept: C2 (Ralph Loop)
```

<!-- AIOX_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::serialize_retry_state
Output: artifact::serialize_retry_state
pre_condition: pipeline step has failed and retry is being evaluated
post_condition: retry state file persisted at .aiox/squad-runtime/{squad}/retry-states/{step}.json
performance: registrar evidências, falhas e próximo passo sem erro silencioso
Completion Criteria: contrato mínimo AIOX explícito e saída rastreável produzida

## Purpose

Serialize the current failure context into a structured retry state file that
`ralph-loop-manager.js` can read on the next attempt. Ensures that fresh-context
retries have all information needed to avoid repeating the same error, and that
doom loop detection is consulted before recommending `retry_fresh`.

## Prerequisites

- [ ] `scripts/lib/doom-loop-detector.js` available (C1 Wave 1)
- [ ] `scripts/lib/ralph-loop-manager.js` available (C2 Wave 2)
- [ ] `.aiox/squad-runtime/` directory or write access to create it
- [ ] Failing step ID and error message are known

## Inputs

```yaml
inputs:
  - name: step_id
    type: string
    required: true
    description: "Unique identifier of the failing pipeline step"

  - name: error_message
    type: string
    required: true
    description: "Error message or description from the failing step"

  - name: squad_name
    type: string
    required: false
    description: "Squad name for namespaced state path (default: global)"

  - name: doom_loop_check
    type: object
    required: false
    source: wf-qa-after-creation (injected from qa_doom_loop_advisory phase)
    description: "Optional doom loop check result to integrate into retry decision"

  - name: max_iterations
    type: integer
    required: false
    default: 5
    description: "Maximum retry attempts before abort"
```

## Workflow / Steps

### Step 1: Classify Error

Apply the error taxonomy to the `error_message`:

```yaml
error_taxonomy:
  transient:
    patterns: [ETIMEDOUT, ECONNRESET, rate_limit, context_length_exceeded, "503", "429"]
    recovery: "Fresh context retry — error is environmental, not logical"
  structural:
    patterns: [schema_validation_failed, missing_required_field, type_mismatch, ENOENT, SyntaxError]
    recovery: "Fix the structural issue before retrying"
  unknown:
    patterns: []  # everything else
    recovery: "Resume from last checkpoint"
```

### Step 2: Consult Doom Loop State

If `doom_loop_check` is provided:
- If `doom_loop_check.detected == true` → **FORCE action = `abort`**
  regardless of error class. Log: "Doom loop suppressed retry."
- If not detected → proceed with error classification

### Step 3: Invoke ralph-loop-manager.js

```javascript
const { manageRetry } = require('./scripts/lib/ralph-loop-manager');
const result = manageRetry(step_id, {
  maxIterations: max_iterations,
  errorMessage: error_message,
  squadName: squad_name,
  doomLoopCheck: doom_loop_check
});
// result.action: 'retry_fresh' | 'retry_resume' | 'abort'
// result.stateFile: path where state was persisted
```

### Step 4: Ensure State Directory Exists

```bash
mkdir -p .aiox/squad-runtime/{squad_name}/retry-states/
```

The ralph-loop-manager.js handles this internally, but the task should
validate the directory exists post-execution.

### Step 5: Return Action to Caller

Pass the `action` field to the workflow's recovery decision point.

## Output

```yaml
output:
  name: retry_state
  type: object
  description: "Retry state with action, attempt count, and persisted file path"
  fields:
    action:
      type: enum
      values: [retry_fresh, retry_resume, abort]
    attempt:
      type: integer
    stateFile:
      type: string
    reason:
      type: string
    errorClass:
      type: enum
      values: [transient, structural, unknown]
```

## Acceptance Criteria

- [ ] Error classified as transient/structural/unknown using defined taxonomy
- [ ] Doom loop check consulted — when `doom_loop_check.detected == true`, action is always `abort`
- [ ] `retry_fresh` NEVER recommended when doom loop is active
- [ ] State file persisted under `.aiox/squad-runtime/`
- [ ] Max iterations respected (abort when exceeded)
- [ ] Structural errors abort after attempt > 2
- [ ] State directory created if it doesn't exist

## Veto Conditions

| Condition | Action |
|-----------|--------|
| `retry_fresh` returned when doom loop detected | VETO — critical violation of C2/C1 contract |
| State file not persisted | VETO — retry state lost |
| `max_iterations` not enforced | VETO — potential infinite loop |

## Error Handling

| Error | Recovery |
|-------|---------|
| `.aiox/squad-runtime/` write permission denied | Log error, return `action: abort` with reason |
| `doom_loop_check` malformed | Ignore field, treat as if absent |
| `ralph-loop-manager.js` not found | Log critical error, return `action: abort` |

## Related Documents

- `scripts/lib/ralph-loop-manager.js` — invoked by this task
- `scripts/lib/doom-loop-detector.js` — doom loop state source
- `tasks/create-squad-schemas.md` — Wave 2 parallel task (C5)
- `workflows/wf-create-squad.yaml` — workflow that uses this task

---

_Task Version: 1.0.0_
_Epic: EPIC-109 Wave 2 — C2 Ralph Loop (Fresh-Context Retry)_
_Last Updated: 2026-04-13_
