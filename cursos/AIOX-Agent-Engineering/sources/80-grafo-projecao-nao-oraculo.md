---
type: source-brief
course: aiox-agent-engineering
source_id: 80
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
updated: '2026-08-12'
---

# Fonte 80 — Grafo é projeção, não oráculo

Síntese para a aula [12d](../aulas/12d-grafo-projecao-nao-oraculo.md). Esta nota **é** a evidência.

O Graph do vault de estudo é mapa humano. Esta fonte é o índice da *capacidade*. Mesma palavra, jobs diferentes.

## Invariantes (fail-closed)

| # | Armadilha | O que a capacidade faz |
|---|---|---|
| I1 | Extract “ok” sem disposição dos candidatos | Recibo: aceito / recusado / ambíguo / irrelevante. Zero aceitos pode ser correto. |
| I2 | Predicado forte sem trecho | No máximo `relacionado_a` |
| I3 | Paths de extract divergentes | Um reconciler; mesmo conjunto |
| I4 | Soft-delete incompleto no traversal | Mesmo predicado em toda leitura |
| I5 | Health verde com cobertura 0 (ou o inverso da busca) | Métrica = query do produto |
| I6 | Merge por semelhança 0.95 | Identidade = tipo + apelido + espaço |
| I7 | Dual-SoT markdown + SQL + grafo | Uma escrita; o resto reconstrói |
| I8 | Síntese cita aresta e não reabre o original | Sem extract, sem conclusão |

Aresta forte sem locator fabrica fato. Pasta `pessoas/ana` ao lado de `empresas/museu` não autoriza emprego.

Banco de grafos “para lembrar” não é o próximo passo. Índice no disco da capacidade, com recibo, basta.

## Relação com as irmãs

- [12c](../aulas/12c-arquivo-fiel-vs-sintese.md) decide se o job 2 existe. Sem aresta necessária, pule esta fonte.
- [12e](../aulas/12e-identidade-tempo-isolamento.md) aprofunda I6 + tempo + isolamento.
- [20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md) recusa este grafo no fan-in da wave.

## Navegação

[Aula 12d](../aulas/12d-grafo-projecao-nao-oraculo.md) · [Fonte 79](79-arquivo-fiel-vs-sintese.md) · [Fonte 81](81-identidade-tempo-isolamento.md) · [FONTES](../FONTES.md)
