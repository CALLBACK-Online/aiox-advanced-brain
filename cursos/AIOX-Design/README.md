---
type: course
course: aiox-design
title: AIOX Design
status: canonical
canonical_scope: cursos/AIOX-Design
sharing_boundary: cursos
source: lives Advanced T1-04/T2-03 + seeds 32/41-43/56-57 + expansão teach v2
source_version: 2.0.0
curriculum_modules: 6
lessons: 20
quizzes: 5
questions: 20
tags: [curso, design, design-system, layer/curso]
---

# AIOX Design

> Do repertório ao Storybook: contrato visual que humano e agente compartilham.

Curso de **design system para IA**: decisão, referências, Brand Book→tokens, DESIGN.md, taxonomia, Storybook como fonte da verdade, governança multi-produto e capstone **executável**.

**Aulas:** 20 · **Módulos:** 6 · **Quizzes:** 5 · **Questões:** 20 · **Capstone:** Storybook obrigatório

- [Brief](COURSE-BRIEF.md) · [Outline](course-outline.md) · [Expansão / proveniência](CURRICULUM-EXPANSION.md)
- [Casos live](casos-live-cohort.md)
- [Avaliações](Assessments.md) · [Rubrica](Rubrica.md) · [Projeto integrador](Projeto-Integrador.md)
- [Glossário](Glossario.md) · [Fontes](FONTES.md) · [AGENT-GUIDE](AGENT-GUIDE.md)
- Pontes: [brand→contrato](ponte/brand-book-para-contrato.md) · [pré-reqs Advanced](ponte/pre-requisitos-advanced.md) · [squads design](ponte/trilha-squads-design.md)

## Progressão teach

```text
M0 Contexto/decisão → M1 Direção visual → M2 Contrato
        → M3 Materialização (Storybook) → M4 Governança → M5 Capstone
```

Uma competência por aula · prática curta · evidência verificável · navegação interna.

## Módulos

1. [M0 — Decisão e repertório](modulos/M0.md) — 01–03
2. [M1 — Direção visual e marca](modulos/M1.md) — 04–06
3. [M2 — Contrato e catálogo](modulos/M2.md) — 07–10
4. [M3 — Storybook como SoT](modulos/M3.md) — 11–14
5. [M4 — Governança e qualidade](modulos/M4.md) — 15–18
6. [M5 — Operação e capstone](modulos/M5.md) — 19–20

## Todas as aulas

1. [Design system é decisão](aulas/01-design-system-e-decisao.md)
2. [Greenfield vs brownfield](aulas/02-design-system-greenfield-brownfield.md)
3. [Repertório e referências](aulas/03-repertorio-e-referencias.md)
4. [Tema visual vs DS](aulas/04-tema-visual-vs-design-system.md)
5. [Top-down vs bottom-up](aulas/05-top-down-vs-bottom-up.md)
6. [Brand Book → tokens](aulas/06-brand-book-para-tokens.md)
7. [Anti-AI-look e exploração](aulas/07-anti-ai-look-e-exploracao.md)
8. [DESIGN.md](aulas/08-design-md-contrato.md)
9. [Tokens e anti-drift](aulas/09-tokens-componentes-anti-drift.md)
10. [Design atômico (Brad Frost) / taxonomia](aulas/10-taxonomia-atomica.md)
11. [Storybook como SoT](aulas/11-storybook-fonte-da-verdade.md)
12. [Stack canônica](aulas/12-stack-tailwind-shadcn-storybook.md)
13. [Install e stories](aulas/13-storybook-install-e-stories.md)
14. [Variantes e a11y](aulas/14-storybook-variantes.md)
15. [Governança](aulas/15-governanca-e-permissoes.md)
16. [Multi-produto](aulas/16-ds-multi-produto.md)
17. [Ciclo screenshot](aulas/17-ciclo-screenshot-correcao.md)
18. [Portão visual](aulas/18-portao-qualidade-visual.md)
19. [Skill vs squad](aulas/19-skill-vs-squad-design.md)
20. [Capstone Storybook](aulas/20-capstone-ds-storybook-executavel.md)

## Capstone (v2)

**Storybook local rodando** com stories mínimas + DESIGN.md + ciclo de correção.
Bloqueio de ambiente ≠ Done. Chromatic opcional.

## Fronteiras

| Não é | Dono |
|-------|------|
| Brand estratégico | `squads/brand/` |
| Oferta/SaaS | `cursos/AIOX-Productizacao/` |
| Harness/runtime | `cursos/AIOX-Agent-Engineering/` |
| Runbook 100+ tasks | Squads 14–15 |

Hub: `cursos/README.md`.
