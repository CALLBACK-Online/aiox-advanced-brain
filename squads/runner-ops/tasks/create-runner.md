# SOP: Create a New Runner

> Process: SP-CREATE-RUNNER | Mode: CRIAR | Version: 1.0.0

## Decision Tree: "Do I Need a Runner?"

```
Is the process autonomous (no human in the loop)?
├── NO → Use a skill (SKILL.md) or workflow
└── YES → Does it orchestrate multiple LLM calls in sequence?
    ├── NO → Single-call skill or bash script is enough
    └── YES → Does it need state tracking across phases?
        ├── NO → Use a simple bash loop with run_llm_prompt()
        └── YES → ✅ CREATE A RUNNER
```

## 7 Phases

### Phase 1: Requirements (~15 min)

- [ ] Define the runner's purpose (1 sentence)
- [ ] List phases (3-8 max). Each phase = 1 LLM call
- [ ] Identify input files and output artifacts
- [ ] Choose target squad: `squads/{squad}/scripts/{runner}.sh`
- [ ] Determine if cascade is needed (multi-model fallback)

### Phase 2: Scaffold (~15 min)

```bash
# Copy the template
cp infrastructure/scripts/runner-lib/templates/runner-template.sh \
   squads/{squad}/scripts/{runner-name}.sh
chmod +x squads/{squad}/scripts/{runner-name}.sh

# Copy pipeline config template
cp infrastructure/scripts/runner-lib/templates/pipeline-phases-template.yaml \
   squads/{squad}/config/pipeline-phases.yaml

# Copy prompt template for each phase
mkdir -p squads/{squad}/templates
cp infrastructure/scripts/runner-lib/templates/prompt-template.md \
   squads/{squad}/templates/phase-{N}-prompt.md
```

### Phase 3: Config (~20 min)

Edit `pipeline-phases.yaml`:
- Set phase names, agents, models
- Set budget per phase (token limits)
- Set max_turns per phase (usually 1)
- Set recommended model per phase complexity

### Phase 4: Implement Phases (~45 min)

Edit the runner script in the `# === CUSTOMIZE ===` sections:
- `build_phase_prompt()` — construct prompts per phase
- `process_phase_output()` — handle LLM responses
- `get_phase_config()` — phase-specific overrides

**DO NOT** reimplement:
- LLM calling → use `run_llm_prompt()`
- State management → use `state_init()`, `state_update()`
- Metrics → auto-handled by `run_llm_prompt()`
- Session tracking → use `session_start()`, `session_end()`
- Cost limits → use `check_cost_cap()`
- Output filtering → use `filter_llm_output()`

**Boundary rule:**
- O runner criado NAO pode sourcear ou importar nada de `squads/runner-ops/`.
- O runner deve depender apenas de `infrastructure/scripts/runner-lib/` e dos assets do squad dono dele.

### Phase 5: Generate Tests (~10 min)

Every new runner MUST ship with a smoke test from day one. No runner without a test passes `validate-runner`.

```bash
# 1. Generate smoke test from template
cp infrastructure/scripts/runner-lib/tests/templates/test-runner-template.sh \
   infrastructure/scripts/runner-lib/tests/smoke/test-{runner-id}.sh
chmod +x infrastructure/scripts/runner-lib/tests/smoke/test-{runner-id}.sh

# 2. Set the 4 required variables in the generated file
#    RUNNER_ID="{runner-id}"
#    RUNNER_PATH="squads/{squad}/scripts/{runner-name}.sh"
#    RUNNER_SQUAD="{squad}"
#    FIXTURE_DIR="infrastructure/scripts/runner-lib/tests/smoke/fixtures/{runner-id}"

# 3. Scaffold fixtures directory
mkdir -p infrastructure/scripts/runner-lib/tests/smoke/fixtures/{runner-id}
cat > infrastructure/scripts/runner-lib/tests/smoke/fixtures/{runner-id}/README.md <<'FIXTURE_EOF'
# Fixtures for {runner-id} smoke test

Place minimal input files here for the smoke test to consume.

## TODO
- [ ] Add sample input file(s) matching what the runner expects
- [ ] If the runner is a validator, add a known-good target to test against
- [ ] If the runner needs a config, add a minimal pipeline-phases.yaml

See: infrastructure/scripts/runner-lib/tests/README.md
Story: 101.16
FIXTURE_EOF

# 4. Customize build_runner_args() if the runner has non-standard args
#    (validators, runners with --source, runners with project dirs)
#    Edit the CUSTOMIZE section in the generated test file.

# 5. Register the runner in runner-registry.yaml
#    (run-smoke-tests.sh reads from the registry — AC from 101.15)
```

### Phase 6: Integration Test (~15 min)

```bash
# Dry run
./{runner-name}.sh --dry-run --squad {test-squad}

# Real run with cheap model
./{runner-name}.sh --squad {test-squad} --model haiku

# Verify outputs
ls outputs/{squad}/{test-squad}/
cat outputs/{squad}/{test-squad}/metrics.jsonl

# Run the smoke test
bash infrastructure/scripts/runner-lib/tests/smoke/test-{runner-id}.sh
```

### Phase 7: Validation (~10 min)

```bash
# Run the runner compliance validator
infrastructure/scripts/runner-lib/validate-runner.sh squads/{squad}/scripts/{runner-name}.sh

# Register in runner-registry.yaml
# Add entry to infrastructure/scripts/runner-lib/runner-registry.yaml
```

---

## Module Checklist

| Module | Required | Purpose |
|--------|----------|---------|
| `pipeline-bootstrap.sh` | ✅ MUST | Loads all runner-lib modules |
| `run_llm_prompt()` | ✅ MUST | LLM calls with retry + fallback |
| `state_init()` / `state_update()` | ✅ MUST | Phase state tracking |
| `record_metrics()` | ✅ MUST | Auto-called by run_llm_prompt |
| `METRICS_FILE` export | ✅ MUST | Where metrics JSONL goes |
| `check_cost_cap()` | ✅ MUST | Budget guard |
| `session_start()` / `session_end()` | ⚠️ SHOULD | Session lifecycle |
| `filter_llm_output()` | ⚠️ SHOULD | Output sanitization |
| `cascade_run()` | 💡 NICE | Multi-model escalation |
| `hooks_load()` / `hooks_run()` | 💡 NICE | Lifecycle extensibility |
| `evaluate_phase_output()` | 💡 NICE | Quality scoring |
| `read_focused_context()` | 💡 NICE | Context management |

## Model Capability Matrix

| Phase Complexity | Recommended Model | Token Budget | Notes |
|------------------|-------------------|-------------|-------|
| Simple extraction | haiku / flash | 2K-4K in, 1K out | Templated output |
| Analysis / Scoring | sonnet / pro | 4K-8K in, 2K-4K out | Requires reasoning |
| Synthesis / Writing | opus / pro | 8K-16K in, 4K-8K out | Creative output |
| Validation / QA | haiku / flash | 2K-4K in, 500B out | JSON scoring |

---

*SOP Created: 2026-04-02 | Process: SP-CREATE-RUNNER v1.0.0*
