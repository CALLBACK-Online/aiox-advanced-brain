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
  aiox_advanced: 48
  aiox_advanced_squads: 4
  total: 52
  counted_at: '2026-08-10'
---
# Codex

Harness de agentes da OpenAI para executar trabalho no repositório. No curso, regras permanentes vivem em `AGENTS.md`; Codex é uma superfície alternativa ao Claude Code.

## Como é usado

Use **Codex** como superfície de execução quando a missão precisar ler e alterar arquivos, rodar validações e devolver um diff sob as regras do repositório.

**Exemplo prático:** na aula [[68-squad-fora-do-claude-code]], entregue ao **Codex** uma Story com arquivos permitidos, `AGENTS.md`, critério de aceite e validator; confira o diff e a saída do validator antes do handoff.

**Não confunda:** **Codex** é a superfície/runtime de execução, não o papel do agente nem o contrato da missão; esses continuam definidos por arquivos, escopo, aceite e evidência.

**Frequência nos cursos:** **52** menções (AIOX Advanced: 48 · AIOX Advanced Squads: 4).

## Aulas

- [[68-squad-fora-do-claude-code]]
- [[03-claude-md-leis-da-fisica]]

## Ver também

- [[AGENTS.md]]
- [[Claude Code]]
- [[Harness]]
- [[Glossário AIOX Advanced]]
