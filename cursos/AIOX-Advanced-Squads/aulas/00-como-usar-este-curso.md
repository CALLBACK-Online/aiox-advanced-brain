---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: como-usar-este-curso
lesson_position: 0
lesson_kind: intro
title: "Como usar este curso e o acervo"
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 12
maturity: study
tags: [curso/aiox-advanced-squads, intro]
---

# Como usar este curso e o acervo

[↑ Curso](../README.md) · [Guia de execução](../Guia-de-execucao.md) · [Mapa de decisão](../Mapa-de-decisao.md) · [→ Advisory Board](01-advisory-board.md)

## Resultado

Saber a diferença entre **estudar** neste repositório e **executar** no seu projeto; copiar um squad; ativar o orquestrador; e ligar este curso ao AIOX Advanced (método).

## Quando usar — e quando não usar

**Use esta aula** antes da primeira missão com qualquer squad do catálogo.

**Não pule** se você ainda trata o repositório como se ele fosse o runtime AIOX completo: não é. É biblioteca de distribuição + cursos.

## Prepare a entrada

- uma missão real em uma frase;
- o nome de um squad candidato (ou dúvida entre dois);
- acesso a este repositório no disco;
- (recomendado) ter lido no Advanced: taxonomia e anatomia de squad.

Pré-requisitos do método: `ponte/pre-requisitos-advanced.md`.

## Como ativar (mental model)

Quatro superfícies possíveis no **seu** runtime (não neste curso):

1. `$skill` — wrapper em `skills/` copiado para a IDE;
2. `@agente` — persona em `squads/{nome}/agents/`;
3. `*comando` — task do agente ativo;
4. `/prefixo:…` — se o runtime registrar o pack.

Se a superfície não existir, use o briefing da aula e peça para carregar o path `squads/{nome}/`.

## Execução guiada

1. Abra `Cursos/README.md` (hub das trilhas).
2. Confirme o pré-requisito do Advanced em `ponte/pre-requisitos-advanced.md`.
3. Escolha o squad no [Mapa de decisão](../Mapa-de-decisao.md).
4. Abra a aula `01`–`24` correspondente.
5. Copie o pacote:

```bash
cp -R squads/<nome> /caminho/do/seu-projeto/squads/
# opcional:
cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

6. Cole o briefing copiável da aula no agente do seu projeto.
7. Exija as quatro evidências do [Guia de execução](../Guia-de-execucao.md).

## Briefing copiável

```text
Estou no acervo aiox-advanced-brain (biblioteca, não runtime).
Missão: {uma frase}.
Squad candidato: {nome} (pasta squads/{nome}/).
Já copiei o squad para meu projeto: {sim/não}.
Pré-requisito Advanced lido: {sim/não — quais aulas}.
Peça: confirme se o squad é o certo; se não, proponha 1 alternativa
com base no mapa de decisão do curso AIOX Advanced Squads.
```

## Evidência de conclusão

- missão escrita;
- squad escolhido com razão;
- path `squads/{nome}` copiado ou plano de cópia;
- lista das 4 evidências que você vai exigir na primeira execução.

## Limites neste acervo

Não há monorepo enterprise multi-tenant aqui. Comandos e paths de runtime valem no **projeto destino**. O curso não publica, não faz deploy e não cria recursos em SaaS sozinho.

## Prática

Pegue uma missão da sua semana. Usando só o Mapa de decisão, escolha um squad. Escreva em 5 linhas por que **não** é o vizinho confuso (ex.: Research vs Advisory, Design System vs Design Ops).
