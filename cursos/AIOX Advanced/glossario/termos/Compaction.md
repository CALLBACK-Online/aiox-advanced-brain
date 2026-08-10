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
# Compaction

Processo de resumir ou reduzir o contexto carregado por uma sessão para continuar uma execução longa, preservando o estado essencial com alguma perda de detalhe do histórico original.

## Como é usado

Use **Compaction** como mecanismo de continuidade, não como fonte de verdade. Antes de uma compactação, mantenha decisões, critérios, estado e próximos passos em arquivos persistentes como SPEC, AGENTS ou [[Rider]], para que o resumo não precise carregar tudo na memória da conversa.

**Exemplo prático:** na aula [[11-goal-vs-loop]], uma execução longa depende de sessão e compaction para continuar, mas SPEC, AGENTS e Rider permanecem no repositório; depois da compactação, o agente relê esses contratos antes de retomar o loop.

**Não confunda:** **Compaction** é uma ação de redução ou resumo do histórico; [[Context bloat]] é a condição de contexto inchado que pode motivá-la; [[Janela de Contexto]] é o limite e a faixa útil em que o modelo trabalha.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[11-goal-vs-loop]]
- [[16-janela-de-contexto]]
- [[17-engenharia-de-contexto]]

## Ver também

- [[Context bloat]]
- [[Janela de Contexto]]
- [[Handoff]]
- [[Rider]]
- [[Glossário AIOX Advanced]]
