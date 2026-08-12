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

### 3. A wave já tem DAG. O agente ainda se perde no fan-in. O que entra no hot path?

A. Grafo de conhecimento da empresa (pessoas, deals, wiki)
B. Sidecar [Neo4j](https://github.com/neo4j/neo4j) / banco de grafos “para lembrar”
C. Cartão de processo no disco (o que rodou, raio, o que não repetir) com atribuição
D. Colar o plano da wave de novo no chat

### 4. Um loop Ralph não converge. Qual correção vem primeiro?

A. Aumentar o número de agentes
B. Remover os gates
C. Executar indefinidamente
D. Tornar estado, critério de parada e feedback observáveis

<details>
<summary>Gabarito comentado</summary>

1. **B.** Dependência e colisão anulam o ganho do paralelismo.
2. **A.** Routing é decisão econômica e de risco por tarefa.
3. **C.** Depois do DAG, a wave precisa de memória de processo no disco — não de cérebro da empresa nem de grafo sidecar.
4. **D.** Loop autônomo precisa saber onde está e quando terminou.

</details>

## Transferência

Desenhe uma wave de três tarefas, marque dependências, ownership e fan-in, e escreva o cartão de processo (feito / raio / não fazer) que a próxima sessão deve ler. Se o briefing também pedir “quem é o cliente”, escreva o veto (aula 12c): córtex é outro sistema, fora do dispatch.
