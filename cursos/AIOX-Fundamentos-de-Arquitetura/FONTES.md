---
type: sources
course: aiox-fundamentos-arquitetura
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
verified_at: 2026-08-10
---

# Fontes técnicas primárias

O curso usa documentação de mantenedores, padrões e projetos oficiais. As aulas traduzem essas fontes para modelos mentais; não substituem a documentação de implementação.

## Web, HTTP e contratos

- [MDN — Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview): cliente/servidor, request/response, proxies e HTTP stateless.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html): descrição padronizada de APIs HTTP.
- [Model Context Protocol — Server primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index): distinção entre prompts, resources e tools.

## Dados e estado

- [PostgreSQL — Tutorial](https://www.postgresql.org/docs/current/tutorial.html): conceitos relacionais, tabelas, consultas e transações.
- [PostgreSQL — Indexes](https://www.postgresql.org/docs/current/indexes.html): índices e trade-offs de acesso.
- [Redis — Client-side caching](https://redis.io/docs/latest/develop/reference/client-side-caching/): cache e invalidação.
- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security): políticas de autorização por linha.

## Comunicação, falhas e escala

- [Azure Architecture Center — Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/): estilos e restrições arquiteturais.
- [Azure — Design to scale out](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/scale-out): escala horizontal e gargalos de sincronização.
- [Azure — Load balancing options](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview): distribuição de carga.
- [Azure — Transient fault handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults): timeout, retry, backoff e retry budget.
- [Azure — Circuit Breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker): isolamento de falhas persistentes.
- [Azure — Background jobs](https://learn.microsoft.com/en-us/azure/architecture/best-practices/background-jobs): workers, filas e reprocessamento.

## Operação e entrega

- [OpenTelemetry — Signals](https://opentelemetry.io/docs/concepts/signals/): logs, métricas e traces.
- [Kubernetes — Probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/): startup, liveness e readiness.
- [Docker — What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/): processos isolados e portabilidade.
- [GitHub Actions — Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration): build e testes automatizados.
- [GitHub Actions — Deployment environments](https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments): ambientes, aprovações e secrets de deploy.

## Segurança e fronteiras

- [OWASP — Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html): ciclo de vida, menor privilégio, rotação e auditoria de secrets.
- [Supabase Auth](https://supabase.com/docs/guides/auth): autenticação versus autorização.
- [Azure — Microservices architecture style](https://learn.microsoft.com/en-us/azure/architecture/microservices/): autonomia, acoplamento, observabilidade e custos de sistemas distribuídos.

## Sistemas agentic

- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): workflows, agentes e padrões compostos.
- [Anthropic — Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents): modelo, harness, tools, ambiente e controle humano.
- [OpenAI Agents SDK — Agents](https://openai.github.io/openai-agents-python/agents/): instruções, tools, handoffs, guardrails e runtime.
- [OpenAI Agents SDK — Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/): manager, handoff e execução paralela.
- [OpenAI Agents SDK — Guardrails](https://openai.github.io/openai-agents-python/guardrails/): validação de inputs, outputs e tool calls.

## Regra de atualização

Se uma aula mudar uma definição ou recomendação, verifique primeiro a fonte correspondente e atualize `verified_at`. Exemplos de fornecedor são ilustrações; o conceito deve continuar portátil.
