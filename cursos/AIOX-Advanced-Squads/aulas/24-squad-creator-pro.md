---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: squad-creator-pro
lesson_position: 24
title: "Squad Creator Pro — DNA, mentes e gates avançados"
squad: squad-creator-pro
agents: 6
tasks: 219
workflows: 52
module: M5
sequence: M5.3
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, squad-creator-pro, layer/curso, curso/squads, squad/squad-creator-pro]
maturity: partial
---

# Squad Creator Pro — DNA, mentes e gates avançados

> Vault: [[squads/squad-creator-pro/README|squad-creator-pro]] · [[skills/squad-creator-pro/SKILL|squad-creator-pro]] · [[cursos/MOC-Squads]]

[← Squad Creator](23-squad-creator.md) · [↑ M5](../modulos/M5-metacapacidades.md) · [⌂ Curso](../README.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `20-determinismo-progressivo` e `23-o-que-e-um-squad` no **AIOX Advanced**. Para criar com profundidade, use `cursos/AIOX-Agent-Engineering/aulas/14-triagem-de-squad.md` a `16-squad-creator.md` e `27-prontidao-de-producao.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/squad-creator-pro/`
- config: `squads/squad-creator-pro/config.yaml`
- agentes: `squads/squad-creator-pro/agents/`
- tasks: `squads/squad-creator-pro/tasks/`
- workflows: `squads/squad-creator-pro/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/squad-creator-pro /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **6 agentes**, **219 tasks**, **52 workflows**.

## Quando usar — e quando não usar

**Use quando:** clonagem mental, DNA, routing e gates avançados na criação de squads.

**Não use quando:** scaffold simples; comece pelo Squad Creator canônico. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`squad-chief`** (`squads/squad-creator-pro/agents/squad-chief.md`).

```text
@squad-chief
# ou, se a skill de entrada estiver instalada:
# $ squad-creator-pro

*help
```

Agentes (amostra): `alan_nicolas`, `ecosystem-analyst`, `heuristic-ops`, `pedro-valerio`, `squad-chief`, `thiago_finch`

Tasks (amostra): `CHANGELOG`, `an-assess-sources-collect`, `an-assess-sources-score`, `an-assess-sources`, `an-clone-review-report`, `an-clone-review-source-trinity`, `an-clone-review-stages-fidelity`, `an-clone-review`

Workflows (amostra): `create-squad`, `validate-squad`, `wf-assess-sources`, `wf-auto-acquire-sources`, `wf-brownfield-upgrade-squad`, `wf-clone-mind`, `wf-clone-review`, `wf-collect-sources`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad squad-creator-pro de squads/squad-creator-pro/.
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
Use o squad squad-creator-pro (Squad Creator Pro).

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
Leia squads/squad-creator-pro/config.yaml e adote a persona de squad-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## O que muda no AIOX Enterprise

Neste acervo, o modo Pro aprofunda DNA, contratos e gates do squad que você está construindo. No Enterprise, o fluxo lê os artefatos, templates e domínios do workspace. Assim, endurece os contratos e prepara o handoff correto quando o squad precisar de integração controlada.

**O ganho prático:** a sofisticação não fica apenas dentro do squad. Ela considera, desde a criação, como contexto, artefatos e autoridade circularão na operação — sem permitir escrita direta e silenciosa nos dados do negócio.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Um consultor sênior de precificação sai da empresa em 60 dias e nada do critério de decisão dele está documentado. A missão: clonar essa expertise rodando `wf-extract-dna` sobre fontes reais (gravações de calls, propostas, decisões passadas) e montar o clone com `wf-clone-mind`, submetendo o resultado ao gate de fidelidade antes de qualquer uso em produção.

**Saída esperada:** um pacote de clone com DNA extraído em camadas (voz e raciocínio) e fontes rastreáveis, score de `wf-fidelity-score` acima do limiar definido no briefing e parecer de revisão comparando saídas do clone com decisões reais do especialista.

**Erro comum neste squad:** extrair de fontes rasas (uma entrevista, dois posts) e obter um clone que imita o vocabulário mas erra as decisões. Detecte cedo: se a avaliação de fontes reprovar em volume ou diversidade, pare antes de montar o clone.

> **Teste rápido**: dê ao clone um caso que o especialista já resolveu — vocabulário parecido com decisão diferente é reprovação.

---

> **Sinal de continuidade**: este era o último squad do catálogo — você agora sabe escolher, operar e criar especialistas. Se o gargalo virou sustentar todos eles em operação — contexto, handoffs e governança a cada missão —, há uma trilha de 30 minutos para diagnosticar o próximo contexto: `cursos/AIOX-Enterprise/README.md`.
