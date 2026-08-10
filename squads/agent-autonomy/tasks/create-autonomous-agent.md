---
task: createAutonomousAgent()
responsavel: "AgentArchitect"
responsavel_type: Agente
executor: agent-architect
atomic_layer: Organism
Entrada:
  - nome: agent_name
    tipo: string
    obrigatorio: true
  - nome: domain
    tipo: string
    obrigatorio: true
  - nome: objective
    tipo: string
    obrigatorio: true
  - nome: available_tools
    tipo: list
    obrigatorio: true
  - nome: target_level
    tipo: string
    obrigatorio: false
Saida:
  - nome: agent_file
    tipo: markdown
    obrigatorio: true
  - nome: validation_report
    tipo: markdown
    obrigatorio: true
Checklist:
  - Agent file criado no path correto
  - Autonomy checklist >= 13/18
  - Reasoning pattern documentado
  - Det vs prob separados
  - Halt condition definida
  - Security check lethal trifecta < 3
---


## Contrato AIOX

Domain: `Tactical`
atomic_layer: Organism
Input: agent_name, domain, objective, available_tools, target_level
Output: agent file, validation report, agent-optimization-plan
Pre-condition: requirements claros e inventário inicial de tools disponível
Post-condition: agente desenhado com det/prob split, halt condition e checklist de autonomia
Performance: atingir autonomy checklist >= 13/18 e bloquear arquitetura sem evidência mínima

## METADATA
- **Executor:** agent-architect (Agent)
- **Elicit:** true
# Task: Create Autonomous Agent

## Metadata

- **id**: AA-T002
- **name**: create-autonomous-agent
- **primary_agent**: agent-architect
- **secondary**: reasoning-engineer, tool-smith
- **trigger**: `*create <agent-name>`
- **inputs**: agent requirements (nome, domínio, objetivo, tools disponíveis)
- **outputs**: agent file (.md) + validation report

## Description

Criar um novo agente autônomo do zero, aplicando os frameworks de autonomia do squad. O agente resultante deve atingir no mínimo L3 na classificação de autonomia.

## Pre-conditions

- [ ] Nome do agente definido
- [ ] Domínio de atuação claro
- [ ] Objetivo principal especificado
- [ ] Tools disponíveis inventariados

## Steps

### Step 1: Define Agent Requirements

Coletar do usuário:

- **Nome**: identificador único do agente
- **Domínio**: área de atuação (ex: "code review", "content generation")
- **Objetivo**: o que o agente deve atingir autonomamente
- **Tools**: quais ferramentas o agente terá acesso
- **Nível alvo**: L3 (mínimo), L4 ou L5

### Step 2: Select Reasoning Pattern (com validação)

Consultar reasoning-engineer para decidir. A tabela abaixo é referência inicial — SEMPRE validar via pesquisa.

| Complexidade da task | Pattern candidato |
|---------------------|-------------------|
| Simples, com tool use | ReAct |
| Iterativa, com critério de sucesso | Reflexion |
| Planejamento com dead ends | Tree of Thoughts |
| Alto valor + espaço de busca grande | LATS |

**Regra**: usar o pattern MAIS SIMPLES que resolve.

#### 2a. Pesquisar evidência do pattern para o domínio

```text
Query (Exa): "[pattern] [domain do agente] agent performance evidence"
Exemplo: "ReAct pattern code review agent evidence"
```

Se não há evidência para o domínio específico: declarar como "default teórico — validar empiricamente" e usar ReAct (menor risco).

### Step 3: Design Architecture (com validação)

Aplicar os 4 frameworks do agent-architect:

1. **Workflow vs Agent**: a task precisa de agente ou um workflow resolve?
2. **ACI Design**: tools seguem os 5 princípios?
3. **Context Engineering**: o que entra no context window e em que ordem?
4. **Det vs Prob split**: quais partes são LLM, quais são código?

#### 3a. Validar decisões de arquitetura

Para decisões não-triviais (ex: "usar sub-agents para context overflow", "implementar memory persistence"), pesquisar:

```text
Query (Exa): "[decisão] AI agent architecture evidence impact"
```

Marcar cada decisão como:

- **Evidenciada**: paper/estudo/caso real suporta
- **Padrão da indústria**: amplamente usado, sem estudo formal mas consenso
- **Experimental**: sem evidência — documentar como hipótese

### Step 4: Build Agent File

Gerar o `.md` do agente com as 10 seções obrigatórias:

```text
1. activation-instructions
2. agent (id, name, role, tier, version, squad, description, primary_minds)
3. persona (voice_dna)
4. methodology / frameworks
5. commands (com aliases pt-br)
6. quality_gate
7. dependencies (tasks, data, receives_from, hands_off_to)
8. security (lethal trifecta check)
9. error_handling
10. halt_conditions
```

### Step 5: Validate Autonomy

Rodar a autonomy-checklist (18 items) no agente criado:

- **>= 13/18**: L3+ — OK para uso
- **>= 15/18**: L4+ — Bom
- **>= 17/18**: L5 — Excelente
- **< 13/18**: Requer fixes antes de usar

### Step 6: Identify Missing Tools

Se T1 (Tool Coverage) falhou:

1. Consultar ecosystem-scout para libs existentes
2. Se nada encontrado → spec para tool-smith construir

### Step 7: Deliver

Entregar:

- Agent file (.md) pronto para uso
- Validation report com scores
- Lista de tools necessárias (se houver gaps)

## Post-conditions

- [ ] Agent file criado no path correto
- [ ] Reasoning pattern validado via pesquisa (Step 2a)
- [ ] Decisões de arquitetura classificadas (evidenciada/padrão/experimental)
- [ ] Autonomy checklist >= 13/18
- [ ] Reasoning pattern documentado com fonte
- [ ] Det vs Prob claramente separados
- [ ] Halt condition definida
- [ ] Security check: lethal trifecta < 3

## Quality Gate

- **QG-003**: Architecture Review + Evidence Check
- Critério: agent file completo, autonomy >= 13/18, security check passed, decisões de design com classificação de evidência

## Handoff

| Situação | Próximo Agent |
|----------|---------------|
| Tool gaps identificados | → ecosystem-scout → tool-smith |
| Reasoning pattern complexo | → reasoning-engineer |
| Validação final | → autonomy-auditor (*audit) |


Completion Criteria: output validado com evidência, responsável definido e pronto para handoff
