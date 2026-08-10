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
# SYNAPSE

Camada de orquestração do runtime AIOX completo, relevante quando o agente sai do laboratório e precisa coordenar execução persistente; não faz parte do pacote deste acervo só-biblioteca.

## Como é usado

Use **SYNAPSE** apenas quando o destino realmente tiver o runtime AIOX correspondente. Descreva jobs, roteamento, ferramentas, limites e observabilidade; neste acervo, trate o termo como referência arquitetural, não como runtime disponível.

**Exemplo prático:** na aula [[67-harness-ambiente-execucao]], se a triagem de tickets precisar rodar 24/7 para um cliente, mapeie runtime, autenticação, tools, logs e budget e registre onde a orquestração profunda dependeria de **SYNAPSE**; não declare essa ativação neste pacote.

**Não confunda:** **SYNAPSE** não é o Claude Code, um harness ou um squad. É uma camada de runtime; citar o nome em uma aula não significa que ela esteja instalada, configurada ou executável no projeto atual.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[67-harness-ambiente-execucao]]
- [[02-aiox-nao-e-ferramenta]]

## Ver também

- [[Runtime AIOX]]
- [[Harness]]
- [[Software House no Computador]]
- [[Glossário AIOX Advanced]]
