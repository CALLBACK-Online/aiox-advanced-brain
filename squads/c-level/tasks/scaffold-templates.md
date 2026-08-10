# Task: Scaffold Templates

task_id: scaffold-templates
```yaml
task:
  task_id: scaffold-templates
  id: scaffold-templates
  name: Scaffold Templates YAML para Workspace 5-Layer
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: false
  output_format: yaml
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace/{spoke}/L0-L4 placeholders
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

Copia os templates YAML de `workspace/_templates/` para o workspace 5-layer, criando a estrutura completa para preenchimento via pipeline de elicitação.

## Prerequisites

- Bootstrap executado (`.user/user.md` existe)
- Workspace criado (`workspace/{spoke}/` existe)
- Preflight workspace-first executado com sucesso:
  - `bash squads/c-level/scripts/bootstrap-c-level-workspace.sh`
  - `bash squads/c-level/scripts/validate-c-level-essentials.sh`

## Usage

```
*scaffold-templates
```

## Workflow

### Fase 0: Validação

1. Verificar se `workspace/{spoke}/` existe. Se não, abortar com mensagem: "Workspace não encontrado. Execute `*bootstrap` primeiro."
2. Verificar se templates já foram scaffolded (existência de `L0-identity/founder-dna.yaml`):
   - **Se existe:** Perguntar se deseja sobrescrever ou manter existentes.
   - **Se não existe:** Prosseguir com scaffold completo.

### Fase 1: Criar Diretórios

```bash
mkdir -p workspace/{spoke}/L0-identity
mkdir -p workspace/{spoke}/L1-strategy
mkdir -p workspace/{spoke}/L2-tactical/brand
mkdir -p workspace/{spoke}/L3-product
mkdir -p workspace/{spoke}/L4-operational
mkdir -p workspace/{spoke}/L4-operational/evidence
```

### Fase 2: Copiar Templates L0-identity

Copiar os seguintes templates de `workspace/_templates/` para `workspace/{spoke}/L0-identity/`:

| Template Source | Target | Método |
|----------------|--------|--------|
| `company-dna.yaml` | `L0-identity/company-dna.yaml` | Cópia direta |
| `founder-dna.yaml` | `L0-identity/founder-dna.yaml` | Cópia direta |
| `credentials.yaml` | `L0-identity/credentials.yaml` | Cópia direta |
| `authority-story.yaml` | `L0-identity/authority-story.yaml` | Cópia direta (placeholder, sintetizado na Fase 6) |

### Fase 3: Copiar Templates L1-strategy

Copiar os seguintes templates de `workspace/_templates/` para `workspace/{spoke}/L1-strategy/`:

| Template Source | Target | Método |
|----------------|--------|--------|
| `icp.yaml` | `L1-strategy/icp.yaml` | Cópia direta |
| `diagnosis.yaml` | `L1-strategy/diagnosis.yaml` | Cópia direta |
| `pricing-strategy.yaml` | `L1-strategy/pricing-strategy.yaml` | Cópia direta |
| `tech-strategy.yaml` | `L1-strategy/tech-strategy.yaml` | Cópia direta |
| `tech-stack.yaml` | `L1-strategy/tech-stack.yaml` | Cópia direta |
| `ai-strategy.yaml` | `L1-strategy/ai-strategy.yaml` | Cópia direta |
| `analytics.yaml` | `L1-strategy/analytics.yaml` | Cópia direta (placeholder) |

### Fase 4: Copiar Templates L2-tactical, L4-operational e Evidence

Copiar os seguintes templates:

| Template Source | Target | Método |
|----------------|--------|--------|
| `brandbook.yaml` | `L2-tactical/brand/brandbook.yaml` | Cópia direta |
| `team-structure.yaml` | `L1-strategy/team-structure.yaml` | Cópia direta |
| `kpi-scorecards.yaml` | `L4-operational/kpi-scorecards.yaml` | Cópia direta (placeholder) |
| `commission-design.yaml` | `L4-operational/commission-design.yaml` | Cópia direta (placeholder) |
| `workspace-context-summary.yaml` | `L4-operational/evidence/workspace-context-summary.yaml` | Cópia direta |

### Fase 5: Atualizar Metadata

Para cada arquivo copiado, atualizar o campo `metadata.company_name` (ou equivalente) com o nome do negócio.

### Fase 6: Relatório

Gerar relatório de scaffold:

```
Scaffold completo para workspace {spoke}

L0-identity (4 arquivos):
  ✅ company-dna.yaml
  ✅ founder-dna.yaml
  ✅ credentials.yaml
  ✅ authority-story.yaml (placeholder)

L1-strategy (7 arquivos):
  ✅ icp.yaml
  ✅ diagnosis.yaml
  ✅ pricing-strategy.yaml
  ✅ tech-strategy.yaml
  ✅ tech-stack.yaml
  ✅ ai-strategy.yaml
  ✅ analytics.yaml (placeholder)

L2-tactical (1 arquivo):
  ✅ brand/brandbook.yaml

L4-operational + evidence (4 arquivos):
  ✅ team-structure.yaml
  ✅ kpi-scorecards.yaml (placeholder)
  ✅ commission-design.yaml (placeholder)
  ✅ L4-operational/evidence/workspace-context-summary.yaml

Total: 16 arquivos scaffolded
Próximo passo: *setup-business-profile
```

## Outputs

| Diretório | Arquivos | Status |
|-----------|----------|--------|
| `workspace/{spoke}/L0-identity/` | 4 YAMLs | Template (vazio) |
| `workspace/{spoke}/L1-strategy/` | 7 YAMLs | Template (vazio) |
| `workspace/{spoke}/L2-tactical/brand/` | 1 YAML | Template (vazio) |
| `workspace/{spoke}/L4-operational/` | 3 YAMLs | Template (vazio) |
| `workspace/{spoke}/L4-operational/evidence/` | 1 YAML | Template (vazio) |

## Validation

- [ ] Diretórios L0-identity/, L1-strategy/, L2-tactical/, L4-operational/ e evidence/ existem
- [ ] 4 arquivos em L0-identity/ copiados
- [ ] 7 arquivos em L1-strategy/ copiados
- [ ] 1 arquivo em L2-tactical/brand/ copiado
- [ ] 4 arquivos em L4-operational/+evidence copiados
- [ ] Metadata atualizado com nome do negócio
- [ ] Nenhum arquivo existente sobrescrito sem confirmação

## Next Steps

Após scaffold:
1. `*setup-business-profile` - Pipeline completo de elicitação
2. Ou executar tasks individuais: `*elicit-founder-dna`, `*elicit-company-profile`, etc.

---

*Task do Squad C-Level - COO Orchestrator*
