---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: design-ops
lesson_position: 15
title: "Design Ops — governar o design system no tempo"
squad: design-ops
agents: 2
tasks: 126
workflows: 23
module: M3
sequence: M3.3
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, design-ops]
maturity: partial
---

# Design Ops — governar o design system no tempo

[← Design System](14-design-system.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Storytelling](16-storytelling.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `32-design-system-greenfield-brownfield; 41-…` — DS vivo e governança.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/design-ops/`
- config: `squads/design-ops/config.yaml`
- agentes: `squads/design-ops/agents/`
- tasks: `squads/design-ops/tasks/`
- workflows: `squads/design-ops/workflows/`
- skill de entrada (opcional): `skills/design-chief/SKILL.md` e/ou `skills/design-system/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/design-ops /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **2 agentes**, **126 tasks**, **23 workflows**.

## Quando usar — e quando não usar

**Use quando:** auditorias, a11y, regressão visual, Storybook e adoção.

**Não use quando:** criar o DS do zero (use Design System). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`design-chief`** (`squads/design-ops/agents/design-chief.md`).

```text
@design-chief
# ou, se a skill de entrada estiver instalada:
# $ design-ops

*help
```

Agentes (amostra): `dave-malouf`, `design-chief`

Tasks (amostra): `a11y-audit`, `aria-audit`, `artifact-create-html`, `artifact-tweak-protocol`, `artifact-verify-postbuild`, `atomic-refactor-execute`, `atomic-refactor-plan`, `audit-reading-experience`

Workflows (amostra): `agentic-readiness`, `audit-only`, `brownfield-complete`, `critical-eye`, `ds-static-to-dynamic-migration`, `dtcg-tokens-governance`, `epic-ds-alignment`, `foundations-pipeline`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad design-ops de squads/design-ops/.
Siga o config.yaml e o orquestrador design-chief.
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
Use o squad design-ops (Design Ops).

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
Leia squads/design-ops/config.yaml e adote a persona de design-chief.
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
