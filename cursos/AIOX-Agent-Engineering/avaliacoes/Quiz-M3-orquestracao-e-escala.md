---
type: quiz
course: aiox-agent-engineering
module: M3
question_count: 4
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---
# Quiz M3 — Orquestração e escala

[Módulo M3](../modulos/M3-orquestracao-e-escala.md) · [Avaliações](../Assessments.md)

### 1. Quando tarefas devem permanecer sequenciais?

A. Quando compartilham o mesmo modelo
B. Quando há dependência de saída ou risco de conflito
C. Quando o time é pequeno
D. Quando cada tarefa dura pouco

### 2. O que o routing de modelos deve otimizar?

A. Adequação entre risco, capacidade, custo e latência
B. Sempre o modelo mais caro
C. Apenas velocidade
D. Quantidade de fornecedores

### 3. Qual pré-condição torna uma wave segura?

A. Prompts idênticos
B. Uma branch compartilhada sem ownership
C. Histórias independentes, contratos claros e fan-in definido
D. Ausência de testes

### 4. Um loop Ralph não converge. Qual correção vem primeiro?

A. Aumentar o número de agentes
B. Remover os gates
C. Executar indefinidamente
D. Tornar estado, critério de parada e feedback observáveis

<details>
<summary>Gabarito comentado</summary>

1. **B.** Dependência e colisão anulam o ganho do paralelismo.
2. **A.** Routing é decisão econômica e de risco por tarefa.
3. **C.** Independência e fan-in são o contrato da wave.
4. **D.** Loop autônomo precisa saber onde está e quando terminou.

</details>

## Transferência

Desenhe uma wave de três tarefas e marque dependências, ownership e fan-in.
