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
  aiox_advanced: 2
  aiox_advanced_squads: 0
  total: 2
  counted_at: '2026-08-10'
---
# Health check

Verificação automática de disponibilidade e saúde operacional de um serviço, normalmente por endpoint, probe ou status. Complementa o smoke test com observação contínua.

## Como é usado

Configure um **Health check** no ambiente publicado para falhar quando o processo ou uma dependência crítica, como o banco, não estiver disponível. Use o status para alerta e decisão operacional.

**Exemplo prático:** na prontidão de produção da aula [[73-prontidao-de-producao]], consulte o endpoint de saúde em production, confirme a resposta e as dependências mínimas e registre o resultado junto do smoke test do fluxo principal.

**Não confunda:** **Health check** não prova que o usuário consegue concluir um fluxo de negócio; um serviço pode responder “vivo” e ainda falhar no login ou pagamento. Combine-o com smoke test.

**Frequência nos cursos:** **2** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 0).

## Aulas

- [[73-prontidao-de-producao]]
- [[72-cicd-pipeline-completa]]

## Ver também

- [[Smoke test]]
- [[Deploy]]
- [[CI-CD]]
- [[Glossário AIOX Advanced]]
