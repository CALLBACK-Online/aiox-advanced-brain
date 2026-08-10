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
  aiox_advanced: 14
  aiox_advanced_squads: 0
  total: 14
  counted_at: '2026-08-10'
---
# Pull Request

Proposta de integração de uma mudança, com diff, contexto e verificações para revisão. É a superfície onde Quality Gate e CodeRabbit analisam o trabalho.

## Como é usado

Use **Pull Request** para propor merge com diff revisável: é sobre o PR que o Quality Gate roda, o CodeRabbit comenta e o revisor decide — a unidade de revisão do ciclo do repositório.

**Exemplo prático:** na aula [[19-ciclo-do-repositorio]], o trabalho sai da branch em um PR; o CodeRabbit aponta findings no diff e o merge só acontece depois do gate.

**Não confunda:** **Pull Request** aberto não é trabalho entregue: sem revisão, gate e merge é só um diff pendente — e um PR gigante que ninguém consegue revisar derrota o propósito da superfície.

**Frequência nos cursos:** **14** menções (AIOX Advanced: 14 · AIOX Advanced Squads: 0).

## Aulas

- [[19-ciclo-do-repositorio]]
- [[06-code-rabbit-boost]]
- [[48-quality-gate-completo]]

## Ver também

- [[Merge]]
- [[Quality Gate]]
- [[CodeRabbit]]
- [[Finding]]
- [[Glossário AIOX Advanced]]
