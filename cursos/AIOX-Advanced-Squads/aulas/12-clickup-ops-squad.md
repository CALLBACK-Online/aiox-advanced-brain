---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: clickup-ops-squad
lesson_position: 12
title: "ClickUp Ops — materializar processo no ClickUp"
squad: clickup-ops-squad
agents: 5
tasks: 30
workflows: 2
module: M2
sequence: M2.3
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, clickup-ops-squad, layer/curso, curso/squads, squad/clickup-ops-squad]
maturity: partial
---

# ClickUp Ops — materializar processo no ClickUp

> Vault: [[squads/clickup-ops-squad/README|clickup-ops-squad]] · [[skills/clickup-ops-squad/SKILL|clickup-ops-squad]] · [[cursos/MOC-Squads]]

[← DB Sage](11-db-sage.md) · [↑ M2](../modulos/M2-dados-materializacao.md) · [⌂ Curso](../README.md) · [→ Brand](13-brand.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `24-entidade-como-unidade-de-processo` — entidade e processo.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/clickup-ops-squad/`
- config: `squads/clickup-ops-squad/config.yaml`
- agentes: `squads/clickup-ops-squad/agents/`
- tasks: `squads/clickup-ops-squad/tasks/`
- workflows: `squads/clickup-ops-squad/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/clickup-ops-squad /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **5 agentes**, **30 tasks**, **2 workflows**.

## Quando usar — e quando não usar

**Use quando:** virar processo validado em Spaces, Lists, fields e automações ClickUp.

**Não use quando:** desenhar o processo do zero (faça SOP/discovery antes). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`clickup-chief`** (`squads/clickup-ops-squad/agents/clickup-chief.md`).

```text
@clickup-chief
# ou, se a skill de entrada estiver instalada:
# $ clickup-ops-squad

*help
```

Agentes (amostra): `api-builder`, `auditor`, `clickup-chief`, `materializer`, `playwright-ops`

Tasks (amostra): `bootstrap-mission`, `create-mission`, `fill-api-gaps`, `map-ui-pages`, `mapped-atm-activate-automations`, `mapped-atm-activate-circuit-breaker`, `mapped-atm-assemble-registry`, `mapped-atm-attach-gate-criteria`

Workflows (amostra): `map-generated-workflow-definition`, `materialization-pipeline`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad clickup-ops-squad de squads/clickup-ops-squad/.
Siga o config.yaml e o orquestrador clickup-chief.
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
Use o squad clickup-ops-squad (ClickUp Ops).

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
Leia squads/clickup-ops-squad/config.yaml e adote a persona de clickup-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Você tem um SOP de publicação de conteúdo já validado e quer vê-lo virar estrutura ClickUp — mas nesta prática, **sem tocar no workspace**. Peça ao squad o plano completo que `materialize-process` executaria via `materialization-pipeline`: quais Lists e fields seriam provisionados, quais automações seriam ativadas e em que ordem. O plano é o entregável; a execução só acontece com autorização explícita.

**Saída esperada:** um plano de materialização com o mapa SOP→estrutura (Space, Lists, fields, automações) etapa por etapa — na ordem das tasks `mapped-atm-*`, como `mapped-atm-provision-lists` —, cada item marcado como criação ou alteração, e os pontos que exigiriam autorização antes de qualquer chamada à API.

**Erro comum neste squad:** deixar o agente "só criar rapidinho" a estrutura no workspace real durante o rascunho — efeito externo sem autorização. Detecte cedo declarando no briefing que a missão termina no plano e conferindo que nenhuma task `mapped-atm-*` foi executada.

> **Teste rápido**: abra o ClickUp depois da prática; se algo novo apareceu lá, você falhou o exercício.
