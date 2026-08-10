---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: abrir-o-vault
lesson_position: 1
title: "Abrir o vault e o mapa"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 12
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Abrir o vault e o mapa

[← Por que Obsidian + IA](00-por-que-obsidian-ia.md) · [⌂ Curso](../README.md) · [→ Wikilinks e grafo](02-wikilinks-e-grafo.md)

## Resultado

Ao final desta aula você consegue **escolher a raiz do vault** adequada e **abrir o arquivo de entrada** sem se perder.

## Quando usar — e quando não usar

**Use** na primeira abertura do material ou ao trocar de máquina.

**Não** abra a raiz do monorepo inteiro se você só quer estudar o método com grafo leve.  
**Não** abra o monorepo AIOX do *seu* produto como se fosse este acervo — são repositórios diferentes.

## Raízes recomendadas

| Vault root | Quando |
|------------|--------|
| `cursos/Introducao-a-Arquitetura-de-Sistemas/` | Entender sistemas e linguagem técnica |
| `cursos/AIOX-Fundamentals/` | Instalar e operar o Core |
| `cursos/AIOX Advanced/` | Estudar o método (grafo grande) |
| `cursos/AIOX-Advanced-Squads/` | Operação 1:1 dos squads |
| `cursos/` | Ver a jornada completa no hub das trilhas |
| `cursos/Obsidian-IA/` | **Este mini-curso** (grafo leve, sem skills/squads coloridos) |
| **Raiz do repo** | **Recomendado para Graph colorido** (cursos + skills + squads) |

No Obsidian: **Open folder as vault** → escolha uma linha da tabela.

Para filtros coloridos (azul/roxo/verde/laranja) e hubs `00-HOME` / MOCs, use a **raiz do repositório**.

## Um vault ou vários?

| Situação | Recomendação |
|----------|----------------|
| Estudar o acervo AIOX com Graph colorido | **Um** vault = raiz deste repo |
| Curso isolado (só Advanced) em foco profundo | Vault na pasta do curso — ok; volte à raiz para skills/squads |
| Vault de vida/livros (ex.: mentelendaria) | **Outro** vault; não misture paths de máquina neste acervo |
| Projeto AIOX de produção | **Não** é vault de estudo; é destino de handoff (aula 06) |

Trocar de vault no Obsidian é barato. Confundir *estudo* com *runtime do produto* é caro.

## Mapa mental do acervo

- Hub: `cursos/README.md` (path no repo; entre cursos use monoespaçado).
- Home do Graph: `00-HOME.md` (só na raiz do repo).
- Base técnica: pasta `cursos/Introducao-a-Arquitetura-de-Sistemas/`.
- Core: pasta `cursos/AIOX-Fundamentals/`.
- Método: pasta `cursos/AIOX Advanced/`.
- Squads: pasta `cursos/AIOX-Advanced-Squads/`.
- Captura local: `notas/` (só README versionado; pastas filhas gitignored).

Com o agent no repo, a skill `obsidian-course-vault` formaliza esse onboarding.

## Primeiros 5 minutos (depois de abrir)

1. Confirme a pasta aberta (título da janela / caminho no Obsidian).
2. Abra `00-HOME.md` **ou** `cursos/README.md`.
3. Abra o README deste mini (`cursos/Obsidian-IA/README.md`).
4. Crie as pastas pessoais se o clone for limpo (abaixo).
5. Só então entre na aula 00/01 — não mergulhe em `skills/` sem mapa.

## Settings mínimas (15 minutos, não 3 horas)

O Obsidian tem dezenas de opções. Para **este** acervo, configure só o que evita caos:

1. **Files & Links → Default location for new notes** → pasta `notas/inbox` (ou equivalente já no `.obsidian/app.json` da raiz).
2. **Default location for new attachments** → `notas/attachments` (crie se não existir; ver `notas/README.md`).
3. Confirme que o vault aberto é a **raiz do repositório** se quiser Graph com skills/squads coloridos.
4. **Não** instale plugin de IA no Obsidian só porque “todo mundo usa” — neste acervo o agent é a superfície de IA (Claude Code / Codex / genérico).
5. (Opcional) **New link format** → shortest path when possible — facilita wikilinks entre pastas.

Instalação multiplataforma e sync mobile/desktop não são pré-requisito deste mini: se ainda não tem o app, instale o desktop e abra a pasta do clone. Tutorial profundo de install/sync fica fora do escopo.

## Pastas pessoais no clone limpo

Só `notas/README.md` vem no git. Crie o restante (Explorer do Obsidian ou terminal na raiz):

```bash
mkdir -p notas/inbox notas/notes notas/MOCs notas/cards notas/retornos notas/attachments
```

Detalhe: `notas/README.md`.

## Prática

1. Abra a **raiz do repositório** como vault.
2. Crie `notas/inbox/`, `notas/retornos/` e as demais pastas pessoais pelo procedimento em `notas/README.md`, caso ainda não existam.
3. Abra o README deste curso e a aula 00.
4. Abra `cursos/README.md`, identifique sua etapa atual e anote por que a raiz do repositório será seu vault padrão (ou por que, excepcionalmente, não).

## Evidência de conclusão

Screenshot mental (ou nota): “Minha root padrão é ___ porque ___.”

## Navegação
[← Anterior](00-por-que-obsidian-ia.md) · [↑ Curso](../README.md) · [Próxima →](02-wikilinks-e-grafo.md)
