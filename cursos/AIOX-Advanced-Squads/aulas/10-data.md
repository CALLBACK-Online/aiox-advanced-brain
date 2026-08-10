---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: data
lesson_position: 10
title: "Data — analytics e decisões com dados"
squad: data
agents: 7
tasks: 12
workflows: 7
module: M2
sequence: M2.1
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, data]
maturity: partial
---

# Data — analytics e decisões com dados

[← Runner Ops](09-runner-ops.md) · [↑ M2](../modulos/M2-dados-materializacao.md) · [⌂ Curso](../README.md) · [→ DB Sage](11-db-sage.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `46-etapas-de-desenvolvimento` — evidência antes de métrica solta.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/data/`
- config: `squads/data/config.yaml`
- agentes: `squads/data/agents/`
- tasks: `squads/data/tasks/`
- workflows: `squads/data/workflows/`
- skill de entrada (opcional): `skills/data/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/data /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **7 agentes**, **12 tasks**, **7 workflows**.

## Quando usar — e quando não usar

**Use quando:** métricas, coortes, atribuição, churn e experimentação.

**Não use quando:** modelagem física de banco ou ETL bruto. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`data-chief`** (`squads/data/agents/data-chief.md`).

```text
@data-chief
# ou, se a skill de entrada estiver instalada:
# $ data

*help
```

Agentes (amostra): `avinash-kaushik`, `data-chief`, `david-spinks`, `nick-mehta`, `peter-fader`, `sean-ellis`, `wes-kao`

Tasks (amostra): `analyze-cohort`, `build-attribution`, `calculate-clv`, `create-dashboard`, `define-north-star`, `design-health-score`, `design-learning-outcomes`, `measure-community`

Workflows (amostra): `cohort-analysis-workflow`, `cohorts-diagnostic`, `create-churn-system`, `fix-completion-rate`, `implement-attribution`, `implement-customer-360`, `optimize-community-workflow`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad data de squads/data/.
Siga o config.yaml e o orquestrador data-chief.
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
Use o squad data (Data).

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
Leia squads/data/config.yaml e adote a persona de data-chief.
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
