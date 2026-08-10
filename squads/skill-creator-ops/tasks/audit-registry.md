# Task: Audit Skill Registry

## Purpose
Auditar skill-registry.yaml contra o filesystem para detectar inconsistências.

## Inputs
- Nenhum (usa paths canônicos)

## Executor
skill-ops-chief

## Steps

1. Ler `skills/skill-registry.yaml`
2. Listar todos diretórios em `skills/` que contêm `SKILL.md`
3. Comparar:
   - Skills no filesystem mas não no registry → **ORPHAN**
   - Skills no registry mas não no filesystem → **PHANTOM**
   - Skills com versão diferente (registry vs frontmatter) → **STALE**
4. Gerar relatório com contagens e ações recomendadas
5. Se `--fix` flag: registrar orphans automaticamente, remover phantoms

## Veto Conditions
- skill-registry.yaml não existe → ABORT
- skills/ não existe → ABORT

## Output
Relatório de auditoria com inconsistências e ações recomendadas.

## Completion Criteria
- Todas skills no filesystem verificadas
- Todas entries no registry verificadas
- Inconsistências listadas com ação recomendada
