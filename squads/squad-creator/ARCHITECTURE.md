# Squad Creator Architecture

## Visao Geral

`squad-creator` e o meta-squad canonico do hub. Cria squads, agents, workflows e tasks via templates e validacao estrutural. Opera em 3 modos: base (24 workflows, 139 tasks, 1 agent), pro (auto-detected via `squad-creator-pro/`), e ecosystem (observabilidade continua).

## Superficie Ativa

- Entrada principal: [`config.yaml`](./config.yaml)
- Agent: [`agents/squad-chief.md`](./agents/squad-chief.md)
- Workflows canonicos: [`workflows/`](./workflows) (24 workflows)
- Tasks atomicas: [`tasks/`](./tasks) (139 tasks)
- Templates de contrato: [`templates/`](./templates) (36 templates)
- Checklists: [`checklists/`](./checklists) (17 checklists)
- Data/knowledge: [`data/`](./data)
- Scripts deterministicos: [`scripts/`](./scripts)
- Runtime transient: `.aiox/squad-runtime/{squad-name}/`

## Modelo de Dominio (4 Camadas)

```
Strategic      Governanca do ecossistema, catalogo e decisoes de arquitetura
Tactical       Orquestracao de criacao, validacao e upgrade de squads
Operational    Scaffolding, geracao de arquivos, instalacao e sincronizacao
Observability  Analise continua: topologia, performance, gaps, radar, custo
```

## Composicao SINKRA (6 niveis)

```
Tokens (29)        Unidades parametricas indivisiveis que governam fluxo entre tasks
    |
Atoms (139)        Tasks atomicas com 1 executor, inputs/outputs definidos
    |
Molecules (9)      Grupos recorrentes de 2+ Atoms em padrao reutilizavel
    |               mol-agent-factory, mol-squad-factory, mol-qa-pipeline,
    |               mol-upgrade-cycle, mol-task-factory, mol-workflow-factory,
    |               mol-provider-qualification, mol-ecosystem-analysis, mol-weekly-cadence
    |
Organisms (8)      Workflows completos com state machine e gestao de estado
    |               org-create-squad, org-create-agent, org-qa-pipeline,
    |               org-upgrade, org-cross-provider, org-ecosystem-analysis,
    |               org-weekly-report, org-self-improve
    |
Templates (36)     Configuraveis (parametros), NUNCA customizaveis (estrutura)
    |
Instances          Squads gerados — identidade unica, lifecycle rastreado
```

## Modelo de Execucao

- Executor formal: `@squad-chief` (unico agent do pack base)
- Pro mode: auto-detected via `squads/squad-creator-pro/config.yaml`
- Especialistas PRO entram por delegacao explicita: `@oalanicolas` (Mind Cloning), `@pedro-valerio` (Quality), `@thiago_finch` (Strategy)
- O pack nao escreve diretamente no workspace de negocios; `workspace_integration.level: read_only`

## Pipelines Principais

### Criacao de Squad

```
detect-squad-context -> parallel-discovery -> create-squad-design
    -> create-squad-build -> create-squad-publish -> create-squad-validate
```

### Criacao de Agent

```
create-agent-research -> create-agent-persona -> create-agent-commands
    -> create-agent-generate -> create-agent-validate -> create-agent-publish
```

### QA After Creation

```
qa-check-structure -> qa-check-schema -> qa-check-references
    -> qa-check-completeness -> qa-check-compatibility -> qa-generate-report
```

### Upgrade Squad

```
upgrade-squad-inventory -> upgrade-squad-gap -> upgrade-squad-plan
    -> upgrade-squad-apply -> upgrade-squad-verify
```

### Ecosystem Analysis

```
topology -> performance -> bottleneck -> gaps -> radar -> cost
```

## Contratos Estruturais

- `artifact_contracts` governam outputs tipados (10 contratos declarados em config.yaml)
- `journey_log` registra lifecycle events do pack
- `process_token_contract` valida 29 tokens declarados contra `data/base-core-contract.yaml`
- `entity_bindings` declaram 8 entidades owned e 2 consumed

## Fusao Kaizen (v6.0.0)

O squad absorveu as capacidades do antigo `kaizen` squad em v6.0.0, adicionando a camada de Observability:

- 8 tasks de observabilidade absorvidas integralmente
- `ecosystem-analyst` com 6 lentes internas (topology, performance, bottleneck, gaps, radar, cost)
- Proveniencia: `EPIC-108 (STORY-108.1 a 108.5)`

## Referencias

- Config: [`config.yaml`](./config.yaml)
- Token contract: [`data/process-token-map.yaml`](./data/process-token-map.yaml)
- Pro overlay: [`squads/squad-creator-pro/`](../squad-creator-pro/)
- Protocolos: [`protocols/ai-first-governance.md`](./protocols/ai-first-governance.md)
