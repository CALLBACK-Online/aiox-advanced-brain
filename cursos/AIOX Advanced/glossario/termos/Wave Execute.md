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
  aiox_advanced: 30
  aiox_advanced_squads: 0
  total: 30
  counted_at: '2026-08-10'
---
# Wave Execute

Pipeline que divide um épico em waves, executa Stories em paralelo onde o grafo permite e fecha cada onda com fan-in, gate e handoff de ownership.

## Como é usado

Use **Wave Execute** depois de decidir que vale paralelizar: desenhe o DAG, declare parallel groups, isole cada Story e barre a próxima wave até o gate fechar.

**Exemplo prático:** na aula [[61-wave-execute]], execute `schema → policies` na Wave 1, APIs independentes na Wave 2 e UIs na Wave 3; faça fan-in e entregue o merge ao dono antes de avançar.

**Não confunda:** **Wave Execute** não é persona, sprint de calendário ou “ligar tudo ao mesmo tempo”; é coordenação por grafo, barreiras e ownership verificável.

**Frequência nos cursos:** **30** menções (AIOX Advanced: 30 · AIOX Advanced Squads: 0).

## Aulas

- [[61-wave-execute]]
- [[59-quando-paralelizar-vs-sequencial]]
- [[58-ralph-paralelizacao]]

## Ver também

- [[Ralph]]
- [[Paralelização]]
- [[SDC]]
- [[Glossário AIOX Advanced]]
