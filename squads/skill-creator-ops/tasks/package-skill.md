# Task: Package Skill

## Purpose
Empacotar skill validada em .zip para distribuição.

## Inputs
- `skill_path` (obrigatório): Path da skill a empacotar
- `output_dir` (opcional): Diretório de saída (default: `./dist/`)

## Executor
skill-ops-chief

## Steps

1. Rodar `python squads/skill-creator-ops/scripts/quick_validate.py {skill_path}`
2. Se validação FAIL → ABORT. "Corrija os erros antes de empacotar."
3. Rodar `python squads/skill-creator-ops/scripts/package_skill.py {skill_path} {output_dir}`
4. Verificar que .zip foi criado
5. Reportar tamanho e conteúdo do package

## Veto Conditions
- Validação falha → ABORT (não empacota skill inválida)
- Skill path não existe → ABORT

## Output
`{skill-name}.zip` no diretório de saída.

## Completion Criteria
- Validação PASS
- .zip criado com estrutura preservada
- Tamanho reportado
