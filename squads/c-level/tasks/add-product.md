# Task: Add Product

task_id: add-product
```yaml
task:
  task_id: add-product
  id: add-product
  name: Adicionar Novo Produto
  agent: cmo-architect
  responsavel_type: Clone
  elicit: true
  accountability_token: TK-CL-008
  executor_validacao: Human
```
## SINKRA Contract

Domain: Strategic
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- outputs/add-product.md
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

O CMO (Market Architect) conduz elicitação para adicionar um novo produto ao workspace, com posicionamento e configuração próprios.

## Pré-requisito

- Workspace configurado (setup-workspace executado)

## Workflow

### Fase 1: Identificação do Produto

```yaml
elicitation:
  questions:
    - id: business_slug
      text: "Qual BU dona do produto? (ex.: lendaria, aiox)"
      required: true

    - id: product_name
      text: "Qual é o nome do produto?"
      required: true

    - id: product_type
      text: "Qual tipo de produto? (SaaS, curso, serviço, físico)"
      required: true

    - id: product_stage
      text: "Em qual estágio está? (ideia, desenvolvimento, lançamento, crescimento)"
      required: true
```

### Fase 2: Posicionamento

```yaml
elicitation:
  questions:
    - id: product_icp
      text: "O ICP deste produto é o mesmo da empresa ou diferente?"
      required: true

    - id: product_value_prop
      text: "Qual é a proposta de valor específica deste produto?"
      required: true

    - id: product_price
      text: "Qual é o modelo de precificação? (one-time, subscription, freemium)"
      required: true

    - id: product_competitors
      text: "Quais são os principais concorrentes deste produto?"
      required: false
```

### Fase 3: Configuração Técnica

```yaml
elicitation:
  questions:
    - id: product_stack
      text: "O stack é o mesmo da empresa ou diferente?"
      required: true

    - id: product_integrations
      text: "Quais integrações este produto precisa?"
      required: false
```

### Fase 4: Output

Criar estrutura em `workspace/{spoke}/L3-product/{product_slug}/`:

**workspace/{spoke}/L3-product/{product_slug}/product-profile.yaml:**
```yaml
metadata:
  product_slug: "{product_slug}"
  business_slug: "{business_slug}"
  generated_by: "squad-c-level-cmo"
  generated_at: "{date}"

overview:
  product_name: "{product_name}"
  product_type: "{product_type}"
  product_stage: "{product_stage}"
  pricing_model: "{product_price}"

positioning:
  icp_scope: "{product_icp}"
  value_proposition: "{product_value_prop}"
  competitors:
    - "{product_competitors}"

technical:
  stack_scope: "{product_stack}"
  integrations:
    - "{product_integrations}"
```

**workspace/{spoke}/L3-product/{product_slug}/positioning.yaml:**
```yaml
metadata:
  product_slug: "{product_slug}"
  business_slug: "{business_slug}"
  generated_by: "squad-c-level-cmo"
  generated_at: "{date}"

positioning:
  value_proposition: "{product_value_prop}"
  icp_details: "{product_icp_details}"
  differentiation: "{diferenciacao_baseada_em_concorrentes}"
  messaging:
    headline: "{headline_sugerida}"
    subheadline: "{subheadline_sugerida}"
```

## Validação

- [ ] Diretório do produto criado
- [ ] `product-profile.yaml` gerado
- [ ] `positioning.yaml` gerado
- [ ] Atualizar `.aiox-core/core-config.yaml` com novo produto
