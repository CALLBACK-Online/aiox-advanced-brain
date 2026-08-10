---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: wikilinks-e-grafo
lesson_position: 2
title: "Wikilinks, backlinks e Graph"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 12
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Wikilinks, backlinks e Graph

[← Abrir o vault](01-abrir-o-vault.md) · [⌂ Curso](../README.md) · [→ Agent como professor](03-agent-como-professor.md)

## Resultado

Ler e criar `[[wikilinks]]`, usar backlinks e abrir o Graph view com intenção.

## Quando usar — e quando não usar

**Use** para estudar qualquer etapa da jornada e montar seus próprios hubs.

**Não** force wikilink para fora da pasta do curso canônico se isso quebrar o validador — cada curso é autocontido.

## Wikilinks

No Obsidian, `[[Nome da nota]]` resolve pelo nome do arquivo (stem) dentro do vault.

Exemplos de intenção:

- Ir para o hub do mini-curso: volte ao [README do curso](../README.md).
- Entre aulas deste mini: use os links de navegação no topo/rodapé.

Fora do Obsidian (GitHub, agent), traduza wikilink → **path relativo**.

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

## Prática

1. Abra o vault na **raiz do repo** (recomendado) ou neste mini.
2. Abra o Graph; confira se os color groups estão ativos (Appearance → se preciso, recarregue).
3. Alternar Orphans off/on e anotar a diferença.
4. Abrir o Home (`00-HOME.md`) e clicar até um squad e uma skill.

## Evidência de conclusão

Você descreve as cores que viu e 1 conexão curso ↔ skill ou curso ↔ squad.
