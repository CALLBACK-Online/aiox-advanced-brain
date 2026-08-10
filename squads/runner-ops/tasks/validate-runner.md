# Task: validate-runner

> Process: RP-VALIDATE-RUNNER | Mode: VALIDAR | Version: 1.0.0
> Owner: runner-validator | Executor: Worker

## Purpose

Executar compliance check em um runner existente contra os padrões runner-lib.
Usa o script autocontido do squad, mas lê/escreve no runtime canônico em `infrastructure/scripts/runner-lib/`.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `runner_path` | ✅ | Path para o script runner (ex: `squads/copy/scripts/copy-runner.sh`) |
| `strict` | ⚠️ | Se `true`, falha em WARNINGs também. Default: false |
| `report` | ⚠️ | Se `true`, gera relatório em `outputs/runner-ops/validation/`. Default: true |

## Veto Conditions

- **BLOCKER:** Runner path não existe → STOP, reportar "Runner not found"
- **BLOCKER:** `infrastructure/scripts/runner-lib/runner-registry.yaml` não existe ao rodar `--all` → STOP
- **WARN:** Runner não usa `pipeline-bootstrap.sh` → flag como CRITICAL violation
- **WARN:** Runner reimplementa funções que existem no runner-lib → flag como HIGH violation
- **BLOCKER:** Runner migrado passa a depender de `squads/runner-ops/` → STOP, viola boundary contract

## Execution

```bash
# Standard validation
bash squads/runner-ops/scripts/validate-runner.sh {runner_path}

# Strict mode (CI)
bash squads/runner-ops/scripts/validate-runner.sh {runner_path} --strict

# Validate all + update registry scores
bash squads/runner-ops/scripts/validate-runner.sh --all --update-registry

# Verbose output (shows all check details)
bash squads/runner-ops/scripts/validate-runner.sh --all --verbose
```

## Output Format

```
RUNNER COMPLIANCE REPORT
========================
Runner: {runner_path}
Date: {date}
Status: PASS | FAIL

CRITICAL VIOLATIONS (blocks merge):
  [C001] Missing pipeline-bootstrap.sh source
  [C002] Direct LLM call without run_llm_prompt()

HIGH VIOLATIONS (must fix):
  [H001] State management reimplemented locally
  [H002] Missing METRICS_FILE export

WARNINGS (recommended):
  [W001] No session_start/session_end lifecycle
  [W002] Missing filter_llm_output() usage

SCORE: {X}/100
VERDICT: PASS | FAIL
```

## Completion Criteria

- [ ] Script executado sem erro de sistema
- [ ] Relatório gerado em `outputs/runner-ops/validation/`
- [ ] PASS/FAIL claramente indicado
- [ ] Violations listadas com código e descrição
- [ ] Score numérico calculado
- [ ] Nenhum runner passou a depender de `squads/runner-ops/`

## Handoff

- **PASS →** Retornar resultado para runner-chief
- **FAIL →** Passar para runner-integrator com lista de violations + relatório path
