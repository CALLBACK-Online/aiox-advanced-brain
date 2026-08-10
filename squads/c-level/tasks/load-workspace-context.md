# Task: Load Workspace Context

task_id: load-workspace-context
```yaml
task:
  task_id: load-workspace-context
  id: load-workspace-context
  name: Carregar Contexto do Workspace
  agent: coo-orchestrator
  responsavel_type: Agent
  trigger: manual
  elicit: false
  commands:
  - '*workspace-context {slug}'
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace/{spoke}/L4-operational/evidence/workspace-context-summary.yaml
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

## Descrição

Task de preflight para consolidar contexto do workspace antes de qualquer elicitação C-Level. Evita sobrescrita, reduz drift e garante handoffs informados entre COO, CEO e CMO.
No Sinkra Hub atual, o `workspace/{spoke}` é resolvido fisicamente para `workspace/businesses/{slug}`.

## Objetivo

1. Validar estrutura mínima com scripts do squad.
2. Ler dados já existentes do workspace.
3. Montar snapshot de contexto para os próximos handoffs.

## Workflow

### Fase 1: Preflight obrigatório

Executar, nesta ordem:

```bash
bash squads/c-level/scripts/bootstrap-c-level-workspace.sh
bash squads/c-level/scripts/validate-c-level-essentials.sh
```

Se a validação falhar, interromper e reportar caminhos faltantes.

### Fase 2: Carregar contexto global

Ler, se existirem:

- `workspace/{spoke}/document-registry.yaml`
- `.user/user.md`
- `.aiox-core/core-config.yaml`
- `squads/c-level/config.yaml`
- `squads/c-level/workflows/`

No hub atual, localizar o spoke alvo via `workspace/_system/config.yaml` e ler o binding físico correspondente em `workspace/businesses/{slug}/`.

Extrair:

- Domínios ativos e providers declarados.
- Preferências de comunicação e idioma.

### Fase 3: Carregar contexto do workspace 5-layer

Ler, se existirem:

- `workspace/{spoke}/L0-identity/company-dna.yaml`
- `workspace/{spoke}/L0-identity/founder-dna.yaml`
- `workspace/{spoke}/L0-identity/credentials.yaml`
- `workspace/{spoke}/L1-strategy/icp.yaml`
- `workspace/{spoke}/L1-strategy/offerbook.yaml`
- `workspace/{spoke}/L1-strategy/pricing-strategy.yaml`
- `workspace/{spoke}/L1-strategy/team-structure.yaml`
- `workspace/{spoke}/L2-tactical/brand/brandbook.yaml`
- `workspace/{spoke}/L2-tactical/brand/domain-decision.yaml`
- `workspace/{spoke}/L2-tactical/movement/` (quando existir)

Mapear:

- Campos críticos já preenchidos.
- Lacunas de dados que devem virar perguntas.
- Dependências para os próximos handoffs.

### Fase 4: Snapshot operacional

Registrar resumo em:

- `workspace/{spoke}/L4-operational/evidence/workspace-context-summary.yaml`
- fallback: resumo inline na resposta do COO.

No hub atual, o arquivo físico preferencial fica em `workspace/businesses/{slug}/L4-operational/evidence/workspace-context-summary.yaml`.

Contrato mínimo do snapshot:

```yaml
workspace_context:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  workspace_health: "pass|fail"
  existing_assets:
    L0-identity: []
    L1-strategy: []
    L2-tactical: []
    L3-product: []
    L4-operational: []
  missing_inputs: []
  handoff_readiness:
    vision-chief: "ready|blocked"
    cmo-architect: "ready|blocked"
    coo-orchestrator: "ready|blocked"
```

## Validação

- [ ] Scripts de preflight executados com sucesso.
- [ ] Contexto global carregado (`document-registry.yaml`, `.user/user.md`, `.aiox-core/core-config.yaml`).
- [ ] Contexto do workspace 5-layer mapeado.
- [ ] Snapshot de contexto produzido sem inventar campos.

## Fallback

Se algum arquivo obrigatório estiver ausente:

1. Reportar caminho exato.
2. Não inventar schema ou dados.
3. Sugerir rodar `*workspace-preflight` e depois retomar com `*workspace-context`.

---

*Task do Squad C-Level - COO Orchestrator*
