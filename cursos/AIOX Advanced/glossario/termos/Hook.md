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
  aiox_advanced: 54
  aiox_advanced_squads: 3
  total: 57
  counted_at: '2026-08-10'
---
# Hook

Gatilho do harness executado em um evento definido — antes ou depois de um comando, ou durante uma validação — para impor uma regra de forma determinística.

## Como é usado

Use **Hook** quando uma regra precisar ser aplicada automaticamente no ponto certo do ciclo, como bloquear uma operação, rodar uma checagem ou registrar uma saída.

**Exemplo prático:** nas aulas [[03-claude-md-leis-da-fisica]] e [[67-harness-ambiente-execucao]], configure um **Hook** pré-comando para barrar uma ação que viola a regra e um pós-comando para executar a validação e registrar seu resultado.

**Não confunda:** **Hook** é o mecanismo acionado por um evento; não é uma instrução solta no prompt nem o veredito do gate que avalia a saída.

**Frequência nos cursos:** **57** menções (AIOX Advanced: 54 · AIOX Advanced Squads: 3).

## Aulas

- [[03-claude-md-leis-da-fisica]]
- [[67-harness-ambiente-execucao]]

## Ver também

- [[CLAUDE md]]
- [[Amarra]]
- [[Constitution]]
- [[Gate]]
- [[Glossário AIOX Advanced]]
