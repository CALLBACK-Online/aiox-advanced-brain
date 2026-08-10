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
  aiox_advanced: 25
  aiox_advanced_squads: 0
  total: 25
  counted_at: '2026-08-10'
---
# Stop rule

Regra de parada declarada antes da execução que obriga o loop a pausar ou encerrar quando surge uma condição de risco, ambiguidade, custo, credencial, destruição ou escopo fora do contrato.

## Como é usado

Defina **Stop rule** no goal, no rider ou na SPEC junto com a ação esperada: parar, pedir decisão, registrar bloqueio ou encerrar com evidência parcial. Inclua também limites objetivos de ciclos, tempo ou budget quando a missão puder se prolongar.

**Exemplo prático:** na aula [[11-goal-vs-loop]], um loop para se a mesma falha objetiva persistir após o limite de tentativas, se faltar credencial ou se a ação for destrutiva. O operador recebe o diagnóstico e decide o próximo passo, em vez de consumir tokens indefinidamente.

**Não confunda:** **Stop rule** é uma condição de controle do processo; **FAIL** é o veredito de um gate sobre o artefato. Um gate pode retornar FAIL e ainda permitir um loop curto de correção; a stop rule determina quando esse loop não deve continuar.

**Frequência nos cursos:** **25** menções (AIOX Advanced: 25 · AIOX Advanced Squads: 0).

## Aulas

- [[11-goal-vs-loop]]
- [[50-rider-modo-elicitacao]]
- [[74-caso-integrado-end-to-end]]

## Ver também

- [[Rider]]
- [[FAIL]]
- [[PASS]]
- [[Definition of Done]]
- [[Glossário AIOX Advanced]]
