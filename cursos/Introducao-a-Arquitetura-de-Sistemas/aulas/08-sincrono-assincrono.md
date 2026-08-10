---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: sincrono-assincrono
lesson_position: 8
module: M3
sequence: M3.2
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [mdn-http, azure-background-jobs]
---

# Comunicação síncrona e assíncrona

## Resultado

Você decide quando o chamador precisa esperar e quando o trabalho deve continuar desacoplado da interação inicial.

## Mapa visual

```text
SÍNCRONO
cliente ──pedido──> serviço ──resultado──> cliente esperando

ASSÍNCRONO
cliente ──aceite──> fila ──> worker ──> resultado persistido/notificado
cliente recebe ID e continua
```

## Modelo mental

No modo **síncrono**, o chamador mantém uma interação aberta esperando resposta. É simples para operações rápidas e dependências necessárias ao resultado imediato.

No modo **assíncrono**, o sistema aceita ou registra trabalho e o conclui depois. Isso permite absorver picos, sobreviver a indisponibilidade temporária e executar tarefas longas, mas exige estado, status, retry e uma forma de comunicar conclusão.

Assíncrono não significa necessariamente paralelo. Uma fila pode ser consumida por um único worker, em ordem. E síncrono não significa instantâneo: apenas que o chamador espera.

## Quando usar — e quando não usar

Prefira síncrono quando a resposta é rápida, necessária para o próximo passo e a falha pode ser devolvida imediatamente. Considere assíncrono para processamento longo, picos, integrações instáveis ou trabalho que não precisa terminar antes da tela continuar.

Não use fila para esconder uma operação que o usuário precisa confirmar na hora. Também não mantenha request HTTP aberta por minutos para processar vídeo se você pode aceitar, devolver um ID e oferecer status.

## Caso rápido

Validar se um cupom existe pode ser síncrono. Gerar um relatório de 500 páginas deve ser assíncrono: `POST /relatorios` retorna `202 Accepted` e um `job_id`; o cliente consulta status ou recebe notificação.

Anti-padrão: responder “sucesso” quando apenas enfileirou. O correto é distinguir aceitação de conclusão.

## Prática

Liste cinco operações do seu sistema. Para cada uma, registre:

- precisa do resultado agora?
- tempo esperado;
- o que acontece se a dependência cair;
- como o usuário acompanha;
- veredito síncrono ou assíncrono.

## Pergunte ao seu agente

```text
Classifique estas operações como síncronas ou assíncronas. Questione latência, necessidade do resultado, pico e tolerância à indisponibilidade. Para as assíncronas, exija estado, status, retry e sinal de conclusão.
```

## Evidência de conclusão

Tabela de operações com modo justificado e, para cada fluxo assíncrono, um contrato de aceitação e acompanhamento.

Fontes: [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) e [Azure — Background jobs](https://learn.microsoft.com/en-us/azure/architecture/best-practices/background-jobs).

[Anterior](07-json-yaml-markdown-contratos.md) · [Próxima: filas e eventos](09-webhook-fila-evento-pubsub.md)
