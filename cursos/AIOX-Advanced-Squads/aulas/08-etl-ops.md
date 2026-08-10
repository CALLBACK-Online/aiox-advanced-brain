---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: etl-ops
lesson_position: 8
title: "ETL Ops — extrair, transformar e carregar"
squad: etl-ops
agents: 4
tasks: 7
workflows: 2
module: M1
sequence: M1.4
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, etl-ops, layer/curso, curso/squads, squad/etl-ops]
maturity: partial
---

# ETL Ops — extrair, transformar e carregar

> Vault: [[squads/etl-ops/README|etl-ops]] · [[skills/etl-ops/SKILL|etl-ops]] · [[cursos/MOC-Squads]]

[← AIOX SOP](07-aiox-sop.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ Runner Ops](09-runner-ops.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `22-pipeline-etl-com-agentes` — pipelines com agentes.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/etl-ops/`
- config: `squads/etl-ops/config.yaml`
- agentes: `squads/etl-ops/agents/`
- tasks: `squads/etl-ops/tasks/`
- workflows: `squads/etl-ops/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/etl-ops /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **4 agentes**, **7 tasks**, **2 workflows**.

## Quando usar — e quando não usar

**Use quando:** pipelines ETL, collectors e carga repetível com a stack existente.

**Não use quando:** analytics de decisão (use Data) ou schema de banco (use DB Sage). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`etl-chief`** (`squads/etl-ops/agents/etl-chief.md`).

```text
@etl-chief
# ou, se a skill de entrada estiver instalada:
# $ etl-ops

*help
```

Agentes (amostra): `etl-chief`, `etl-extractor`, `etl-transformer`, `knowledge-extractor`

Tasks (amostra): `compile`, `enrich`, `etl-env-bootstrap`, `extract-keyframes`, `extract-podcast`, `process`, `summarize-book`

Workflows (amostra): `etl-pipeline`, `etl-thresholds`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad etl-ops de squads/etl-ops/.
Siga o config.yaml e o orquestrador etl-chief.
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
Use o squad etl-ops (ETL Ops).

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
Leia squads/etl-ops/config.yaml e adote a persona de etl-chief.
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
