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
  aiox_advanced: 15
  aiox_advanced_squads: 0
  total: 15
  counted_at: '2026-08-10'
---
# Self-heal

Loop automático ou assistido que corrige findings de review, roda a verificação novamente e para por circuit breaker quando não há progresso. A aprovação continua separada de quem corrigiu.

## Como é usado

Use **Self-heal** depois que um quality gate produzir findings objetivos e cada correção puder ser revalidada pelo mesmo critério ou por um revisor independente.

**Exemplo prático:** nas aulas [[48-quality-gate-completo]] e [[49-apply-qa-fixes-loop]], corrija um teste quebrado e um estado vazio ausente, rode os testes e o gate novamente e pare para escalar se o mesmo finding reaparecer.

**Não confunda:** **Self-heal** não é retry infinito nem autoaprovação; cada iteração precisa de evidência, limite de tentativas e revisão independente quando o risco exigir.

**Frequência nos cursos:** **15** menções (AIOX Advanced: 15 · AIOX Advanced Squads: 0).

## Aulas

- [[48-quality-gate-completo]]
- [[49-apply-qa-fixes-loop]]
- [[06-code-rabbit-boost]]

## Ver também

- [[Apply QA Fixes]]
- [[Finding]]
- [[No-self-review]]
- [[Quality Gate]]
- [[Glossário AIOX Advanced]]
