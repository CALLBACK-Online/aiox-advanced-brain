---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: agent-autonomy
lesson_position: 5
title: "Agent Autonomy — auditar e elevar autonomia"
squad: agent-autonomy
agents: 6
tasks: 7
workflows: 1
module: M1
sequence: M1.1
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, agent-autonomy, layer/curso, curso/squads, squad/agent-autonomy]
maturity: partial
---

# Agent Autonomy — auditar e elevar autonomia

> Vault: [[squads/agent-autonomy/README|agent-autonomy]] · [[skills/agent-autonomy/SKILL|agent-autonomy]] · [[cursos/MOC-Squads]]

[← Domain Decoder](04-domain-decoder.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ Claude Code Mastery](06-claude-code-mastery.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `11-goal-vs-loop`, `20-determinismo-progressivo` e `21-deterministico-primeiro-llm-onde-gera-ouro` no **AIOX Advanced**. Para aprofundar composição de agents, use `cursos/AIOX-Agent-Engineering/aulas/03-subagents-vs-swarm.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/agent-autonomy/`
- config: `squads/agent-autonomy/config.yaml`
- agentes: `squads/agent-autonomy/agents/`
- tasks: `squads/agent-autonomy/tasks/`
- workflows: `squads/agent-autonomy/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/agent-autonomy /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **6 agentes**, **7 tasks**, **1 workflows**.

## Quando usar — e quando não usar

**Use quando:** medir autonomia, loops, ownership e falhas de agentes.

**Não use quando:** criar um agente de domínio sem diagnóstico. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`autonomy-chief`** (`squads/agent-autonomy/agents/autonomy-chief.md`).

```text
@autonomy-chief
# ou, se a skill de entrada estiver instalada:
# $ agent-autonomy

*help
```

Agentes (amostra): `agent-architect`, `autonomy-auditor`, `autonomy-chief`, `ecosystem-scout`, `reasoning-engineer`, `tool-smith`

Tasks (amostra): `audit-agent`, `create-autonomous-agent`, `diagnose-autonomy-failure`, `optimize-agent`, `search-ecosystem`, `suggest-tools`, `teach-reasoning`

Workflows (amostra): `autonomy-thresholds`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad agent-autonomy de squads/agent-autonomy/.
Siga o config.yaml e o orquestrador autonomy-chief.
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
Use o squad agent-autonomy (Agent Autonomy).

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
Leia squads/agent-autonomy/config.yaml e adote a persona de autonomy-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Pegue um agente seu que já falhou de verdade — ficou em loop, pediu confirmação a cada passo ou “concluiu” sem terminar. Rode `audit-agent` para medir a autonomia atual e, sobre o pior sintoma, rode `diagnose-autonomy-failure` até chegar a uma causa raiz acionável: prompt, tools, critério de parada ou contexto. Só depois considere `optimize-agent` — otimizar sem diagnóstico é chute.

**Saída esperada:** relatório de auditoria com (1) nível de autonomia medido com evidência de sessões reais, não impressão, (2) causa raiz do loop apontando o componente específico (goal, tool, critério de parada), (3) prescrição de correção acompanhada de um teste que provaria a melhora.

**Erro comum neste squad:** tratar o sintoma em vez da causa — reescrever o prompt inteiro quando o problema era um critério de parada ausente ou uma tool que falha em silêncio. Detecte cedo: se o diagnóstico não cita nenhum trecho de transcript ou log do agente, ele foi feito de ouvido.

> **Teste rápido**: reproduza o loop original depois da correção; se você não sabe como reproduzi-lo, também não sabe se consertou.
