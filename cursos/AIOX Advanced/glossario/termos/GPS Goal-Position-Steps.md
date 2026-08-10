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
  aiox_advanced: 31
  aiox_advanced_squads: 0
  total: 31
  counted_at: '2026-08-10'
---
# GPS Goal/Position/Steps

Frame de comando: Goal (resultado), Position (estado atual), Steps (próximos passos com gates). Evita loop sem alvo.

## Como é usado

Use **GPS Goal/Position/Steps** para dirigir (ou reancorar) um agente: declare o Goal como resultado final verificável, a Position como o estado real de agora e os Steps como os próximos passos, cada um com seu gate de verificação.

**Exemplo prático:** na aula [[11-goal-vs-loop]], um agente preso em loop consertando o mesmo teste é reancorado com GPS: "Goal: suíte verde no CI; Position: 3 testes de auth falhando por fixture desatualizada; Steps: 1) atualizar a fixture, 2) rodar a suíte local, 3) reportar o resultado" — o loop morre porque agora existe alvo e critério de chegada.

**Não confunda:** **GPS Goal/Position/Steps** não é backlog nem plano de projeto: é o frame de um comando. Goal sem verificação vira loop; Steps sem gate viram atividade sem prova de progresso.

**Frequência nos cursos:** **31** menções (AIOX Advanced: 31 · AIOX Advanced Squads: 0).

## Aulas

- [[11-goal-vs-loop]]
- [[08-principio-processo-certo]]

## Ver também

- [[Goal vs Loop]]
- [[Briefing]]
- [[Glossário AIOX Advanced]]
