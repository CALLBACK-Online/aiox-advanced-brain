---
type: source-brief
course: aiox-agent-engineering
source_id: 79
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
updated: '2026-08-12'
---

# Fonte 79 — Arquivo fiel vs cérebro que sintetiza

Síntese para a aula [12c](../aulas/12c-arquivo-fiel-vs-sintese.md). Esta nota **é** a evidência. Sem arquivo de outro repositório.

A aula [20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md) recusa grafo de conhecimento no *hot path da wave*. Esta fonte responde o job **2** da [fonte 78](78-quatro-jobs-de-memoria.md): a capacidade *é* um córtex — ou precisa de um.

## A pergunta real

Não é “qual software é melhor?”. É **qual eixo o job 2 está comprando?**

| | Arquivo fiel ([mempalace](https://github.com/milla-jovovich/mempalace)) | Cérebro que sintetiza ([gbrain](https://github.com/garrytan/gbrain)) |
|--|---|---|
| Devolve | Trechos | Resposta citada + o que falta |
| Path quente | Sem chamada cara no raw | Embed + síntese |
| Confiança | Auditável palavra por palavra | Útil, interpretada |
| Imbatível quando | Offline, compliance, o agente já sintetiza | Multi-hop, reunião com buraco |

Frase que vale aula: **o arquivo é a melhor memória; o cérebro é o melhor cérebro.**

**Camadas:** frio = arquivo; quente = síntese. O cérebro **nunca** vira fonte da verdade de fidelidade. O arquivo **nunca** precisa virar o board da empresa.

**Anti-padrão:** só síntese e esperar zero-custo offline; só arquivo e esperar “o que eu ainda não sei?”.

## Grafo = projeção (o detalhe está na [fonte 80](80-grafo-projecao-nao-oraculo.md))

Se o job for 2 *e* houver relações, a aula [12d](../aulas/12d-grafo-projecao-nao-oraculo.md) é obrigatória. Banco de grafos no fan-in da wave continua proibido.

## O que absorver

| Absorver | Como fica no projeto do aluno |
|---|---|
| Decisão arquivo / síntese / camadas | Uma frase + o que *não* entra |
| Compiled truth ≠ timeline | Síntese reescrita vs evidência append-only |
| Crença ≠ fato | Take atribuído não vira fato do dono |
| Grafo reordena, não autoriza | Sem locator, sem predicado forte |
| Supersede para estado mutável | Um fato vigente |

## O que não absorver

- Um store só para original e síntese.
- Grafo no fan-in da wave — job 4, aula [20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md).
- Arestas sem regra — aula [12d](../aulas/12d-grafo-projecao-nao-oraculo.md).

Pré-requisito: [aula 12b](../aulas/12b-quatro-jobs-um-store.md).

## Navegação

[Aula 12c](../aulas/12c-arquivo-fiel-vs-sintese.md) · [Fonte 78](78-quatro-jobs-de-memoria.md) · [Fonte 80](80-grafo-projecao-nao-oraculo.md) · [FONTES](../FONTES.md) · [Curso](../README.md)
