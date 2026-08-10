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
  aiox_advanced: 4
  aiox_advanced_squads: 4
  total: 8
  counted_at: '2026-08-10'
---
# /comando

Sintaxe de barra que dispara um processo nomeado, com greeting, skill/workflow e gate definidos pelo projeto.

## Como é usado

Use **/comando** quando precisar do ritual completo: a barra aciona o greeting builder, que puxa o núcleo do projeto (CLAUDE.md, core-config, PRD/Stories) antes de responder e segue etapas com critério de saída.

**Exemplo prático:** na aula [[45-doze-agentes-orbitais]], com um épico pronto para paralelizar, dispare `/wave-execute`: o comando carrega o núcleo, monta as waves e só encerra devolvendo artefato, status ou bloqueio declarado — em vez de uma resposta solta de chat.

**Não confunda:** **/comando** não é sinônimo de **@agente**: a barra aciona processo; a arroba carrega a persona. Ambos dependem do runtime que os implementa.

**Frequência nos cursos:** **8** menções (AIOX Advanced: 4 · AIOX Advanced Squads: 4).

## Aulas

- [[45-doze-agentes-orbitais]]

## Ver também

- [[Glossário AIOX Advanced]]
