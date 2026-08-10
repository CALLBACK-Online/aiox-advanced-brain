---
type: course-brief
course: aiox-design
course_slug: aiox-design
status: canonical
created_date: "2026-08-10"
materialized_date: "2026-08-10"
instructor: "Equipe AIOX"
canonical_scope: cursos/AIOX-Design
sharing_boundary: cursos
source: curadoria de cursos/AIOX Advanced/lessons (M6/M9) + squads design-* + skills design-*
tags: [curso, design, design-system, layer/curso]
---

# COURSE BRIEF — AIOX Design

> Design system e contrato visual para humanos e agentes — sem virar curso de Figma nem runbook de squad.

**Estado:** materializado (aulas + quizzes + validador). Brief permanece como contrato curricular.

Outline detalhado: [`course-outline.md`](course-outline.md).

---

## 1. Basic info

| Campo | Valor |
|-------|--------|
| **Título** | AIOX Design |
| **Subtítulo** | Do gosto por tela ao contrato que a IA lê antes de gerar interface |
| **Slug** | `aiox-design` |
| **Pasta prevista** | `cursos/AIOX-Design/` |
| **Duração estimada** | 3h30–4h15 (leitura + exercícios + capstone), sem contar operação real de squad |
| **Categoria** | Design system · UI com agentes · contrato de produto |
| **Tipo** | Misto (critério + artefato + ponte operacional) |
| **Nível** | Intermediário (assume que a pessoa já gera UI com IA e sofre deriva) |
| **Formato** | Self-paced Markdown (Obsidian / GitHub), autocontido em `cursos/AIOX-Design/` |

---

## 2. Problema que o curso resolve

### Dor superficial

“A IA gera telas diferentes a cada prompt; parece AI slop; não sei se preciso de design system.”

### Dor real

Não existe **decisão visual registrada** (token + regra + componente). Cada geração **redecide** cor, espaço e hierarquia. Retrabalho infinito; marca incoerente; QA visual impossível.

### Dor profunda

A pessoa controla código e processo (CLAUDE.md, stories, gates), mas o **visual fica fora do método** — o agente inventa estética no gosto.

### Antes → depois

| Antes | Depois |
|-------|--------|
| Pede tela; aceita o que vier; corrige pixel a pixel | Decide uma vez; grava em `DESIGN.md`; próxima tela **herda** |
| “Design system” = pasta de componentes soltos | DS = **decisão de arquitetura** + taxonomia + prova de variantes |
| Confunde squad design-system com “aprender design” | Sabe **julgar** o contrato e **quando** chamar squad/skill |

---

## 3. Público-alvo (ICP)

- Builders e devs que usam Claude Code / Codex / agentes para UI.
- PMs / founders técnicos que fecham interface com IA e precisam de coerência.
- Alunos do **AIOX Advanced** que chegaram em M9 (ou travaram em UI) e querem trilha dedicada.
- Quem vai operar `squads/design-system` ou `design-ops` e precisa do **critério**, não só do `@design-chief`.

**Não é o público primário:** designer de produto que só quer portfólio Figma sem agentes; curso de acessibilidade WCAG completo; certificação de design system enterprise genérico.

---

## 4. Objetivos de aprendizagem (curso)

Ao concluir, a pessoa consegue:

1. **Explicar** por que design system no AIOX é decisão registrada (token + regra), não estética por reflexo.
2. **Distinguir** greenfield vs brownfield de DS e escolher a porta de entrada correta.
3. **Redigir ou auditar** um `DESIGN.md` mínimo que um agente leia **antes** de gerar tela (par de CLAUDE.md / AGENTS.md).
4. **Classificar** UI na taxonomia atômica (átomo → página) e aplicar REUSE > ADAPT > CREATE no visual.
5. **Justificar** a stack canônica Tailwind + ShadCN + Storybook *para IA* (não por moda).
6. **Definir** variantes e portões (a11y, dark, responsivo) como evidência, não como “depois a gente vê”.
7. **Roteirizar** skill isolada vs `design-system` vs `design-ops` vs `brand` vs craft (`impeccable`) com anti-escopo claro.
8. **Entregar** um capstone: briefing de tela → contrato + 1 componente com variantes prováveis/descritas.

Bloom dominante: **Apply** e **Evaluate** (não só remember).

---

## 5. Fronteiras (anti-escopo)

