---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: http-request-response-api
lesson_position: 3
module: M1
sequence: M1.3
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [mdn-http, openapi]
---

# HTTP, request, response, API e endpoint

## Resultado

Você consegue ler uma interação HTTP simples e identificar operação, endereço, entrada, resultado e erro esperado.

## Mapa visual

```text
REQUEST
POST /reservas
headers: autorização, formato
body: { horario, servico }
            ↓
        API / endpoint
            ↓
RESPONSE
201 Created
body: { id, status }
```

## Modelo mental

HTTP é um protocolo de mensagens entre cliente e servidor. A mensagem de ida é a **request**; a de volta é a **response**. Uma **API** é o contrato de capacidades oferecidas a outro software. Um **endpoint** é uma operação concreta desse contrato, normalmente combinando método e caminho.

Uma request costuma trazer:

- método: intenção como `GET`, `POST`, `PATCH` ou `DELETE`;
- caminho: recurso alvo;
- headers: metadados, autenticação e formato;
- body: dados enviados, quando aplicável.

A response traz código de status, headers e possivelmente um body. `2xx` indica sucesso; `4xx`, problema relacionado à solicitação; `5xx`, falha no servidor ou dependência. Isso não elimina a necessidade de um erro de domínio claro.

## Quando usar — e quando não usar

Use HTTP quando a interação combina bem com request/response e interoperabilidade web. Documente o contrato quando mais de um componente ou equipe depende dele.

Não transforme toda interação em API HTTP. Trabalho demorado, picos de carga ou entrega que precisa sobreviver a indisponibilidade podem exigir mecanismo assíncrono. Também não confunda “API” com implementação: o contrato é o que consumidores enxergam; o código interno pode mudar.

## Caso rápido

`POST /reservas` pode retornar `201` com a reserva, `409` se o horário acabou e `422` se os dados violam uma regra. Retornar sempre `200` com `{ sucesso: false }` esconde semântica de transporte e dificulta clientes, logs e alertas.

Anti-padrão: expor tabelas diretamente como endpoints sem modelar a intenção do negócio. `POST /aprovar-reembolso` comunica melhor uma decisão do que permitir que qualquer cliente altere uma coluna `status`.

## Prática

Especifique uma operação com:

1. método e caminho;
2. request mínima;
3. response de sucesso;
4. dois erros previsíveis;
5. regra que o servidor precisa validar.

Não escreva código. O exercício é contrato.

## Pergunte ao seu agente

```text
Revise este contrato HTTP como consumidor e como servidor. Encontre ambiguidades, validações ausentes, erros mal representados e detalhes internos vazando. Não implemente; devolva uma versão mínima do contrato.
```

## Evidência de conclusão

Contrato que outra pessoa consegue consumir sem adivinhar método, payload, sucesso, falhas e regra de autorização.

Fontes: [MDN — Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) e [OpenAPI Specification](https://spec.openapis.org/oas/latest.html).

[Anterior](02-cliente-servidor-frontend-backend.md) · [Quiz M1](../avaliacoes/Quiz-M1-ler-o-mapa.md) · [Próxima: estado](04-estado-entidade-ciclo-de-vida.md)
