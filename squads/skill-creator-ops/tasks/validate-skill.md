# Task: Validate Skill

## Purpose
Validar uma skill contra o checklist de qualidade AllFluence (12 checks).

## Inputs
- `skill_path` (obrigatório): Path do diretório da skill (e.g., `.claude/skills/tech-search/`)

## Executor
skill-validator

## Steps

1. Verificar que `skill_path` existe e contém `SKILL.md`
2. Rodar `python squads/skill-creator-ops/scripts/quick_validate.py {skill_path}`
3. Se script retorna PASS: executar checks adicionais (registry, tier structure)
4. Gerar relatório usando `templates/validation-report-tmpl.yaml`
5. Retornar verdict: PASS | PASS_WITH_WARNINGS | FAIL

## Veto Conditions
- Skill path não existe → ABORT
- SKILL.md não encontrado → FAIL imediato
- Name não é kebab-case → FAIL

## Output
`validation-report.yaml` preenchido com 12 checks e score.

## Completion Criteria
- Todos 12 checks executados
- Score calculado
- Findings documentados
