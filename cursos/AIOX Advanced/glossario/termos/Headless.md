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
  aiox_advanced: 0
  aiox_advanced_squads: 8
  total: 8
  counted_at: '2026-08-10'
---
# Headless

Execução sem depender da interface interativa da IDE ou de uma sessão aberta: o processo recebe ambiente, gatilho, estado, orçamento, métricas e critérios de recuperação definidos.

## Como é usado

Use **Headless** quando um processo precisa rodar fora da IDE, de modo recorrente ou agendado, com observabilidade e evidência. A aula [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]] orienta preparar um processo executável, o ambiente e o gatilho antes de criar ou governar o runner.

**Exemplo prático:** “executar uma rotina agendada fora da IDE, com orçamento e métricas” é sinal de `runner-ops`. O `runner-chief` deve validar o lifecycle, os limites e o smoke test; a conclusão só vale quando há artefato, critérios verificáveis, premissas e próximo handoff.

**Não confunda:** **Headless** descreve a superfície de execução, não o grau de autonomia. Um script agendado pode ser headless e totalmente determinístico; um agente pode ter autonomia dentro de uma IDE. Autonomia exige decisão, estado, stop condition e recuperação — headless apenas remove a dependência da interface interativa.

**Frequência nos cursos:** **8** menções (AIOX Advanced: 0 · AIOX Advanced Squads: 8).

## Aulas

- [[cursos/AIOX-Advanced-Squads/aulas/05-agent-autonomy]]
- [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]]

## Ver também

- [[Runner]]
- [[Orquestrador]]
- [[Generic prompt]]
- [[Maturidade]]
- [[Glossário AIOX Advanced]]
