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
  aiox_advanced: 9
  aiox_advanced_squads: 16
  total: 25
  counted_at: '2026-08-10'
---
# SOP

Standard Operating Procedure: procedimento repetível, escrito para humano e/ou agente, com pré-condições, passos, entradas, saídas, critérios e tratamento de exceções. Sai da cabeça e vira execução auditável.

## Como é usado

Use **SOP** quando uma operação recorrente precisa produzir o mesmo resultado mesmo com outro executor. Especifique sequência, responsável, evidência esperada e o que fazer quando um check falhar.

**Exemplo prático:** um SOP de ETL manda validar a fonte, extrair os dados, conferir a contagem de linhas, salvar o relatório e abrir exceção se houver divergência; outro executor consegue seguir e deixar a mesma evidência.

**Não confunda:** **SOP** não é uma explicação conceitual nem uma lista de desejos. Ele descreve uma operação executável e auditável; um workflow pode ordenar etapas, mas não substitui os passos e critérios do SOP.

**Frequência nos cursos:** **25** menções (AIOX Advanced: 9 · AIOX Advanced Squads: 16).

## Aulas

- [[39-pasta-os-curadoria-local]]
- [[22-pipeline-etl-com-agentes]]
- [[30-runner-executavel-deterministico]]

## Ver também

- [[Runner]]
- [[Workflow]]
- [[Pasta OS]]
- [[Artefato]]
- [[Glossário AIOX Advanced]]
