# Task: Bootstrap

task_id: bootstrap
```yaml
task:
  task_id: bootstrap
  id: bootstrap
  name: Bootstrap do Workspace
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: true
  required: true
  order: 1
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace/_system/config.yaml
- squads/c-level/config.yaml
Output:
- .user/user.md
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

Primeira task obrigatória do Squad C-Level. Garante que a estrutura base do `workspace/{spoke}` está pronta para uso, com templates canônicos e scripts de governança.
No Sinkra Hub atual, esse spoke é materializado sob `workspace/businesses/{slug}/L0-identity` ... `L4-operational`.

**IMPORTANTE:** Esta task deve ser executada ANTES de qualquer outra task do squad.

## Workflow

### Fase 1: Verificar bootstrap do workspace

```bash
bash squads/c-level/scripts/bootstrap-c-level-workspace.sh
bash squads/c-level/scripts/validate-c-level-essentials.sh
```

Se a validação falhar, o COO deve reportar exatamente quais paths canônicos ainda faltam.

### Fase 2: Confirmar essenciais do workspace

Validar a existência destes ativos:

- `workspace/_system/config.yaml`
- `workspace/businesses/`
- `workspace/_templates/business-template/`
- `workspace/scripts/scaffold-workspace.js`
- `workspace/scripts/resolve-squad-workspace-readiness.cjs`
- `squads/c-level/config.yaml`

### Fase 3: Output

Registrar um resumo com:

- diretórios criados pelo bootstrap
- warnings de essenciais ausentes
- status geral do preflight (`pass` ou `fail`)

## Estrutura Final

```
.user/
└── user.md                          # Perfil do usuário
.aiox-core/
└── core-config.yaml                 # Configuração do workspace
workspace/
└── {spoke}/
    ├── document-registry.yaml       # Registro de documentos
    ├── L0-identity/                 # TTL: 365d
    ├── L1-strategy/                 # TTL: 90d
    ├── L2-tactical/                 # TTL: 60d
    ├── L3-product/                  # TTL: 30d
    └── L4-operational/              # TTL: 7d
```

No Sinkra Hub atual, o bootstrap também valida:

- `workspace/_system/config.yaml`
- `workspace/businesses/`
- `workspace/_templates/business-template/`
- `workspace/scripts/`

## Validação

- [ ] `bootstrap-c-level-workspace.sh` executou sem erro
- [ ] `validate-c-level-essentials.sh` passou
- [ ] `workspace/_system/config.yaml` existe
- [ ] `workspace/businesses/` existe
- [ ] `workspace/_templates/business-template/` existe
- [ ] O contrato canônico `workspace/{spoke}` permanece preservado na documentação e no uso do squad

## Próximos Passos

Após bootstrap, sugerir:
1. `*add-business {slug}` - Instanciar um business com 5 layers
2. `*workspace-context {slug}` - Carregar snapshot antes dos handoffs
3. `*setup-business-profile {slug}` - Pipeline completo de perfil

---

*Task do Squad C-Level - COO Orchestrator*
