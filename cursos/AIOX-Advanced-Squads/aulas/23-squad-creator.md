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

Antes de operar este squad, revise `23-o-que-e-um-squad` e `24-entidade-como-unidade-de-processo` no **AIOX Advanced**. Para construir a capacidade, use `cursos/AIOX-Agent-Engineering/aulas/13-reuse-adapt-create.md` a `16-squad-creator.md`.

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

## O que muda no AIOX Enterprise

Aqui você cria o squad a partir do briefing e valida sua estrutura no projeto de destino. No Enterprise, o Squad Creator também lê templates, domínios e contratos do workspace antes do scaffolding, sem escrever diretamente nos dados do negócio.

**O ganho prático:** o novo squad não nasce como uma ilha. Ele já pode ser desenhado para conversar com o ecossistema existente e encaminhar à governança qualquer integração que exija autoridade maior.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

A operação precisa de uma capacidade de “suporte técnico N2” que nenhum squad do ecossistema cobre por inteiro. A missão: rodar `create-squad-discover` primeiro e respeitar o veredito na ordem REUSE → ADAPT → CREATE — só avance para o scaffold via `wf-create-squad` se o discovery provar que não há prior art aproveitável nem squad vizinho que resolva com ajustes.

**Saída esperada:** o artefato de discovery com o veredito documentado e o prior art comparado; se o veredito for CREATE, o pacote novo com config.yaml, agentes e tasks gerados pelo scaffold e validação estrutural aprovada antes de publicar.

**Erro comum neste squad:** pular o discovery e criar um duplicado do que já existe com outro nome — o ecossistema fragmenta e a manutenção dobra. Detecte cedo: se o documento de discovery não lista os squads vizinhos comparados, a triagem não aconteceu.

> **Teste rápido**: você consegue apontar no discovery por que REUSE e ADAPT foram descartados antes do CREATE?
