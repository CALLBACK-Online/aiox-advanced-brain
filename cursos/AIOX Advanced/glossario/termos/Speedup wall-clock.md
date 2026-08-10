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
  aiox_advanced: 47
  aiox_advanced_squads: 0
  total: 47
  counted_at: '2026-08-10'
---
# Speedup wall-clock

Speedup é a razão entre o tempo de uma baseline e o tempo da alternativa; **wall-clock real** é o tempo de relógio do dispatch até a entrega final validada. No AIOX, o speedup que importa é `T_sequencial / T_paralelo_real`, incluindo espera, throttle, fan-in, conflitos, retrabalho e quality gate.

## Como é usado

Meça primeiro uma baseline sequencial com o mesmo escopo. Depois meça o caminho paralelo até o batch estar convergido e validado — não apenas até o primeiro worker responder. Compare os dois tempos, registre capacidade e custo de convergência e só aumente o grau de paralelismo se o wall-clock final melhorar.

**Exemplo prático:** na aula [[59-quando-paralelizar-vs-sequencial]], a estimativa ideal é `max(tempos) + fan-in`, enquanto a real acrescenta conflito, correção e throttle. Na aula [[61-wave-execute]], a decisão compara o wall-clock da wave com a sequência pura e admite `unified-branch` quando uma revisão atômica vale mais que o paralelo.

**Não confunda:** o tempo até o agente mais rápido terminar, a quantidade de tokens poupada ou o throughput de uma etapa não são o wall-clock do resultado. Speedup sem fan-in limpo é uma prévia; o ganho só existe quando o artefato correto passa pelo gate.

**Frequência nos cursos:** **47** menções (AIOX Advanced: 47 · AIOX Advanced Squads: 0).

## Aulas

- [[59-quando-paralelizar-vs-sequencial]]
- [[61-wave-execute]]
- [[58-ralph-paralelizacao]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/12-concorrencia-paralelismo-fanout-fanin]]

## Ver também

- [[Concorrência]]
- [[Fan-in Fan-out]]
- [[DAG]]
- [[Paralelização]]
- [[Wave Execute]]
- [[Glossário AIOX Advanced]]

