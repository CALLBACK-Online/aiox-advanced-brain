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
  aiox_advanced: 16
  aiox_advanced_squads: 0
  total: 16
  counted_at: '2026-08-10'
---
# Release

Entrega versionada de uma mudança para consumo dos usuários ou de outros sistemas, com escopo, versão, evidência e caminho operacional conhecidos. Uma release pode estar pronta antes de ser promovida ao ambiente de produção.

## Como é usado

Use **Release** para identificar e comunicar uma versão concreta: registre o commit ou artefato, as mudanças incluídas, a estratégia de exposição, o responsável e o plano de rollback antes da promoção.

**Exemplo prático:** após o Quality Gate, o DevOps etiqueta `v1.8.0`, registra o commit, publica as release notes e promove o mesmo artefato para staging. A versão só vira release de production depois do smoke test e da decisão de promoção.

**Não confunda:** **Release** nomeia a entrega versionada; **Deploy** coloca um artefato em um ambiente; **Rollback** retorna a uma versão ou configuração conhecida como boa. São momentos relacionados, mas não são sinônimos.

**Frequência nos cursos:** **16** menções (AIOX Advanced: 16 · AIOX Advanced Squads: 0).

## Aulas

- [[05-ambientes-local-staging-production]]
- [[72-cicd-pipeline-completa]]
- [[71-vercel-deploy]]
- [[25-core-config-leis-sociais]]

## Ver também

- [[Deploy]]
- [[Rollback]]
- [[CI-CD]]
- [[Production readiness]]
- [[Glossário AIOX Advanced]]
