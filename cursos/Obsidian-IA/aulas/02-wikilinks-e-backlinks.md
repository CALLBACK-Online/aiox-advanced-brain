---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: wikilinks-e-backlinks
lesson_position: 2
title: "Wikilinks e backlinks"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 10
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Wikilinks e backlinks

[← Abrir o vault](01-abrir-o-vault.md) · [⌂ Curso](../README.md) · [→ Graph do acervo](03-graph-do-acervo.md)

## Resultado

Ao final desta aula você consegue **ler e criar** `[[wikilinks]]`, **usar backlinks** e **traduzir** wikilink → path relativo fora do Obsidian.

## Quando usar — e quando não usar

**Use** para estudar qualquer etapa da jornada e montar seus próprios hubs.

**Não** force wikilink para fora da pasta do curso canônico se isso quebrar o validador — cada curso é autocontido.  
O **Graph colorido** (o “wow” visual) é a [próxima aula](03-graph-do-acervo.md) — aqui você só prepara os **elos** que o grafo mostra.

## Wikilinks

No Obsidian, `[[Nome da nota]]` resolve pelo nome do arquivo (stem) dentro do vault.

Exemplos de intenção:

- Ir para o hub do mini-curso: volte ao [README do curso](../README.md).
- Entre aulas deste mini: use os links de navegação no topo/rodapé.

Fora do Obsidian (GitHub, agent), traduza wikilink → **path relativo**.

### Higiene de links (notas pessoais)

Nas suas notas em `notas/`:

| Faça | Evite |
|------|--------|
| Linkar a fonte canônica por path (`cursos/…/aula.md`) ou wikilink do stem | Editar o arquivo canônico para “fechar” o link |
| Títulos de nota **declarativos** e únicos o suficiente | `[[nota]]`, `[[1]]`, `[[temp]]` que colidem no vault |
| Preferir link **para** a aula, não reescrever a aula | Criar cópia da aula em `notas/` e divergir para sempre |
| No Context Brief, path + síntese | Só wikilink sem texto — o agent do projeto pode não resolver `[[…]]` |

Cursos canônicos usam links markdown relativos entre si de propósito (validador + GitHub). Suas notas podem misturar wikilink (Obsidian) e path (handoff).

## Backlinks

**Backlinks** = quem aponta para a nota atual — útil para ver “quem depende desta ideia”.

1. Abra qualquer aula ou hub.
2. Painel **Backlinks** (ou clique no contador de links de entrada).
3. Pergunte: *quem depende desta ideia?* Se ninguém aponta, a nota ainda é uma ilha (ok no inbox; perigoso em MOC).

Backlink é **local** (uma nota). Graph (aula 03) é **global** (o mapa do vault).

## Busca vs backlink vs Graph (prévia)

| Precisa de… | Use |
|-------------|-----|
| Nome ou trecho de texto | **Busca** (`Cmd/Ctrl+O` ou Search) |
| “Quem aponta para *esta* nota?” | **Backlinks** |
| “Como o acervo se organiza em cores?” | **Graph** → [aula 03](03-graph-do-acervo.md) |
| Navegação estável entre aulas deste curso | **Links markdown** no rodapé (`## Navegação`) |
| Agent no repo (“me ensine X”) | Peça **path** — ele lê arquivo |

## Prática

1. Abra a [próxima aula](03-graph-do-acervo.md) e depois volte a esta.
2. Na sua nota de inbox (ou rascunho), linke **uma** aula canônica por path relativo **e** por wikilink do stem (se o nome for único).
3. Abra os backlinks de `00-HOME.md` (vault na raiz) e anote 2 notas que apontam para o hub.

## Evidência de conclusão

Você cria um wikilink válido, traduz um wikilink para path relativo e descreve o que um backlink mostra (sem precisar do Graph ainda).

## Navegação
[← Anterior](01-abrir-o-vault.md) · [↑ Curso](../README.md) · [Próxima →](03-graph-do-acervo.md)
