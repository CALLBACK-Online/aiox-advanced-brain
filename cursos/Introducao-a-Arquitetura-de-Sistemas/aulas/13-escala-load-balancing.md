---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: escala-load-balancing
lesson_position: 13
module: M5
sequence: M5.1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [azure-scale-out, azure-load-balancing]
---

# Escala vertical, horizontal e load balancing

## Resultado

Você identifica o gargalo antes de adicionar capacidade e distingue fortalecer uma instância de multiplicar instâncias.

## Mapa visual

```text
Vertical (scale up)              Horizontal (scale out)
1 servidor → mais CPU/RAM        1 → 2 → 4 instâncias
                                 tráfego → load balancer → instâncias
```

## Modelo mental

**Escala vertical** aumenta recursos de uma instância: mais CPU, memória ou disco. É simples, mas possui limite físico, custo crescente e ainda concentra falha.

**Escala horizontal** adiciona instâncias. Pode aumentar capacidade e disponibilidade, mas exige que estado, jobs e arquivos não fiquem presos a uma máquina.

**Load balancer** distribui tráfego entre recursos capazes de responder. Ele não corrige banco lento, lock global ou código ineficiente; apenas reparte a carga que pode ser repartida.

Escala é medida pelo ganho de throughput em relação aos recursos adicionados. Duplicar servidores e obter 10% de ganho revela gargalo compartilhado.

## Quando usar — e quando não usar

Escale depois de medir CPU, memória, latência, throughput, banco e dependências. Vertical costuma ser suficiente no início. Horizontal é valioso quando a aplicação é replicável e a demanda ou disponibilidade justificam.

Não comece por Kubernetes ou dez serviços para um produto sem carga. Não mantenha sessão apenas na memória local e espere distribuir requests livremente. Não confunda pico de cinco minutos com crescimento permanente.

## Caso rápido

Uma API com CPU saturada e requests independentes pode ganhar com mais instâncias. Se todas disputam a mesma consulta sem índice, o banco continua gargalo e pode piorar. Se upload fica no disco local, a próxima request pode cair em outra instância e não encontrar o arquivo.

Anti-padrão: autoscaling sem limite ou métrica de negócio. O sistema pode escalar custo em resposta a abuso.

## Prática

Para um fluxo, registre demanda atual, SLO de latência, gargalo medido e três opções: otimizar, scale up, scale out. Diga qual sinal dispara cada uma e qual custo novo aparece.

## Pergunte ao seu agente

```text
Antes de recomendar escala, peça evidências de CPU, memória, latência, throughput, banco e dependências. Compare otimização, escala vertical e horizontal. Se sugerir load balancer, explique estado, health checks e limite de custo.
```

## Evidência de conclusão

Decisão de capacidade ligada a uma métrica e a um gargalo, com critério de entrada e saída; nenhuma tecnologia aparece apenas por moda.

Fontes: [Azure — Scale out](https://learn.microsoft.com/en-us/azure/architecture/guide/design-principles/scale-out) e [Load balancing](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview).

[Anterior](12-concorrencia-paralelismo-fanout-fanin.md) · [Próxima: falhas transitórias](14-timeout-retry-backoff-rate-limit.md)
