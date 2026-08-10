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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# Concorrência

Concorrência é a capacidade de fazer vários trabalhos progredirem no mesmo intervalo de tempo, alternando ou compartilhando recursos quando necessário. Ela descreve a organização do progresso, não a execução simultânea em hardware diferente.

## Como é usado

Use concorrência para definir quantos jobs ou agentes podem estar ativos, escolher limites de capacidade e evitar que uma fila, API ou recurso compartilhado seja saturado. O número de trabalhos concorrentes deve respeitar rate limits, dependências, ownership e criticidade; aumentar N sem medir pode aumentar espera e retrabalho.

**Exemplo prático:** na aula [[59-quando-paralelizar-vs-sequencial]], o batch só sobe o número de frentes quando não há dependência de artefato, os paths são disjuntos e N cabe na capacidade. Rate limit ou overlap transforma o restante em execução sequencial ou em uma wave com barreira.

**Não confunda:** concorrência é progresso sobreposto; **paralelismo** é execução realmente simultânea em recursos distintos. Um programa assíncrono ou uma fila com um único worker pode ser concorrente sem ser paralelo, e várias frentes paralelas também precisam de concorrência controlada.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[59-quando-paralelizar-vs-sequencial]]
- [[58-ralph-paralelizacao]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/12-concorrencia-paralelismo-fanout-fanin]]

## Ver também

- [[Fan-in Fan-out]]
- [[Paralelização]]
- [[DAG]]
- [[Speedup wall-clock]]
- [[Glossário AIOX Advanced]]

