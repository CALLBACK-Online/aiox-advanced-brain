---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: slides-creator
lesson_position: 17
title: "Slides Creator — decks com narrativa e QA"
squad: slides-creator
agents: 7
tasks: 53
workflows: 1
module: M3
sequence: M3.5
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, slides-creator]
maturity: partial
---

# Slides Creator — decks com narrativa e QA

[← Storytelling](16-storytelling.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Conteúdo](18-conteudo.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `18-yaml-markdown-json-sweet-spot` — estrutura de artefato.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/slides-creator/`
- config: `squads/slides-creator/config.yaml`
- agentes: `squads/slides-creator/agents/`
- tasks: `squads/slides-creator/tasks/`
- workflows: `squads/slides-creator/workflows/`
- skill de entrada (opcional): `skills/slide-creator/SKILL.md` (nome quase homônimo)
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/slides-creator /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **7 agentes**, **53 tasks**, **1 workflows**.

## Quando usar — e quando não usar

**Use quando:** briefing → narrativa → slides → notas → QA de deck.

**Não use quando:** só texto de venda sem deck (Copy) ou só história sem slides. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`slide-chief`** (`squads/slides-creator/agents/slide-chief.md`).

```text
@slide-chief
# ou, se a skill de entrada estiver instalada:
# $ slides-creator

*help
```

Agentes (amostra): `content-architect`, `design-planner`, `design-renderer`, `qa-inspector`, `slide-chief`, `template-curator`, `visual-scout`

Tasks (amostra): `apply-design-revision`, `apply-scqa`, `build-pyramid`, `catalog-sources-apa`, `classify-slide-type`, `clone-visual-style-signature`, `compose-grid-layout`, `compress-outline-to-slide-functions`

Workflows (amostra): `generate-presentation`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad slides-creator de squads/slides-creator/.
Siga o config.yaml e o orquestrador slide-chief.
Missão: <descreva>.
```

## Execução guiada

1. **Confirme o fit** com o mapa de decisão e o anti-escopo acima.
2. **Cole o briefing** (modelo abaixo) e peça confirmação de rota.
3. **Deixe o chief rotear** para o especialista/task; não pule o diagnóstico.
4. **Exija artefatos intermediários** (plano, hipótese, estrutura) antes do polimento.
5. **Aplique o gate** da missão (checklist, score, revisão ou smoke).
6. **Registre evidência**: briefing, decision-log, deliverable, validation.
7. **Só então** publique, envie ou grave em sistema externo — se autorizado.

## Briefing copiável

```text
Use o squad slides-creator (Slides Creator).

Objetivo: {mudança observável}
Estado atual: {o que existe hoje}
Entradas: {arquivos, dados, links, decisões}
Público: {quem usa a saída}
Restrições: {prazo, stack, marca, segurança}
Saída esperada: {artefato e formato}
Critérios de aceite:
1. {teste objetivo 1}
2. {teste objetivo 2}
3. {teste objetivo 3}
Fora de escopo: {o que não mexer}

Antes de executar: confirme rota, dependências ausentes e qualquer efeito externo.
Leia squads/slides-creator/config.yaml e adote a persona de slide-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integração multi-tenant enterprise que foi deliberadamente removida deste acervo.

## Prática

Descreva uma missão real em 5 linhas. Explique por que **este** squad e não o vizinho do mesmo módulo. Escreva o briefing copiável preenchido e a lista de evidências que você exigiria antes de dar a missão como “feita”.
