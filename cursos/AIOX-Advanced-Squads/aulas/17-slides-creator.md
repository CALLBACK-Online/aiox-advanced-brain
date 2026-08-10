---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: slides-creator
lesson_position: 17
title: "Slides Creator — decks com narrativa e QA"
squad: slides-creator
agents: 7
tasks: 53
workflows: 1
module: M3
sequence: M3.5
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, slides-creator, layer/curso, curso/squads, squad/slides-creator]
maturity: partial
---

# Slides Creator — decks com narrativa e QA

> Vault: [[squads/slides-creator/README|slides-creator]] · [[skills/slides-creator/SKILL|slides-creator]] · [[cursos/MOC-Squads]]

[← Storytelling](16-storytelling.md) · [↑ M3](../modulos/M3-marca-experiencia-narrativa.md) · [⌂ Curso](../README.md) · [→ Conteúdo](18-conteudo.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/aulas/`) revise: `18-yaml-markdown-json-sweet-spot` — estrutura de artefato.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/slides-creator/`
- config: `squads/slides-creator/config.yaml`
- agentes: `squads/slides-creator/agents/`
- tasks: `squads/slides-creator/tasks/`
- workflows: `squads/slides-creator/workflows/`
- skill de entrada (opcional): `skills/slide-creator/SKILL.md` (nome quase homônimo)
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/slides-creator /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **7 agentes**, **53 tasks**, **1 workflows**.

## Quando usar — e quando não usar

**Use quando:** briefing → narrativa → slides → notas → QA de deck.

**Não use quando:** só texto de venda sem deck (Copy) ou só história sem slides. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`slide-chief`** (`squads/slides-creator/agents/slide-chief.md`).

```text
@slide-chief
# ou, se a skill de entrada estiver instalada:
# $ slides-creator

*help
```

Agentes (amostra): `content-architect`, `design-planner`, `design-renderer`, `qa-inspector`, `slide-chief`, `template-curator`, `visual-scout`

Tasks (amostra): `apply-design-revision`, `apply-scqa`, `build-pyramid`, `catalog-sources-apa`, `classify-slide-type`, `clone-visual-style-signature`, `compose-grid-layout`, `compress-outline-to-slide-functions`

Workflows (amostra): `generate-presentation`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad slides-creator de squads/slides-creator/.
Siga o config.yaml e o orquestrador slide-chief.
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
Use o squad slides-creator (Slides Creator).

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
Leia squads/slides-creator/config.yaml e adote a persona de slide-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## O que muda no AIOX Enterprise

Aqui você fornece conteúdo, referências e restrições para construir o deck. No Enterprise, o Slides Creator consome o contexto de marca do workspace. O operador controla a prontidão, o handoff e o destino de renderização de cada implantação.

**O ganho prático:** o deck não precisa reaprender a identidade visual nem depender de uma entrega genérica. A narrativa chega ao aplicativo de destino já orientada pela marca que a empresa mantém.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Monte o deck de 10 slides que apresenta o resultado do trimestre à diretoria, com uma decisão pedida: aprovar o orçamento do próximo ciclo. Rode o workflow `generate-presentation` do briefing à renderização, estruturando o argumento com `apply-scqa` e exigindo que cada slide passe pelos gates de QA do pacote antes de considerar pronto.

**Saída esperada:** um deck com (1) action titles que afirmam a conclusão de cada slide (não rótulos como "Resultados"), (2) densidade dentro do limite validado — nada de parágrafos em slide — e (3) relatório de QA anexo mostrando quais validações rodaram e o que foi corrigido.

**Erro comum neste squad:** aceitar o deck "bonito" sem rodar o QA — títulos-rótulo e slides lotados passam despercebidos porque o visual distrai. Detecte cedo: leia apenas os títulos em sequência; se eles não contarem o argumento completo sozinhos, o deck reprova antes de qualquer ajuste visual.

> **Teste rápido**: alguém que leia só os action titles consegue reproduzir sua recomendação? Se não, volte ao gate `validate-action-title`.
