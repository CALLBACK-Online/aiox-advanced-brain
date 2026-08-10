---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: squad-creator
lesson_position: 23
title: "Squad Creator — criar uma capacidade organizacional"
squad: squad-creator
agents: 1
tasks: 150
workflows: 26
module: M5
sequence: M5.2
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, squad-creator, layer/curso, curso/squads, squad/squad-creator]
maturity: partial
---

# Squad Creator — criar uma capacidade organizacional

> Vault: [[squads/squad-creator/README|squad-creator]] · [[skills/squad-creator/SKILL|squad-creator]] · [[cursos/MOC-Squads]]

[← Skill Creator Ops](22-skill-creator-ops.md) · [↑ M5](../modulos/M5-metacapacidades.md) · [⌂ Curso](../README.md) · [→ Squad Creator Pro](24-squad-creator-pro.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `33-anatomia-de-um-squad; 34-squad-creator-passo-a-passo; 55-triagem-de-squad-novo` — criar capacidade.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/squad-creator/`
- config: `squads/squad-creator/config.yaml`
- agentes: `squads/squad-creator/agents/`
- tasks: `squads/squad-creator/tasks/`
- workflows: `squads/squad-creator/workflows/`
- skill de entrada (opcional): `skills/squad-chief/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/squad-creator /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **1 agentes**, **150 tasks**, **26 workflows**.

## Quando usar — e quando não usar

**Use quando:** scaffold, validar e publicar um squad canônico.

**Não use quando:** só uma skill; ou quando prior art já resolve com REUSE. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`squad-chief`** (`squads/squad-creator/agents/squad-chief.md`).

```text
@squad-chief
# ou, se a skill de entrada estiver instalada:
# $ squad-creator

*help
```

Agentes (amostra): `squad-chief`

Tasks (amostra): `an-clone-review`, `an-compare-outputs`, `an-validate-clone`, `audit-output-quality`, `auto-heal-close`, `auto-heal-resolve`, `auto-heal`, `auto-healing-gate`

Workflows (amostra): `create-squad`, `validate-squad`, `wf-auto-heal`, `wf-create-agent`, `wf-create-greeting-script`, `wf-create-pipeline`, `wf-create-squad`, `wf-create-task`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad squad-creator de squads/squad-creator/.
Siga o config.yaml e o orquestrador squad-chief.
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
Use o squad squad-creator (Squad Creator).

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
Leia squads/squad-creator/config.yaml e adote a persona de squad-chief.
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
