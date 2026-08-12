---
type: source-brief
course: aiox-agent-engineering
source_id: 81
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
updated: '2026-08-12'
---

# Fonte 81 — Identidade, tempo e isolamento

Síntese para a aula [12e](../aulas/12e-identidade-tempo-isolamento.md). Esta nota **é** a evidência.

Três perguntas que fabricam fato em silêncio: quem é, ainda vale, quem pode ver.

## Identidade

- Superfície igual ≠ entidade igual. Pessoa “Apple” ≠ empresa “Apple”.
- Identidade canônica = tipo + apelido registrado + espaço da capacidade.
- Embedding / similaridade 0.95 é *candidato*. Merge automático vaza e mente.
- Denylist de termos genéricos (“system”, “user”, “memory” como pessoas).
- Matching case-fold **único** em todos os paths.

## Tempo

- Estado mutável (cargo, status, contagem) exige sucessor — não append eterno.
- `valid_to < valid_from` o write **recusa** (intervalo invertido some de todo as-of).
- Supersede é um primitivo atômico. invalidate+add na mão no mesmo dia cria dois fatos.
- Datas em linguagem natural (“março”, “ontem”) não podem devolver o mesmo vazio de “sem fato”. Parse estrito.
- Half-open `[from, to)` documentado e testado.

## Isolamento

- Workspace / capacidade em **toda** aresta e hop.
- Attribution obrigatória e não vazia.
- Cross-workspace impossível por schema, não por header.
- Caderno do empregado (job 3 da [12b](../aulas/12b-quatro-jobs-um-store.md)) fora do índice compartilhado.
- Zero singleton global de grafo; um grafo por conexão de workspace.
- Chave de cache = path canônico, não a string crua do usuário.

## Contrato mínimo (o que a aula pede no PRD)

```yaml
memoria:
  job: "1|2|3|4"
  identidade: "tipo + apelido + espaco; merge so com humano"
  tempo: "estado mutavel usa supersede; datas estritas"
  isolamento: "aresta.espaco = capacidade; empregado fora"
  esquecer: "quem apaga, o que some da leitura, o recibo"
```

## Navegação

[Aula 12e](../aulas/12e-identidade-tempo-isolamento.md) · [Fonte 80](80-grafo-projecao-nao-oraculo.md) · [Fonte 82](82-menor-cerebro-suficiente.md) · [FONTES](../FONTES.md)
