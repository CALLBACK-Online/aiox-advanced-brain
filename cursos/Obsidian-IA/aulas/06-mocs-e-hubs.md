---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: mocs-e-hubs
lesson_position: 6
title: "MOCs e hubs de estudo"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 14
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# MOCs e hubs de estudo

[← Captura sem poluir](05-captura-sem-poluir.md) · [⌂ Curso](../README.md) · [→ Context Brief](07-do-estudo-a-execucao.md)

## Resultado

Ao final desta aula você consegue **montar um MOC** (Mapa de Conteúdo) com propósito, seções e ≥5 destinos reais — hub de navegação, não resumo infinito.

## Quando usar — e quando não usar

**Use** quando tiver ≥5 notas/aulas no mesmo tema ou uma dor recorrente.

**Não** faça um “MOC do universo AIOX” na primeira semana.  
**Não** substitua o hub oficial do acervo por uma cópia divergente em `notas/` — **linke** o oficial; personalize o *seu* recorte.

## Ideia (LYT-light)

MOC = propósito em uma frase + seções + links com meia linha de “por quê”.

Skill: `course-moc` (`skills/course-moc/SKILL.md`).

Destino pessoal: `notas/MOCs/MOC - {Tema}.md`.

## Hub oficial × MOC pessoal

| | **Hub / MOC do acervo** | **Seu MOC em `notas/`** |
|--|-------------------------|-------------------------|
| Onde | `00-HOME.md`, `cursos/MOC-Acervo-AIOX.md` (e irmãos MOC-Skills / MOC-Squads), READMEs de curso | `notas/MOCs/` |
| Dono | Maintainer do pacote | Você |
| Função | Mapa canônico da biblioteca | Seu recorte por dor/trilha |
| Edição | Só via PR / maintainers | Livre (gitignored) |

Comece **navegando** os hubs oficiais. Crie MOC pessoal quando o tema *seu* puxar mais de cinco destinos ou uma dor que o hub genérico não prioriza.

Hubs úteis (paths no repo):

- `00-HOME.md` — dashboard do vault
- `cursos/MOC-Acervo-AIOX.md` — visão do acervo
- `cursos/MOC-Skills.md` / `cursos/MOC-Squads.md` — inventários
- README de cada curso — ordem canônica da trilha

## Tipos úteis

1. Por **posição na jornada** (núcleo comum ou rota de aplicação)
2. Por **módulo** de um curso
3. Por **dor** (“agente em loop”, “design system drift”)
4. Por **squad** (aula + pré-requisito + skill)
5. Trilha personalizada de 5–12 passos

## Captura basta ou preciso de MOC?

| Situação | Mecanismo |
|----------|-----------|
| 1–4 insights no mesmo tema | Inbox / atômicas (aula 05) |
| ≥5 destinos ou “sempre volto a este tema” | **MOC** |
| Missão com transformação observável | Context Brief (aula 07) — o MOC alimenta as **fontes**, não substitui o Brief |

## Esqueleto

```markdown
# MOC - {Tema}

> Para quem / para quê (uma frase)

## Entrada
- [aula ou nota] — por que começar aqui

## Fundamentos
- … — meia linha de porquê

## Prática / operação
- skill ou squad (path) — maturidade se souber

## Evidência de que entendi
- [ ] consigo explicar X sem ler
- [ ] completei exercício Y
```

Cada bullet: **destino real** + **meia linha de porquê**. Lista de 40 links sem propósito não é MOC.

## Anti-padrões de hub

1. **MOC-universo** na semana 1 — sem massa crítica.
2. **Resumo infinito** — MOC não é segunda aula; é mapa.
3. **Sem critério de evidência** — se não há como saber que “entendeu”, é só índice.
4. **Duplicar o README do curso** palavra por palavra — linke o README e acrescente *seu* recorte.
5. **MOC sem links para canônico** — vira ilha; o Graph âmbar fica órfão do azul/roxo.

## Ponte para o Context Brief

Quando o MOC estiver maduro o bastante para uma missão:

1. Escolha 1–3 fontes do MOC (não as 20).
2. Copie paths + “por quê” para o template da aula 07.
3. O MOC permanece no vault; o Brief viaja para o projeto.

## Prática

Crie um MOC com **no mínimo 5** destinos reais (aulas ou notas suas) sobre um tema que você vai usar esta semana. Cada destino com meia linha de porquê. Se ainda não tem 5 itens, continue capturando (aula 05) e volte.

## Evidência de conclusão

Arquivo de MOC aberto no Obsidian com seções Entrada + Fundamentos + Evidência **e** ≥5 destinos com “por quê”.

## Navegação
[← Anterior](05-captura-sem-poluir.md) · [↑ Curso](../README.md) · [Próxima →](07-do-estudo-a-execucao.md)
