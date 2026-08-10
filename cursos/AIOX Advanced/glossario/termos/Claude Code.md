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
  aiox_advanced: 85
  aiox_advanced_squads: 23
  total: 108
  counted_at: '2026-08-10'
---
# Claude Code

CLI e harness de agentes da Anthropic, com instruções, skills, hooks, MCP e subagents. É a superfície de execução, não o próprio modelo de linguagem.

## Como é usado

Use **Claude Code** como a superfície principal de execução do método: é o harness da Anthropic onde vivem CLAUDE.md, skills, hooks, MCP e subagents — é nele que as leis do repositório são carregadas e os squads rodam.

**Exemplo prático:** na aula [[03-claude-md-leis-da-fisica]], o `CLAUDE.md` define as leis carregadas em cada sessão; na aula [[68-squad-fora-do-claude-code]], o mesmo squad é portado para outro harness.

**Não confunda:** Claude Code é o harness, não o modelo: o modelo (Claude) gera as respostas; o Claude Code é o ambiente que dá a ele ferramentas, contexto do repositório e superfícies como skills e hooks.

**Frequência nos cursos:** **108** menções (AIOX Advanced: 85 · AIOX Advanced Squads: 23).

## Aulas

- [[03-claude-md-leis-da-fisica]]
- [[68-squad-fora-do-claude-code]]
- [[27-otimizacao-claude-md]]

## Ver também

- [[CLAUDE md]]
- [[Harness]]
- [[MCP]]
- [[Hook]]
- [[Codex]]
- [[Glossário AIOX Advanced]]
