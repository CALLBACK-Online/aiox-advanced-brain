---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: wikilinks-e-grafo
lesson_position: 2
title: "Wikilinks, backlinks e Graph"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 14
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Wikilinks, backlinks e Graph

[← Abrir o vault](01-abrir-o-vault.md) · [⌂ Curso](../README.md) · [→ Agent como professor](03-agent-como-professor.md)

## Resultado

Ao final desta aula você consegue **ler e criar** `[[wikilinks]]`, **usar backlinks** e **abrir o Graph** com uma intenção clara (não só “explorar”).

## Quando usar — e quando não usar

**Use** para estudar qualquer etapa da jornada e montar seus próprios hubs.

**Não** force wikilink para fora da pasta do curso canônico se isso quebrar o validador — cada curso é autocontido.  
**Não** use o Graph como procrastinação: se a pergunta é “qual aula de captura?”, a busca ou o README bastam.

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

## Backlinks e Graph

- **Backlinks**: quem aponta para a nota atual — útil para ver “quem depende desta ideia”.
- **Graph**: mapa colorido do acervo (config em `.obsidian/graph.json` na raiz do repo).

### Cores deste vault (raiz = repositório)

| Cor | Query / pasta |
|-----|----------------|
| Azul | `cursos/AIOX Advanced` — método |
| Roxo | `cursos/AIOX-Advanced-Squads` — aulas de squad |
| Ciano | `cursos/Obsidian-IA` — este mini |
| Azul-base | `cursos/Introducao-a-Arquitetura-de-Sistemas` e `cursos/AIOX-Fundamentals` — base técnica e Core |
| Verde | `skills/` |
| Laranja | `squads/` |
| Âmbar | `notas/` |
| Rosa | tags `#hub` (Home + MOCs) |

Para ver **skills e squads** no mesmo Graph, abra a **raiz do repositório** como vault (não só esta pasta).

### Controles úteis

1. **Orphans off** — some o anel de arquivos soltos; sobra o que tem link.
2. **Orphans on** — audita o que ainda não está no cérebro (ainda colorido por pasta).
3. Filtro: `path:skills` ou `path:squads/brand` para zoom.
4. Hubs de conexão (paths no repo): `00-HOME.md`, `cursos/MOC-Acervo-AIOX.md`, `cursos/MOC-Skills.md`, `cursos/MOC-Squads.md`.

Perguntas boas no Graph:

1. Os nove cursos aparecem ligados pelos hubs, com núcleo comum, rotas de aplicação e vitrine Enterprise distinguíveis?
2. Os hubs rosa puxam arestas para verde/laranja?
3. Quais pastas ainda são só órfãs?

## Busca vs grafo vs wikilink

Três modos de achar coisa — use o mais barato:

| Precisa de… | Use |
|-------------|-----|
| Nome ou trecho de texto | **Busca** (`Cmd/Ctrl+O` ou Search) |
| “O que se conecta a isto?” | **Backlinks** / **Graph** |
| Navegação estável entre aulas deste curso | **Links markdown** no rodapé (`## Navegação`) |
| Agent no repo (“me ensine X”) | Peça **path** — ele lê arquivo; Graph é para *você* |

## Agent e o grafo

O agent **não** “vê” o Graph visual. Ele localiza por path, busca e contrato (`AGENTS.md`). Use o Graph para *sua* intuição; use o agent para *trilha + evidência* (aula 03). Combinar os dois: você aponta um hub no Graph; o agent detalha a aula e o exercício.

## Prática

1. Abra o vault na **raiz do repo** (recomendado) ou neste mini.
2. Abra o Graph; confira se os color groups estão ativos (Appearance → se preciso, recarregue).
3. Alternar Orphans off/on e anotar a diferença.
4. Abrir o Home (`00-HOME.md`) e clicar até um squad e uma skill.
5. Na sua nota de inbox (ou rascunho), linke **uma** aula canônica por path relativo.

## Evidência de conclusão

Você descreve as cores que viu, 1 conexão curso ↔ skill ou curso ↔ squad, e sabe traduzir um wikilink para path fora do Obsidian.

## Navegação
[← Anterior](01-abrir-o-vault.md) · [↑ Curso](../README.md) · [Próxima →](03-agent-como-professor.md)