| Este curso ensina | Este curso **não** ensina |
|-------------------|---------------------------|
| Critério e contrato visual AIOX | Figma avançado, brand book completo de agência |
| `DESIGN.md`, tokens, taxonomia, Storybook como prova | SDC inteiro, deploy, produtivização (Advanced M0–M12) |
| Quando chamar cada skill/squad de design | Runbook completo de 100+ tasks do squad (→ curso Squads) |
| Anti-deriva e anti-AI-look no nível de **decisão** | Polimento craft pixel a pixel (`impeccable` pós-gate) |
| Ponte para Fundamentos (contratos/formatos) se útil | Arquitetura de sistemas genérica (filas, RLS, fan-out) |

### Separação de cursos

```text
AIOX Advanced (método)     →  story, gates, “UI sem contrato é risco” (ponte fina)
AIOX Design (este)         →  julgamento + artefato visual legível por IA     ← DONO
AIOX Advanced Squads 13–15 →  ativar brand / design-system / design-ops
skills/design-*            →  procedimento no projeto destino (após copiar)
Fund. Arquitetura          →  opcional: contratos, fronteiras (não bloqueia)
```

---

## 6. Pré-requisitos

**Mínimo**

- Já gerou UI (ou pediu UI) com LLM pelo menos uma vez.
- Conforto lendo Markdown e paths de repositório.

**Recomendado (não bloqueante)**

- AIOX Advanced: `02-aiox-nao-e-ferramenta`, `03-claude-md-leis-da-fisica`, `08-principio-processo-certo`.
- Noção de que existe `skills/` e `squads/` neste acervo (`catalog.json`).

**Opcional**

- Introdução à Arquitetura de Sistemas: aula de contratos JSON/YAML/Markdown (`07-…`) se a pessoa não entende “contrato de arquivo”.

---

## 7. Estrutura curricular (resumo)

| Módulo | Nome | Aulas | ~Tempo | Evidência do módulo |
|--------|------|------:|-------:|---------------------|
| **M0** | Decisão, não estética | 2 | 45–55 min | Lista de decisões visuais → token vs pontual |
| **M1** | Contrato e taxonomia | 3 | 70–85 min | Rascunho de `DESIGN.md` + mapa átomo→organismo |
| **M2** | Stack e prova | 3 | 55–70 min | Checklist de variantes + escolha de stack justificada |
| **M3** | Operação e fechamento | 2 | 40–50 min | Rota skill/squad + capstone |

**Totais planejados:** 4 módulos · **10 aulas** · **3 quizzes** (M0–M2) · **1 capstone** (M3) · **1 rubrica**.

Detalhe aula a aula: [`course-outline.md`](course-outline.md).

---

## 8. Fontes seed (acervo existente — não inventar asset)

### Aulas método (AIOX Advanced) — conteúdo a **curar/derivar** (cursos autocontidos)

| Seed | Uso no AIOX Design |
|------|--------------------|
| `lessons/41-design-system-e-decisao.md` | Aula 01 |
| `lessons/32-design-system-greenfield-brownfield.md` | Aula 02 |
| `lessons/43-design-md-novo-contrato.md` | Aula 03 |
| `lessons/42-design-atomico-brad-frost.md` | Aula 04 |
| `lessons/56-tailwind-shadcn-storybook.md` | Aula 06 |
| `lessons/57-storybook-para-variantes.md` | Aula 07 |
| `conceitos/DESIGN md.md` | Conceito âncora / glossário |
| `avaliacoes/Quiz M9 - Design System.md` | Base para quizzes (adaptar) |

### Operação (não copiar runbook; **ponte**)

| Asset | Path |
|-------|------|
| Aula squad design-system | `cursos/AIOX-Advanced-Squads/aulas/14-design-system.md` |
| Aula squad design-ops | `cursos/AIOX-Advanced-Squads/aulas/15-design-ops.md` |
| Aula squad brand | `cursos/AIOX-Advanced-Squads/aulas/13-brand.md` |
| Pacotes | `squads/design-system/`, `squads/design-ops/`, `squads/brand/` |

### Skills (âncora de acervo; maturidade em `catalog.json`)

| Skill | Maturidade (snapshot) | Papel na trilha |
|-------|----------------------|-----------------|
| `design-md` | portable | Contrato / lint de DESIGN.md |
| `design-system` | study | Construir biblioteca |
| `design-ops` | study | Governar no tempo |
| `design-chief` | (catalog) | Orquestrador design |
| `aiox-ux-designer` | (catalog) | UX de build |
| `impeccable` | portable | Craft **pós**-gate (anti-escopo parcial) |
| `brand` | study | Marca (fronteira com M3) |

