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
  aiox_advanced_squads: 27
  total: 27
  counted_at: '2026-08-10'
---
# Generic prompt

Instrução portátil da rota que carrega o `config.yaml`, o agente de entrada e a missão quando o runtime não oferece um comando, skill ou registro de agente confirmado.

## Como é usado

Use **Generic prompt** como fallback seguro. Depois de escolher a rota, copie o texto de `generic_prompt` em `agent-router.json`, acrescente o briefing e peça ao agente que leia os paths indicados. A aula [[cursos/AIOX-Advanced-Squads/aulas/00-como-usar-este-curso]] ensina a usar o briefing quando a superfície do runtime não existe.

**Exemplo prático:** para Runner Ops, o prompt da rota diz: “Leia `squads/runner-ops/config.yaml` e `squads/runner-ops/agents/runner-chief.md`. Configure execução headless com estado, orçamento, métricas e evidência de conclusão.” Em seguida, acrescente a missão concreta e os critérios de aceite; o agente deve confirmar a rota antes de operar.

**Não confunda:** **Generic prompt** não é um comando registrado e não cria a integração por si só. Ele é texto de contexto que funciona em um agente genérico. `/prefixo:comando`, `@runner-chief`, `$runner-ops` e `*task` só podem ser usados quando o runtime e o pacote registrarem essas superfícies, como explica o [[cursos/AIOX-Advanced-Squads/Guia-de-execucao]].

**Frequência nos cursos:** **27** menções (AIOX Advanced: 0 · AIOX Advanced Squads: 27).

## Aulas

- [[cursos/AIOX-Advanced-Squads/aulas/00-como-usar-este-curso]]
- [[cursos/AIOX-Advanced-Squads/aulas/09-runner-ops]]
- [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad]]
- [[cursos/AIOX-Advanced-Squads/aulas/14-design-system]]
- [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]]
- [[cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro]]

## Ver também

- [[Roteamento de squad]]
- [[Orquestrador]]
- [[Harness]]
- [[Maturidade]]
- [[cursos/AIOX-Advanced-Squads/Guia-de-execucao]]
- [[Glossário AIOX Advanced]]
