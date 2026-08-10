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
  aiox_advanced: 5
  aiox_advanced_squads: 0
  total: 5
  counted_at: '2026-08-10'
---
# Contrato de API

Acordo explícito da superfície de uma API: entrada, saída, autenticação, idempotência, estados, erros e, quando houver, webhooks. No AIOX, a API é contrato de chamada — não apenas uma rota HTTP ou um wrapper de prompt.

## Como é usado

Use **Contrato de API** antes de codar a integração: congele schemas de input/output, quem pode disparar a operação, estados observáveis, classes de erro e o critério de sucesso. Para jobs curtos e baratos, uma chamada síncrona pode bastar; se a execução passar de alguns segundos ou chamar tools, trate-a como job orientado a estados, não como request síncrono heróico.

**Exemplo prático:** na aula [[68-squad-fora-do-claude-code]], o contrato mínimo usa `POST /jobs` com payload versionado e `idempotency-key`, `GET /jobs/:id` para `queued | running | succeeded | failed | cancelled` e `POST /jobs/:id/cancel` como kill switch. O contrato também registra auth, schemas de entrada e saída, erros e o [[Quality Gate|QG]] do job.

**Não confunda:** **Contrato de API** não é REST por estética nem um `POST /run` que esconde estado no chat. Também não substitui o [[Data contract|contrato de dados]]: a API descreve a fronteira de chamada e seu ciclo; o contrato de dados define o que o app pode ler ou escrever sem contornar policy. **Alerta de segurança:** endpoint público, timeout ou wrapper de LLM não resolvem autenticação, isolamento ou secrets.

**Frequência nos cursos:** **5** menções (AIOX Advanced: 5 · AIOX Advanced Squads: 0).

## Aulas

- [[68-squad-fora-do-claude-code]]
- [[69-escada-progressiva-script-a-saas]]

## Ver também

- [[Data contract]]
- [[Schema]]
- [[Autenticação e Autorização]]
- [[Idempotência]]
- [[Tenant isolation]]
- [[Glossário AIOX Advanced]]
