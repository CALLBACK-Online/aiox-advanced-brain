---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: graph-do-acervo
lesson_position: 3
title: "Graph do acervo: o mapa colorido"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 16
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Graph do acervo: o mapa colorido

[← Wikilinks e backlinks](02-wikilinks-e-backlinks.md) · [⌂ Curso](../README.md) · [→ Agent como professor](04-agent-como-professor.md)

## Resultado

Ao final desta aula você consegue **abrir o Graph na raiz do repositório**, **reconhecer as cores do acervo AIOX**, usar **filtros e órfãos** com intenção e **restaurar** a config limpa se o mapa “perder as cores”.

## Quando usar — e quando não usar

**Use** para:

- sentir o acervo como sistema (cursos × skills × squads × notas);
- achar hubs e clusters antes de mergulhar em uma trilha;
- auditar ilhas (órfãos) e conexões que faltam nas *suas* notas.

**Não use** o Graph como procrastinação infinita nem como substituto de:

- busca (“qual arquivo tem a palavra X?”);
- agent com path (“me ensine a próxima aula”);
- Context Brief (missão + evidência — aulas 07–08).

O Graph **impressiona** — e deve. Depois do “uau”, a pergunta útil é: *o que este mapa me diz para estudar ou conectar agora?*

## Pré-requisito: raiz certa

| Vault aberto em… | O que você vê no Graph |
|------------------|-------------------------|
| **Raiz do repositório** | Cursos + `skills/` + `squads/` + `notas/` coloridos — **o mapa completo** |
| Só `cursos/Obsidian-IA/` | Mini-curso isolado (cianinho) — útil, mas sem o “uau” skills/squads |
| Só um curso grande | Grafo denso daquele curso — bom para foco, mau para inventário |

Se as cores “sumiram”, confira primeiro se a janela do Obsidian é a **raiz do clone**, não uma subpasta.

## Abrir e ler o mapa (5 minutos)

1. **Open folder as vault** → raiz deste repositório.
2. Abra a **Visualização em gráfico** (Graph view).
3. Em **Filtros** (recomendado no modo estudo):
   - **Órfãos = OFF** — some o anel de arquivos sem link; sobra o cérebro conectado.
   - **Etiquetas = ON** se quiser ver hubs `#hub`.
4. Em **Grupos**, deve haver queries como `path:skills`, `path:squads`, `path:"cursos/AIOX Advanced"`, `tag:#hub`.

Config versionada: `.obsidian/graph.json` (e backups em `.obsidian/`). Guia curto: `.obsidian/README.md`.

## Cores deste acervo (o “uau” com legenda)

Ordem aproximada dos grupos (o primeiro match pinta o nó). Valores alinhados a `.obsidian/graph.LOCKED.json` / `graph.aiox-brain.json`:

| Cor (intuição) | Query típica | O que é |
|----------------|--------------|---------|
| **Rosa / magenta** | `tag:#hub` | Home e MOCs oficiais — âncoras de navegação |
| **Verde** | `path:skills` / `tag:#layer/skill` | Skills portáteis |
| **Laranja** | `path:squads` / `tag:#layer/squad` | Squads multi-agente |
| **Âmbar** | `path:notas` / `tag:#layer/nota` | Suas capturas (gitignored) |
| **Roxo** | `path:"cursos/AIOX-Advanced-Squads"` | Aulas 1:1 de squads |
| **Ciano** | `path:"cursos/Obsidian-IA"` | **Este mini-curso** |
| **Azul método** | `path:"cursos/AIOX Advanced"` | Curso de método |
| **Azul-base cursos** | `path:cursos` (fallback) | Demais cursos (Arquitetura, Fundamentals, Design…) |

Não decore RGB: decore **camadas** — hub · curso · skill · squad · nota.

## Controles que mudam a história

| Controle | Efeito | Quando usar |
|----------|--------|-------------|
| **Órfãos OFF** | Mapa “limpo”, só o que tem aresta | Estudo e impressão do sistema |
| **Órfãos ON** | Anel de arquivos soltos | Auditoria: o que ainda não entrou no cérebro |
| Filtro `path:skills` | Zoom verde | “Quais skills existem e como se ligam?” |
| Filtro `path:squads` | Zoom laranja | Antes de rotear um squad |
| Filtro `path:"cursos/Obsidian-IA"` | Só este mini | Ver se suas notas se conectam ao ciano |
| Clique em nó + arrastar / local graph | Foco em um hub | Partir de `00-HOME` ou de um MOC |

