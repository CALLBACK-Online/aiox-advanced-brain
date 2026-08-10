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
  aiox_advanced: 57
  aiox_advanced_squads: 17
  total: 74
  counted_at: '2026-08-10'
---
# ETL

Extract → Transform → Load: extrair, transformar e carregar dados. No AIOX, é um fluxo repetível de materialização, com etapas que podem ser conferidas e retomadas.

## Como é usado

Use **ETL** quando dados precisam sair de uma fonte e chegar a um destino de forma repetível: extraia, normalize para o schema alvo e carregue com checkpoint em cada etapa.

**Exemplo prático:** na aula [[22-pipeline-etl-com-agentes]], um collector extrai, um transformador normaliza e o loader carrega no Supabase ([[70-supabase-via-data-engineer]]); cada etapa registra checkpoint.

**Não confunda:** ETL sem checkpoints e evidência pode duplicar ou corromper dados. E um script único que "puxa e joga" não é pipeline: sem etapas separadas e verificáveis, não há onde inspecionar nem de onde retomar.

**Frequência nos cursos:** **74** menções (AIOX Advanced: 57 · AIOX Advanced Squads: 17).

## Aulas

- [[22-pipeline-etl-com-agentes]]
- [[70-supabase-via-data-engineer]]

## Ver também

- [[Pipeline canônico]]
- [[Runner]]
- [[Supabase]]
- [[Glossário AIOX Advanced]]
