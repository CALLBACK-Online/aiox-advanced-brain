---
type: quiz
course: aiox-agent-engineering
module: M0
question_count: 4
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---
# Quiz M0 — Arquitetura da capacidade

[Módulo M0](../modulos/M0-arquitetura-da-capacidade.md) · [Avaliações](../Assessments.md)

### 1. Um procedimento tem entrada e saída estáveis, mas não precisa de persona nem julgamento. Qual unidade é suficiente?

A. Squad
B. Skill
C. Swarm
D. Agente autônomo

### 2. Quando um comando manual deve virar workflow?

A. Quando fica visualmente complexo
B. Quando usa mais de um arquivo
C. Quando a sequência recorrente precisa de estado, gates e evidência
D. Sempre que houver um agente

### 3. Qual sinal justifica um runner determinístico?

A. A execução precisa ser repetível, observável e independente de conversa
B. O prompt ficou longo
C. Existem duas personas
D. O resultado será lido por uma pessoa

### 4. Em um pipeline agentic, qual desenho reduz o risco de saída inconsistente?

A. Um único prompt sem contrato
B. Mais modelos em paralelo
C. Memória ilimitada
D. Etapas com schemas, checkpoints e validação explícita

<details>
<summary>Gabarito comentado</summary>

1. **B.** Skill resolve procedimento estreito sem inflar a arquitetura.
2. **C.** Recorrência, estado e gates justificam orquestração.
3. **A.** Runner transforma intenção em execução operacional reproduzível.
4. **D.** Contratos entre etapas tornam o pipeline auditável.

</details>

## Transferência

Classifique uma capacidade real em task, skill, agent, workflow, squad e runner; risque as camadas que ela ainda não precisa.
