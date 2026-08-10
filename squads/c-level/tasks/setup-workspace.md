# Task: Setup Workspace

task_id: setup-workspace
```yaml
task:
  task_id: setup-workspace
  id: setup-workspace
  name: Setup Completo do Workspace
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: true
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace-setup-summary.md
pre_condition:
- Bootstrap executado ou contexto do business carregado.
post_condition:
- Decisão ou artefato registrado com handoff explícito para a próxima etapa.
performance:
- Responder sem inventar dados e escalar bloqueios estruturais imediatamente.
Error Handling:
- Escalar blockers estruturais imediatamente e interromper a execução quando o input canônico estiver inconsistente.
Completion Criteria:
- [ ] Output produzido no caminho esperado.
- [ ] Critérios de completude registrados.

## Descricao

O COO orquestra o setup completo do workspace para um negocio especifico, garantindo que todos os outputs vao para YAMLs canonicos com template previo.

## Pre-requisitos

- Bootstrap executado (`.user/user.md` existe)
- Workspace criado (`workspace/{spoke}/` existe)
- Preflight workspace-first aprovado:
  - `bash squads/c-level/scripts/bootstrap-c-level-workspace.sh`
  - `bash squads/c-level/scripts/validate-c-level-essentials.sh`

## Usage

```bash
*setup-workspace {slug}
```

## Workflow

### Fase 1: Contexto e Preflight

1. Executar scripts de preflight.
2. Executar `*workspace-context {slug}` (`load-workspace-context.md`).
3. Garantir scaffold template-first (`*scaffold-templates {slug}`) antes de qualquer escrita.

### Fase 2: Orquestracao por C-Level

```yaml
execution_order:
  - agent: coo-orchestrator
    task: elicit-company-profile
    output: workspace/{spoke}/L0-identity/company-dna.yaml

  - agent: cmo-architect
    task: elicit-icp-yaml
    output: workspace/{spoke}/L1-strategy/icp.yaml

  - agent: cmo-architect
    task: elicit-brand-yaml
    output: workspace/{spoke}/L2-tactical/brand/brandbook.yaml

  - agent: cto-architect
    task: elicit-tech-strategy
    output: workspace/{spoke}/L1-strategy/tech-strategy.yaml

  - agent: cio-engineer
    task: elicit-tech-stack
    output: workspace/{spoke}/L1-strategy/tech-stack.yaml

  - agent: caio-architect
    task: elicit-ai-strategy
    output: workspace/{spoke}/L1-strategy/ai-strategy.yaml

  - agent: coo-orchestrator
    task: elicit-operations
    output: .aiox-core/core-config.yaml
```

### Fase 3: Consolidacao

1. Verificar completude dos YAMLs gerados.
2. Consolidar pendencias e bloqueios no resumo final da execucao.
3. Nao criar artefatos `.md` em `workspace/{spoke}/` fora do contrato de templates.

## Outputs esperados

- `workspace/{spoke}/L0-identity/company-dna.yaml`
- `workspace/{spoke}/L1-strategy/icp.yaml`
- `workspace/{spoke}/L2-tactical/brand/brandbook.yaml`
- `workspace/{spoke}/L1-strategy/tech-strategy.yaml`
- `workspace/{spoke}/L1-strategy/tech-stack.yaml`
- `workspace/{spoke}/L1-strategy/ai-strategy.yaml`
- `workspace/{spoke}/L4-operational/evidence/workspace-context-summary.yaml`

## Validacao

- [ ] Preflight workspace-first passou.
- [ ] `*workspace-context {slug}` executado antes dos handoffs.
- [ ] Todos os outputs do setup foram gravados em YAML canonico com template correspondente.
- [ ] Nenhum output novo foi salvo em `workspace/` sem template.
