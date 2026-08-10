---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: research
lesson_position: 2
title: "Research — inteligência e discovery multi-fonte"
squad: research
agents: 14
tasks: 65
workflows: 5
module: M0
sequence: M0.2
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, research]
maturity: study
---

# Research — inteligência e discovery multi-fonte

[← Advisory Board](01-advisory-board.md) · [↑ M0](../modulos/M0-escolha-pesquisa-dominio.md) · [⌂ Curso](../README.md) · [→ Code Anatomist](03-code-anatomist.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `36-tech-research-multi-fonte; 37-spy-bench-comparativo` — pesquisa com evidência.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/research/`
- config: `squads/research/config.yaml`
- agentes: `squads/research/agents/`
- tasks: `squads/research/tasks/`
- workflows: `squads/research/workflows/`
- skill de entrada (opcional): `skills/research/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/research /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **14 agentes**, **65 tasks**, **5 workflows**.

## Quando usar — e quando não usar

**Use quando:** pesquisa técnica, competitiva, discovery e benchmark com evidência.

**Não use quando:** decisão política sem dados ou engenharia reversa de código. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`research-chief`** (`squads/research/agents/research-chief.md`).

```text
@research-chief
# ou, se a skill de entrada estiver instalada:
# $ research

*help
```

Agentes (amostra): `bench-analyst`, `benchmark-runtime`, `booth`, `creswell`, `dr-orchestrator`, `forsgren`, `gilad`, `klein` … (+2)

Tasks (amostra): `bench-absorb`, `bench-battle-card`, `bench-codebase-recon`, `bench-company-intel`, `bench-deep-compare`, `bench-detect`, `bench-framework`, `bench-gap-analysis`

Workflows (amostra): `bench-comparison-pipeline`, `wf-competitive-intel`, `wf-deep-research`, `wf-product-discovery`, `wf-quick-research`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad research de squads/research/.
Siga o config.yaml e o orquestrador research-chief.
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
Use o squad research (Research).

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
Leia squads/research/config.yaml e adote a persona de research-chief.
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
