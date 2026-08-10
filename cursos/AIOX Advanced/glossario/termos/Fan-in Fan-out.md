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
  aiox_advanced: 91
  aiox_advanced_squads: 0
  total: 91
  counted_at: '2026-08-10'
---
# Fan-in Fan-out

**Fan-out** é abrir uma execução em vários ramos independentes; **fan-in** é fechar esses ramos, reunindo resultados, conflitos, falhas e validação em uma entrega única. Fan-out distribui; fan-in reconcilia.

## Como é usado

Defina o contrato de fan-in antes do dispatch: quais ramos são esperados, quem tem ownership, o que acontece em caso de timeout ou falha e qual gate autoriza a convergência. Só faça fan-out quando o grafo permitir independência suficiente; a convergência pode ser um merge, uma síntese ou uma validação, conforme o tipo de saída.

**Exemplo prático:** na aula [[61-wave-execute]], o preflight monta o DAG, o dispatch executa um full-cycle por Story e o fan-in detecta conflitos entre branches antes do merge. Na aula [[58-ralph-paralelizacao]], o batch também termina com diff, ordem de merge e quality gate.

**Não confunda:** fan-out não garante paralelismo — ramos podem ser enfileirados ou limitados por capacidade — e fan-in não é “o último que escrever vence”. Fan-out é a abertura da topologia; fan-in é a barreira de reintegração e decisão.

**Frequência nos cursos:** **91** menções (AIOX Advanced: 91 · AIOX Advanced Squads: 0).

## Aulas

- [[58-ralph-paralelizacao]]
- [[59-quando-paralelizar-vs-sequencial]]
- [[61-wave-execute]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/12-concorrencia-paralelismo-fanout-fanin]]

## Ver também

- [[Concorrência]]
- [[DAG]]
- [[Paralelização]]
- [[Speedup wall-clock]]
- [[Glossário AIOX Advanced]]

