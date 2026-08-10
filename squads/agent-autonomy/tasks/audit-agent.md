---
task: auditAgent()
responsavel: "AutonomyAuditor"
responsavel_type: Agente
executor: autonomy-auditor
atomic_layer: Molecule
Entrada:
  - nome: agent_file_path
    tipo: string
    obrigatorio: true
  - nome: agent_id
    tipo: string
    obrigatorio: true
Saida:
  - nome: audit_report
    tipo: markdown
    obrigatorio: true
Checklist:
  - Agent file existe e e legivel
  - Report gerado com todos os scores
  - Autonomy level L1-L5 classificado
  - Recomendacoes listadas com agente responsavel
---


## Contrato AIOX

Domain: `Operational`
atomic_layer: Molecule
Input: agent_file_path, agent_id, sintomas observados
Output: autonomy-audit-report, cross-domain-handoff
Pre-condition: agente alvo acessível e contexto mínimo do caso disponível
Post-condition: relatório auditado, failure modes classificados e handoff definido
Performance: executar min 3 queries de evidência e bloquear entrega sem score completo

## METADATA
- **Executor:** autonomy-auditor (Clone)
- **Elicit:** true
# Task: Audit Agent

## Metadata

- **id**: AA-T001
- **name**: audit-agent
- **primary_agent**: autonomy-auditor
- **trigger**: `*audit <agent-id>`
- **inputs**: agent file path (.md)
- **outputs**: audit report (.md)

## Description

Auditar um agente existente para avaliar seu nível de autonomia usando o framework dos 3 Pilares (Weng) + 4 Failure Modes + Níveis L1-L5.

## Pre-conditions

- [ ] Agent file existe e é legível
- [ ] Agent file contém definição completa (persona, commands, dependencies)

## Steps

### Step 1: Collect Agent Definition

```text
Ler o arquivo do agente completo.
Extrair: persona, commands, tools, dependencies, handoffs.
```

### Step 2: Evaluate 3 Pillars

Para cada pilar, avaliar 3 critérios (0-10):

**Planning (peso 0.35)**

| Critério | Pergunta | Score |
|----------|----------|-------|
| P1 — Task Decomposition | Agente consegue quebrar tarefas complexas em sub-tarefas? | /10 |
| P2 — Self-Reflection | Agente avalia sua própria performance e corrige erros? | /10 |
| P3 — Goal Persistence | Agente mantém foco no objetivo ao longo de múltiplos steps? | /10 |

**Memory (peso 0.30)**

| Critério | Pergunta | Score |
|----------|----------|-------|
| M1 — Working Memory | Agente gerencia eficientemente o context window? | /10 |
| M2 — Long-Term Memory | Agente persiste aprendizados entre sessões? | /10 |
| M3 — Cross-Agent Memory | Agente preserva contexto em handoffs? | /10 |

**Tool Use (peso 0.35)**

| Critério | Pergunta | Score |
|----------|----------|-------|
| T1 — Tool Coverage | Agente tem tools suficientes para suas tarefas? | /10 |
| T2 — Tool Quality (ACI) | Tools seguem os 5 princípios ACI? | /10 |
| T3 — Error Recovery | Agente lida com falhas de tools graciosamente? | /10 |

### Step 3: Detect Failure Modes

Para cada failure mode, verificar presença:

| FM | Nome | Sintoma a verificar |
|----|------|---------------------|
| FM-1 | Context Saturation | Quality degrada ao longo da conversa? |
| FM-2 | Tool Brittleness | Retry rate alto? Tool selection imprecisa? |
| FM-3 | Reasoning Drift | Steps irrelevantes? Tangentes? |
| FM-4 | Evaluator Absence | Agente sabe quando completou? |

### Step 4: Classify Autonomy Level

Com base nos scores, classificar L1-L5:

| Score Médio | Nível | Descrição |
|-------------|-------|-----------|
| 0-3 | L1 — Operator | Humano aprova cada ação |
| 4-5 | L2 — Collaborator | Humano edita outputs |
| 6-7 | L3 — Consultant | Agente executa por períodos |
| 8-9 | L4 — Approver | Humano só resolve blockers |
| 10 | L5 — Observer | Humano só monitora |

