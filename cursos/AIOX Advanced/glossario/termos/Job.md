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
  aiox_advanced: 77
  aiox_advanced_squads: 0
  total: 77
  counted_at: '2026-08-10'
---
# Job

Job é uma unidade persistida de trabalho, com identidade, entrada, estado e resultado ou erro acompanháveis ao longo do ciclo de execução. Pode ser agendado, colocado em fila, retomado e reprocessado sem depender da memória de uma sessão de chat.

## Como é usado

Modele um job quando uma execução precisa sobreviver ao fechamento do cliente, ter status, timeout, retry, idempotência ou auditoria. Uma API pode aceitar a solicitação, devolver um `job_id` e deixar um worker atualizar estados como `pending`, `running`, `succeeded` e `failed`.

**Exemplo prático:** na aula [[67-harness-ambiente-execucao]], o harness mínimo registra `job_id`, duração, erro e tokens, com limite de tokens por job, timeout e dead-letter. Na aula [[68-squad-fora-do-claude-code]], a extração do squad congela contratos e passa pelo runner de Job + worker antes de expor uma API.

**Não confunda:** job é o registro persistível do trabalho; **task** é uma unidade delimitada que pode estar dentro dele; **worker** é quem executa. Um job pode conter várias tasks e não é sinônimo de processo, agente ou item da fila.

**Frequência nos cursos:** **77** menções (AIOX Advanced: 77 · AIOX Advanced Squads: 0).

## Aulas

- [[67-harness-ambiente-execucao]]
- [[68-squad-fora-do-claude-code]]
- [[72-cicd-pipeline-completa]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/10-processo-task-job-worker-runner]]

## Ver também

- [[Job queue]]
- [[Task]]
- [[Worker]]
- [[Harness]]
- [[Workflow]]
- [[Glossário AIOX Advanced]]

