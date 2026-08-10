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
  aiox_advanced: 7
  aiox_advanced_squads: 0
  total: 7
  counted_at: '2026-08-10'
---
# Model routing

Escolher o modelo certo por tipo de tarefa (custo, modalidade, qualidade) e separar quem executa de quem revisa.

## Como é usado

Use **Model routing** ao montar o fluxo de trabalho: classifique cada tarefa por exigência (mecânica ou crítica, texto ou multimodal, volume ou precisão) e roteie para o modelo com o melhor custo-benefício — garantindo que quem revisa não é o mesmo motor que executou.

**Exemplo prático:** na aula [[60-routing-modelos]], a geração em lote de descrições vai para um modelo rápido e barato, a decisão de arquitetura vai para o modelo mais forte disponível, e o review do PR usa um motor diferente do que escreveu o código (no-self-review).

**Não confunda:** **Model routing** não é usar sempre o modelo mais caro "para garantir": é uma decisão declarada de custo, modalidade e qualidade por tipo de tarefa — e a separação executor/revisor faz parte da regra, não é opcional.

**Frequência nos cursos:** **7** menções (AIOX Advanced: 7 · AIOX Advanced Squads: 0).

## Aulas

- [[60-routing-modelos]]
- [[06-code-rabbit-boost]]

## Ver também

- [[Three-brain]]
- [[No-self-review]]
- [[CodeRabbit]]
- [[Token Economy]]
- [[Glossário AIOX Advanced]]
