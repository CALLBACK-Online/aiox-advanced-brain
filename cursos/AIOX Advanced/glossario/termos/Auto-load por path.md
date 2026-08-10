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
  aiox_advanced: 2
  aiox_advanced_squads: 0
  total: 2
  counted_at: '2026-08-10'
---
# Auto-load por path

Regra específica de caminho que entra no contexto somente quando o agente trabalha em um path coberto, mantendo detalhes fora das sessões irrelevantes.

## Como é usado

Use **Auto-load por path** para ativar uma instrução no momento em que o agente entra no diretório ou arquivo correspondente, reduzindo o contexto global sem perder uma regra necessária naquele trecho.

**Exemplo prático:** na aula [[27-otimizacao-claude-md]], coloque as regras de tokens e acessibilidade em uma regra carregada para `src/components/**`; ao editar uma tela, confirme que ela foi aplicada e que uma task de backend não carregou esse detalhe.

**Não confunda:** **Auto-load por path** decide quando carregar contexto, não quem tem permissão para editar nem qual agente executará a tarefa. Ativar uma regra pelo caminho não substitui autoridade, escopo ou gate.

**Frequência nos cursos:** **2** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 0).

## Aulas

- [[27-otimizacao-claude-md]]

## Ver também

- [[Glossário AIOX Advanced]]
