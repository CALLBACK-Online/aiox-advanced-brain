# Task: Elicit Product Portfolio

task_id: elicit-product-portfolio
```yaml
task:
  task_id: elicit-product-portfolio
  id: elicit-product-portfolio
  name: Elicitação de Portfólio de Produtos
  agent: cmo-architect
  responsavel_type: Clone
  co_agent: coo-orchestrator
  elicit: true
  output_format: yaml
  target: workspace/{spoke}/L1-strategy/product-portfolio.yaml
  registry_id: L1-012
  accountability_token: TK-CL-008
  executor_validacao: Human
```
## SINKRA Contract

Domain: Tactical
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace/{spoke}/L3-product/product-portfolio.yaml
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

O CMO Architect (com apoio do COO Orchestrator) conduz elicitação para documentar o portfólio completo de produtos {spoke_name} — catálogo centralizado com lifecycle, módulos de produção, BUs envolvidas, estágio de validação e pricing de referência.

Este documento é **pré-requisito** para:
- Criação do product-squad (se aprovado)
- Calculadora de precificação com bônus embutido
- Proposta de valores no proposal-generator
- Atribuição de receita por produto no bonus-squad

## Pré-requisitos

- Workspace configurado (bootstrap executado)
- `L1-004 offerbook.yaml` — POPULATED (fonte de offers atuais)
- `L1-005 pricing-strategy.yaml` — POPULATED (fonte de pricing)
- `L1-010 bu-map.yaml` — POPULATED (mapeamento de BUs)

## Contexto Carregado Antes da Elicitação

```yaml
context_files:
  - workspace/{spoke}/L1-strategy/offerbook.yaml        # Offers existentes
  - workspace/{spoke}/L1-strategy/pricing-strategy.yaml  # Pricing atual
  - workspace/{spoke}/L1-strategy/bu-map.yaml            # BUs e squads
  - workspace/{spoke}/L0-identity/core-processes.yaml    # Processos por produto
  - workspace/{spoke}/L1-strategy/bonus-model.yaml       # Modelo de bônus (custos, rates)
```

## Workflow

### Fase 0: Inventário Automático

Antes de elicitar, o agente DEVE:

1. Ler `offerbook.yaml` e extrair todos os produtos/offers existentes
2. Ler `L3-product/` e listar instâncias já criadas
3. Ler `core-processes.yaml` e mapear processos por produto
4. Apresentar ao CEO: "Encontrei N produtos implícitos no workspace. Vou confirmar cada um."

### Fase 1: Catálogo de Produtos (por produto encontrado + novos)

Para CADA produto, elicitar:

```yaml
elicitation:
  phase: 1
  name: "Catálogo de Produtos"
  repeat_per_product: true
  questions:
    - id: product_slug
      text: "Qual o slug canonico deste produto? (ex.: product-a, product-b, saas-core)"
      required: true
      maps_to: products[].slug

    - id: product_name
      text: "Nome oficial do produto?"
      required: true
      maps_to: products[].name

    - id: product_type
      text: "Tipo? (service, saas, hybrid, course, physical)"
      required: true
      maps_to: products[].type
      options: [service, saas, hybrid, course, physical]

    - id: product_stage
      text: "Estágio atual? (ideation, beta, launched, validated, mature, sunset)"
      required: true
      maps_to: products[].stage
      options: [ideation, beta, launched, validated, mature, sunset]
      note: "'validated' = produto com receita recorrente provada. 'launched' = no mercado mas sem validação."

    - id: product_revenue_2025
      text: "Receita anual deste produto (2025 ou projeção)?"
      required: false
      maps_to: products[].revenue_annual

    - id: product_revenue_share
      text: "% do faturamento total da empresa que este produto representa?"
      required: false
      maps_to: products[].revenue_share_pct

    - id: product_owner_bu
      text: "Qual BU é dona deste produto? (referência: bu-map.yaml)"
      required: true
      maps_to: products[].owner_bu

    - id: product_owner_person
      text: "Quem é o responsável direto (head/lead) por este produto?"
      required: true
      maps_to: products[].owner_person
```

### Fase 2: Variantes e Tiers (por produto)

