# Design Ops Architecture

## Tese

`design-ops` é o container canônico do provider de design.

O legado em `squads/design-system/` permanece como fonte de referência e
extração, não como casa do estado futuro.

## Ownership

`design-ops` possui:

- tokens
- foundations
- componentes-base
- acessibilidade do provider
- registry e metadata
- runtime técnico do starter

`design-ops` não possui:

- composição de páginas
- superfícies especializadas de app
- roster legacy multiagente

## Runtime Strategy

Nesta rodada, o runtime de contexto do `design-chief` continua reaproveitando
os resolvers de `design-system` para evitar duplicação prematura.

Isso é uma ponte operacional, não uma dependência de ownership.

O ownership canônico já muda para `design-ops`; a extração física do restante
do runtime pode acontecer em wave posterior.

## Pipeline Strategy (MVP)

Para capturar o ganho prático do modelo "constraint-first", o squad expõe um
pipeline mínimo em `squads/design-ops/scripts/`:

- `context-injector.cjs`: coleta contexto ativo + snippets curados legados
- `resolve-project context contracts.cjs`: valida resolução dos contratos canônicos
- `autofix-deterministic.cjs`: aplica correções determinísticas e idempotentes
- `run-minimal-pipeline.cjs`: gera relatório único para benchmark local

Esse MVP substitui narrativa genérica por execução reproduzível e mensurável.
