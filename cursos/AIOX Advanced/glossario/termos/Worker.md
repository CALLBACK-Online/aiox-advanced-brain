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
  aiox_advanced: 78
  aiox_advanced_squads: 1
  total: 79
  counted_at: '2026-08-10'
---
# Worker

Executor focado em trabalho mecânico e repetível na taxonomia dos Quatro Executores. Recebe limites claros, transforma uma entrada e devolve uma saída; não assume decisão aberta nem decisão final.

## Como é usado

Use **Worker** para delegar uma operação previsível e delimitada, como varrer arquivos, normalizar dados ou repetir uma validação, deixando exceções e decisões novas para um Agent ou Humano.

**Exemplo prático:** nas aulas [[15-quatro-executores]] e [[30-runner-executavel-deterministico]], entregue ao **Worker** uma pasta e regras de normalização; ele processa os arquivos, produz o relatório e encaminha casos fora do padrão para revisão.

**Não confunda:** **Worker** não escolhe o escopo nem resolve ambiguidade de negócio: ele executa o procedimento delimitado; Agent raciocina sobre exceções e Humano mantém a decisão final.

**Frequência nos cursos:** **79** menções (AIOX Advanced: 78 · AIOX Advanced Squads: 1).

## Aulas

- [[15-quatro-executores]]
- [[30-runner-executavel-deterministico]]

## Ver também

- [[Quatro Executores]]
- [[Agent]]
- [[Humano]]
- [[Clone]]
- [[Runner]]
- [[Glossário AIOX Advanced]]
