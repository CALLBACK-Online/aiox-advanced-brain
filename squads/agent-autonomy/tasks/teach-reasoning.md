---
task: teachReasoning()
responsavel: "ReasoningEngineer"
responsavel_type: Agente
executor: reasoning-engineer
atomic_layer: Molecule
Entrada:
  - nome: concept_or_pattern
    tipo: string
    obrigatorio: true
  - nome: agent_id
    tipo: string
    obrigatorio: false
Saida:
  - nome: reasoning_section
    tipo: markdown
    obrigatorio: true
Checklist:
  - Pattern explicado com clareza
  - Exemplos concretos fornecidos
  - Anti-patterns documentados
---


## Contrato AIOX

Domain: `Tactical`
atomic_layer: Molecule
Input: concept_or_pattern, agent_id
Output: reasoning_section, cross-domain-handoff
Pre-condition: pattern alvo identificado e domínio do agente conhecido
Post-condition: pattern explicado com fonte, anti-patterns e critérios de escalação
Performance: validar pattern via pesquisa externa e explicitar quando for recomendação teórica

## METADATA
- **Executor:** reasoning-engineer (Clone)
- **Elicit:** true
# Task: Teach Reasoning

## Metadata

- **id**: AA-T007
- **name**: teach-reasoning
- **primary_agent**: reasoning-engineer
- **trigger**: `*teach <agent-id> <pattern>` ou `*teach <concept>`
- **inputs**: agent-id (opcional) + conceito/pattern a ensinar
- **outputs**: instruções aplicadas ao agente ou explicação educativa

## Description

Ensinar COMO um agente deve raciocinar e atuar — não O QUE fazer. Foco em patterns de reasoning, self-evaluation, error recovery e halt conditions. Baseado na pedagogia de Shunyu Yao (ReAct/ToT) e Noah Shinn (Reflexion).

## Pre-conditions

- [ ] Conceito ou pattern identificado
- [ ] Agente alvo identificado (se aplicável)

## Steps

### Step 1: Identify What to Teach

| Request | Teaching Path |
|---------|--------------|
| "Como o agente deve pensar?" | Reasoning pattern selection |
| "O agente não sabe quando parar" | Halt conditions + evaluator design |
| "O agente fica em loop" | Loop detection + escalation |
| "O agente não corrige erros" | Self-reflection + Reflexion pattern |
| "O agente perde o foco" | Goal persistence + scope boundaries |
| "Qual pattern usar?" | Pattern selection decision tree |

### Step 2: Validate Pattern Selection via Pesquisa Externa

**ANTES de recomendar um pattern**, pesquisar se há evidência de que funciona para o tipo de agente.

#### 2a. Pesquisar evidência

Usar Exa (`mcp__exa__web_search_exa`):

```text
Query: "[pattern] [agent domain] AI agent performance improvement evidence"
Exemplo: "ReAct pattern content generation agent evidence improvement"
```

#### 2b. Verificar compatibilidade

| Pergunta | Ação se NÃO |
|----------|-----------------------|
| O pattern tem evidência de melhoria para agentes deste domínio? | Pesquisar alternativas |
| O custo (tokens, latência) é justificável para o caso de uso? | Considerar pattern mais simples |
| Existe benchmark ou caso real documentado? | Marcar como "baseado em teoria" |

#### 2c. Documentar fonte

Ao recomendar um pattern, incluir:

- Fonte da evidência (paper, blog técnico, benchmark)
- Domínio onde foi validado
- Se não há evidência direta: declarar "recomendação teórica — validar empiricamente"

### Step 3: Explain the Pattern

Para cada pattern, ensinar com a estrutura:

```text
## Pattern: {nome}

### O que é
{definição em 1-2 frases}

### Quando usar
{critérios claros de quando este pattern é adequado}

### Quando NÃO usar
{anti-patterns, situações onde outro pattern é melhor}

### Como implementar no prompt
{instruções concretas para embutir no prompt do agente}

### Exemplo
{exemplo concreto de uso}

### Failure modes
{o que pode dar errado e como prevenir}
```

