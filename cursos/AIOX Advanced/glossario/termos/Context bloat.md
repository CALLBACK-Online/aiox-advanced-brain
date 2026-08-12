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
  aiox_advanced: 5
  aiox_advanced_squads: 0
  total: 5
  counted_at: '2026-08-10'
---
# Context bloat

Acúmulo de histórico, arquivos, comandos, skills e MCPs dentro do contexto de uma sessão, consumindo a faixa útil e degradando gradualmente a atenção do modelo.

## Como é usado

Use **Context bloat** para nomear o problema operacional antes de escolher a correção. Meça a ocupação, identifique o peso morto e decida entre limpar, exportar o estado ou recomeçar com apenas as fontes relevantes.

**Exemplo prático:** na aula [[16-janela-de-contexto]], o comando `/context` mostra histórico longo e arquivos inteiros ocupando quase toda a sessão; o operador exporta o trabalho, limpa o contexto e recarrega só o trecho necessário antes de continuar.

**Não confunda:** **Context bloat** é uma condição de contexto inchado; [[Janela de Contexto]] é o limite e a faixa de qualidade que a sessão pode usar. Bloat é excesso de carga, não o tamanho da janela em si.

**Frequência nos cursos:** **5** menções (AIOX Advanced: 5 · AIOX Advanced Squads: 0).

## Aulas

- [[16-janela-de-contexto]]
- [[17-engenharia-de-contexto]]
- [[11-goal-vs-loop]]
- [[76-orientacao-do-agente]]

## Ver também

- [[Janela de Contexto]]
- [[Engenharia de Contexto]]
- [[Compaction]]
- [[Handoff]]
- [[Glossário AIOX Advanced]]
