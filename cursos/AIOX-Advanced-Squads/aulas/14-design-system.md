---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: design-system
lesson_position: 14
title: "Design System — construir a biblioteca visual"
squad: design-system
agents: 11
tasks: 108
workflows: 15
module: M3
sequence: M3.2
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, design-system, layer/curso, curso/squads, squad/design-system]
maturity: partial
---

# Design System — construir a biblioteca visual

> Vault: [[squads/design-system/README|design-system]] · [[skills/design-system/SKILL|design-system]] · [[cursos/MOC-Squads]]

[← Brand](13-brand.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Design Ops](15-design-ops.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise método e gates no **AIOX Advanced** (`13-pensamento-estruturado-antes-do-terminal`, `48-quality-gate-completo`) e faça no **AIOX Design** ao menos as aulas 01–04 e 09.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/design-system/`
- config: `squads/design-system/config.yaml`
- agentes: `squads/design-system/agents/`
- tasks: `squads/design-system/tasks/`
- workflows: `squads/design-system/workflows/`
- skill de entrada (opcional): `skills/design-system/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/design-system /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **11 agentes**, **108 tasks**, **15 workflows**.

## Quando usar — e quando não usar

**Use quando:** tokens, foundations, componentes e registry do design system.

**Não use quando:** governança contínua e drift (use Design Ops). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`design-chief`** (`squads/design-system/agents/design-chief.md`).

```text
@design-chief
# ou, se a skill de entrada estiver instalada:
# $ design-system

*help
```

Agentes (amostra): `brad-frost`, `dan-mall`, `dave-malouf`, `design-chief`, `ds-foundations-lead`, `ds-token-architect`, `image-generator`, `nano-banana-generator` … (+2)

Tasks (amostra): `a11y-audit`, `aria-audit`, `atomic-refactor-execute`, `atomic-refactor-plan`, `audit-reading-experience`, `audit-tailwind-config`, `bootstrap-shadcn-library`, `bundle-audit`

Workflows (amostra): `agentic-readiness`, `audit-only`, `brownfield-complete`, `critical-eye`, `dtcg-tokens-governance`, `epic-ds-alignment`, `foundations-pipeline`, `greenfield-new`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad design-system de squads/design-system/.
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
Use o squad design-system (Design System).

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
Leia squads/design-system/config.yaml e adote a persona de design-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## O que muda no AIOX Enterprise

Neste acervo, você leva ao squad o contexto visual que conseguir reunir. No Enterprise, o Design System pode consumir o contexto de marca do workspace. Também lê os tokens visuais sociais e os padrões de interface de marketing, depois da validação de prontidão.

**O ganho prático:** o trabalho não começa por uma paleta genérica nem por referências soltas. Componentes e decisões visuais partem de uma verdade de marca já organizada para aquela empresa e aplicação.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Escolha um produto seu (ou um projeto de estudo) em que cor, espaçamento e tipografia vivem hardcoded nos componentes. A missão é construir a primeira camada de foundations: extrair os valores reais do código com `ds-extract-tokens` e consolidá-los em tokens nomeados rodando o workflow `foundations-pipeline`. O objetivo não é redesenhar o produto — é dar nome e fonte única ao que já existe.

**Saída esperada:** um arquivo de tokens (cor, tipografia, espaçamento) com (1) nomes semânticos em vez de valores brutos (`color.action.primary`, não `blue-500`), (2) cada token rastreável a um uso real no código de origem e (3) pelo menos um componente refatorado consumindo os tokens como prova de adoção.

**Erro comum neste squad:** inventar uma paleta "ideal" no vácuo em vez de partir do que o produto já usa — nasce um DS paralelo que ninguém adota. Detecte cedo: se os tokens propostos não baterem com nenhum valor encontrado na extração, o squad está desenhando, não sistematizando.

> **Teste rápido**: pergunte de qualquer token "de onde veio este valor?" — se a resposta não apontar para o produto real, refaça a extração.
