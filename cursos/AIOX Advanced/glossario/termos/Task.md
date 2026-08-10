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
  aiox_advanced: 562
  aiox_advanced_squads: 105
  total: 667
  counted_at: '2026-08-10'
---
# Task

Unidade atômica de trabalho na taxonomia AIOX: passo executável com entrada/saída. Skills e agentes orquestram tasks; runners as repetem com determinismo.

## Como é usado

Use **Task** para transformar um resultado maior em um passo executável, declarando entrada, transformação, saída e critério de pronto.

**Exemplo prático:** em vez de “melhorar o produto”, escreva uma **Task** como “ler o fluxo de checkout, listar cada estado e salvar um mapa”; uma Skill ou Workflow pode então orquestrar esse passo.

**Não confunda:** **Task** é um passo de trabalho, não a entrega completa: Story define o incremento aceito e PRD define o produto ou módulo que o contém.

**Frequência nos cursos:** **667** menções (AIOX Advanced: 562 · AIOX Advanced Squads: 105).

## Aulas

- [[28-taxonomia-task-skill-agent-workflow-runner]]
- [[30-runner-executavel-deterministico]]

## Ver também

- [[Taxonomia AIOX]]
- [[Skill]]
- [[Workflow]]
- [[Runner]]
- [[Glossário AIOX Advanced]]
