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
  aiox_advanced: 9
  aiox_advanced_squads: 0
  total: 9
  counted_at: '2026-08-10'
---
# Job queue

Job queue é uma fila durável que guarda jobs aceitos, mas ainda não processados, até que workers os reivindiquem. Ela desacopla a requisição da execução, absorve picos e permite controlar concorrência, retry, timeout, status e dead-letter.

## Como é usado

Enfileire o `job_id` depois de validar o contrato de entrada; faça um worker reivindicar o job com lease ou visibilidade limitada; registre sucesso, falha e tentativa de forma idempotente. A fila deve deixar claro o que está aguardando, executando, atrasado ou abandonado.

**Exemplo prático:** na aula [[67-harness-ambiente-execucao]], o caminho do lab ao harness inclui “Job queue: Async + status”; o caso usa limite de tokens por job, timeout de 90 segundos e dead-letter. Na aula [[68-squad-fora-do-claude-code]], a job queue sustenta a extração do squad com contratos congelados.

**Não confunda:** job queue não é o job: a fila transporta e agenda unidades de trabalho. Também não é Pub-Sub: numa fila, normalmente cada item é reivindicado por um worker; em Pub-Sub, o evento pode ser entregue a vários assinantes independentes.

**Frequência nos cursos:** **9** menções (AIOX Advanced: 9 · AIOX Advanced Squads: 0).

## Aulas

- [[67-harness-ambiente-execucao]]
- [[68-squad-fora-do-claude-code]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/10-processo-task-job-worker-runner]]

## Ver também

- [[Job]]
- [[Worker]]
- [[Pub-Sub]]
- [[Harness]]
- [[Workflow]]
- [[Glossário AIOX Advanced]]

