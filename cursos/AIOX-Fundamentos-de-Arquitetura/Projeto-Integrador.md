---
type: capstone
course: aiox-fundamentos-arquitetura
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
---

# Projeto integrador — Arquitetura explicável

Escolha um sistema real pequeno: agenda, checkout, onboarding, atendimento, conteúdo ou processamento de documentos. Não implemente o software; produza uma arquitetura que outra pessoa consiga revisar.

## Entrega

1. **Fronteira:** objetivo, usuários, componentes internos e sistemas externos.
2. **Fluxo crítico:** request inicial até resposta ou conclusão assíncrona.
3. **Estado:** entidades, fonte de verdade, cache e arquivos.
4. **Comunicação:** contratos, chamadas síncronas, filas, eventos ou webhooks.
5. **Execução:** processos, workers, workflow e qualquer fan-out/fan-in.
6. **Confiabilidade:** timeout, retry, idempotência, rate limit e falha degradada.
7. **Operação:** logs, métricas, trace, health check, deploy e rollback.
8. **Segurança:** identidade, autorização, secrets e isolamento de tenant, se existir.
9. **Camada agentic:** modelo, contexto, tools, memória, orquestração, gates e pontos de aprovação humana.
10. **Trade-offs:** três decisões, alternativa rejeitada e sinal que faria reconsiderar.

## Formato sugerido

```text
arquitetura.md
├── contexto e fronteira
├── diagrama de componentes
├── fluxo crítico
├── decisões por camada
├── falhas e observabilidade
├── camada agentic
└── trade-offs e dúvidas abertas
```

## Portão

Passe a entrega pela [Rubrica](Rubrica.md). Depois peça ao agente uma revisão adversarial: ele deve encontrar acoplamentos, estado sem dono, efeitos duplicáveis, ausência de evidência e tecnologia sem necessidade.
