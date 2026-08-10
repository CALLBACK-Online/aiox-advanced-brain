# Task: Test Skill

## Purpose
Testar uma skill em sandbox isolado, verificando execução end-to-end.

## Inputs
- `skill_path` (obrigatório): Path da skill a testar
- `golden_output_path` (opcional): Path do golden output para regression test

## Executor
skill-tester

## Steps

1. Criar sandbox: `tests/sandbox/skill-tests/{skill-name}/`
2. **Smoke test:** Verificar SKILL.md parseable, frontmatter válido
3. **Functional test:** Se skill tem `scripts/`, executar cada script com inputs de exemplo
4. **Integration test:** Se skill é `user-invocable: true`, simular invocação
5. **Regression test:** Se `golden_output_path` fornecido, comparar output vs golden
6. Gerar relatório usando `templates/test-result-tmpl.yaml`
7. Limpar sandbox (opcional)

## Veto Conditions
- Skill path não existe → ABORT
- SKILL.md não parseable → FAIL no smoke test (bloqueia demais testes)

## Output
`test-result.yaml` preenchido com todos testes executados e scores.

## Completion Criteria
- Todos níveis de teste executados (ou SKIP documentado)
- Score calculado
- Evidências capturadas
