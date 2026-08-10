---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: runner-ops
lesson_position: 9
title: "Runner Ops — runners headless e governança"
squad: runner-ops
agents: 5
tasks: 9
workflows: 0
module: M1
sequence: M1.5
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, runner-ops]
maturity: partial
---

# Runner Ops — runners headless e governança

[← ETL Ops](08-etl-ops.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ Data](10-data.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `28-taxonomia-…; 30-runner-executavel-deterministico` — runner determinístico.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/runner-ops/`
- config: `squads/runner-ops/config.yaml`
- agentes: `squads/runner-ops/agents/`
- tasks: `squads/runner-ops/tasks/`
- workflows: `squads/runner-ops/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/runner-ops /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **5 agentes**, **9 tasks**, **0 workflows**.

## Quando usar — e quando não usar

**Use quando:** criar, validar e governar runners determinísticos fora da IDE.

**Não use quando:** workflow só conceitual sem execução headless. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`runner-chief`** (`squads/runner-ops/agents/runner-chief.md`).

```text
@runner-chief
# ou, se a skill de entrada estiver instalada:
# $ runner-ops

*help
```

Agentes (amostra): `runner-architect`, `runner-chief`, `runner-integrator`, `runner-monitor`, `runner-validator`

Tasks (amostra): `create-runner`, `evolve-module`, `gateway-runner-integration`, `integrate-runner`, `monitor-runners`, `register-runner`, `retire-runner`, `update-runner`

Workflows (amostra): _(nenhum workflow yaml listado; use tasks e o chief)_

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad runner-ops de squads/runner-ops/.
Siga o config.yaml e o orquestrador runner-chief.
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
Use o squad runner-ops (Runner Ops).

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
Leia squads/runner-ops/config.yaml e adote a persona de runner-chief.
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
