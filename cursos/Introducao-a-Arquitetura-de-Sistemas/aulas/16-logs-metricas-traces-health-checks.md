---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: logs-metricas-traces-health-checks
lesson_position: 16
module: M6
sequence: M6.1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [opentelemetry-signals, kubernetes-probes]
reading_minutes: 5
---

# Logs, métricas, traces e health checks

## Resultado

Você escolhe o sinal certo para responder uma pergunta operacional e diferencia “processo vivo” de “serviço pronto”.

## Mapa visual

```text
Log:    qual evento aconteceu?
Métrica: quanto/como varia no tempo?
Trace:  por onde esta operação passou?
Probe:  iniciou? está vivo? está pronto para tráfego?
```

## Modelo mental

**Log** registra evento discreto com contexto. **Métrica** mede valores agregáveis, como taxa, latência e erros. **Trace** conecta etapas da mesma operação através de componentes usando correlação. **Health check** responde a uma pergunta operacional específica.

Em ambientes orquestrados:

- startup: terminou de inicializar?
- liveness: travou de forma que reiniciar ajuda?
- readiness: pode receber tráfego agora?

Observabilidade não é “ter dashboard”; é conseguir inferir estado interno pelos sinais produzidos e investigar falha sem adivinhar.

## Quando usar — e quando não usar

Defina sinais a partir de perguntas: “qual etapa está lenta?”, “quantos jobs falharam?”, “qual tenant é afetado?”. Correlacione logs e traces por request/job ID. Use readiness para retirar instância temporariamente incapaz.

Não logue secrets, tokens ou payload sensível. Não use identificadores de alta cardinalidade indiscriminadamente em métricas. Não faça liveness depender de toda dependência externa: uma oscilação pode reiniciar todas as instâncias e piorar a cascata.

## Caso rápido

O usuário diz “checkout lento”. A métrica mostra p95 alto; o trace localiza a espera no pagamento; o log correlacionado mostra `timeout`; readiness continua verde porque a API ainda atende outros endpoints. Cada sinal responde uma parte.

Anti-padrão: log `deu erro` sem timestamp, operação, correlação, tipo e dependência.

## Prática

Escolha um fluxo e escreva cinco perguntas operacionais. Para cada uma, escolha log, métrica, trace ou probe; defina campos e alerta, sem registrar dado sensível.

## Pergunte ao seu agente

```text
Converta estas perguntas operacionais em sinais. Para cada uma, escolha log, métrica, trace ou health check, defina correlação e evite secrets/alta cardinalidade. Diferencie startup, liveness e readiness.
```

## Evidência de conclusão

Plano de observabilidade no qual cada sinal responde uma pergunta e permite localizar o componente afetado.

Fontes: [OpenTelemetry — Signals](https://opentelemetry.io/docs/concepts/signals/) e [Kubernetes — Probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/).

[Anterior](15-idempotencia-deduplicacao-circuit-breaker.md) · [Próxima: runtime](17-runtime-harness-ambiente-container.md)
