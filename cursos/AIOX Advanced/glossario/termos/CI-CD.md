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
  aiox_advanced: 103
  aiox_advanced_squads: 0
  total: 103
  counted_at: '2026-08-10'
---
# CI/CD

Integração e entrega contínuas: pipeline que integra mudanças, executa build e testes, aplica quality gates e promove o artefato para preview ou production. No AIOX, cada promoção precisa deixar evidência.

## Como é usado

Use **CI/CD** a cada mudança integrada para repetir os mesmos checks e impedir que um artefato avance sem os critérios definidos. Separe o que roda automaticamente do que exige decisão de promoção.

**Exemplo prático:** um pull request dispara lint, testes e build; com **PASS**, a pipeline publica uma preview, roda o smoke test e só promove a mesma versão para production se a evidência estiver íntegra.

**Não confunda:** **CI/CD** não é sinônimo de deploy automático nem substitui um quality gate. Uma pipeline rápida que não testa o aceite ou não bloqueia falhas apenas automatiza a passagem do problema.

**Frequência nos cursos:** **103** menções (AIOX Advanced: 103 · AIOX Advanced Squads: 0).

## Aulas

- [[72-cicd-pipeline-completa]]
- [[71-vercel-deploy]]
- [[73-prontidao-de-producao]]

## Ver também

- [[Deploy]]
- [[Vercel]]
- [[Quality Gate]]
- [[Local Staging Production]]
- [[Smoke test]]
- [[Glossário AIOX Advanced]]
