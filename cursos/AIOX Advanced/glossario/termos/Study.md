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
  aiox_advanced: 0
  aiox_advanced_squads: 5
  total: 5
  counted_at: '2026-08-10'
---
# Study

Label de maturidade: ler anatomia, agentes e tasks; orientar — sem prometer execução autônoma no laptop nu.

## Como é usado

Use **Study** como label de maturidade no `catalog.json` deste acervo: um squad ou skill marcado `study` serve para ler a anatomia — agentes, tasks, workflows, config — e orientar a execução, sem prometer que roda autônomo no "laptop nu", fora do runtime completo.

**Exemplo prático:** na aula [[33-anatomia-de-um-squad]], uma resposta roteada declara a maturidade no cabeçalho ("Maturidade: study"): o operador estuda o `config.yaml` e os agentes do squad neste repositório, mas a execução real acontece no projeto destino, com as dependências que o squad exige instaladas.

**Não confunda:** `study` não é squad quebrado nem rascunho: é a promessa honesta do que este acervo entrega para aquele item — anatomia legível e orientação. Prometer execução autônoma para um item `study` é inflar maturidade.

**Frequência nos cursos:** **5** menções (AIOX Advanced: 0 · AIOX Advanced Squads: 5).

## Aulas

- [[28-taxonomia-task-skill-agent-workflow-runner]]
- [[33-anatomia-de-um-squad]]

## Ver também

- [[Maturidade]]
- [[Portable]]
- [[Runtime AIOX]]
- [[Glossário AIOX Advanced]]
