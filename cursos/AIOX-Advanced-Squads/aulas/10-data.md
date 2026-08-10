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
tags: [curso/aiox-advanced-squads, squad, data, layer/curso, curso/squads, squad/data]
maturity: partial
---

# Data — analytics e decisões com dados

> Vault: [[squads/data/README|data]] · [[skills/data/SKILL|data]] · [[cursos/MOC-Squads]]

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

## O que muda no AIOX Enterprise

Neste acervo, você prepara a análise e entrega o artefato no projeto escolhido. No Enterprise, o Data Squad consome o contexto real do negócio e registra análises canônicas no espaço estratégico de analytics do workspace.

**O ganho prático:** a métrica deixa de ser uma resposta isolada. Ela passa a compor a memória estratégica que sustenta novas decisões e pode ser revisitada sem refazer toda a investigação.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

A diretoria afirma que "o churn aumentou", mas ninguém sabe se o problema é geral ou concentrado nas turmas recentes. Rode o workflow `cohorts-diagnostic` para separar o efeito por coorte de entrada e use `analyze-cohort` para comparar a retenção das últimas quatro coortes com a base histórica antes de aceitar qualquer narrativa.

**Saída esperada:** um diagnóstico com curva de retenção por coorte, a coorte (ou o comportamento transversal) responsável pela queda identificada com números, e uma recomendação acionável com as premissas de dados declaradas.

**Erro comum neste squad:** responder com a métrica agregada sem segmentar — a média esconde que uma única coorte puxa tudo para baixo. Detecte cedo exigindo o corte por coorte no primeiro artefato intermediário, antes de qualquer dashboard.

> **Teste rápido**: se a resposta cabe em um número único sem dizer de qual coorte e período ele veio, a análise não terminou.
