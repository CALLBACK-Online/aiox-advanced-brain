---
name: course-moc
description: >
  Cria e atualiza Mapas de Conteúdo (MOCs/hubs) para estudar o AIOX Advanced:
  por módulo, por tema, por dor ou por squad. Use quando o usuário pedir MOC,
  mapa mental do curso, hub de navegação, índice por tema, “como se conecta X e Y”,
  ou organizar o grafo de estudo sem alterar as aulas canônicas.
---

# Course MOC — mapas de conteúdo do curso

## Princípio (LYT, adaptado)

Um **MOC** (Map of Content) é um hub de navegação: poucas frases de contexto + links para notas/aulas que importam. Não substitui a aula; **orienta o caminho**.

Inspiração: Linking Your Thinking (hubs/MOCs). Implementação: Markdown + wikilinks neste acervo.

## Onde gravar

| Tipo | Destino | Versionar no git do brain? |
|------|---------|----------------------------|
| MOC **canônico** do pacote (raro) | Só se for melhoria do curso acordada | Sim, com validate |
| MOC de **estudo do aluno** | `notas/MOCs/` | Não (gitignored) |
| MOC no vault pessoal | Vault da pessoa | Fora deste repo |

Padrão de nome: `MOC - {Tema}.md` ou `hub-{slug}.md`.

## Tipos de MOC úteis aqui

1. **Por módulo** — ex.: “M5 Determinismo” → aulas + glossário + quiz.
2. **Por dor** — ex.: “Agente em loop” → aulas método + squad `agent-autonomy`.
3. **Por squad** — aula do curso Squads + pré-req Advanced + skill de entrada.
4. **Trilha personalizada** — 5–12 links ordenados para o objetivo da pessoa.

## Algoritmo

1. Definir o **propósito** do mapa em uma frase.
2. Limitar escopo (módulo, tema ou missão) — evitar “mapa do universo”.
3. Coletar 5–15 destinos reais (paths ou wikilinks que resolvem no vault escolhido).
4. Agrupar em seções (Fundamentos → Prática → Operação → Evidência).
5. Para cada link: meia linha de “por que está aqui”.
6. Fechar com **próximo passo** e, se couber, Context Brief + skill/squad de execução.
7. Não duplicar o README do curso; o MOC é recorte intencional.

## Template

```markdown
# MOC - {Tema}

> {Uma frase: para quem / para quê}

## Entrada
- [[{aula ou README}]] — comece aqui

## Fundamentos
- [[…]] — …

## Prática / operação
- [[…]] — …
- Squad/skill: `{id}` → `skills/…` ou `squads/…`
- Context Brief: `cursos/Obsidian-IA/templates/context-brief.md`

## Evidência de que “entendi”
- [ ] {explicar X}
- [ ] {aplicar Y em um caso real}

## Fora de escopo deste mapa
- …
```

Se o vault for só `cursos/AIOX Advanced/`, use wikilinks pelo título da nota. Se o agent estiver no repo, cite **paths relativos** para não ambiguidade.

## Fontes canônicas para montar hubs

- `cursos/README.md` — matriz método ↔ squads
- `cursos/AIOX Advanced/README.md` — módulos e rotas
- `cursos/AIOX-Advanced-Squads/Mapa-de-decisao.md`
- `cursos/AIOX-Advanced-Squads/agent-router.json` — sinais por squad
- `catalog.json` — existência e maturidade

## Guardrails

- Não inventar aulas; verificar que o arquivo existe.
- Não mover arquivos canônicos para “ficar mais LYT”.
- Preferir atualizar MOC pessoal a editar índices oficiais.
- Se o mapa alimentar uma operação, passe por `aiox-brain` para preparar o Context Brief antes de `aiox-squads` ou da skill do domínio.
