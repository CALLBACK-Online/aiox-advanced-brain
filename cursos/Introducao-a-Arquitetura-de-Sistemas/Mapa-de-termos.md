---
type: decision-map
course: introducao-arquitetura-sistemas
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
---

# Mapa de termos técnicos

[Curso](README.md) · [Glossário](Glossario.md) · [Guia para agentes](AGENT-GUIDE.md)

| Se a dúvida contém… | Comece aqui |
|----------------------|-------------|
| sistema, componente, fronteira, dependência | [Aula 01](aulas/01-sistema-componentes-fronteiras.md) |
| cliente, servidor, frontend, backend | [Aula 02](aulas/02-cliente-servidor-frontend-backend.md) |
| HTTP, request, response, API, endpoint | [Aula 03](aulas/03-http-request-response-api.md) |
| estado, stateless, entidade, ciclo de vida | [Aula 04](aulas/04-estado-entidade-ciclo-de-vida.md) |
| banco, schema, tabela, índice, transação | [Aula 05](aulas/05-banco-schema-indice-transacao.md) |
| cache, arquivo, blob, object storage | [Aula 06](aulas/06-cache-arquivos-object-storage.md) |
| JSON, YAML, Markdown, contrato | [Aula 07](aulas/07-json-yaml-markdown-contratos.md) |
| síncrono, assíncrono, espera | [Aula 08](aulas/08-sincrono-assincrono.md) |
| webhook, fila, evento, pub/sub | [Aula 09](aulas/09-webhook-fila-evento-pubsub.md) |
| processo, task, job, worker, runner | [Aula 10](aulas/10-processo-task-job-worker-runner.md) |
| workflow, pipeline, batch, stream | [Aula 11](aulas/11-workflow-pipeline-batch-stream.md) |
| concorrência, paralelo, fan-out, fan-in | [Aula 12](aulas/12-concorrencia-paralelismo-fanout-fanin.md) |
| escala vertical/horizontal, load balancer | [Aula 13](aulas/13-escala-load-balancing.md) |
| timeout, retry, backoff, rate limit | [Aula 14](aulas/14-timeout-retry-backoff-rate-limit.md) |
| idempotência, duplicação, circuit breaker | [Aula 15](aulas/15-idempotencia-deduplicacao-circuit-breaker.md) |
| logs, métricas, traces, health check | [Aula 16](aulas/16-logs-metricas-traces-health-checks.md) |
| runtime, harness, ambiente, container | [Aula 17](aulas/17-runtime-harness-ambiente-container.md) |
| CI, CD, deploy, rollback | [Aula 18](aulas/18-cicd-deploy-rollback.md) |
| autenticação, autorização, secret | [Aula 19](aulas/19-autenticacao-autorizacao-secrets.md) |
| tenant, isolamento, RLS | [Aula 20](aulas/20-multitenancy-isolamento-rls.md) |
| monólito, módulo, microsserviço, acoplamento | [Aula 21](aulas/21-monolito-modulos-microsservicos.md) |
| modelo, contexto, memória, tool, skill | [Aula 22](aulas/22-modelo-contexto-memoria-tool-skill.md) |
| orquestrador, squad, human-in-the-loop, gate | [Aula 23](aulas/23-orquestrador-squad-human-in-loop.md) |
| desenhar ou revisar uma arquitetura completa | [Aula 24](aulas/24-capstone-arquitetura-agentic.md) |

## Ordem de decisão

Quando vários termos aparecem juntos, não comece pela tecnologia. Pergunte nesta ordem:

1. Qual valor o sistema entrega e onde termina sua fronteira?
2. Qual estado precisa sobreviver?
3. Quem se comunica com quem e com qual contrato?
4. O que executa cada etapa?
5. Como falha, escala e é observado?
6. Quem pode fazer o quê?
7. Onde a IA decide e onde o humano mantém controle?
