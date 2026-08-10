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
  aiox_advanced: 35
  aiox_advanced_squads: 0
  total: 35
  counted_at: '2026-08-10'
---
# Paralelização

Rodar frentes em paralelo. Só depois de decidir se o grafo de dependências e o ownership de arquivos permitem — senão vira conflito.

## Como é usado

Use **Paralelização** só depois de duas checagens: o grafo de dependências permite frentes independentes? Cada frente tem ownership exclusivo dos arquivos que vai tocar? Sem essas duas respostas, o paralelo vira conflito de merge.

**Exemplo prático:** Na aula [[59-quando-paralelizar-vs-sequencial]], três Stories independentes que tocam pastas distintas rodam com três agentes em paralelo; quando duas frentes precisam do mesmo arquivo, a execução vira sequencial ou entra um lock de sequência — e a decisão é registrada antes de disparar.

**Não confunda:** **Paralelização** não é acelerar tudo de uma vez: frentes com dependência entre si ou com arquivos compartilhados produzem conflito e retrabalho — o tempo "ganho" volta como merge quebrado.

**Frequência nos cursos:** **35** menções (AIOX Advanced: 35 · AIOX Advanced Squads: 0).

## Aulas

- [[59-quando-paralelizar-vs-sequencial]]
- [[58-ralph-paralelizacao]]
- [[61-wave-execute]]

## Ver também

- [[Ralph]]
- [[Wave Execute]]
- [[Glossário AIOX Advanced]]
