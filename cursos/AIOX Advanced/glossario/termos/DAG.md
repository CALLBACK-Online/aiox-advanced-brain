---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 6
  aiox_advanced_squads: 0
  total: 6
  counted_at: '2026-08-10'
---
# DAG

DAG é um grafo direcionado acíclico (*Directed Acyclic Graph*): nós representam tarefas, Stories ou artefatos; arestas direcionadas representam dependências; acíclico significa que nenhum caminho volta ao próprio nó. Ele mostra o que precisa acontecer antes do quê.

## Como é usado

Monte o DAG antes de despachar trabalho. Ordene os nós topologicamente, coloque em uma mesma wave apenas o que está pronto e não depende entre si e mantenha as arestas que representam artefatos, ownership ou barreiras. O DAG orienta a sequência, mas ainda exige checagem de capacidade e risco.

**Exemplo prático:** na aula [[61-wave-execute]], o preflight constrói o DAG do épico: `schema → policies`, APIs independentes depois e UIs quando suas dependências estão prontas. A aula [[59-quando-paralelizar-vs-sequencial]] usa as arestas para localizar o ponto que mata o speedup.

**Não confunda:** um DAG não é qualquer fluxograma nem significa que todos os nós podem rodar em paralelo. Se existe ciclo, o grafo não é acíclico; se existe recurso compartilhado ou risco alto, o scheduler ainda pode serializar nós que não têm uma aresta explícita.

**Frequência nos cursos:** **6** menções (AIOX Advanced: 6 · AIOX Advanced Squads: 0).

## Aulas

- [[61-wave-execute]]
- [[59-quando-paralelizar-vs-sequencial]]
- [[58-ralph-paralelizacao]]

## Ver também

- [[Fan-in Fan-out]]
- [[Paralelização]]
- [[Wave Execute]]
- [[Épico]]
- [[Story]]
- [[Glossário AIOX Advanced]]

