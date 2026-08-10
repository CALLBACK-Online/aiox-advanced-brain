# Task: Test Execution Pipeline

## Purpose
Testar a qualidade de execução das skills `/story-executor` e `/wave-execute` usando o Epic 99 test harness. Reseta stories para estado limpo, executa a skill alvo, e mede EQB score comparando vs golden outputs.

## Inputs
- `mode` (obrigatório): `manual` | `story-executor` | `wave-execute`
- `scope` (opcional): `all` | `99.1` | `99.2` | `99.3` | `99.4` | `99.5` | `wave-1` | `wave-2` (default: `all`)
- `skip_reset` (opcional): `true` para pular o reset (útil quando quer medir sem re-executar)

## Executor
skill-tester

## Scripts
- `tests/epic-99/reset.sh` — Reseta stories e sandbox para estado pré-execução
- `tests/epic-99/eqb-score.js` — Mede EQB score (8 dimensões × peso)

## Steps

### Phase A: Reset (skip se `skip_reset: true`)

1. Executar `bash tests/epic-99/reset.sh` (ou `--wave 1` / `--wave 2` conforme scope)
2. Verificar que [x] count = 0 nos story files
3. Verificar que sandbox está limpo

### Phase B: Execute (skip se `mode: manual` — assume que human já executou)

**Se `mode: story-executor`:**
1. Para cada story no scope:
   ```
   /story-executor docs/stories/epic-99/STORY-{id}-{name}.md
   ```
2. Aguardar conclusão de cada story antes da próxima (sequencial)
3. Para Wave 1: executar 99.1, 99.2 (paralelo possível)
4. Para Wave 2: executar 99.3, 99.4, 99.5 (paralelo possível)

**Se `mode: wave-execute`:**
1. `/wave-execute 99 1` (Wave 1: stories 99.1 + 99.2)
2. Aguardar Wave 1 completar
3. `/wave-execute 99 2` (Wave 2: stories 99.3 + 99.4 + 99.5)
4. Aguardar Wave 2 completar

### Phase C: Measure

1. Executar `node tests/epic-99/eqb-score.js --all --phase {mode}`
2. Capturar EQB comparison matrix
3. Calcular delta vs golden baseline (100%)
4. Classificar resultado: EXCELLENT (>=95%) | GOOD (>=80%) | ACCEPTABLE (>=60%) | POOR (<60%)

### Phase D: Report

1. Gerar relatório com:
   - Mode usado (manual / story-executor / wave-execute)
   - EQB comparison matrix (8 dimensões × 5 stories)
   - Overall average score
   - Gaps identificados (dimensões abaixo de 80%)
   - Recomendações de melhoria para as skills
2. Salvar relatório em `tests/epic-99/reports/eqb-{mode}-{timestamp}.md`

## Veto Conditions
- Golden inputs não existem em `tests/golden-inputs/epic-99/` → ABORT
- Golden outputs não existem em `tests/golden-outputs/epic-99/` → ABORT
- `eqb-score.js` não encontrado → ABORT
- Reset falha (stories ainda têm [x] após reset) → ABORT

## Output
- EQB comparison matrix (terminal output)
- Relatório salvo em `tests/epic-99/reports/`

## Completion Criteria
- Reset executado (ou skipped)
- Skill alvo executada (ou manual confirmed)
- EQB score calculado para todas stories no scope
- Relatório gerado com gaps e recomendações

## Usage Examples

```bash
# Testar story-executor (Phase 2 completo)
/skill-creator-ops:skill-tester *test-execution-pipeline mode:story-executor scope:all

# Testar wave-execute (Phase 3 completo)
/skill-creator-ops:skill-tester *test-execution-pipeline mode:wave-execute scope:all

# Apenas medir sem re-executar (após execução manual)
/skill-creator-ops:skill-tester *test-execution-pipeline mode:manual skip_reset:true

# Testar apenas Wave 1 com story-executor
/skill-creator-ops:skill-tester *test-execution-pipeline mode:story-executor scope:wave-1

# Testar uma story específica
/skill-creator-ops:skill-tester *test-execution-pipeline mode:story-executor scope:99.1
```
