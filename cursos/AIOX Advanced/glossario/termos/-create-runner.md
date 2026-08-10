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
  aiox_advanced: 12
  aiox_advanced_squads: 0
  total: 12
  counted_at: '2026-08-10'
---
# /create-runner

A skill que faz scaffold de um Runner novo a partir dos templates e guardrails canônicos de runner-lib.

## Como é usado

Acione **/create-runner** quando um procedimento já validado precisar virar um Runner determinístico: a skill gera o scaffold — estrutura de pastas, contrato de entrada/saída, guardrails — a partir dos templates canônicos de runner-lib, em vez de você montar tudo à mão e esquecer alguma proteção.

**Exemplo prático:** na aula [[30-runner-executavel-deterministico]], o operador parte de um briefing como "gerar o relatório semanal de métricas", roda **/create-runner**, revisa o scaffold produzido (entrada esperada, passos, saída, guardrails) e só então preenche a lógica específica — o resultado é um Runner que repete o procedimento sem depender de prompt.

**Não confunda:** rodar **/create-runner** não é o mesmo que ter um Runner pronto: a skill entrega o esqueleto com guardrails; a lógica do procedimento, o teste com dados reais e a definição do ambiente de execução continuam sendo trabalho seu.

**Frequência nos cursos:** **12** menções (AIOX Advanced: 12 · AIOX Advanced Squads: 0).

## Aulas

- [[30-runner-executavel-deterministico]]

## Ver também

- [[Glossário AIOX Advanced]]
