---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: advisory-board
lesson_position: 1
title: "Advisory Board — decisões sem groupthink"
squad: advisory-board
agents: 11
tasks: 8
workflows: 2
module: M0
sequence: M0.1
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, advisory-board]
maturity: partial
---

# Advisory Board — decisões sem groupthink

[← Como usar este curso](00-como-usar-este-curso.md) · [↑ M0](../modulos/M0-escolha-pesquisa-dominio.md) · [⌂ Curso](../README.md) · [→ Research](02-research.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `35-mesa-redonda-advisory-board` — decisão com múltiplas perspectivas.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/advisory-board/`
- config: `squads/advisory-board/config.yaml`
- agentes: `squads/advisory-board/agents/`
- tasks: `squads/advisory-board/tasks/`
- workflows: `squads/advisory-board/workflows/`
- skill de entrada (opcional): `skills/advisory-board/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/advisory-board /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **11 agentes**, **8 tasks**, **2 workflows**.

## Quando usar — e quando não usar

**Use quando:** decisão estratégica com perspectivas múltiplas e dissenso explícito.

**Não use quando:** descoberta factual pura ou execução de task já decidida. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`board-chair`** (`squads/advisory-board/agents/board-chair.md`).

```text
@board-chair
# ou, se a skill de entrada estiver instalada:
# $ advisory-board

*help
```

Agentes (amostra): `board-chair`, `brene-brown`, `charlie-munger`, `derek-sivers`, `naval-ravikant`, `patrick-lencioni`, `peter-thiel`, `ray-dalio` … (+2)

Tasks (amostra): `board-meeting`, `crisis-advisory`, `devils-advocate`, `issue-processing`, `load-advisory-context`, `opportunity-eval`, `quick-consult`, `strategic-review`

Workflows (amostra): `wf-board-meeting`, `wf-issue-processing`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad advisory-board de squads/advisory-board/.
Siga o config.yaml e o orquestrador board-chair.
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
Use o squad advisory-board (Advisory Board).

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
Leia squads/advisory-board/config.yaml e adote a persona de board-chair.
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
