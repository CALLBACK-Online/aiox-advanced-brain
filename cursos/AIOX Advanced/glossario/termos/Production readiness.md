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
  aiox_advanced: 1
  aiox_advanced_squads: 0
  total: 1
  counted_at: '2026-08-10'
---
# Production readiness

Estado comprovado em que o sistema pode operar em production com falhas visíveis, recuperação conhecida e responsabilidade definida. Inclui, conforme o risco, health check, smoke test, logs, alertas, secrets, dependências, segurança, custo, rollback, backup/restore e on-call.

## Como é usado

Use **Production readiness** como gate antes da promoção: confira o ambiente real, execute o caminho crítico, confirme o rollback, prove o restore de dados e registre quem responde a um incidente. Cada item precisa de evidência ou de uma decisão explícita de risco aceito.

**Exemplo prático:** antes de abrir o produto ao público, a equipe verifica a URL de production, roda o smoke test, confirma logs e alertas, restaura um backup em staging, testa o retorno para a versão anterior e registra o on-call. Sem esses resultados, a Story não está pronta para production, mesmo que o build passe.

**Não confunda:** **Production readiness** não é “funciona no meu notebook”, nem é apenas **Deploy** ou **Release**. Readiness prova que o sistema e a operação sobrevivem ao ambiente real: há diagnóstico, recuperação e dono, não só uma execução local bem-sucedida.

**Frequência nos cursos:** **1** menção (AIOX Advanced: 1 · AIOX Advanced Squads: 0).

## Aulas

- [[73-prontidao-de-producao]]
- [[71-vercel-deploy]]
- [[72-cicd-pipeline-completa]]
- [[05-ambientes-local-staging-production]]

## Ver também

- [[Deploy]]
- [[Release]]
- [[Rollback]]
- [[Backup restore]]
- [[On-call]]
- [[Evidência]]
- [[Glossário AIOX Advanced]]
