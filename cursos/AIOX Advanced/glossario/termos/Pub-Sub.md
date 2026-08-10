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
# Pub-Sub

Pub-Sub (*publish-subscribe*) é um padrão em que um produtor publica um evento em um tópico e cada assinatura recebe sua própria entrega. O produtor não precisa conhecer diretamente os consumidores, que podem reagir ao mesmo fato de forma independente.

## Como é usado

Use Pub-Sub quando um fato — por exemplo, `PagamentoConfirmado` — precisa acionar vários consumidores, como e-mail, analytics e fraude. Dê identidade, versão e significado ao evento; trate duplicação, atraso, reordenação e falha de entrega conforme as garantias do broker.

**Exemplo prático:** na aula [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/09-webhook-fila-evento-pubsub]], o mapa mostra um produtor publicando em um tópico e cópias chegando a E-mail, Analytics e Fraude. A mesma aula separa esse padrão da fila, que distribui trabalho entre workers, e do webhook, que entrega uma notificação HTTP.

**Não confunda:** Pub-Sub distribui um fato para múltiplas assinaturas; uma fila normalmente entrega cada job a um worker por vez. Pub-Sub também não é uma resposta síncrona nem substitui uma job queue quando existe um único dono que precisa reivindicar, executar e acompanhar um trabalho.

**Frequência nos cursos:** **1** menção (AIOX Advanced: 1 · AIOX Advanced Squads: 0).

## Aulas

- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/09-webhook-fila-evento-pubsub]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/10-processo-task-job-worker-runner]]

## Ver também

- [[Job queue]]
- [[Job]]
- [[Worker]]
- [[Workflow]]
- [[Glossário AIOX Advanced]]

