---
type: source-brief
course: aiox-agent-engineering
source_id: 78
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
updated: '2026-08-12'
---

# Fonte 78 — Quatro jobs de memória

Síntese para a aula [12b](../aulas/12b-quatro-jobs-um-store.md). Esta nota **é** a evidência. Sem arquivo de outro repositório.

A [aula 11](../aulas/11-pasta-os.md) ensina repertório de *código* (clone + Grep). Esta fonte classifica o *job* de memória da capacidade. Sem isso, o PRD pede “um cérebro” e quatro verdades caem no mesmo lugar.

## Quatro jobs que a palavra “cérebro” mistura

| Job | Pergunta | O que a operação *sabe* | O que este store recusa |
|---|---|---|---|
| **1. Sistema nervoso** | Quem faz o quê, por quê, o que bloqueia? | Goal, assignment, cartão, custo do run | Wiki de cliente, tom, transcrição |
| **2. Córtex institucional** | O que é verdade sobre o mundo? | Pessoa, empresa, deal, reunião — com citação e gap | Org-chart, fan-in da wave, folha |
| **3. Memória do empregado** | Como *este* humano ou agente trabalha? | Preferência, identidade, caderno pessoal | Fato da firma, prova, board compartilhado |
| **4. Resíduo do trabalho** | O que *este* cartão já fez? | Ledger, issue, PRD, cartão da wave | Enciclopédia, identidade pessoal |

Um store só para os quatro é o anti-padrão. Quem mistura perde a fonte da verdade e acha que o agente “sabe a empresa” quando só leu o último cartão.

## Quem ilustra cada job (GitHub; não instale)

Lista completa: [FONTES](../FONTES.md#acesso-ao-material-github).

| Projeto | Job que *é* | Job que *não* é |
|---|---|---|
| [Paperclip](https://github.com/paperclipai/paperclip) | nervoso (control plane) | wiki / córtex |
| [gbrain](https://github.com/garrytan/gbrain) | córtex (síntese + grafo) | nervoso, arquivo offline |
| [mempalace](https://github.com/milla-jovovich/mempalace) | arquivo fiel (eixo do córtex) | nervoso, resíduo de wave |
| [Memori](https://github.com/MemoriLabs/Memori) | log de ação (complementa o 4) | knowledge vault |
| [gsd-2](https://github.com/gsd-build/gsd-2) | resíduo tribal no disco | produto de memória |
| [OpenClaw](https://github.com/openclaw/openclaw), [LifeOS](https://github.com/danielmiessler/LifeOS) | caderno / OS da *vida* | DB da empresa |
| [mem0](https://github.com/mem0ai/mem0), [supermemory](https://github.com/supermemoryai/supermemory) | SDK / camada para plugar | operar a wave ou a firma |

## Relação com as aulas deste curso

- [20b](../aulas/20b-grafo-codigo-e-memoria-de-processo.md) aplica o **job 4** à wave.
- [12c](../aulas/12c-arquivo-fiel-vs-sintese.md) materializa o **job 2** se o PRD o comprou.
- [12f](../aulas/12f-menor-cerebro-suficiente.md) recusa store novo se 0–2 já cobrem o sintoma.
- Aula 76 do Advanced: mapa de trabalho (job 4 *numa* sessão). Não é córtex.

## O que absorver

| Absorver | Como fica no projeto do aluno |
|---|---|
| Nomear o job antes da ferramenta | Uma frase no PRD: “esta capacidade compra X; recusa Y” |
| Recusa como design | Nervoso não é wiki; córtex não é board |
| Heartbeat fino + pull | Ninguém acorda com a wiki no prompt |
| Caderno do empregado fora do índice compartilhado | Preferência pessoal não entra no fan-in |
| Resíduo no cartão, não no chat | Ponte para a aula 20b |

## O que não absorver

- Um monólito “cérebro” com os quatro jobs.
- Instalar um store pelo ranking de marketing.
- Copiar o caderno pessoal para o contexto da equipe.
- Tratar a Pasta OS (aula 11) como memória de *fato*: clone é repertório de código.

Pré-requisito: [aula 11](../aulas/11-pasta-os.md) e [aula 12](../aulas/12-research-ao-prd.md). O PRD nomeia o job de memória ou declara que não há.

Acesso opcional aos repositórios: [FONTES — GitHub](../FONTES.md#acesso-ao-material-github).

## Navegação

[Aula 12b](../aulas/12b-quatro-jobs-um-store.md) · [Fonte 79](79-arquivo-fiel-vs-sintese.md) · [FONTES](../FONTES.md) · [Curso](../README.md)
