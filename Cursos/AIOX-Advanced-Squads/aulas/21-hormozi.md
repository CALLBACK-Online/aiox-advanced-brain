---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: hormozi
lesson_position: 21
title: "Hormozi — oferta, leads e escala $100M"
squad: hormozi
agents: 16
tasks: 57
workflows: 10
module: M4
sequence: M4.4
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, hormozi]
maturity: partial
---

# Hormozi — oferta, leads e escala $100M

[← Sales](20-sales.md) · [↑ M4](../modulos/M4-aquisicao-conteudo-vendas.md) · [⌂ Curso](../README.md) · [→ Skill Creator Ops](22-skill-creator-ops.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `Cursos/AIOX Advanced/lessons/`) revise: `62-service-as-software; 64-vender-pela-dor-e-roi` — oferta e escala.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `Cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `Cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/hormozi/`
- config: `squads/hormozi/config.yaml`
- agentes: `squads/hormozi/agents/`
- tasks: `squads/hormozi/tasks/`
- workflows: `squads/hormozi/workflows/`
- skill de entrada (opcional): `skills/hormozi/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/hormozi /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **16 agentes**, **57 tasks**, **10 workflows**.

## Quando usar — e quando não usar

**Use quando:** Grand Slam Offer, leads, money models e sistemas de lançamento.

**Não use quando:** branding institucional ou research técnico profundo. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`hormozi-chief`** (`squads/hormozi/agents/hormozi-chief.md`).

```text
@hormozi-chief
# ou, se a skill de entrada estiver instalada:
# $ hormozi

*help
```

Agentes (amostra): `hormozi-ads`, `hormozi-advisor`, `hormozi-audit`, `hormozi-chief`, `hormozi-closer`, `hormozi-content`, `hormozi-copy`, `hormozi-hooks` … (+2)

Tasks (amostra): `architect-offer-stack`, `build-marketing-machine`, `build-scaling-team`, `calculate-30-day-profit`, `calculate-ppd`, `create-ad-angles`, `create-ad-campaign`, `create-bonus-stack`

Workflows (amostra): `wf-context-diagnosis`, `wf-full-launch-sequence`, `wf-grand-slam-offer`, `wf-growth-decision`, `wf-lead-magnet-pipeline`, `wf-money-model-design`, `wf-opportunity-screening`, `wf-paid-ads-campaign`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad hormozi de squads/hormozi/.
Siga o config.yaml e o orquestrador hormozi-chief.
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
Use o squad hormozi (Hormozi).

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
Leia squads/hormozi/config.yaml e adote a persona de hormozi-chief.
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
