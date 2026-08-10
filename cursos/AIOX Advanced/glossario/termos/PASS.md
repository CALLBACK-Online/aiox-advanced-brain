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
  aiox_advanced: 54
  aiox_advanced_squads: 0
  total: 54
  counted_at: '2026-08-10'
---
# PASS

Veredito do Quality Gate que confirma que a Story ou o artefato satisfez os critérios de aceite e os checks exigidos. O ciclo pode avançar para merge ou promoção.

## Como é usado

Use **PASS** somente depois de executar o gate, resolver os findings bloqueadores e anexar evidência suficiente para outra pessoa repetir a conferência. O veredito deve identificar o que foi verificado.

**Exemplo prático:** após corrigir um erro de foco, rode novamente testes, lint, build e smoke test; registre os resultados e marque **PASS**. Só então o PR pode seguir para merge conforme o contrato do gate.

**Não confunda:** **PASS** não significa que “os testes principais passaram” ou que não existe nenhum nit. Significa que todos os critérios bloqueadores do gate foram atendidos; uma exceção formal deve ser registrada como waiver.

**Frequência nos cursos:** **54** menções (AIOX Advanced: 54 · AIOX Advanced Squads: 0).

## Aulas

- [[48-quality-gate-completo]]
- [[49-apply-qa-fixes-loop]]

## Ver também

- [[Quality Gate]]
- [[FAIL]]
- [[CONCERNS]]
- [[WAIVED]]
- [[Glossário AIOX Advanced]]
