---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: domain-decoder
lesson_position: 4
title: "Domain Decoder — regras de negócio no código"
squad: domain-decoder
agents: 8
tasks: 6
workflows: 2
module: M0
sequence: M0.4
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, domain-decoder, layer/curso, curso/squads, squad/domain-decoder]
maturity: partial
---

# Domain Decoder — regras de negócio no código

> Vault: [[squads/domain-decoder/README|domain-decoder]] · [[skills/domain-decoder/SKILL|domain-decoder]] · [[cursos/MOC-Squads]]

[← Code Anatomist](03-code-anatomist.md) · [↑ M0](../modulos/M0-escolha-pesquisa-dominio.md) · [⌂ Curso](../README.md) · [→ Agent Autonomy](05-agent-autonomy.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `cursos/AIOX Advanced/lessons/`) revise: `38-code-anatomy-domain-decoder` — regras de domínio no código.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/domain-decoder/`
- config: `squads/domain-decoder/config.yaml`
- agentes: `squads/domain-decoder/agents/`
- tasks: `squads/domain-decoder/tasks/`
- workflows: `squads/domain-decoder/workflows/`
- skill de entrada (opcional): `skills/decoder-chief/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/domain-decoder /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **8 agentes**, **6 tasks**, **2 workflows**.

## Quando usar — e quando não usar

**Use quando:** formalizar regras, taxonomias e decisões a partir de brownfield.

**Não use quando:** mapa arquitetural completo (use Code Anatomist). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`decoder-chief`** (`squads/domain-decoder/agents/decoder-chief.md`).

```text
@decoder-chief
# ou, se a skill de entrada estiver instalada:
# $ domain-decoder

*help
```

Agentes (amostra): `barbara-von-halle`, `decoder-chief`, `eric-evans`, `graham-witt`, `james-taylor`, `martin-fowler`, `michael-feathers`, `ronald-ross`

Tasks (amostra): `characterize-legacy`, `classify-rules`, `express-rules`, `extract-rules`, `map-domain`, `model-decisions`

Workflows (amostra): `wf-extract-rules`, `wf-standardize-rules`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad domain-decoder de squads/domain-decoder/.
Siga o config.yaml e o orquestrador decoder-chief.
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
Use o squad domain-decoder (Domain Decoder).

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
Leia squads/domain-decoder/config.yaml e adote a persona de decoder-chief.
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
