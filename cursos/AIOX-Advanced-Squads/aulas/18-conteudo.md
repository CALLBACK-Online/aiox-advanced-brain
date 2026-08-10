---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: conteudo
lesson_position: 18
title: "Conteúdo — Instagram e calendário social"
squad: conteudo
agents: 10
tasks: 28
workflows: 9
module: M4
sequence: M4.1
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, conteudo, layer/curso, curso/squads, squad/conteudo]
maturity: study
---

# Conteúdo — Instagram e calendário social

> Vault: [[squads/conteudo/README|conteudo]] · [[skills/conteudo/SKILL|conteudo]] · [[cursos/MOC-Squads]]

[← Slides Creator](17-slides-creator.md) · [↑ M4](../modulos/M4-aquisicao-conteudo-vendas.md) · [⌂ Curso](../README.md) · [→ Copy](19-copy.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise M0–M1 do **AIOX Advanced ativo** — método e contexto antes de calendário.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/conteudo/`
- config: `squads/conteudo/config.yaml`
- agentes: `squads/conteudo/agents/`
- tasks: `squads/conteudo/tasks/`
- workflows: `squads/conteudo/workflows/`
- skill de entrada (opcional): `skills/conteudo/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/conteudo /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **10 agentes**, **28 tasks**, **9 workflows**.

## Quando usar — e quando não usar

**Use quando:** carrosséis, Reels, Stories, campanhas e pesquisa de concorrentes.

**Não use quando:** funil de vendas B2B completo (Sales) ou brand strategy profunda. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`content-chief`** (`squads/conteudo/agents/content-chief.md`).

```text
@content-chief
# ou, se a skill de entrada estiver instalada:
# $ conteudo

*help
```

Agentes (amostra): `carousel-creator`, `competitor-analyst`, `content-chief`, `content-planner`, `content-repurposer`, `content-validator`, `positioning-expert`, `reels-creator` … (+2)

Tasks (amostra): `analyze-competitor`, `atomize-content`, `audit-content`, `create-bio`, `create-campaign`, `create-carousel`, `create-clc`, `create-content-series`

Workflows (amostra): `wf-21-days`, `wf-atomization`, `wf-campaign`, `wf-competitor-intel`, `wf-create-content`, `wf-hook-testing`, `wf-multiplicar`, `wf-positioning`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad conteudo de squads/conteudo/.
Siga o config.yaml e o orquestrador content-chief.
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
Use o squad conteudo (Conteúdo).

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
Leia squads/conteudo/config.yaml e adote a persona de content-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## O que muda no AIOX Enterprise

Neste acervo, você entrega ao squad o contexto de marca e estratégia a cada missão. No Enterprise, o Conteúdo lê identidade, estratégia e direção tática do workspace. Carrosséis, reels e textos retornam à camada operacional do negócio.

**O ganho prático:** o calendário deixa de ser uma sequência de peças avulsas. Cada conteúdo nasce da mesma estratégia e volta para um histórico operacional que pode alimentar os próximos ciclos de copy, marca e distribuição.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Planeje duas semanas de conteúdo para um perfil real no Instagram — por exemplo, uma consultoria que posta "quando dá" e sem funil. A missão: sair do improviso para um calendário com pilares definidos, misturando carrossel, Reels e Stories com intenção (atrair, nutrir, converter). Estruture com `plan-calendar` e prepare os ganchos das peças principais com `create-hook-batch`.

**Saída esperada:** um calendário de 14 dias com (1) cada peça amarrada a um pilar e a uma etapa do funil, (2) formato e gancho definidos por post — não "post sobre X" — e (3) pelo menos duas variações de hook para as peças de maior aposta.

**Erro comum neste squad:** gerar volume sem estratégia — 14 posts que não conversam entre si nem com o posicionamento. Detecte cedo: se você não consegue dizer qual pilar e qual etapa do funil cada peça atende, o calendário é uma lista, não um plano; volte à estratégia antes de escrever legendas.

> **Teste rápido**: aponte para qualquer dia do calendário e responda "por que esta peça, neste dia, para quem?" — sem resposta, o planejamento não terminou.
