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
  aiox_advanced: 15
  aiox_advanced_squads: 31
  total: 46
  counted_at: '2026-08-10'
---
# Roteamento de squad

Contrato que transforma uma necessidade em linguagem natural na rota de squad adequada, com sinais, anti-sinais, entradas, entrega, evidências, limites e agente de entrada definidos.

## Como é usado

Use **Roteamento de squad** seguindo o algoritmo da [[cursos/AIOX-Advanced-Squads/AGENT-GUIDE]]: extraia verbo, objeto, estado e entrega; consulte o [[cursos/AIOX-Advanced-Squads/Mapa-de-decisao]]; compare as rotas candidatas em `cursos/AIOX-Advanced-Squads/agent-router.json`; confirme o anti-escopo na aula; e só então verifique runtime, maturidade e dependências.

**Exemplo prático:** “quero operar uma pipeline fora da IDE com estado, orçamento e métricas” aponta para `runner-ops`, porque bate nos sinais de execução headless e pipeline agendado. “Quero extrair, transformar e carregar uma fonte” aponta para `etl-ops`, não Runner Ops. O roteamento registra ainda `runner-chief` ou `etl-chief`, os inputs e a evidência esperada; não escolhe apenas pelo nome parecido.

**Não confunda:** um alias é só uma pista de busca — por exemplo, `runner headless` ou `criar squad`. O **Roteamento de squad** é o contrato completo da rota: inclui `signals`, `anti_signals`, `lesson`, `squad_path`, `entry_agent`, `inputs`, `deliverable`, `evidence`, `limits` e `generic_prompt`. Alias não substitui comparação de fronteiras nem validação de existência.

**Frequência nos cursos:** **46** menções (AIOX Advanced: 15 · AIOX Advanced Squads: 31).

## Aulas

- [[cursos/AIOX-Advanced-Squads/aulas/00-como-usar-este-curso]]
- [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]]
- [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad]]
- [[cursos/AIOX-Advanced-Squads/aulas/14-design-system]]
- [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]]
- [[cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro]]

## Ver também

- [[Orquestrador]]
- [[Anti-escopo]]
- [[Briefing]]
- [[Generic prompt]]
- [[cursos/AIOX-Advanced-Squads/Mapa-de-decisao]]
- [[Glossário AIOX Advanced]]
