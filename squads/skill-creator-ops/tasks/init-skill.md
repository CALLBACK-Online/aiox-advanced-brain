# Task: Init Skill

## Purpose
Criar scaffold de uma nova skill com template AllFluence completo.

## Inputs
- `skill_name` (obrigatório): Nome kebab-case da skill (e.g., `my-new-skill`)
- `skill_path` (opcional): Path destino (default: `.claude/skills/`)

## Executor
skill-ops-chief

## Steps

1. Validar nome: kebab-case, max 40 chars, sem hyphens duplos
2. Verificar se skill já existe no path → se sim, ABORT
3. Rodar `python squads/skill-creator-ops/scripts/init_skill.py {skill_name} --path {skill_path}`
4. Verificar que SKILL.md foi criado com frontmatter AllFluence (9 campos)
5. Apresentar next steps ao usuário

## Veto Conditions
- Nome não é kebab-case → ABORT com sugestão de correção
- Skill já existe → ABORT ("Use *validate para checar a existente")
- Path destino não existe → ABORT

## Output
Diretório da skill criado com SKILL.md + scripts/ + references/ + assets/

## Completion Criteria
- Diretório criado
- SKILL.md com frontmatter AllFluence válido
- Subdirectories criados (scripts/, references/, assets/)
