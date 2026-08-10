---
task: diagnoseAutonomyFailure()
responsavel: "AutonomyAuditor"
responsavel_type: Agente
executor: autonomy-auditor
atomic_layer: Molecule
Entrada:
  - nome: agent_file_path
    tipo: string
    obrigatorio: true
  - nome: problem_description
    tipo: string
    obrigatorio: true
Saida:
  - nome: diagnosis_report
    tipo: markdown
    obrigatorio: true
Checklist:
  - Pelo menos 1 failure mode identificado
  - Root cause analysis completa (5 Whys)
  - Recomendacoes com agente responsavel
  - Handoff preparado
---


## Contrato AIOX

Domain: `Operational`
atomic_layer: Molecule
Input: agent_file_path, problem_description
Output: diagnosis_report, cross-domain-handoff
Pre-condition: sintoma observado descrito e agente alvo identificado
Post-condition: root cause validada, fixes classificados e responsável definido
Performance: documentar 5 whys completos e rejeitar fix sem evidência externa

## METADATA
- **Executor:** autonomy-auditor (Clone)
- **Elicit:** true
# Task: Diagnose Autonomy Failure

## Metadata

- **id**: AA-T003
- **name**: diagnose-autonomy-failure
- **primary_agent**: autonomy-auditor
- **trigger**: `*diagnose <agent-id>`
- **inputs**: agent file path + descrição do problema observado
- **outputs**: diagnosis report com root cause e fix recommendations

## Description

Diagnosticar por que um agente não está executando de forma autônoma. Identificar a causa raiz entre os 4 Failure Modes e os 3 Pilares, e recomendar ações corretivas específicas.

## Pre-conditions

- [ ] Agent file existe
- [ ] Problema observado descrito (ex: "agente fica pedindo confirmação", "agente perde contexto")

## Steps

### Step 1: Collect Symptoms

Perguntar ao usuário:

1. **O que o agente deveria fazer?** (objetivo esperado)
2. **O que o agente está fazendo?** (comportamento observado)
3. **Quando falha?** (em qual step/momento)
4. **Com que frequência?** (sempre, às vezes, em condições específicas)

### Step 2: Map Symptoms to Failure Modes

| Sintoma | Failure Mode Provável |
|---------|----------------------|
| Quality degrada ao longo da conversa | FM-1: Context Saturation |
| Agente usa tool errada ou retenta muito | FM-2: Tool Brittleness |
| Agente faz steps irrelevantes, perde foco | FM-3: Reasoning Drift |
| Agente pergunta "fiz certo?" ou entra em loop | FM-4: Evaluator Absence |
| Agente não consegue quebrar task complexa | Pilar: Planning (P1) |
| Agente esquece o que fez antes | Pilar: Memory (M1/M2) |
| Agente não tem tool para executar ação | Pilar: Tool Use (T1) |

### Step 3: Deep Diagnosis

Para cada failure mode identificado, investigar:

**FM-1 — Context Saturation**

- Quantos tokens o context window acumula por sessão?
- Há dados stale que não são limpos?
- O agente usa sub-agents para delegar?
- Há compaction ou just-in-time retrieval?

**FM-2 — Tool Brittleness**

- Quantas tools o agente tem?
- As tools são ACI-compliant? (rodar aci-checklist)
- Os retornos das tools são parseáveis?
- Há overlap entre tools (agente não sabe qual usar)?

**FM-3 — Reasoning Drift**

- O agente tem goal re-injection?
- Há max steps definido?
- O agente tem scope boundaries claros?
- O reasoning pattern é adequado para a complexidade?

**FM-4 — Evaluator Absence**

- O agente tem critérios de sucesso mensuráveis?
- Há self-evaluation no reasoning loop?
- Há quality gates definidos?
- O agente sabe quando escalar para humano?

### Step 4: Root Cause Analysis

Aplicar 5 Whys na causa raiz mais provável:

```text
1. Por que o agente falha? → [sintoma]
2. Por que [sintoma] acontece? → [causa imediata]
3. Por que [causa imediata]? → [causa intermediária]
4. Por que [causa intermediária]? → [causa estrutural]
5. Por que [causa estrutural]? → [root cause]
```

### Step 5: Validate Fixes via Pesquisa Externa (BLOCKING)

**GATE OBRIGATÓRIO** — A RCA (Step 4) identifica a causa real. Este step valida se o FIX proposto realmente funciona.

#### 5a. Para cada fix candidato, pesquisar evidência

Usar Exa (`mcp__exa__web_search_exa`):

```text
Query: "[fix proposto] [tipo do agente] AI agent evidence [failure mode]"
Exemplo: "compaction strategy context saturation fix evidence AI agents"
```

Min 1 query por fix candidato.

#### 5b. Teste de 3 perguntas

| Pergunta | Se NÃO |
|----------|-----------------------|
| Existe evidência de que este fix resolve este failure mode na prática? | Rebaixar para "hipótese" |
| O tipo de agente é compatível com o fix? (criativo ≠ código ≠ pipeline) | Descartar |
| É possível validar se o fix funcionou? | Marcar como "não verificável" |

#### 5c. Classificar cada fix

| Classificação | Ação |
|---------------|------|
| **Validado** | Incluir como recomendação forte com fonte |
| **Hipótese** | Incluir com disclaimer "sem evidência direta — testar e medir" |
| **Descartado** | NÃO incluir — documentar na seção "descartados" |

#### 5d. Tabela de referência (ponto de partida, NÃO prescrição)

| Root Cause | Fix candidato | Agent Responsável |
|-----------|---------------|-------------------|
| Context saturation | Redesenhar memory strategy | agent-architect |
| Tool brittleness | Criar/melhorar tools (ACI) | tool-smith |
| Reasoning drift | Configurar reasoning pattern | reasoning-engineer |
| Evaluator absence | Adicionar quality gates | agent-architect |
| Tool gaps | Encontrar/criar tools | ecosystem-scout → tool-smith |
| Prompt inadequado | Reescrever com pattern correto | reasoning-engineer |

SEMPRE validar via 5a-5c antes de recomendar. A tabela é referência, não verdade absoluta.

### Step 6: Deliver Report

```text
## Diagnosis Report: {agent-id}

### Problema Reportado
{descrição do usuário}

### Failure Modes Detectados
- {FM-X}: {descrição} — Severidade: {alta/média/baixa}

### Root Cause (5 Whys)
{cadeia de 5 whys}

### Recomendações
| # | Ação | Classificação | Fonte | Responsável | Prioridade |
|---|------|---------------|-------|-------------|------------|
| 1 | {ação} | Validado/Hipótese | {link} | {agent} | {P1/P2/P3} |

### Descartados (transparência)
| Fix candidato | Motivo da rejeição |
|---------------|-------------------|
| {fix} | {motivo} |

### Fontes
- {link_1}
- {link_2}

### Próximo Passo
Handoff para {agent} com contexto: {resumo}
```

## Post-conditions

- [ ] Ao menos 1 failure mode identificado
- [ ] Root cause analysis completa (5 Whys)
- [ ] Pesquisa externa executada para cada fix candidato (Step 5)
- [ ] Fixes classificados como Validado/Hipótese/Descartado
- [ ] Fontes documentadas para fixes validados
- [ ] Recomendações com agent responsável definido
- [ ] Handoff preparado

## Quality Gate

- **QG-002**: Diagnosis Complete + Evidence Gate


Completion Criteria: output validado com evidência, responsável definido e pronto para handoff