### Step 5: Devil's Advocate — Pesquisa Externa Obrigatória

**BLOCKING GATE** — Nenhuma recomendação pode ser emitida sem este step.

Antes de gerar recomendações, validar cada finding contra evidência externa.
Usar Exa (`mcp__exa__web_search_exa`) para pesquisar.

#### 5a. Para cada recomendação candidata, pesquisar:

```text
Query: "[recomendação] AI agent evidence impact"
Exemplo: "self-reflection loop AI agent practical improvement evidence"
Nota: Exa retorna resultados recentes por default. NÃO hardcodar anos na query.
```

#### 5b. Aplicar o teste de 3 perguntas a cada recomendação:

| Pergunta | Se a resposta for NÃO |
|----------|-----------------------|
| Existe evidência empírica (paper, benchmark, caso real) de que isso melhora agentes na prática? | Rebaixar para "teórico — sem evidência" |
| O tipo de agente auditado (criativo vs código vs pipeline) é compatível com a técnica? | Descartar — técnica não se aplica |
| É possível medir antes/depois de forma objetiva? | Marcar como "não mensurável — risco de cargo cult" |

#### 5c. Classificar cada recomendação:

| Classificação | Critério | Ação |
|---------------|----------|------|
| **Validada** | Evidência empírica + aplica ao tipo de agente + mensurável | Incluir no relatório como recomendação forte |
| **Plausível** | Lógica sólida mas sem evidência direta ou difícil de medir | Incluir com disclaimer "sem evidência direta" |
| **Descartada** | Sem evidência + não se aplica ao tipo OU cargo cult identificado | NÃO incluir no relatório |

#### 5d. Pesquisar o que REALMENTE importa para o tipo de agente:

```text
Query: "what actually improves [agent type] agents performance evidence"
Exemplo: "what actually improves architecture design AI agents performance"
```

Incorporar findings da pesquisa como recomendações adicionais se tiverem evidência forte.

#### 5e. Documentar fontes:

Cada recomendação validada DEVE ter pelo menos 1 fonte:

- Paper (arxiv, ICML, NeurIPS)
- Estudo empírico (Anthropic, METR, OpenAI)
- Case study publicado (blog técnico com dados)

Recomendações sem fonte = **Plausível** no máximo.

### Step 6: Generate Report

Usar template de report com:

- Executive Summary (1 parágrafo)
- Scores por pilar (tabela) — com disclaimer: "scores são avaliação qualitativa, não medição"
- Failure modes detectados
- Nível de autonomia classificado
- Recomendações priorizadas — APENAS validadas e plausíveis (com classificação visível)
- Seção "Fontes" — links das pesquisas que validaram/invalidaram recomendações
- Seção "Descartadas" — recomendações que pareciam boas mas foram invalidadas pela pesquisa (transparência)
- Agent para handoff (qual agente do squad deve atuar)

## Post-conditions

- [ ] Report gerado com todos os scores preenchidos
- [ ] Nível L1-L5 classificado
- [ ] Devil's advocate executado com pesquisa externa (Step 5)
- [ ] Cada recomendação classificada como Validada/Plausível/Descartada
- [ ] Seção "Fontes" com pelo menos 1 link por recomendação validada
- [ ] Seção "Descartadas" presente (mesmo que vazia)
- [ ] Handoff definido (se necessário)

## Quality Gate

- **QG-002**: Diagnosis Complete
- Critério: todos os 9 critérios avaliados, 4 FMs verificados, nível classificado, pesquisa externa realizada (min 3 queries Exa), recomendações validadas contra evidência

## Handoff

| Resultado | Próximo Agent |
|-----------|---------------|
| Falhas em P1-P3 | → reasoning-engineer |
| Falhas em M1-M3 | → agent-architect |
| Falhas em T1-T3 | → tool-smith |
| FM-1 a FM-4 detectados | → tasks/diagnose-autonomy-failure.md (AA-T003) |
| Redesign necessário | → agent-architect |


Completion Criteria: output validado com evidência, responsável definido e pronto para handoff
