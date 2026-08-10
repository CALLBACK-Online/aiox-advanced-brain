---
task: optimizeAgent()
responsavel: "AgentArchitect"
responsavel_type: Agente
executor: agent-architect
atomic_layer: Molecule
Entrada:
  - nome: agent_file
    tipo: string
    obrigatorio: true
  - nome: audit_report
    tipo: string
    obrigatorio: false
Saida:
  - nome: agent_file_updated
    tipo: markdown
    obrigatorio: true
  - nome: optimization_report
    tipo: markdown
    obrigatorio: true
Checklist:
  - Audit report disponivel ou executar audit primeiro
  - Agent file atualizado com otimizacoes
  - Autonomy score melhorou
  - Changelog atualizado
  - Re-validacao executada
---


## Contrato AIOX

Domain: `Tactical`
atomic_layer: Molecule
Input: agent_file_path, target_metrics, optimization_goal
Output: optimized_agent_file, optimization_report, agent-optimization-plan
Pre-condition: baseline do agente conhecida e meta de melhoria definida
Post-condition: otimizações aplicadas com changelog, before/after e próxima revisão
Performance: só aplicar otimização validada ou experimental rastreável e medir delta final

## METADATA
- **Executor:** agent-architect (Agent)
- **Elicit:** true
# Task: Optimize Agent

## Metadata

- **id**: AA-T004
- **name**: optimize-agent
- **primary_agent**: agent-architect
- **secondary**: reasoning-engineer
- **trigger**: `*optimize <agent-id>`
- **inputs**: agent file + audit report (opcional)
- **outputs**: agent file atualizado + optimization report

## Description

Otimizar um agente existente para aumentar seu nível de autonomia. Parte de um audit report (se disponível) ou executa audit primeiro. Foca nas áreas com maior impacto no score de autonomia.

## Pre-conditions

- [ ] Agent file existe
- [ ] Audit report disponível OU executar `*audit` primeiro

## Steps

### Step 1: Assess Current State

Se não há audit report:

- Executar task `audit-agent` primeiro
- Coletar scores dos 3 pilares + failure modes

Se há audit report:

- Ler report e extrair scores e recomendações

### Step 2: Identify Optimization Targets

Priorizar por impacto (peso × gap):

```text
Impact Score = (peso do pilar) × (10 - score atual)
```

| Critério | Peso | Score Atual | Gap | Impact |
|----------|------|-------------|-----|--------|
| P1 | 0.35 | ? | ? | ? |
| P2 | 0.35 | ? | ? | ? |
| P3 | 0.35 | ? | ? | ? |
| M1 | 0.30 | ? | ? | ? |
| M2 | 0.30 | ? | ? | ? |
| M3 | 0.30 | ? | ? | ? |
| T1 | 0.35 | ? | ? | ? |
| T2 | 0.35 | ? | ? | ? |
| T3 | 0.35 | ? | ? | ? |

Focar nos **top 3 por impact score**.

### Step 3: Validate Optimization Candidates (Pesquisa Externa — BLOCKING)

**GATE OBRIGATÓRIO** — Nenhuma otimização pode ser aplicada sem este step.

Para cada target identificado no Step 2, ANTES de aplicar qualquer técnica:

#### 3a. Pesquisar evidência da técnica candidata

Usar Exa (`mcp__exa__web_search_exa`) para cada otimização planejada:

```text
Query: "[técnica] [tipo do agente] AI agent improvement evidence"
Exemplo: "compaction context window agent performance improvement evidence"
```

Min 2 queries por otimização candidata.

#### 3b. Teste de compatibilidade (3 perguntas)

| Pergunta | Se NÃO |
|----------|-----------------------|
| Existe evidência empírica de que esta técnica melhora agentes na prática? | Rebaixar para "experimental" |
| O tipo de agente (criativo/código/pipeline) é compatível com a técnica? | Descartar — não se aplica |
| É possível medir antes/depois objetivamente? | Marcar como "não mensurável" |

#### 3c. Classificar cada otimização

| Classificação | Critério | Ação |
|---------------|----------|------|
| **Validada** | Evidência + compatível + mensurável | Aplicar no Step 4 |
| **Experimental** | Lógica sólida mas sem evidência direta | Aplicar com flag "experimental" no changelog |
| **Descartada** | Sem evidência ou incompatível com tipo de agente | NÃO aplicar |

#### 3d. Pesquisar alternativas reais

```text
Query: "what actually improves [agent type] agents [problem area]"
```

Se a pesquisa revelar técnicas melhores que as da tabela abaixo, substituir.

#### 3e. Tabela de técnicas candidatas (referência, NÃO prescrição)

As técnicas abaixo são ponto de partida — SEMPRE validar via 3a-3d antes de aplicar.

**Planning**

| Critério | Técnica candidata |
|----------|-------------------|
| P1 — Task Decomposition | Instruções de decomposição no prompt |
| P2 — Self-Reflection | Checkpoint de auto-avaliação |
| P3 — Goal Persistence | Goal re-injection a cada N steps |

**Memory**

| Critério | Técnica candidata |
|----------|-------------------|
| M1 — Working Memory | Compaction + just-in-time retrieval |
| M2 — Long-Term Memory | Persistência (files, memory dir) |
| M3 — Cross-Agent Memory | Handoff protocol com artifact |

**Tool Use**

| Critério | Técnica candidata |
|----------|-------------------|
| T1 — Tool Coverage | Tools faltantes (scout → smith) |
| T2 — Tool Quality | Refatorar tools para ACI compliance |
| T3 — Error Recovery | Retry logic + fallback tools |

### Step 4: Apply Validated Optimizations

Aplicar APENAS otimizações classificadas como **Validada** ou **Experimental**.

Para cada otimização aplicada, registrar:

- Fonte da evidência (link)
- Classificação (validada/experimental)
- Métrica de sucesso esperada (como medir se funcionou)

### Step 5: Update Agent File

Editar o `.md` do agente incorporando as otimizações.

Manter histórico de versão no agent file:

```yaml
version: "{{next_version}}"  # incrementar minor para otimizações
changelog:
  - "{{next_version}}: {{optimization_summary}}"
```

### Step 6: Re-validate

Rodar autonomy-checklist novamente no agente otimizado.

Comparar scores antes/depois:

```text
## Optimization Results

| Critério | Antes | Depois | Delta |
|----------|-------|--------|-------|
| P1 | 5 | 8 | +3 |
| Overall | 45/90 | 62/90 | +17 |
| Level | L2 | L3 | +1 |
```

### Step 7: Deliver

- Agent file atualizado
- Optimization report com antes/depois
- Classificação de cada otimização aplicada (validada/experimental) com fontes
- Lista de otimizações descartadas (transparência)
- Recomendações para próxima iteração (se nível alvo não atingido)

## Post-conditions

- [ ] Pesquisa externa executada (min 2 queries por otimização candidata)
- [ ] Cada otimização classificada como Validada/Experimental/Descartada
- [ ] Agent file atualizado APENAS com otimizações validadas/experimentais
- [ ] Fontes documentadas para cada otimização aplicada
- [ ] Score de autonomia melhorou (ou justificativa se não melhorou)
- [ ] Changelog atualizado no agent file (com classificação)
- [ ] Re-validação executada

## Quality Gate

- **QG-003**: Architecture Review + Evidence Gate
- Critério: otimizações têm evidência documentada, pesquisa externa realizada


Completion Criteria: output validado com evidência, responsável definido e pronto para handoff
