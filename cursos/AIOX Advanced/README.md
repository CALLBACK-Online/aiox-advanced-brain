---
type: course
course: aiox-advanced
title: AIOX Advanced
status: canonical
canonical_scope: cursos/AIOX Advanced
sharing_boundary: cursos
source: upstream monorepo/apps/aiox-courses
source_format: lesson.md (via content-to-md.mjs)
source_version: 2.0.0
source_status: ready_to_ship
synced_at: 2026-08-10
curriculum_modules: 6
lessons: 28
quizzes: 6
questions: 48
tags: [curso, aiox-advanced, metodo, sdc, determinismo, layer/curso]
---

# AIOX Advanced

> Da intenção ao sistema entregue: método, contexto, SDC, determinismo e evidência.

O Advanced volta a ter uma promessa única. Ele ensina **como conduzir o trabalho com AIOX**. Construção de capacidades agentic, design e monetização possuem cursos próprios.

**Aulas ativas:** 28 · **Módulos:** 5 + Capstone · **Quizzes:** 6 · **Questões:** 48

- Avaliações: [[Assessments|6 checkpoints e 48 questões]]
- Conclusão: [[Projeto Integrador]] · [[Rubrica]]
- Mapa histórico (75 aulas): [[MOC-Todas-Aulas]]
- Dúvidas de campo: [[support/README|Central de suporte]]
- Histórico: [[archive/README|Arquivo curricular da edição de 75 aulas]]

## Fronteira curricular

| Pergunta | Curso dono |
|---|---|
| Como operar o método AIOX do briefing à evidência? | **AIOX Advanced** |
| Como projetar agents, squads, workflows, runners e runtime? | `cursos/AIOX-Agent-Engineering/` |
| Como construir contrato visual e sistema de design? | `cursos/AIOX-Design/` |
| Como transformar capacidade em oferta e monetização? | `cursos/AIOX-Productizacao/` |
| Como escolher e operar um squad publicado? | `cursos/AIOX-Advanced-Squads/` |

As bases continuam em `cursos/Introducao-a-Arquitetura-de-Sistemas/` e `cursos/AIOX-Fundamentals/`. A ordem recomendada de todo o acervo está em `cursos/README.md`.

## Gate de entrada

Você consegue instalar ou auditar o AIOX Core, escolher um agent e concluir uma story local com evidência. Se isso ainda não é verdade, use [[ponte/pre-requisitos-arquitetura|Pré-requisitos de arquitetura e Core]].

## Resultado do curso

Ao concluir, você consegue:

1. estruturar o problema antes de delegar;
2. manter leis, contexto e ambientes sob controle;
3. transformar briefing em stories e fechar o SDC com quality gates;
4. escolher determinismo e autonomia proporcionais ao risco;
5. atuar em brownfield com evidência do sistema real;
6. entregar uma fatia funcional, auditável e reproduzível.

## Módulos

1. [[modulos/Módulo 0 - Mindset e Princípios|M0 — Mindset e princípios]] — 5 aulas
2. [[modulos/Módulo 1 - Sistema e Contexto|M1 — Sistema e contexto]] — 8 aulas
3. [[modulos/Módulo 2 - SDC e Qualidade|M2 — SDC e qualidade]] — 5 aulas
4. [[modulos/Módulo 3 - Determinismo e Comando|M3 — Determinismo e comando]] — 4 aulas
5. [[modulos/Módulo 4 - Método e Brownfield|M4 — Método e brownfield]] — 4 aulas
6. [[modulos/Módulo C - Capstone|Capstone — Sinais em sistema entregue]] — 2 aulas

## Sequência ativa

### M0 — Mindset e princípios

1. [[aulas/01-token-economy-mindset|Token Economy Mindset]]
2. [[aulas/08-principio-processo-certo|Respeite o processo]]
3. [[aulas/12-repertorio-vs-tecnica|Repertório vence técnica]]
4. [[aulas/13-pensamento-estruturado-antes-do-terminal|Desenhe antes de codar]]
5. [[aulas/26-nao-delegar-pensar|Não delegue o pensar]]

### M1 — Sistema e contexto

6. [[aulas/03-claude-md-leis-da-fisica|CLAUDE.md como lei da física]]
7. [[aulas/05-ambientes-local-staging-production|Local, staging e production]]
8. [[aulas/15-quatro-executores|Quatro executores]]
9. [[aulas/16-janela-de-contexto|Janela de contexto]]
10. [[aulas/17-engenharia-de-contexto|Engenharia de contexto]]
11. [[aulas/18-yaml-markdown-json-sweet-spot|YAML, Markdown e JSON]]
12. [[aulas/25-core-config-leis-sociais|core-config]]
13. [[aulas/27-otimizacao-claude-md|Otimização do CLAUDE.md]]

### M2 — SDC e qualidade

14. [[aulas/06-code-rabbit-boost|CodeRabbit Boost]]
15. [[aulas/19-ciclo-do-repositorio|Ciclo do repositório]]
16. [[aulas/46-etapas-de-desenvolvimento|Briefing, PRD e stories]]
17. [[aulas/48-quality-gate-completo|Quality Gate completo]]
18. [[aulas/49-apply-qa-fixes-loop|Apply QA Fixes Loop]]

### M3 — Determinismo e comando

19. [[aulas/11-goal-vs-loop|Goal vs Loop]]
20. [[aulas/20-determinismo-progressivo|Determinismo progressivo]]
21. [[aulas/21-deterministico-primeiro-llm-onde-gera-ouro|Determinístico primeiro]]
22. [[aulas/50-rider-modo-elicitacao|Rider: operador como piloto]]

### M4 — Método e brownfield

23. [[aulas/23-o-que-e-um-squad|O que é um squad]]
24. [[aulas/24-entidade-como-unidade-de-processo|Entidade como unidade de processo]]
25. [[aulas/31-brownfield-discovery|Brownfield Discovery]]
26. [[aulas/53-brownfield-enhancement|Brownfield Enhancement]]

### Capstone

27. [[aulas/44-metodo-s2s|Método S2S]]
28. [[aulas/74-caso-integrado-end-to-end|Caso integrado end-to-end]]

## O que mudou na edição 2.0

- 27 aulas passaram a compor AIOX Agent Engineering.
- 6 aulas foram absorvidas por AIOX Design.
- 5 aulas passaram a AIOX Productização.
- 4 aulas sobre sistema, agentes e story ficaram como histórico por sobreposição com as bases.
- 4 versões substituídas e 1 FAQ saíram da contagem curricular.

Nada foi descartado. A rastreabilidade está em [[archive/README|archive/]] e no frontmatter das novas aulas.

## Depois do Advanced

O Advanced encerra o núcleo comum. Escolha a próxima rota pelo resultado exigido pela missão:

- construa capacidades próprias em `cursos/AIOX-Agent-Engineering/`;
- materialize contrato visual em `cursos/AIOX-Design/`;
- opere um pacote publicado em `cursos/AIOX-Advanced-Squads/`;
- productize uma capacidade comprovada em `cursos/AIOX-Productizacao/`.

Gate, artefato de passagem e combinações: [[ponte/trilhas-de-aplicacao|Rotas de aplicação depois do Advanced]].

O curso termina com artefato funcionando e evidência verificável, não com consumo de conteúdo.
