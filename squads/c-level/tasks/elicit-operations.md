# Task: Elicit Operations

task_id: elicit-operations
```yaml
task:
  task_id: elicit-operations
  id: elicit-operations
  name: Elicitação de Estrutura Operacional
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: true
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Tactical
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace/{spoke}/L0-identity/core-processes.yaml
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

O COO (Operations Orchestrator) conduz elicitação para definir estrutura operacional, processos e configuração geral do workspace.

## Workflow

### Fase 1: Estrutura da Empresa

```yaml
elicitation:
  questions:
    - id: company_stage
      text: "Em qual estágio está a empresa? (ideia, MVP, growth, scale)"
      required: true

    - id: team_size
      text: "Qual o tamanho atual do time?"
      required: true

    - id: departments
      text: "Quais áreas/departamentos existem?"
      required: true
```

### Fase 2: Produtos

```yaml
elicitation:
  questions:
    - id: products
      text: "Quais produtos a empresa oferece? (liste todos)"
      required: true

    - id: main_product
      text: "Qual é o produto principal/carro-chefe?"
      required: true

    - id: product_stage
      text: "Em qual estágio cada produto está?"
      required: false
```

### Fase 3: Processos

```yaml
elicitation:
  questions:
    - id: workflows
      text: "Quais são os principais workflows da empresa?"
      required: true

    - id: tools
      text: "Quais ferramentas vocês usam? (Notion, Slack, etc)"
      required: false

    - id: cadence
      text: "Qual a cadência de reuniões/rituais?"
      required: false
```

### Fase 4: Output

**.aiox-core/core-config.yaml:**
```markdown
# Configuração do Workspace

## Empresa

- **Estágio:** {company_stage}
- **Tamanho do Time:** {team_size}
- **Áreas:** {departments}

## Produtos

### Principal
{main_product}

### Todos os Produtos
{products}

### Estágios
{product_stage}

## Operações

### Workflows Principais
{workflows}

### Ferramentas
{tools}

### Cadência
{cadence}

---

*Gerado via Squad C-Level (COO) em {date}*
```

## Validação

- [ ] Estrutura da empresa documentada
- [ ] Produtos listados
- [ ] Processos identificados
- [ ] Arquivo salvo em `.aiox-core/core-config.yaml`
