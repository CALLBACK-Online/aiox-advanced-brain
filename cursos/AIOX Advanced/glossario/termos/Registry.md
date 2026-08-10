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
  aiox_advanced: 2
  aiox_advanced_squads: 3
  total: 5
  counted_at: '2026-08-10'
---
# Registry

Registro estruturado e consultável de capacidades, componentes ou rotas, com identidade, paths, estado e referências suficientes para descoberta, validação e ativação.

## Como é usado

Use **Registry** quando nomes soltos já não bastam para governar um ecossistema. O registro deve permitir responder o que existe, onde está, como é ativado e se pode ser usado. Na aula [[cursos/AIOX-Advanced-Squads/aulas/14-design-system]], o registry organiza tokens e componentes; em [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]], o inventário de `catalog.json` e o ciclo Validate–Discover–Install evitam instalar um squad quebrado.

**Exemplo prático:** uma rota em `agent-router.json` não guarda apenas o nome do squad: traz `lesson`, `squad_path`, `entry_agent`, sinais, anti-sinais, inputs, deliverable, evidence, limits e `generic_prompt`. No ClickUp Ops, a task `mapped-atm-assemble-registry` monta o registro da materialização. Em todos os casos, o registro serve para conferir e operar, não só para exibir uma lista.

**Não confunda:** **Registry** não é um catálogo informal de nomes e descrições mantido de memória. Um catálogo pode ser índice humano; o registry é um contrato estruturado, com campos e autoridade de atualização, que sustenta discovery, validação, lifecycle ou ativação. Ter uma pasta `components/` ou uma lista de squads não prova que exista registry utilizável.

**Frequência nos cursos:** **5** menções (AIOX Advanced: 2 · AIOX Advanced Squads: 3).

## Aulas

- [[cursos/AIOX-Advanced-Squads/aulas/12-clickup-ops-squad]]
- [[cursos/AIOX-Advanced-Squads/aulas/14-design-system]]
- [[cursos/AIOX-Advanced-Squads/aulas/23-squad-creator]]
- [[cursos/AIOX-Advanced-Squads/aulas/24-squad-creator-pro]]

## Ver também

- [[Design System]]
- [[Roteamento de squad]]
- [[Squad]]
- [[Materialização]]
- [[Maturidade]]
- [[Glossário AIOX Advanced]]
