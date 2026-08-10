---
type: course-outline
course: aiox-design
status: canonical
canonical_scope: cursos/AIOX-Design
parent_brief: COURSE-BRIEF.md
lessons_planned: 10
modules_planned: 4
tags: [curso, design, outline]
---

# Course outline — AIOX Design

Brief: [`COURSE-BRIEF.md`](COURSE-BRIEF.md).

Convenções:

- **Slug de arquivo** materializado em `aulas/` (canônico).
- **Seed** = origem no acervo (curar, não copiar cegamente).
- **Resultado** = objetivo verificável (rubrica teach #1).
- **Exercício** = prática mínima (teach #3).
- **Âncora** = path real no repo (teach #2).
- **Ponte** = próximo passo operacional ou de método (teach #5).

---

## Mapa dos módulos

```text
M0 Decisão          M1 Contrato + taxonomia     M2 Stack + prova        M3 Operação + capstone
01 DS = decisão  →  03 DESIGN.md             →  06 Stack canônica    →  09 Skill vs squad
02 Green/Brown   →  04 Taxonomia atômica     →  07 Variantes/Storybook → 10 Capstone
                    05 Tokens e anti-drift   →  08 Portão de qualidade
```

---

## M0 — Decisão, não estética

**Resultado do módulo:** a pessoa separa “gosto na hora” de “decisão registrada” e escolhe a porta greenfield/brownfield.

**Quiz M0:** 4 questões (token vs pontual; DS como arquitetura; green vs brown; anti-escopo Figma-only).

### Aula 01 — Design system é decisão, não estética

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/01-design-system-e-decisao.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/41-design-system-e-decisao.md` |
| **~min** | 20–25 |
| **Bloom** | understand → apply |
| **Resultado** | Diante de 5 escolhas visuais de um produto fictício, marca quais viram **token/regra** e quais ficam **pontuais**, com uma frase de critério cada. |
| **Ideias-chave** | Decidir uma vez; herança; DS como arquitetura; custo de redecidir a cada tela; anti-AI-slop via consistência. |
| **Exercício** | Tabela: escolha visual → token \| pontual \| por quê (produto: app de agenda ou o do aluno). |
| **Portão** | Explica sem ler a aula: “o que vira token e o que não vira”. |
| **Âncora** | Conceito futuro no glossário do curso; skill `skills/design-md/SKILL.md` (como destino do contrato). |
| **Ponte** | Método: Advanced ainda cobre SDC; aqui o foco é só o visual. |

### Aula 02 — Greenfield vs brownfield de design system

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/02-design-system-greenfield-brownfield.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/32-design-system-greenfield-brownfield.md` |
| **~min** | 20–25 |
| **Bloom** | apply |
| **Resultado** | Classifica **um** produto real (ou o do aluno) como greenfield DS, brownfield com DS implícito, ou brownfield com DS legado — e nomeia a **primeira ação** de cada caso. |
| **Ideias-chave** | Entrar sem apagar UI; inventariar antes de padronizar; quando **não** reescrever o design system inteiro. |
| **Exercício** | Mini discovery: 5 screenshots ou rotas → o que já é padrão? o que é exceção? qual risco se “padronizar tudo já”? |
| **Portão** | Escolhe a porta de entrada correta para o próprio contexto. |
| **Âncora** | `squads/design-system/` (construir) vs `squads/design-ops/` (governar) — só menção; detalhe na aula 09. |
| **Ponte** | Brownfield de **código** (Advanced M6 / code-anatomist) ≠ brownfield de **DS**; não misturar missões. |

**Evidência M0:** arquivo curto `decisoes-visuais.md` (local/`notas/`) com a tabela da aula 01 + classificação da aula 02.

---

## M1 — Contrato e taxonomia

**Resultado do módulo:** existe um rascunho de `DESIGN.md` e um mapa de componentes em camadas atômicas.

**Quiz M1:** 4–5 questões (papel do DESIGN.md; par CLAUDE/AGENTS; átomo vs molécula; REUSE/ADAPT/CREATE; o que não vai no contrato).

### Aula 03 — DESIGN.md: o contrato que a IA lê antes da tela

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/08-design-md-contrato.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/43-design-md-novo-contrato.md` + `cursos/AIOX Advanced/conceitos/DESIGN md.md` |
| **~min** | 25–30 |
| **Bloom** | apply |
| **Resultado** | Escreve um **DESIGN.md mínimo** (seções: princípios, tokens base, componentes canônicos, o que é proibido, como a IA deve ler). |
| **Ideias-chave** | Terceiro contrato (com CLAUDE.md e AGENTS.md); lido **antes** de gerar; token + regra; prompt solto ≠ contrato. |
| **Exercício** | Scaffold do arquivo com 1 cor primária, 1 espaçamento, 1 componente Button, 3 “nunca faça”. |
| **Portão** | Diff mental: gerar tela **com** vs **sem** o arquivo. |
| **Âncora** | `skills/design-md/SKILL.md` (portable) — “depois de copiar, use a skill para lintar/validar o contrato”. |
| **Ponte** | Não confundir com `skills/impeccable` (craft depois do gate de conformidade). |

### Aula 04 — Design atômico e taxonomia de componentes

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/10-taxonomia-atomica.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/42-design-atomico-brad-frost.md` |
| **~min** | 25–30 |
| **Bloom** | apply |
| **Resultado** | Classifica 8 elementos de uma UI (lista fornecida na aula) em átomo / molécula / organismo / template / página e aponta 1 erro comum de granularidade. |
| **Ideias-chave** | Brad Frost; composição; API de props estável; por que taxonomia importa para agentes (REUSE). |
| **Exercício** | Mapa 1 tela do produto do aluno (ou mock da aula) nas 5 camadas. |
| **Portão** | Explica por que “Card mágico que faz tudo” quebra taxonomia e o agente. |
| **Âncora** | `skills/design-system/SKILL.md`; menção a padrões ds-taxonomy no ecossistema AIOX se existirem no runtime da pessoa (sem inventar comando). |
| **Ponte** | Squad design-system: tokens + foundations + registry — aula 09. |

### Aula 05 — Tokens, componentes e anti-drift

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/09-tokens-componentes-anti-drift.md` |
| **Seed** | Síntese nova (não há aula Advanced 1:1); puxar trechos de 41/43 + práticas `design-ops` |
| **~min** | 20–25 |
| **Bloom** | apply / evaluate |
| **Resultado** | Completa o DESIGN.md da aula 03 com: escala de tipo, 2 estados de Button, regra de **não** hardcodar cor no JSX, e um “sintoma de drift” + ação. |
| **Ideias-chave** | Token semântico vs bruto; fonte única; drift = decisão fora do contrato; anti-AI-look (consistência > originalidade aleatória). |
| **Exercício** | Auditoria de 1 trecho de UI (exemplo na aula ou do aluno): 3 violações possíveis do contrato. |
| **Portão** | Nomeia 1 métrica simples de drift (“telas com cor fora do token”). |
| **Âncora** | `skills/design-ops/SKILL.md` ou `squads/design-ops/` (governança no tempo). |
| **Ponte** | Aula 08 (portão de qualidade) aprofunda prova; aqui é o **modelo mental** do drift. |

**Evidência M1:** `DESIGN.md` rascunho versionável + diagrama de taxonomia (Mermaid ou lista indentada).

---

## M2 — Stack e prova

**Resultado do módulo:** a pessoa justifica a stack canônica e descreve como provar variantes **antes** de chamar a tela de pronta.

**Quiz M2:** 4 questões (por que Storybook para IA; o que a stack não resolve; variante mínima; portão vs craft).

### Aula 06 — Tailwind + ShadCN + Storybook (stack canônica para IA)

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/12-stack-tailwind-shadcn-storybook.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/56-tailwind-shadcn-storybook.md` |
| **~min** | 20–25 |
| **Bloom** | understand → evaluate |
| **Resultado** | Escreve um parágrafo “por que esta stack **para agentes**” e lista 2 casos em que **outra** stack seria aceitável (com trade-off). |
| **Ideias-chave** | Tokens ↔ utility; componentes copiáveis; Storybook como catálogo legível; canônico ≠ religião. |
| **Exercício** | Matriz: necessidade do produto × peça da stack × risco se omitir. |
| **Portão** | “Stack sem DESIGN.md resolve deriva?” — resposta esperada: não. |
| **Âncora** | Paths do acervo apenas; não inventar CLI de install se não estiver documentada no seed. |
| **Ponte** | Implementação real no projeto do aluno; curso não substitui docs oficiais Tailwind/ShadCN. |

### Aula 07 — Variantes: a11y, dark mode, responsivo

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/14-storybook-variantes.md` |
| **Seed** | `cursos/AIOX Advanced/archive/migrated/lessons/57-storybook-para-variantes.md` |
| **~min** | 20–25 |
| **Bloom** | apply |
| **Resultado** | Para o Button (ou componente do capstone), define a **matriz mínima de variantes** (estado × tema × breakpoint × a11y) e o que conta como “provado”. |
| **Ideias-chave** | Variante como especificação; a11y não é afterthought; dark/responsivo como eixos; Storybook como evidência. |
| **Exercício** | Preencher template de matriz (tabela na aula). |
| **Portão** | Sabe dizer o que **falta** provar se só existe “happy path light desktop”. |
| **Âncora** | `squads/design-ops/` (auditorias, regressão visual, Storybook). |
| **Ponte** | Capstone pode ser **documental** se não houver Storybook rodando (ver brief §14). |

### Aula 08 — Portão de qualidade visual (antes do craft)

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/18-portao-qualidade-visual.md` |
| **Seed** | Síntese nova + fronteira com `skills/impeccable` e design-ops |
| **~min** | 15–20 |
| **Bloom** | evaluate |
| **Resultado** | Ordena um checklist de 8 itens em: **bloqueia merge**, **pode waiver com motivo**, **é só polish** — e classifica `impeccable` como pós-conformidade. |
| **Ideias-chave** | Conformance vs craft; quality gate visual; não polir o que viola o contrato; Chromatic/regressão como ideia (sem exigir conta). |
| **Exercício** | 3 findings fictícios → severidade + ação (fix contrato / fix componente / impeccable / ignorar). |
| **Portão** | Explica a frase: “impeccable depois do gate, nunca no lugar do DESIGN.md”. |
| **Âncora** | `skills/impeccable/SKILL.md` (portable); `skills/design-ops` / aula Squads 15. |
| **Ponte** | Aula 09: quem executa o quê no acervo. |

**Evidência M2:** matriz de variantes + checklist de portão preenchidos.

---

## M3 — Operação e capstone

**Resultado do módulo:** a pessoa escolhe o menor mecanismo suficiente e fecha um ciclo artificial completo.

**Sem quiz de módulo** — a evidência é o capstone + rubrica.

### Aula 09 — Skill, squad e marca: o menor mecanismo suficiente

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/19-skill-vs-squad-design.md` |
| **Seed** | `cursos/AIOX-Advanced-Squads/aulas/13-brand.md`, `14-design-system.md`, `15-design-ops.md` + `catalog.json` (maturidade) |
| **~min** | 20–25 |
| **Bloom** | evaluate |
| **Resultado** | Para 4 missões curtas (cenários na aula), escolhe: só `design-md` · `design-system` · `design-ops` · `brand` · `impeccable` · sequência — com **anti-escopo** de uma linha cada. |
| **Ideias-chave** | Construir vs governar; marca ≠ DS; study/partial maturity; copiar `squads/` ao projeto; não simular run. |
| **Exercício** | Tabela missão → mecanismo → evidência esperada → o que **não** fazer. |
| **Portão** | “Preciso de design-ops para criar o primeiro Button?” — resposta esperada: não. |
| **Âncora** | Paths canônicos: `squads/design-system/`, `squads/design-ops/`, `squads/brand/`, skills listadas no brief. |
| **Ponte** | Curso Squads aulas 13–15 para briefing completo e ativação. |

### Aula 10 — Capstone: do briefing ao contrato com prova

| Campo | Conteúdo |
|-------|----------|
| **Arquivo** | `aulas/20-capstone-ds-storybook-executavel.md` |
| **Seed** | Integra 01–09; alinhado a evidência M9 Advanced (contrato + variantes) |
| **~min** | 30–40 |
| **Bloom** | create / evaluate |
| **Resultado** | Entrega um pacote mínimo (ver rubrica abaixo). |
| **Fluxo sugerido** | 1) Briefing de 1 tela/feature · 2) Atualizar DESIGN.md · 3) Spec do componente (taxonomia + API) · 4) Matriz de variantes · 5) Rota operacional (skill/squad) · 6) Autocrítica (o que falta para produção). |
| **Exercício** | = o capstone. |
| **Portão** | Rubrica ≥ 80 e zero falha crítica (sem contrato ou sem anti-escopo de operação). |
| **Âncora** | Tudo que foi citado no curso; opcional: copiar skill `design-md` no projeto destino. |
| **Ponte** | Leve a UI sob contrato para a missão em andamento; opere os Squads 14–15 quando precisar executar ou governar o sistema de design. |

---

## Rubrica do capstone (rascunho)

| Critério | Peso | Nota máxima se… |
|----------|-----:|-----------------|
| **DESIGN.md utilizável** | 30 | Agente saberia o que ler: tokens, proibições, 1+ componente |
| **Taxonomia e escopo** | 15 | Componente na camada certa; REUSE/ADAPT/CREATE explícito |
| **Matriz de variantes** | 20 | Pelo menos estados + 1 eixo tema ou breakpoint + 1 nota a11y |
| **Portão vs craft** | 10 | Separa bloqueio de polish; não usa impeccable como desculpa |
| **Rota operacional** | 15 | Mecanismo mínimo + maturidade declarada + anti-escopo |
| **Clareza e honestidade** | 10 | Limitações explícitas; sem inventar comando/runtime |

**Falha crítica (zero automático):** ausência de contrato; ou “rodar squad” sem dizer que é study/partial e precisa copiar pacote.

**Storybook rodando:** bônus, não obrigatório no vault self-paced.

---

## Quizzes (planejamento)

| ID | Módulo | Questões | Foco |
|----|--------|----------|------|
| Quiz-M0 | M0 | 4 | Decisão vs gosto; green/brown |
| Quiz-M1 | M1 | 5 | DESIGN.md; taxonomia; drift |
| Quiz-M2 | M2 | 4 | Stack; variantes; portão vs craft |

Gabarito: distribuir respostas corretas entre A/B/C/D (padrão validadores do acervo).

---

## Glossário mínimo do curso (a materializar)

| Termo | Definição de trabalho |
|-------|----------------------|
| **Token** | Decisão visual registrada como valor reutilizável |
| **DESIGN.md** | Contrato visual lido pela IA antes de gerar UI |
| **Drift** | UI que foge do contrato sem atualizar o contrato |
| **Átomo / molécula / …** | Camadas da taxonomia atômica |
| **Variante** | Eixo de prova (estado, tema, breakpoint, a11y) |
| **Portão visual** | Critério que bloqueia “pronto” sem prova |
| **Craft / impeccable** | Polimento **depois** da conformidade |
| **Design-system (squad)** | Construir biblioteca |
| **Design-ops (squad)** | Governar DS no tempo |

---

## Ordem de estudo e tempo

| Rota | Percurso | ~Tempo |
|------|----------|--------|
| **Essencial** | 01 → 03 → 04 → 07 → 09 → 10 | ~2h15 |
| **Completa** | 01–10 na ordem | ~3h45 + quizzes |
| **Só contrato** | 01, 03, 05, 10 | ~1h30 (emergência de projeto) |

Pré-leitura opcional no Advanced: `03-claude-md-leis-da-fisica` (por que contratos de arquivo existem).

---

## Checklist de materialização por aula

Ao escrever cada `.md` em `aulas/`:

- [x] Frontmatter (`type`, `course`, `lesson_position`, `module`, `status: canonical`)
- [x] Resultado verificável (“Ao final você consegue…”)
- [x] Mapa Mermaid ou tabela de decisão (1 por aula)
- [x] Exercício com portão
- [x] Âncora `skills/` ou `squads/` ou seed declarado
- [x] Navegação prev/next/módulo/README **dentro** do curso
- [x] Sem path absoluto de máquina
- [x] Termos no [Glossário](Glossario.md) do curso

---

## Diff vs Advanced M9 (transparência)

| Advanced hoje | AIOX Design outline |
|---------------|---------------------|
| 41, 43 essential; 32, 42, 56, 57 complete | Todos no curso Design; 05 e 08 **novos** |
| Quiz M9 único | Quizzes M0–M2 + capstone |
| Ponte squad no **módulo** | Ponte em **cada** aula relevante + aula 09 dedicada |
| Sem trilha “só design” | Trilha default para dor de UI |

---

## Próximo artefato (não neste passo)

Após aprovação humana do brief/outline:

1. `README.md` do curso (hub aluno)
2. `aulas/01-…` … `10-…`
3. `modulos/M0-…` … `M3-…`
4. `avaliacoes/`, `Rubrica.md`, `ponte/`, `_tools/validate_course.py`
5. Integração `npm run validate` + hub `cursos/README.md`
