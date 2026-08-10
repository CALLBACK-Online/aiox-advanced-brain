# Task: Candidate Reliability Test for Cross-Provider Qualification

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `qualify-provider-reliability` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Agent` |

## Metadata

```yaml
id: qualify-provider-reliability
name: "Candidate Reliability Test for Cross-Provider Qualification"
category: qualification
agent: squad-chief
elicit: false
autonomous: true
description: >
  Executes the candidate model N times via LLM Router to measure success rate,
  latency variance, and reliability. Applies veto conditions for unreliable
  models. Corresponds to Phase 2 of wf-cross-provider-qualification.yaml.
accountability:
  human: squad-operator
  scope: review_only
domain: Operational

```


<!-- SINKRA_CONTRACT -->
Domain: `Operational`
atomic_layer: Atom
Input: request::qualify_provider_reliability
Output: artifact::qualify_provider_reliability
pre_condition: preflight PASS AND candidate model disponível via LLM Router AND baseline disponível
post_condition: reliability metrics (success rate, latency variance, error rate) de N execuções, veto se unreliable
performance: Agent, < 5 min para N runs, veto automático se success rate < threshold
Completion Criteria: N runs completed AND success_rate calculado AND latency_variance medida AND veto conditions avaliadas
error_handling: fail-loud, VETO on quality gate failure, escalate to squad-chief
## Purpose

Determine whether the candidate model can reliably produce results. A single
successful run is insufficient -- multiple runs expose variance in latency,
error rate, and output quality.

## Prerequisites

- [ ] `qualify-provider-baseline` completed successfully
- [ ] LLM Router service available
- [ ] Test directory exists

## Inputs

| Parameter | Type | Required | Source |
|-----------|------|----------|--------|
| `task_name` | string | Yes | From pipeline |
| `candidate_model` | string | Yes | From pipeline |
| `test_input` | object | Yes | From cross_provider_candidates |
| `reliability_runs` | number | No | Default: 3 |

## Workflow

### Step 1: Execute reliability runs

```yaml
for_each_run:
  index: 1..{reliability_runs}
  command: |
    node services/llm-router/index.js \
      --task "{task_name}" \
      --model "{candidate_model}" \
      --input "{test_input.target}" \
      --output "test-cases/cross-provider/{task_name}/{candidate_model}/run-{i}.yaml"
  record:
    - run_number
    - success (true/false)
    - latency_ms
    - tokens (input, output)
    - error (null or message)
```

### Step 2: Check reliability threshold

```yaml
reliability_check:
  - condition: "success_rate < 0.5"
    action: "VETO (CPQ_VC_003)"
  - condition: "avg_latency_ms > 60000"
    action: "FLAG as batch-only (CPQ_VC_006)"
```

## Output

```yaml
reliability_output:
  runs: []
  success_rate: 0.0
  avg_latency_ms: 0
  latency_variance:
    min_ms: 0
    max_ms: 0
    stddev_ms: 0
  total_cost_usd: 0.0
  reliability_verdict: "PASS|BATCH_ONLY|FAIL"
```

## Veto Conditions

```yaml
veto_conditions:
  - id: CPQ_VC_003
    trigger: "Model returns error in >50% of runs"
    action: "BLOCK - Model not reliable for this task"
  - id: CPQ_VC_006
    trigger: "Average latency > 60s"
    action: "FLAG - Only use for batch/async jobs"
```

## Acceptance Criteria

- [ ] All configured runs executed (or attempted)
- [ ] Success rate, average latency, and variance calculated
- [ ] Reliability verdict assigned (PASS, BATCH_ONLY, or FAIL)
- [ ] Run output files saved per iteration
- [ ] Veto conditions evaluated

## Related Documents

- `wf-cross-provider-qualification.yaml` -- Parent workflow
- `qualify-provider-baseline.md` -- Previous task in pipeline
- `qualify-provider-compare.md` -- Next task in pipeline

---

_Task Version: 1.0.0_
_Extracted from: wf-cross-provider-qualification.yaml v1.0 (Phase 2)_