```yaml
elicitation:
  phase: 2
  name: "Variantes e Tiers"
  repeat_per_product: true
  condition: "product_type != 'physical'"
  questions:
    - id: has_tiers
      text: "Este produto tem tiers/variantes? (sim/não)"
      required: true

    - id: tiers
      text: "Liste os tiers com nome e preço de referência (ex.: ENTRY R$5K, CORE R$17K, PREMIUM R$80K)"
      required: true
      condition: "has_tiers == sim"
      maps_to: products[].variants[]

    - id: tier_differentiator
      text: "O que diferencia um tier do outro? (escopo, módulos, SLA, volume)"
      required: true
      condition: "has_tiers == sim"
      maps_to: products[].tier_logic
```

### Fase 3: Módulos de Produção (por produto)

```yaml
elicitation:
  phase: 3
  name: "Módulos de Produção"
  repeat_per_product: true
  questions:
    - id: production_modules
      text: |
        Quais módulos de produção são ativados para entregar este produto?
        (ex.: casting, roteiro, gravação, edição, motion, color grading,
        sound design, legendagem, thumbnail, etc.)
      required: true
      maps_to: products[].modules[]

    - id: module_costs
      text: |
        Para cada módulo listado, qual o custo médio estimado?
        (ex.: casting R$2K, edição R$3K, motion R$4K)
        Se não souber exato, estimativa está OK.
      required: false
      maps_to: products[].modules[].cost_estimate

    - id: bus_involved
      text: |
        Quais BUs participam da entrega deste produto?
        (ex.: bu-producao faz edição, bu-comercial faz proposta, bu-growth faz mídia)
      required: true
      maps_to: products[].bus_involved[]

    - id: sla_days
      text: "Qual o SLA de entrega em dias úteis?"
      required: true
      maps_to: products[].sla_days
```

### Fase 4: Validação e Cases

```yaml
elicitation:
  phase: 4
  name: "Validação e Cases"
  repeat_per_product: true
  questions:
    - id: validation_status
      text: "Este produto está validado pelo mercado? (validated, hypothesis, deprecated)"
      required: true
      maps_to: products[].validation.status
      options: [validated, hypothesis, deprecated]

    - id: validation_evidence
      text: |
        Se validado: qual a evidência? (ex.: "880 projetos entregues, 200+ marcas",
        "R$4.27M receita anual", "NPS 72")
      required: false
      condition: "validation_status == validated"
      maps_to: products[].validation.evidence

    - id: cases
      text: "Liste 1-3 cases de sucesso deste produto (cliente + resultado)"
      required: false
      maps_to: products[].validation.cases[]

    - id: known_risks
      text: "Quais os riscos conhecidos deste produto? (margem, dependência, mercado)"
      required: false
      maps_to: products[].validation.risks[]
```

### Fase 5: Estratégia de Portfólio (consolidada)

```yaml
elicitation:
  phase: 5
  name: "Estratégia de Portfólio"
  questions:
    - id: portfolio_strategy
      text: |
        Qual a estratégia de portfólio? Como os produtos se relacionam?
        (ex.: {business_type} é cash cow, MaaS é growth bet, ACS é extensão de valor)
      required: true
      maps_to: portfolio.strategy

    - id: cross_sell
      text: "Existe cross-sell entre produtos? (ex.: cliente {business_type} → upsell MaaS)"
      required: false
      maps_to: portfolio.cross_sell[]

    - id: retirement_policy
      text: "Quando um produto é aposentado (sunset)? Critérios?"
      required: false
      maps_to: portfolio.retirement_policy

    - id: new_product_process
      text: |
        Como nasce um novo produto hoje? Quem decide, como valida, como precifica?
        (descreva o processo atual, mesmo que informal)
      required: true
      maps_to: portfolio.new_product_process

    - id: margin_target
      text: |
        Qual a margem mínima aceitável por produto?
        (ex.: "mínimo 40% MC bruta" ou "depende do tier")
      required: true
      maps_to: portfolio.margin_target
```

### Fase 6: Síntese e Output

1. **Consolidar respostas** num YAML estruturado
2. **Cruzar com offerbook.yaml** — validar que nenhum produto foi esquecido
3. **Cruzar com bonus-model.yaml** — vincular custos fixos e rates
4. **Gerar `product-portfolio.yaml`** em `workspace/{spoke}/L1-strategy/`
5. **Registrar no document-registry.yaml** como L1-012
6. **Calcular completude** por produto e geral

## Output Template

