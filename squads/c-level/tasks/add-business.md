# Add Business

task_id: add-business
```yaml
task:
  task_id: add-business
  id: add-business
  name: Adicionar Novo Negócio
  agent: coo-orchestrator
  responsavel_type: Agent
  trigger: manual
  elicit: false
  commands:
  - '*add-business {slug}'
  accountability_token: TK-CL-008
```

> **Preserva a abstração canônica `workspace/{spoke}`.** No Sinkra Hub atual, esse spoke é materializado em `workspace/businesses/{slug}/L0-identity` ... `L4-operational` via scaffold determinístico do workspace.

## Description

Adiciona um novo negócio ao workspace com estrutura template-first.

## Prerequisites

- Bootstrap executado (`workspace/_system/config.yaml` e `workspace/scripts/scaffold-workspace.js` existem)

## Usage

```
*add-business {slug}
```

**Exemplo:**
```
*add-business lendario
*add-business synkra
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace/businesses/{slug}/document-registry.yaml
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

## Workflow

### 1. Validar Slug

- Deve ser snake_case: `meu_negocio`
- Sem caracteres especiais
- Único (não pode existir já)

### 2. Criar Estrutura do Negócio (5-layer)

```bash
node workspace/scripts/scaffold-workspace.js {slug}
```

### 3. Scaffold de Templates (obrigatorio)

O scaffold canônico já cria:

- diretórios `L0-identity` a `L4-operational`
- `document-registry.yaml`
- placeholders e templates base

Se precisar reforçar o baseline do squad, executar depois:

```bash
*scaffold-templates {slug}
```

### 4. Atualizar document-registry.yaml

Garantir que o novo negócio tenha `workspace/{spoke}/document-registry.yaml` válido.
No hub atual, isso corresponde a `workspace/businesses/{slug}/document-registry.yaml`.

### 5. Registrar Slug em workspace/_system/config.yaml

**OBRIGATÓRIO** — sem esta step o `load-workspace-context.md` não resolve o slug → physical path.

Adicionar entrada no array `businesses[]`:

```yaml
businesses:
  # ... entradas existentes
  - slug: {slug}
    path: workspace/businesses/{slug}/
    layers: [L0-identity, L1-strategy, L2-tactical, L3-product, L4-operational]
    created: "{YYYY-MM-DD}"
```

Validar:

```bash
npm run validate:yaml:changed
```

**Anti-pattern detectado em AIOXsquad/AIOX-enterprise#55:** scaffold físico sem registry update produz drift silencioso — o slug existe no filesystem mas é invisível para `load-workspace-context.md`.

## Outputs

| Arquivo | Descrição |
|---------|-----------|
| `workspace/{spoke}/` | Raiz do workspace do negócio |
| `workspace/{spoke}/L0-identity/` | Company DNA, founder DNA, credenciais |
| `workspace/{spoke}/L1-strategy/` | ICP, pricing, offerbook, estratégia |
| `workspace/{spoke}/L2-tactical/` | Brand, design, movement |
| `workspace/{spoke}/L3-product/` | Produtos |
| `workspace/{spoke}/L4-operational/` | Operação, conteúdo, evidências |

## Validation

- [ ] Slug é válido (snake_case)
- [ ] Negócio não existia
- [ ] Todos os diretórios criados
- [ ] `document-registry.yaml` criado e parseável
- [ ] Templates base presentes no namespace do business

## Next Steps

Após criar o negócio:
1. `*workspace-context {slug}` - Snapshot operacional antes dos handoffs
2. `*setup-business-profile {slug}` - Pipeline completo de perfil
3. Ou individualmente: `*elicit-vision`, `*elicit-icp`, etc.
4. `*setup-workspace` para setup técnico (Sistema A)

---

*Task do Squad C-Level - COO Orchestrator*
