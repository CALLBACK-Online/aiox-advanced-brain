---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: storytelling
lesson_position: 16
title: "Storytelling — arco, tensão e memorabilidade"
squad: storytelling
agents: 13
tasks: 13
workflows: 1
module: M3
sequence: M3.4
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, storytelling, layer/curso, curso/squads, squad/storytelling]
maturity: partial
---

# Storytelling — arco, tensão e memorabilidade

> Vault: [[squads/storytelling/README|storytelling]] · [[skills/storytelling/SKILL|storytelling]] · [[cursos/MOC-Squads]]

[← Design Ops](15-design-ops.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Slides Creator](17-slides-creator.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `12-repertorio-vs-tecnica` — narrativa com repertório.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/storytelling/`
- config: `squads/storytelling/config.yaml`
- agentes: `squads/storytelling/agents/`
- tasks: `squads/storytelling/tasks/`
- workflows: `squads/storytelling/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/storytelling /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **13 agentes**, **13 tasks**, **1 workflows**.

## Quando usar — e quando não usar

**Use quando:** narrativas com arco, emoção e estrutura memorável.

**Não use quando:** copy de conversão direta (use Copy) ou deck executivo (Slides). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`blake-snyder`** (`squads/storytelling/agents/blake-snyder.md`).

```text
@blake-snyder
# ou, se a skill de entrada estiver instalada:
# $ storytelling

*help
```

Agentes (amostra): `blake-snyder`, `dan-harmon`, `donald-miller`, `joseph-campbell`, `keith-johnstone`, `kindra-hall`, `marshall-ganz`, `matthew-dicks` … (+2)

Tasks (amostra): `apply-abt`, `apply-beat-sheet`, `apply-heros-journey`, `apply-save-the-cat`, `apply-story-circle`, `craft-personal-story`, `craft-public-narrative`, `craft-ted-talk`

Workflows (amostra): `story-creation`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad storytelling de squads/storytelling/.
Siga o config.yaml e o orquestrador blake-snyder.
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
Use o squad storytelling (Storytelling).

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
Leia squads/storytelling/config.yaml e adote a persona de blake-snyder.
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
