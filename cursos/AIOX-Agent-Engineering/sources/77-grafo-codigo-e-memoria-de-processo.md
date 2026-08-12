---
type: source-brief
course: aiox-agent-engineering
source_id: 77
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
updated: '2026-08-12'
---

# Fonte 77 — Grafo de código e memória de processo

Síntese para a aula [20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md). Esta nota **é** a evidência. Cabe neste acervo. Não aponte o aluno para outro repositório.

A aula 20b ensina **três grafos**. Feature sem fio (o cartão existe e o fan-in não lê) não é um quarto grafo — é falha. Os quatro *jobs* de memória estão na [fonte 78](78-quatro-jobs-de-memoria.md). Arquivo fiel vs síntese: [fonte 79](79-arquivo-fiel-vs-sintese.md).

## Três grafos que a palavra “grafo” mistura

| Grafo | O que guarda | Onde isto vive neste curso | Serve para wave? |
|---|---|---|---|
| **Trabalho** | Dependência e overlap (DAG) | Aulas 18 e 20 | Sim — é o plano. |
| **Processo** | Ação, resultado, atribuição (story + run) | Aula 20b: cartão no disco | Sim — é o registro do que *rodou*. |
| **Conhecimento** | Pessoas, empresas, deals, páginas | Job 2 da 12b / 12c. Fora do dispatch. | Não. É o mundo. |

Banco de grafos “porque memória precisa de grafo” ([Neo4j](https://github.com/neo4j/neo4j)) não é o próximo passo depois de Wave Execute. Quem ilustra cada job: [FONTES](../FONTES.md#sistemas-citados-github).

## Invariantes (não instale nada para usar isto)

1. **Silêncio** — escrita “ok” e leitura 0, sem alarme.
2. **Tipo sem texto** — predicado forte (`trabalha_em`) por pasta, sem locator.
3. **Dual-SoT** — uma autoridade de escrita; o resto é projeção regenerável.
4. **Grafo ≠ oráculo** — sinal de ranking não é prova nem gate de conclusão.
5. **Feature sem fio** — se o path principal da wave não lê o cartão, ele não existe.
6. **Store errado** — wiki do mundo não entra no fan-in.

## O que absorver na capacidade

| Absorver | Como fica no projeto do aluno |
|---|---|
| Ledger (agora / feito / próximo / não fazer) | Arquivo no disco da wave — aula 76 do Advanced + esta fonte |
| Atribuição obrigatória | Toda linha tem story + run |
| Uma escrita canônica | Não dual-write chat + markdown + banco |
| Supersede para estado mutável | “esta task substitui aquela” |
| Recusar conhecimento no hot path | Wiki do mundo não entra na wave |

Pré-requisito de método: aula 76 do Advanced (`cursos/AIOX Advanced/aulas/76-orientacao-do-agente.md`). Pré-requisito de jobs: [aula 12b](../aulas/12b-quatro-jobs-um-store.md). Esta fonte é o resíduo da wave (job 4).

Acesso opcional aos repositórios: [FONTES — GitHub](../FONTES.md#acesso-ao-material-github).

## Navegação

[Aula 20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md) · [Fonte 78](78-quatro-jobs-de-memoria.md) · [Fonte 79](79-arquivo-fiel-vs-sintese.md) · [FONTES](../FONTES.md) · [Curso](../README.md)
