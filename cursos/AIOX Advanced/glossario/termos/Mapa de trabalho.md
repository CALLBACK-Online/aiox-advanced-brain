---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-12'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 1
  aiox_advanced_squads: 0
  total: 1
  counted_at: '2026-08-12'
---
# Mapa de trabalho

O GPS do projeto no disco: pedido → story → task → gate → evidência, mais um ledger que diz agora / feito / próximo / não fazer. Mostra onde o agente está e o que está fazendo — não o que a empresa sabe do mundo.

## Como é usado

Use **Mapa de trabalho** quando o agente se perde, redescobre decisão antiga ou retoma uma sessão perguntando o que estava em curso. A orientação vive em arquivos magros (`CLAUDE.md` com ponteiros, Brand Card, SOT, ADRs, `progress.md`), não no chat.

**Exemplo prático:** na aula [[76-orientacao-do-agente]], o aluno mata o terminal e pede “continue de onde paramos”. Se o agente relê o ledger e retoma, o mapa existe. Se pergunta o que era, o mapa ainda está no chat.

**Não confunda:** **Mapa de trabalho** não é grafo de conhecimento (pessoas, deals, evidências) nem grafo de código (dependências do repo). Também não é o [[Brand Book]]: o livro de identidade visual não orienta a sessão.

## Aulas

- [[76-orientacao-do-agente]]
- [[11-goal-vs-loop]]
- [[27-otimizacao-claude-md]]

## Ver também

- [[Orientação do Agente]]
- [[Brand Card]]
- [[GPS Goal-Position-Steps]]
- [[DAG]]
- [[Compaction]]
- [[Glossário AIOX Advanced]]
