---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: sales
lesson_position: 20
title: "Sales — funil completo de vendas"
squad: sales
agents: 9
tasks: 9
workflows: 0
module: M4
sequence: M4.3
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, sales, layer/curso, curso/squads, squad/sales]
maturity: partial
---

# Sales — funil completo de vendas

> Vault: [[squads/sales/README|sales]] · [[skills/sales/SKILL|sales]] · [[cursos/MOC-Squads]]

[← Copy](19-copy.md) · [↑ M4](../modulos/M4-aquisicao-conteudo-vendas.md) · [⌂ Curso](../README.md) · [→ Hormozi](21-hormozi.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `24-entidade-como-unidade-de-processo` no **AIOX Advanced**. Para dor, ROI e estágio comercial, use `cursos/AIOX-Productizacao/aulas/02-dor-e-roi.md`, `03-distribuicao-vs-produto.md` e `05-estagios-de-monetizacao.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/sales/`
- config: `squads/sales/config.yaml`
- agentes: `squads/sales/agents/`
- tasks: `squads/sales/tasks/`
- workflows: `squads/sales/workflows/`
- skill de entrada (opcional): `skills/sales/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/sales /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **9 agentes**, **9 tasks**, **0 workflows**.

## Quando usar — e quando não usar

**Use quando:** diagnóstico, qualificação, prospecção, negociação e fechamento.

**Não use quando:** só uma landing page (Copy) ou oferta $100M completa (Hormozi). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`sales-chief`** (`squads/sales/agents/sales-chief.md`).

```text
@sales-chief
# ou, se a skill de entrada estiver instalada:
# $ sales

*help
```

Agentes (amostra): `aaron-ross`, `challenger-sale`, `chet-holmes`, `chris-voss`, `david-sandler`, `jeb-blount`, `keenan`, `neil-rackham` … (+1)

Tasks (amostra): `close-deal`, `create-cold-outreach`, `create-email-sequences`, `create-followup-sequence`, `create-sales-copy`, `create-sales-scripts`, `diagnose-deal`, `negotiate-deal`

Workflows (amostra): _(nenhum workflow yaml listado; use tasks e o chief)_

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad sales de squads/sales/.
Siga o config.yaml e o orquestrador sales-chief.
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
Use o squad sales (Sales).

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
Leia squads/sales/config.yaml e adote a persona de sales-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Você vende uma mentoria B2B de R$ 24 mil e hoje o “funil” é responder WhatsApp quando aparece lead. A missão: desenhar o funil completo desse produto — da prospecção ao fechamento — começando por `qualify-prospect` para definir critérios objetivos de entrada e usando `diagnose-deal` como rito padrão para toda oportunidade parada. Cada etapa precisa de critério de saída explícito e dono nomeado.

**Saída esperada:** um documento de funil com etapas nomeadas e critérios de entrada/saída, roteiro de qualificação com perguntas e desqualificadores, e sequência de follow-up mapeada etapa a etapa.

**Erro comum neste squad:** pular a qualificação e tratar todo lead como oportunidade — o pipeline incha e a taxa de fechamento despenca. Detecte cedo contando oportunidades sem próximo passo agendado: mais que zero já é sintoma.

> **Teste rápido**: pegue uma oportunidade qualquer do funil desenhado — se você não sabe dizer a etapa e o próximo passo dela, o desenho falhou.
