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
  aiox_advanced: 28
  aiox_advanced_squads: 0
  total: 28
  counted_at: '2026-08-10'
---
# Gemini

Motor Google citado no roteamento multi-modelo (three-brain) para tarefas e revisões sem autorrevisão.

## Como é usado

Use **Gemini** como o cérebro de pesquisa no routing multi-modelo do AIOX: cada tarefa vai para o modelo com melhor fitness — Codex para QA, Gemini para research com citações e grounding, Claude para orquestração e o resto. Um segundo modelo também entra como revisor externo, evitando a autorrevisão de quem gerou o código.

**Exemplo prático:** na aula [[60-routing-modelos]], a tabela de routing declara a linha "Research → Gemini-class, fallback Claude long, evidência: citações/fontes": a escolha do modelo vem com fallback e métrica, e uma tarefa de pesquisa que sai sem fontes citadas falhou no critério, não importa o modelo.

**Não confunda:** incluir Gemini não é colecionar assinaturas de modelo: sem tabela de routing, fallback e evidência esperada por tipo de tarefa, trocar de modelo é "opinião de stand-up", não roteamento por fitness.

**Frequência nos cursos:** **28** menções (AIOX Advanced: 28 · AIOX Advanced Squads: 0).

## Aulas

- [[60-routing-modelos]]
- [[06-code-rabbit-boost]]

## Ver também

- [[Model routing]]
- [[Three-brain]]
- [[CodeRabbit]]
- [[Glossário AIOX Advanced]]
