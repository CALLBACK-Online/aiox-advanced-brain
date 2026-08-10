# Task: Elicit ICP

task_id: elicit-icp
```yaml
task:
  task_id: elicit-icp
  id: elicit-icp
  name: Elicitação de ICP e Proposta de Valor
  agent: cmo-architect
  responsavel_type: Clone
  elicit: true
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
- icp-brief.md
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

O CMO (Market Architect) conduz elicitação profunda para definir ICP (Ideal Customer Profile), proposta de valor, brand e messaging.

## Workflow

### Fase 0: Contexto do Workspace

Antes de iniciar a elicitação:

1. Ler `workspace/{spoke}/L0-identity/company-dna.yaml` (se existir) para alinhar ICP com missão/visão.
2. Ler `workspace/{spoke}/L1-strategy/icp.yaml` (se existir):
   - **Se existe:** Apresentar ICP atual e perguntar se deseja refinar ou substituir.
   - **Se não existe:** Prosseguir com elicitação completa.
3. Usar missão e valores da empresa (se disponíveis) para contextualizar perguntas — ex.: conectar "dores do cliente" com "problema que resolvemos".

### Fase 1: ICP (Ideal Customer Profile)

```yaml
elicitation:
  questions:
    - id: customer_profile
      text: "Quem é seu cliente ideal? (cargo, empresa, setor)"
      required: true

    - id: company_size
      text: "Qual o tamanho típico da empresa do seu cliente?"
      required: true

    - id: pain_points
      text: "Quais são as maiores dores do seu cliente?"
      required: true

    - id: buying_process
      text: "Como seu cliente toma decisão de compra?"
      required: true

    - id: channels
      text: "Onde seu cliente busca soluções?"
      required: true

    - id: budget
      text: "Qual o orçamento típico do seu cliente?"
      required: false

    - id: perfect_customer
      text: "O que faz um cliente ser 'perfeito' para você?"
      required: true
```

### Fase 2: Proposta de Valor

```yaml
elicitation:
  questions:
    - id: transformation
      text: "Qual transformação você entrega ao cliente?"
      required: true

    - id: differentiation
      text: "O que você faz que ninguém mais faz?"
      required: true

    - id: why_choose
      text: "Por que um cliente escolheria você sobre a concorrência?"
      required: true

    - id: results
      text: "Qual é o resultado tangível que o cliente obtém?"
      required: true

    - id: time_to_value
      text: "Em quanto tempo o cliente vê resultados?"
      required: false
```

### Fase 3: Brand (Opcional)

```yaml
elicitation:
  questions:
    - id: brand_personality
      text: "Se sua marca fosse uma pessoa, como ela seria?"
      required: false

    - id: brand_words
      text: "Quais 3 palavras definem sua marca?"
      required: false

    - id: tone_of_voice
      text: "Qual tom de voz sua marca usa?"
      required: false

    - id: brand_never
      text: "O que sua marca NUNCA faria?"
      required: false
```

### Fase 4: Output

Criar múltiplos arquivos:

**workspace/{spoke}/L1-strategy/icp.yaml:**
```markdown
# Ideal Customer Profile (ICP)

## Perfil Demográfico

- **Cargo:** {extraído de customer_profile}
- **Setor:** {extraído de customer_profile}
- **Tamanho da empresa:** {company_size}
- **Orçamento típico:** {budget}

## Perfil Psicográfico

### Dores Principais
{pain_points formatado como lista}

### Processo de Compra
{buying_process}

### Canais de Busca
{channels}

## Cliente Perfeito

{perfect_customer}

---

*Gerado via Squad C-Level (CMO) em {date}*
```

**workspace/{spoke}/L1-strategy/value-proposition.yaml:**
```markdown
# Proposta de Valor

## Transformação

{transformation}

## Diferenciação

{differentiation}

## Por que Nos Escolher

{why_choose}

## Resultados Tangíveis

{results}

## Time to Value

{time_to_value}

---

*Gerado via Squad C-Level (CMO) em {date}*
```

**workspace/{spoke}/L2-tactical/brand/brandbook.yaml** (se respondido):
```markdown
# Brand Guidelines

## Personalidade

{brand_personality}

## Palavras-Chave

1. {word_1}
2. {word_2}
3. {word_3}

## Tom de Voz

{tone_of_voice}

## O Que Nunca Fazemos

{brand_never}

---

*Gerado via Squad C-Level (CMO) em {date}*
```

## Validação

- [ ] ICP claramente definido
- [ ] Proposta de valor diferenciada
- [ ] Arquivos criados em `workspace/{spoke}/L1-strategy/` e `workspace/{spoke}/L2-tactical/brand/`
