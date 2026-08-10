# Task: Elicit Tech Strategy

task_id: elicit-tech-strategy
```yaml
task:
  task_id: elicit-tech-strategy
  id: elicit-tech-strategy
  name: Elicitação de Estratégia Tecnológica
  agent: cto-architect
  responsavel_type: Agent
  elicit: true
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Strategic
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- tech-strategy.md
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

O CTO (Tech Architect) conduz elicitação para definir estratégia tecnológica de alto nível, arquitetura e roadmap técnico.

## Workflow

### Fase 1: Contexto do Produto

```yaml
elicitation:
  questions:
    - id: product_core
      text: "Qual é o core do seu produto? (web app, mobile, API, SaaS, etc)"
      required: true

    - id: scale
      text: "Qual escala você precisa suportar? (usuários, requests, volume de dados)"
      required: true

    - id: constraints
      text: "Quais são suas restrições técnicas? (budget, prazo, tamanho do time)"
      required: true
```

### Fase 2: Arquitetura

```yaml
elicitation:
  questions:
    - id: architecture
      text: "Qual arquitetura prefere? (monolito, microserviços, serverless, híbrido)"
      required: true

    - id: legacy
      text: "Existe stack legado que precisa integrar?"
      required: false

    - id: availability
      text: "Qual nível de disponibilidade você precisa? (99%, 99.9%, 99.99%)"
      required: true

    - id: security
      text: "Quais são os requisitos de segurança? (compliance, LGPD, SOC2, etc)"
      required: true
```

### Fase 3: Evolução

```yaml
elicitation:
  questions:
    - id: iteration_speed
      text: "Qual é a velocidade de iteração desejada? (deploys por dia/semana)"
      required: true

    - id: tech_bets
      text: "Quais tecnologias emergentes você considera adotar?"
      required: false

    - id: tech_avoid
      text: "Quais tecnologias você quer evitar e por quê?"
      required: false
```

### Fase 4: Output

Preencher `workspace/{spoke}/L1-strategy/tech-strategy.yaml` (a partir de `workspace/_templates/tech-strategy.yaml`):

```yaml
metadata:
  company_name: "{company_name}"
  product_name: "{product_name}"
  status: "COMPLETE"
  last_updated: "{iso_datetime}"
  owner: "CTO"

strategy_context:
  product_core: "{product_core}"
  current_scale:
    users: "{scale_users}"
    requests_per_day: "{scale_requests}"
    data_volume: "{scale_data}"
  key_constraints:
    budget: "{budget_constraint}"
    timeline: "{timeline_constraint}"
    team_capacity: "{team_constraint}"

platform_decisions:
  application_architecture: "{architecture}"
  integration_strategy: "{legacy_or_none}"

security_and_reliability:
  availability_target: "{availability}"
  compliance_requirements:
    - "{security_requirement_1}"

roadmap:
  now_0_3m:
    - "{roadmap_item_1}"
  next_3_6m:
    - "{roadmap_item_2}"
  later_6_12m:
    - "{roadmap_item_3}"

tradeoffs:
  accepted:
    - "{tech_bets}"
  rejected:
    - "{tech_avoid}"
```

## Validação

- [ ] Arquitetura definida
- [ ] Requisitos de escala claros
- [ ] Direção tecnológica documentada
- [ ] Arquivo salvo em `workspace/{spoke}/L1-strategy/tech-strategy.yaml`
