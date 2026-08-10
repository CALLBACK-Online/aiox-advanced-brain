---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: timeout-retry-backoff-rate-limit
lesson_position: 14
module: M5
sequence: M5.2
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [azure-transient-faults]
---

# Timeout, retry, backoff e rate limit

## Resultado

Você trata falhas transitórias sem esperar para sempre nem criar tempestade de tentativas.

## Mapa visual

```text
chamada ── timeout ──> falhou
                      ├─ erro transitório? retry limitado
                      │                  └─ backoff + jitter
                      └─ erro permanente? falhar/compensar

entrada ── rate limit ──> protege capacidade
```

## Modelo mental

**Timeout** define quanto esperar antes de considerar que uma tentativa não concluiu. Sem ele, conexões e workers podem ficar presos.

**Retry** repete uma operação quando existe chance real de recuperação. **Backoff** aumenta o intervalo entre tentativas; jitter adiciona variação para clientes não voltarem todos no mesmo instante.

**Rate limit** restringe operações em uma janela para proteger capacidade, custo ou política. Pode devolver `429` e sinalizar quando tentar novamente.

Esses mecanismos trabalham juntos. Retry sem timeout não sabe quando agir; retry sem limite multiplica carga; rate limit sem feedback incentiva clientes a insistirem.

## Quando usar — e quando não usar

Use retry para falhas transitórias conhecidas, com máximo e orçamento agregados. Respeite `Retry-After` quando fornecido. Use rate limit na borda e em recursos caros.

Não repita automaticamente erro de validação, permissão ou operação não idempotente. Não configure timeout arbitrariamente curto. Não faça retry imediato em dezenas de workers: isso derruba uma dependência que tentava se recuperar.

## Caso rápido

Uma API externa responde `503`. O cliente espera com backoff e tenta até três vezes dentro de um orçamento. Se a operação cria cobrança sem chave idempotente, repetir pode cobrar de novo; o retry deve esperar a proteção da próxima aula.

Anti-padrão: cada camada faz três retries. Cliente, API e SDK multiplicam 3 × 3 × 3 = 27 tentativas para uma ação.

## Prática

Escolha três dependências e documente timeout, erros transitórios, máximo de retries, backoff, orçamento total e comportamento final. Classifique uma operação que nunca deve repetir automaticamente.

## Pergunte ao seu agente

```text
Desenhe a política de timeout/retry desta dependência. Diferencie erro transitório e permanente, detecte retries em camadas, inclua backoff, jitter, orçamento e rate limit. Bloqueie retry se a operação não for idempotente.
```

## Evidência de conclusão

Política finita em que cada tentativa tem motivo, limite e sinal; o sistema protege a dependência em vez de amplificar a falha.

Fonte: [Azure — Transient fault handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults).

[Anterior](13-escala-load-balancing.md) · [Próxima: idempotência](15-idempotencia-deduplicacao-circuit-breaker.md)