### Step 4: Apply to Agent (se aplicável)

Se um agent-id foi fornecido:

1. Ler o agent file atual
2. Identificar onde o pattern deve ser inserido
3. Gerar a seção de reasoning para o agent file
4. Sugerir edição (não editar diretamente sem aprovação)

### Step 5: Teach Self-Evaluation

Independente do pattern, SEMPRE ensinar:

**5 Princípios de Autonomia:**

1. **Ensinar patterns, não respostas** — o agente aprende a pensar, não a copiar
2. **Ensinar self-evaluation** — critérios mensuráveis de "completei corretamente"
3. **Ensinar error taxonomy** — classificar erros em recuperáveis vs fatais
4. **Ensinar quando parar** — halt conditions explícitas (max steps + progress check)
5. **Ensinar quando escalar** — critérios claros de "preciso de ajuda humana"

### Step 6: Deliver

**Se aplicado a agente**: seção de reasoning pronta para inserir no agent file
**Se educativo**: explicação completa do conceito com exemplos

## Teaching Library (Quick Reference)

### ReAct (padrão — usar como default)

```text
Para CADA step, siga este ciclo:
1. THOUGHT: O que preciso fazer agora? Por quê?
2. ACTION: Qual tool/ação executo?
3. OBSERVATION: O que o resultado me diz?
4. Repita até atingir o objetivo ou max steps.
```

**Custo**: baixo (1 call/step)
**Quando**: qualquer task com tool use
**Fonte**: Yao et al., 2022 — arxiv.org/abs/2210.03629

### Reflexion (quando há critério mensurável de sucesso)

```text
1. EXECUTE: Tente completar a task
2. EVALUATE: O resultado atende os critérios?
3. REFLECT: Se não, o que deu errado? O que fazer diferente?
4. RETRY: Execute novamente com a reflexão em mente
(max N tentativas)
```

**Custo**: médio (N tentativas)
**Quando**: critério claro de sucesso/falha + budget de retry. Evidência forte em coding agents (SWE-Bench). Sem evidência para agentes criativos/subjetivos.
**Fonte**: Shinn et al., 2023 — arxiv.org/abs/2303.11366

### Tree of Thoughts (raro — planejamento com dead ends)

```text
1. GENERATE: Proponha K abordagens diferentes
2. EVALUATE: Qual tem maior probabilidade de sucesso?
3. EXPLORE: Siga a melhor, mantenha as outras como backup
4. BACKTRACK: Se a melhor falhar, tente a próxima
```

**Custo**: alto (K × depth calls)
**Quando**: planejamento complexo com risco de dead ends
**Fonte**: Yao et al., 2023 — arxiv.org/abs/2305.10601

### LATS (muito raro — alto valor + espaço de busca grande)

```text
MCTS: Select → Expand → Simulate → Backpropagate → Reflect
```

**Custo**: muito alto
**Quando**: tasks de altíssimo valor com espaço de busca grande
**Fonte**: Zhou et al., 2023 — arxiv.org/abs/2310.04406

**NOTA**: A frequência relativa de uso (qual pattern é mais comum) depende do domínio e tipo de agente. NÃO existe distribuição fixa universal. SEMPRE validar via Step 2 qual pattern tem evidência para o caso específico.

## Post-conditions

- [ ] Pesquisa externa validou o pattern para o tipo de agente (Step 2)
- [ ] Pattern explicado com clareza
- [ ] Fonte do pattern documentada (paper/estudo)
- [ ] Exemplos concretos fornecidos
- [ ] Se aplicado a agente: seção pronta para inserção
- [ ] Anti-patterns documentados
- [ ] Se sem evidência direta: declarado como "recomendação teórica"

## Quality Gate

- **QG-004**: Reasoning Validated + Evidence Check


Completion Criteria: output validado com evidência, responsável definido e pronto para handoff
