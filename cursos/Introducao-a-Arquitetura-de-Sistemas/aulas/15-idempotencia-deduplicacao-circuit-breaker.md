---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: idempotencia-deduplicacao-circuit-breaker
lesson_position: 15
module: M5
sequence: M5.3
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [azure-circuit-breaker]
reading_minutes: 5
---

# Idempotência, deduplicação e circuit breaker

## Resultado

Você impede que repetição legítima multiplique efeitos e evita que dependência persistentemente falha derrube o restante do sistema.

## Mapa visual

```text
mesma idempotency_key ──> mesmo resultado final
event_id já processado ──> deduplicar
falhas acima do limite ──> circuit OPEN ──> falhar rápido
                                      └─ depois: HALF-OPEN testa recuperação
```

## Modelo mental

**Idempotência** é propriedade da operação: repeti-la com a mesma intenção não muda o efeito final além da primeira aplicação. Uma chave idempotente permite reconhecer a mesma tentativa.

**Deduplicação** detecta mensagens ou eventos já processados, geralmente por identificador e janela de retenção. Ajuda a realizar idempotência, mas não substitui regras de domínio.

**Circuit breaker** observa falhas de uma dependência. Fechado, permite chamadas; aberto, falha rápido; semiaberto, testa recuperação. Ele protege recursos e evita cascata quando retry não resolverá imediatamente.

## Quando usar — e quando não usar

Exija idempotência em cobrança, criação de pedido, webhook e job reprocessável. Use deduplicação quando a entrega pode ser “pelo menos uma vez”. Considere circuit breaker para dependências remotas com falhas persistentes e fallback possível.

Não trate operações diferentes como duplicadas só porque o payload coincide. Defina escopo e validade da chave. Não use circuit breaker para esconder erro de regra local. E não retorne dado velho como fallback sem comunicar degradação.

## Caso rápido

O cliente envia `idempotency_key=checkout-123`. A primeira tentativa cria a cobrança e persiste resultado. A conexão cai antes da response. Na repetição, o servidor retorna a mesma cobrança, não cria outra. Se o provedor estiver indisponível por tempo prolongado, o circuit abre e evita milhares de conexões penduradas.

Anti-padrão: marcar mensagem como processada antes de persistir o efeito, perder energia e descartar a nova entrega como duplicada.

## Prática

Desenhe uma operação repetível com chave, armazenamento do resultado, janela, transação e resposta na repetição. Depois defina estados do circuit e comportamento degradado.

## Pergunte ao seu agente

```text
Faça threat modeling de duplicação e cascata para esta operação. Defina idempotency key, escopo, persistência, transação, deduplicação e estados do circuit breaker. Mostre o que acontece se cair antes e depois do efeito.
```

## Evidência de conclusão

Teste de cenário demonstrando que duas entregas produzem um efeito e que uma dependência falha não consome recursos indefinidamente.

Fonte: [Azure — Circuit Breaker](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker).

[Anterior](14-timeout-retry-backoff-rate-limit.md) · [Quiz M5](../avaliacoes/Quiz-M5-escala-e-confiabilidade.md) · [Próxima: observabilidade](16-logs-metricas-traces-health-checks.md)
