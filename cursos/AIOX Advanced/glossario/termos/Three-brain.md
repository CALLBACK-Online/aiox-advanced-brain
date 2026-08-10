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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# Three-brain

Padrão de roteamento multi-motor (Claude / Codex / Gemini / reviewer) com proibição de autorrevisão.

## Como é usado

Use **Three-brain** quando o fluxo se beneficiar de motores diferentes em papéis diferentes: um motor executa, outro revisa, outro pesquisa ou arbitra — e nenhum deles revisa o próprio trabalho.

**Exemplo prático:** Na aula [[60-routing-modelos]], o código é implementado com Claude, o review do PR fica com outro motor (ex.: CodeRabbit sobre Codex) e uma terceira lente arbitra divergências — a proibição de autorrevisão impede que o erro do executor passe pelo viés dele mesmo.

**Não confunda:** **Three-brain** não é rodar três modelos na mesma tarefa por redundância: é roteamento de papéis distintos entre motores, com a fronteira explícita de que executor e revisor nunca são o mesmo.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[60-routing-modelos]]
- [[06-code-rabbit-boost]]

## Ver também

- [[Model routing]]
- [[No-self-review]]
- [[Self-heal]]
- [[Glossário AIOX Advanced]]
