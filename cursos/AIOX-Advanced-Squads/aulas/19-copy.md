---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: copy
lesson_position: 19
title: "Copy — peças de alta conversão"
squad: copy
agents: 27
tasks: 86
workflows: 18
module: M4
sequence: M4.2
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, copy]
maturity: partial
---

# Copy — peças de alta conversão

[← Conteúdo](18-conteudo.md) · [↑ M4](../modulos/M4-aquisicao-conteudo-vendas.md) · [⌂ Curso](../README.md) · [→ Sales](20-sales.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `Cursos/AIOX Advanced/lessons/`) revise: `M11 produtivização (recomendado)` — oferta e dor.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `Cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `Cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/copy/`
- config: `squads/copy/config.yaml`
- agentes: `squads/copy/agents/`
- tasks: `squads/copy/tasks/`
- workflows: `squads/copy/workflows/`
- skill de entrada (opcional): `skills/copy/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/copy /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **27 agentes**, **86 tasks**, **18 workflows**.

## Quando usar — e quando não usar

**Use quando:** páginas, e-mails, VSL, scripts e frameworks de copywriters.

**Não use quando:** posicionamento de marca inteiro ou negociação comercial ao vivo. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`copy-chief`** (`squads/copy/agents/copy-chief.md`).

```text
@copy-chief
# ou, se a skill de entrada estiver instalada:
# $ copy

*help
```

Agentes (amostra): `alex-hormozi`, `andre-chaperon`, `ben-settle`, `claude-hopkins`, `clayton-makepeace`, `copy-chief`, `copy-ops-worker`, `dan-kennedy` … (+2)

Tasks (amostra): `analyze-mental-conversation`, `apply-sugarman-triggers`, `audit-copy-hopkins`, `audit-landing-page`, `avatar-research`, `blend`, `briefing`, `create-book-funnel`

Workflows (amostra): `map-generated-quality-gates`, `map-generated-workflow-definition`, `wf-1-full-launch`, `wf-10-webinar-cold-weekly`, `wf-11-ghosted-recovery`, `wf-2-paid-traffic`, `wf-3-high-ticket`, `wf-4-organic-content`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad copy de squads/copy/.
Siga o config.yaml e o orquestrador copy-chief.
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
Use o squad copy (Copy).

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
Leia squads/copy/config.yaml e adote a persona de copy-chief.
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
