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
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, aiox-sop, layer/curso, curso/squads, squad/aiox-sop]
maturity: partial
---

# AIOX SOP — processos repetíveis e auditáveis

> Vault: [[squads/aiox-sop/README|aiox-sop]] · [[skills/aiox-sop/SKILL|aiox-sop]] · [[cursos/MOC-Squads]]

[← Claude Code Mastery](06-claude-code-mastery.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ ETL Ops](08-etl-ops.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `19-ciclo-do-repositorio`, `24-entidade-como-unidade-de-processo` e `48-quality-gate-completo` no **AIOX Advanced**. Para taxonomia e workflow, use `cursos/AIOX-Agent-Engineering/aulas/02-taxonomia-da-capacidade.md` e `06-workflow-vs-comando.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

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

## O que muda no AIOX Enterprise

Neste acervo, o resultado é um SOP portátil que você instala e mantém no projeto de destino. No Enterprise, a fábrica também pode consumir o contexto operacional canônico de um negócio. Depois do gate de prontidão, publica a versão legível por máquina no namespace de SOPs desse workspace.

**O ganho prático:** o processo deixa de ser um documento solto. Ele passa a viver junto da operação que descreve, com contexto e governança para ser reutilizado sem reconstrução manual.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

O processo de onboarding de cliente da sua operação existe só na cabeça de uma pessoa. Rode `structured-interview` com quem executa hoje para extrair o passo a passo real, deixe o `sop-extractor` estruturar o rascunho e passe o resultado por `audit-sop` antes de considerar o documento pronto. Nada de escrever o SOP "de memória": a entrevista é a fonte.

**Saída esperada:** um SOP em Markdown com passos numerados e executáveis, dono e gatilho declarados por etapa, e critérios de aceite que permitem a outra pessoa rodar o processo sem perguntar nada.

**Erro comum neste squad:** documentar o processo idealizado em vez do praticado — o SOP descreve o que "deveria" acontecer e ninguém segue. Detecte cedo pedindo a quem executa que aponte, passo a passo, onde o rascunho diverge da rotina real antes do audit.

> **Teste rápido**: se alguém que nunca executou o processo não consegue completá-lo só lendo o SOP, a missão não está feita.
