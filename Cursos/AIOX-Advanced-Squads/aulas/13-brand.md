---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: brand
lesson_position: 13
title: "Brand — fundamentos, posicionamento e ativação"
squad: brand
agents: 16
tasks: 21
workflows: 9
module: M3
sequence: M3.1
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, brand]
maturity: partial
---

# Brand — fundamentos, posicionamento e ativação

[← ClickUp Ops](12-clickup-ops-squad.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Design System](14-design-system.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `Cursos/AIOX Advanced/lessons/`) revise: `12-repertorio-vs-tecnica` — repertório antes de estética.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `Cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `Cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/brand/`
- config: `squads/brand/config.yaml`
- agentes: `squads/brand/agents/`
- tasks: `squads/brand/tasks/`
- workflows: `squads/brand/workflows/`
- skill de entrada (opcional): `skills/brand/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/brand /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **16 agentes**, **21 tasks**, **9 workflows**.

## Quando usar — e quando não usar

**Use quando:** naming, posicionamento, narrativa e sistema de marca.

**Não use quando:** componentes de UI (Design System) ou QA visual (Design Ops). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`brand-chief`** (`squads/brand/agents/brand-chief.md`).

```text
@brand-chief
# ou, se a skill de entrada estiver instalada:
# $ brand

*help
```

Agentes (amostra): `aaker-brand-identity`, `archetype-consultant`, `brand-chief`, `brand-strategist`, `domain-scout`, `heyward-dtc-brand`, `keller-brand-equity`, `miller-sticky-brand` … (+2)

Tasks (amostra): `brand-activation`, `brand-book`, `brand-consulting`, `brand-diagnosis`, `brand-identity`, `brand-messaging`, `brand-quality-gate`, `create-brand-epic`

Workflows (amostra): `wf-brand-activation-system`, `wf-brand-all-hands`, `wf-brand-complete`, `wf-brand-consulting`, `wf-brand-foundations`, `wf-brand-mockup-generation`, `wf-brand-positioning-narrative`, `wf-logo-brainstorm`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad brand de squads/brand/.
Siga o config.yaml e o orquestrador brand-chief.
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
Use o squad brand (Brand).

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
Leia squads/brand/config.yaml e adote a persona de brand-chief.
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