Perguntas boas no Graph (responda em voz alta ou na inbox):

1. Os hubs rosa puxam arestas para **verde** (skills) e **laranja** (squads)?
2. O **ciano** (este mini) está isolado ou ligado a `cursos/` e a `notas/`?
3. Com órfãos ON, o anel é enorme de `notas/` vazias ou de lixo de pasta — ou de material canônico sem link?
4. Consigo ir de um hub rosa até **uma skill** e **um squad** em poucos cliques?

## Local Graph vs Graph global

| Vista | Escopo | Use para |
|-------|--------|----------|
| **Graph global** | Vault inteiro | Inventário, cores, “onde está o acervo” |
| **Local graph** (nota aberta) | Vizinhos da nota atual | Estudar uma aula e ver o que ela puxa |

Fluxo poderoso: Global → clique no hub → Local da aula → leia → capture em `notas/` com link de volta.

## Se as cores sumiram (recuperação)

O Obsidian às vezes sobrescreve `graph.json` quando a aba Graph fica aberta. Restaure o mapa limpo:

```bash
# Na raiz do repositório — feche a aba Graph no Obsidian antes
./.obsidian/RESTORE-GRAPH.sh
# ou:
cp .obsidian/graph.LOCKED.json .obsidian/graph.json
```

Depois: reabra o Graph → Filtros: Órfãos OFF · Etiquetas ON → confira os grupos.

Modo auditoria (órfãos ON): copie `graph.aiox-brain.audit.json` sobre `graph.json` (ver `.obsidian/README.md`).

## Graph × agent × busca

| Superfície | O Graph faz? | Quem resolve |
|------------|--------------|--------------|
| Ver o sistema colorido | **Sim** — é a força | Você no Obsidian |
| Achar texto exato | Não | Busca |
| Ensinar com path + exercício | Não | Agent (aula 04) |
| Executar skill no projeto | Não | Projeto + handoff (aulas 07–08) |

O agent **não** enxerga o canvas do Graph. Você usa o mapa para *intuir*; o agent para *trilha e evidência*. Combinar: “Vi no Graph o cluster de squads roxos; me ensine a aula 00 de Squads com path.”

O Graph colorido mostra o **acervo para o humano**. Não é o índice de relações da capacidade (pessoa–empresa, story–arquivo). Um é navegação de estudo; o outro, se existir, vive no projeto e exige recibo — ver `cursos/AIOX-Agent-Engineering/aulas/12d-grafo-projecao-nao-oraculo.md`.

## Anti-padrões (depois do uau)

1. **Scroll infinito** no Graph sem abrir um arquivo.
2. **Só Graph, zero captura** — o mapa não vira memória.
3. **Vault na pasta errada** e concluir que “o acervo não tem cores”.
4. **Editar `graph.json` à mão** no meio da sessão com Graph aberto (prefira o script de restore).
5. **Achar que cor = maturidade da skill** — cor é *camada/pasta*, não qualidade.

## Prática

1. Abra a **raiz do repo** como vault e o Graph global.
2. Se não houver grupos coloridos, rode o restore (seção acima) e reabra.
3. Órfãos OFF → descreva 3 cores que você vê e o que cada uma representa.
4. Clique em `00-HOME` (ou no hub rosa) e navegue até **1 skill** (verde) e **1 squad** (laranja).
5. Alternar Órfãos ON por 30s; anote *uma* pergunta de auditoria (“por que X está solto?”).
6. (Opcional) Local graph de uma aula deste mini: o ciano se liga a alguma nota sua?

## Evidência de conclusão

Você (1) descreve o mapa com **≥3 cores e seus significados**, (2) relata o caminho hub → skill e hub → squad, e (3) sabe **como restaurar** o Graph se as cores sumirem.

## Navegação
[← Anterior](02-wikilinks-e-backlinks.md) · [↑ Curso](../README.md) · [Próxima →](04-agent-como-professor.md)
