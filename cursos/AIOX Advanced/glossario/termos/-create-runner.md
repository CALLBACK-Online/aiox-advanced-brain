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

Acione **/create-runner** quando um Workflow já estável precisar virar um Runner determinístico: a skill gera o scaffold — estrutura de pastas, contrato de entrada/saída, guardrails — a partir dos templates canônicos de runner-lib (o runtime que vive em `infrastructure/scripts/runner-lib/`), em vez de você montar tudo à mão e esquecer alguma proteção.

**Exemplo prático:** na aula [[30-runner-executavel-deterministico]], o operador parte de um procedimento validado como "gerar o relatório semanal de métricas", roda **/create-runner**, revisa o scaffold produzido (entrada esperada, passos, saída, guardrails), preenche a lógica específica e valida com a suíte do runner-lib (`npm test` e o floor de cobertura) — o resultado é um Runner que repete o procedimento igual toda vez, sem depender de prompt.

**Não confunda:** rodar **/create-runner** não é o mesmo que ter um Runner pronto: a skill entrega o esqueleto com guardrails, mas a lógica do procedimento e o teste com dados reais continuam sendo trabalho seu — e o Workflow precisa ter estabilizado antes; Runner improvisado para processo que ainda muda é o anti-padrão apontado na aula.

**Frequência nos cursos:** **12** menções (AIOX Advanced: 12 · AIOX Advanced Squads: 0).

## Aulas

- [[30-runner-executavel-deterministico]]

## Ver também

- [[Glossário AIOX Advanced]]
