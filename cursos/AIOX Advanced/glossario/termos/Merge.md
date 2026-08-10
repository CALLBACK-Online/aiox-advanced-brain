---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 167
  aiox_advanced_squads: 0
  total: 167
  counted_at: '2026-08-10'
---
# Merge

Integrar a mudança na branch principal após gates. Merge sem evidência é atalho caro.

## Como é usado

Use **Merge** para integrar uma mudança na branch principal somente depois dos gates: lint, testes, review e aceite verdes, com evidência registrada — integração é conclusão de ciclo, não atalho.

**Exemplo prático:** na aula [[19-ciclo-do-repositorio]], a mudança sobe por PR, passa pelo Quality Gate ([[48-quality-gate-completo]]) e só então é integrada por quem tem autoridade; a CI/CD segue desse evento.

**Não confunda:** **Merge** integra na branch principal; push publica commits no remoto; deploy coloca a versão em execução. Sem evidência, o merge só desloca o risco para produção.

**Frequência nos cursos:** **167** menções (AIOX Advanced: 167 · AIOX Advanced Squads: 0).

## Aulas

- [[19-ciclo-do-repositorio]]
- [[48-quality-gate-completo]]
- [[72-cicd-pipeline-completa]]

## Ver também

- [[Pull Request]]
- [[CI-CD]]
- [[Quality Gate]]
- [[Glossário AIOX Advanced]]
