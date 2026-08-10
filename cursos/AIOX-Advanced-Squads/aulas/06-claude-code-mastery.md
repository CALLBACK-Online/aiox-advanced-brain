---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: claude-code-mastery
lesson_position: 6
title: "Claude Code Mastery — ambiente Claude Code"
squad: claude-code-mastery
agents: 8
tasks: 31
workflows: 3
module: M1
sequence: M1.2
status: canonical
canonical_scope: Cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, claude-code-mastery]
maturity: study
---

# Claude Code Mastery — ambiente Claude Code

[← Agent Autonomy](05-agent-autonomy.md) · [↑ M1](../modulos/M1-autonomia-operacoes.md) · [⌂ Curso](../README.md) · [→ AIOX SOP](07-aiox-sop.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, no curso **AIOX Advanced** (pasta `Cursos/AIOX Advanced/lessons/`) revise: `03-claude-md-leis-da-fisica; 17-engenharia-de-contexto` — setup e contexto.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `Cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `Cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/claude-code-mastery/`
- config: `squads/claude-code-mastery/config.yaml`
- agentes: `squads/claude-code-mastery/agents/`
- tasks: `squads/claude-code-mastery/tasks/`
- workflows: `squads/claude-code-mastery/workflows/`
- skill de entrada (opcional): `skills/claude-code-mastery/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/claude-code-mastery /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **8 agentes**, **31 tasks**, **3 workflows**.

## Quando usar — e quando não usar

**Use quando:** hooks, skills, MCP, subagentes e integração de projeto no Claude Code.

**Não use quando:** implementar feature de produto de negócio. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`claude-mastery-chief`** (`squads/claude-code-mastery/agents/claude-mastery-chief.md`).

```text
@claude-mastery-chief
# ou, se a skill de entrada estiver instalada:
# $ claude-code-mastery

*help
```

Agentes (amostra): `claude-mastery-chief`, `config-engineer`, `hooks-architect`, `mcp-integrator`, `project-integrator`, `roadmap-sentinel`, `skill-craftsman`, `swarm-orchestrator`

Tasks (amostra): `align-memory-context`, `audit-integration`, `audit-settings`, `audit-setup`, `brownfield-setup`, `ci-cd-setup`, `claude-md-engineer`, `configure-claude-code`

Workflows (amostra): `wf-audit-complete`, `wf-knowledge-update`, `wf-project-setup`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad claude-code-mastery de squads/claude-code-mastery/.
Siga o config.yaml e o orquestrador claude-mastery-chief.
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
Use o squad claude-code-mastery (Claude Code Mastery).

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
Leia squads/claude-code-mastery/config.yaml e adote a persona de claude-mastery-chief.
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