**Regra de materialização:** aulas do AIOX Design vivem **dentro** de `cursos/AIOX-Design/`; texto derivado dos seeds Advanced; links internos do curso resolvem na própria pasta; assets `skills/` e `squads/` citados em monoespaçado (padrão biblioteca).

---

## 9. Voice e didática (rubrica teach)

Cada aula **deve** ter:

1. **Objetivo verificável** — “Ao final você consegue…” (não “falaremos sobre”).
2. **Ancoragem no acervo** — path real `skills/…`, `squads/…` ou aula irmã.
3. **Exercício ou portão** — prática curta com critério de “passou”.
4. **Navegação** — módulo · anterior · próxima · README (dentro do curso).
5. **Ponte método ↔ operação** — onde couber, bloco “Depois desta aula”.
6. **Termo no glossário** — token, DESIGN.md, átomo, variante, drift, etc.

**Tom:** direto, em português; analogia concreta; anti-hype; anti-receita cega de “só use ShadCN”.

**Relação prática/teoria:** ~65/35.

---

## 10. Avaliação e sucesso

| Artefato | Critério |
|----------|----------|
| Quizzes M0–M2 | Recuperação ativa; gabarito balanceado A/B/C/D se no padrão do acervo |
| Capstone | Ver rubrica em outline: contrato mínimo + 1 componente + rota de operação |
| Métrica de curso | 100% aulas com objetivo + exercício + âncora; 0 paths de máquina; validate verde quando scaffold existir |

**Aprovação curricular:** materializado em 10 aulas + validador (status `canonical`).

---

## 11. Relação com o Advanced após o launch

| Fase | Advanced M9 | AIOX Design |
|------|-------------|-------------|
| **Agora (só brief)** | Dono atual do conteúdo | Draft |
| **Materialização** | Mantém seeds; adiciona ponte “trilha completa → AIOX Design” | Dono pedagógico do design |
| **Estabilização (opcional)** | Essencial: 1 aula ponte + link; Completa design pode encolher | Curso default para quem sofre com UI |

Não apagar M9 no dia 1. Pontes bidirecionais primeiro (`ponte/` nos dois cursos).

---

## 12. Riscos e restrições

| Risco | Mitigação |
|-------|-----------|
| Duplicar Squads 14–15 | Aula 09 só **roteamento**; runbook fica no curso Squads |
| Virar tutorial Tailwind | Stack é **meio** de prova para IA; critério em M0–M1 |
| Copiar 6 aulas Advanced sem curadoria | Outline exige exercício novo + âncora skill/squad por aula |
| Squad maturity `study` | Declarar maturidade; não prometer run autônomo |
| Curso autocontido vs wikilink cross-course | Paths monoespaçados + pontes; validar com `_tools` no scaffold |

---

## 13. Ordem de implementação (pós-aprovação do brief)

1. Aprovar este brief + outline (humano).
2. Scaffold: `README`, `modulos/`, `aulas/00–09`, `avaliacoes/`, `ponte/`, `Rubrica.md`, `_tools/validate_course.py`, hook em `npm run validate`.
3. Materializar M0–M1 (aulas 01–05) → validate.
4. Materializar M2–M3 (06–10) + quizzes → validate.
5. Atualizar `cursos/README.md`, Advanced M9, Squads pré-reqs, MOCs.
6. (Opcional) enxugar Essencial do Advanced.

---

## 14. Decisões fechadas (materialização)

- [x] Slug `aiox-design` e pasta `cursos/AIOX-Design/`
- [x] **10 aulas** / 4 módulos (inclui 05 anti-drift e 08 portão visual)
- [x] Capstone **documental** — Storybook rodando = bônus, não obrigatório
- [x] Scaffold completo: README, aulas, quizzes, `_tools/validate_course.py`, hook em `npm run validate`

**Currículo shipped:** 10 aulas com capstone documental (Storybook “como provaria”); quem tiver ambiente roda o stack na prática.

---

## Navegação

- Outline: [`course-outline.md`](course-outline.md)
- Hub de trilhas (quando publicado): `cursos/README.md`
- Seeds método: `cursos/AIOX Advanced/modulos/Módulo 9 - Design System.md`
- Operação: `cursos/AIOX-Advanced-Squads/aulas/14-design-system.md`
