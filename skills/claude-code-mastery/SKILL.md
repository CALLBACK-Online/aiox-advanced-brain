---
name: claude-code-mastery
description: |
  Claude Code Mastery — hooks, skills, subagentes, MCPs, plugins, agent teams e integração de projetos no Claude Code.
  Use quando quer configurar, dominar ou evoluir o ambiente Claude Code.
---

# Claude Code Mastery Squad


## Quando usar

- Use esta skill como **porta de entrada** do squad `claude-code-mastery` quando a missão for a dor coberta pela aula do curso.
- **Não use** como substituto do mapa de decisão se a intenção for ambígua entre vários squads — use `aiox-squads` primeiro.

## Quando não usar

- Missão de outro domínio (escolha outro squad/skill).
- Só quer estudar anatomia sem copiar o pacote: leia a aula e o `squads/claude-code-mastery/` sem ativar runtime.

## Aula do curso (como usar de verdade)

`cursos/AIOX-Advanced-Squads/aulas/06-claude-code-mastery.md`

Lá estão: quando usar/evitar, briefing, ativação, evidência e limites de maturidade.


Squad com **8 agentes** especializados.

> **Maturidade neste acervo:** `partial` — ver `docs/runtime-dependencies.md`.
> Fonte canônica de materiais: `../upstream-monorepo` (quando sincronizado).

## Agents

- **claude-mastery-chief** (`claude-mastery-chief`)
- **config-engineer** (`config-engineer`)
- **hooks-architect** (`hooks-architect`)
- **mcp-integrator** (`mcp-integrator`)
- **project-integrator** (`project-integrator`)
- **roadmap-sentinel** (`roadmap-sentinel`)
- **skill-craftsman** (`skill-craftsman`)
- **swarm-orchestrator** (`swarm-orchestrator`)

## Activation

O orchestrador principal é `claude-mastery-chief`. Para ativar:

1. Leia `squads/claude-code-mastery/agents/claude-mastery-chief.md` e adote a persona
2. Carregue config: `squads/claude-code-mastery/config.yaml`
3. Siga o mission router do chief para delegar trabalho

## Available Tasks

- `align-memory-context`
- `audit-integration`
- `audit-settings`
- `audit-setup`
- `brownfield-setup`
- `ci-cd-setup`
- `claude-md-engineer`
- `configure-claude-code`
- `context-rot-audit`
- `create-agent-definition`
- `create-rules`
- `create-team-topology`
- `delete-claude-code-mastery`
- `diagnose`
- `enterprise-config`
- `hook-designer`
- `integrate-project`
- `mcp-integration-plan`
- `mcp-workflow`
- `multi-project-setup`
- `optimize-context`
- `optimize-workflow`
- `parallel-decomposition`
- `permission-strategy`
- … e mais 7 tasks em `squads/claude-code-mastery/tasks/`

## Available Workflows

- `wf-audit-complete`
- `wf-knowledge-update`
- `wf-project-setup`

## Squad Directory

`squads/claude-code-mastery/`
