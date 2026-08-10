---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: aiox-sop
lesson_position: 7
title: "AIOX SOP — processos repetíveis e auditáveis"
squad: aiox-sop
agents: 6
tasks: 21
workflows: 5
module: M1
sequence: M1.3
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, aiox-sop]
maturity: partial
---

# AIOX SOP — processos repetíveis e auditáveis

[← Claude Code Mastery](06-claude-code-mastery.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ ETL Ops](08-etl-ops.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `Cursos/AIOX Advanced/lessons/`) revise: `28-taxonomia-task-skill-agent-workflow-runner` — processo e taxonomia.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `Cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `Cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/aiox-sop/`
- config: `squads/aiox-sop/config.yaml`
- agentes: `squads/aiox-sop/agents/`
- tasks: `squads/aiox-sop/tasks/`
- workflows: `squads/aiox-sop/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/aiox-sop /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **6 agentes**, **21 tasks**, **5 workflows**.

## Quando usar — e quando não usar

**Use quando:** criar, extrair e otimizar SOPs para humanos e agentes.

**Não use quando:** documentação cosmética sem processo executável. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`sop-chief`** (`squads/aiox-sop/agents/sop-chief.md`).

```text
@sop-chief
# ou, se a skill de entrada estiver instalada:
# $ aiox-sop

*help
```

Agentes (amostra): `sop-analyst`, `sop-auditor`, `sop-chief`, `sop-creator`, `sop-extractor`, `sop-ml-architect`

Tasks (amostra): `analyze-sop`, `analyze-squad`, `analyze-workflow`, `audit-batch`, `audit-sop`, `benchmark-sop`, `certify-sop`, `check-environment`

Workflows (amostra): `wf-sop-audit-pipeline`, `wf-sop-creation-pipeline`, `wf-sop-extraction-pipeline`, `wf-sop-pipeline-definition`, `wf-sop-quality-gates`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad aiox-sop de squads/aiox-sop/.
Siga o config.yaml e o orquestrador sop-chief.
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
Use o squad aiox-sop (AIOX SOP).

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
Leia squads/aiox-sop/config.yaml e adote a persona de sop-chief.
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