```yaml
# Product Portfolio — {spoke_name}
# Layer: L1-strategy
# State: POPULATED
# Owner: c-level (CMO + COO)
# TTL: 90 days
# Generated: {date}
# Task: elicit-product-portfolio

version: "1.0.0"
layer: L1-strategy
state: POPULATED
lastModified: "{date}"

# ─── CATÁLOGO DE PRODUTOS ────────────────────────────────────────────

products:
  - slug: "{product_slug}"
    name: "{product_name}"
    type: "{service|saas|hybrid|course|physical}"
    stage: "{ideation|beta|launched|validated|mature|sunset}"
    owner:
      bu: "{bu_id}"
      person: "{nome}"
    revenue:
      annual: "{R$X}"
      share_pct: "{X%}"
    variants:
      - name: "{tier_name}"
        price: "{R$X}"
        modules: ["{mod1}", "{mod2}"]
    tier_logic: "{o que diferencia tiers}"
    modules:
      - name: "{module_name}"
        cost_estimate: "{R$X}"
        bu_responsible: "{bu_id}"
    bus_involved: ["{bu_id_1}", "{bu_id_2}"]
    sla_days: "{N}"
    validation:
      status: "{validated|hypothesis|deprecated}"
      evidence: "{evidência}"
      cases:
        - client: "{nome}"
          result: "{resultado}"
      risks:
        - "{risco}"

# ─── ESTRATÉGIA DE PORTFÓLIO ─────────────────────────────────────────

portfolio:
  strategy: "{como produtos se relacionam}"
  cross_sell:
    - from: "{product_slug}"
      to: "{product_slug}"
      trigger: "{quando cross-sell acontece}"
  retirement_policy: "{critérios de sunset}"
  new_product_process: "{como nasce um produto novo}"
  margin_target: "{margem mínima aceitável}"

# ─── MÉTRICAS DE PORTFÓLIO ───────────────────────────────────────────

metrics:
  total_products: "{N}"
  validated: "{N}"
  hypothesis: "{N}"
  deprecated: "{N}"
  total_revenue: "{R$X}"
  avg_margin: "{X%}"

# ─── DEPENDÊNCIAS ────────────────────────────────────────────────────

dependencies:
  upstream:
    - "L0-001: company-dna.yaml (missão, valores)"
    - "L0-004: core-processes.yaml (processos por produto)"
  downstream:
    - "L1-004: offerbook.yaml (offers derivam de produtos)"
    - "L1-005: pricing-strategy.yaml (pricing por produto)"
    - "L1-009: bonus-model.yaml (custo-bônus por margem)"
    - "L3-product/{slug}/ (instâncias por produto)"
  consumers:
    - "bonus-squad: parâmetros de custo para simulação"
    - "proposal-generator: catálogo + preços para proposta de valores"
    - "product-squad (futuro): gestão operacional do catálogo"
```

## Validação

- [ ] Todos os produtos do offerbook.yaml estão no catálogo
- [ ] Cada produto tem slug, nome, tipo, estágio e owner
- [ ] Produtos validados têm evidência documentada
- [ ] Módulos de produção listados com custo estimado (mesmo que aproximado)
- [ ] BUs envolvidas por produto mapeadas
- [ ] Estratégia de portfólio documentada (cross-sell, retirement, margin target)
- [ ] Margem meta definida (input para calculadora de precificação futura)
- [ ] Registrado no document-registry.yaml como L1-012
- [ ] YAML válido salvo em `workspace/{spoke}/L1-strategy/product-portfolio.yaml`

## Veto Conditions

- **VETO_NO_OFFERBOOK:** Se `offerbook.yaml` não está POPULATED → BLOQUEIA. Sem offers, não há produtos pra catalogar.
- **VETO_DUPLICATE_SLUG:** Se dois produtos têm o mesmo slug → BLOQUEIA. Slugs devem ser únicos.
- **VETO_NO_OWNER:** Produto sem owner (BU + pessoa) → BLOQUEIA. Sem dono, produto é órfão.

## Completion Criteria

- Portfolio com mínimo 3 produtos documentados ({business_type}, MaaS, ACS são conhecidos)
- Cada produto com estágio de validação declarado
- Estratégia de portfólio consolidada
- Document-registry atualizado

## Next Steps

Após product-portfolio preenchido:
1. Criar `product-taxonomy.yaml` (L1-013) — se necessário após avaliar se a taxonomia precisa de doc separado ou vive dentro do portfolio
2. Atualizar `entity-architecture.yaml` (L1-011) — incluir Product como entidade
3. Avaliar criação do product-squad com base nos dados coletados
4. Implementar calculadora de precificação usando módulos e custos do catálogo

---

*Task do Squad C-Level — CMO Architect + COO Orchestrator*
*Criada: 2026-03-24*
*Contexto: Round Table Product Squad Gap Analysis*
