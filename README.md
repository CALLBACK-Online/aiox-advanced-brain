
> Vault: [[00-HOME]] · [[cursos/MOC-Acervo-AIOX]] · [[cursos/entradas/README|entradas]]

# AIOX Advanced Brain

> **Segundo cérebro educacional do AIOX Advanced** — curso, skills e squads para estudar o método e aplicar em projetos reais.

| | |
|---|---|
| **Repositório** | [github.com/oalanicolas/aiox-advanced-brain](https://github.com/oalanicolas/aiox-advanced-brain) |
| **Pacote** | `aiox-advanced-brain` · **v0.6.0** (`catalog.json`) |
| **Licença** | [MIT](LICENSE) (empacotamento e material original; “minds” de terceiros permanecem dos autores) |
| **Tipo** | Biblioteca de **distribuição e estudo** — não é o runtime AIOX completo |

```text
Entrada: estudar → capturar/MOC → Context Brief → próxima trilha
Depois do Core: Context Brief + asset → executar no projeto → validar → devolver aprendizado
```

---

## Sumário

1. [O que é (e o que não é)](#o-que-é-e-o-que-não-é)
2. [Fundamentals, Advanced ou Enterprise?](#fundamentals-advanced-ou-enterprise)
3. [O que está incluído](#o-que-está-incluído)
4. [Primeiros 15 minutos](#primeiros-15-minutos)
5. [Baixar o material](#baixar-o-material)
6. [Navegar com o Obsidian](#navegar-o-conteúdo-com-o-obsidian) (inclui [segundo cérebro](#usar-este-repositório-como-segundo-cérebro))
7. [Trilhas de estudo](#trilhas-de-estudo)
8. [Copiar skills e squads para o projeto](#copiar-skills-e-squads-para-o-projeto)
9. [Maturidade (leia antes de executar)](#maturidade-leia-antes-de-executar)
10. [Skill ou squad?](#skill-ou-squad)
11. [Usar com Claude Code, Codex ou outro agent](#usar-com-claude-code-codex-ou-outro-agent)
12. [Missões frequentes](#missões-frequentes)
13. [Estrutura do repositório](#estrutura-do-repositório)
14. [Guia das 67 skills](#guia-das-67-skills)
15. [Guia dos 24 squads](#guia-dos-24-squads)
16. [Nomes legados e aliases](#nomes-legados-e-aliases)
17. [FAQ](#faq)
18. [Documentação e licença](#documentação-e-licença)

---

## O que é (e o que não é)

### É

- O **acervo da turma**: fundamentos técnicos + AIOX Core + método + operação em um único repositório.
- Um **vault de curso** (Markdown + wikilinks) pensado para o [Obsidian](https://obsidian.md).
- Uma **biblioteca de assets**: **67** skills e **24** squads para copiar para o *seu* projeto (inclui skills de vault de estudo).
- Um **roteador para agents**: mapa de decisão, `AGENT-GUIDE.md` e `agent-router.json` para escolher o squad certo a partir de linguagem natural.
- Material com **gates e evidência** — o curso termina no artefato que funciona, não no consumo de aulas.

### Não é

| Expectativa comum | Realidade neste repo |
|-------------------|----------------------|
| “Instalei e o AIOX inteiro roda” | Aqui não há monorepo/runtime completo (`.aiox-core`, SYNAPSE, etc.) |
| “Toda skill executa sozinha” | Muitas exigem runtime AIOX (`runtime-aiox`) ou dependências no destino (`partial`) |
| “É o produto Enterprise” | Componentes multi-tenant corporativos **não** estão no pacote ([NOTICE.md](NOTICE.md)) |
| “GitHub substitui o vault” | No GitHub você baixa; o grafo de ~2.000 links se navega melhor no **Obsidian** |

**Modelo mental:** este repositório é a **biblioteca + o cérebro de estudo**. O **projeto seu** é onde a execução acontece.

---

## Fundamentals, Advanced ou Enterprise?

Você não escolhe pelo nome “mais avançado”. Escolhe pelo gargalo que precisa remover agora.

| Seu gargalo | Próxima etapa | Você avança quando… |
|-------------|---------------|---------------------|
| Ainda não instalou nem operou o Core com segurança | **AIOX Fundamentals** | Conclui o primeiro ciclo AIOX local com evidência |
| Opera o básico, mas ainda não conduz o método de ponta a ponta | **AIOX Advanced** | Transforma intenção em sistema entregue, com SDC, gates e evidência |
| Já constrói, mas a operação é fragmentada e difícil de manter | **AIOX Enterprise** | Opera contexto, execução e evolução sobre uma base integrada e mantida |

**Fundamentos dá a base operacional. Advanced dá profundidade ao método. Enterprise dá o ambiente de produção.**

Na jornada educacional, [Introdução à Arquitetura de Sistemas](cursos/Introducao-a-Arquitetura-de-Sistemas/README.md) vem antes do Fundamentals. Quem já domina a base pode usar o projeto integrador como diagnóstico e encurtar o estudo, sem confundir os dois cursos.

[Compare as três etapas e veja se o seu gargalo já é de operação →](JORNADA-AIOX.md)

---

## O que está incluído

| Camada | Conteúdo (fonte: `catalog.json` v0.6.0) |
|--------|----------------------------------------|
| **Skills** | **67** em [`skills/`](skills/): base AIOX, entradas de squad, roteador `aiox-squads` e skills de vault/ensino |
| **Squads** | **24** canônicos em [`squads/`](squads/) |
| **Curso método** | [AIOX Advanced](cursos/AIOX%20Advanced/README.md) — **28 aulas**, **6 módulos**, **6 quizzes**, **48 questões** |
| **Curso Agent Engineering** | [AIOX Agent Engineering](cursos/AIOX-Agent-Engineering/README.md) — **28 aulas**, **7 módulos**, **6 quizzes**, **24 questões**, capstone |
| **Grafo** | Milhares de wikilinks entre cursos, conceitos, skills e squads |
| **Curso arquitetura** | [Introdução à Arquitetura de Sistemas](cursos/Introducao-a-Arquitetura-de-Sistemas/README.md) — **24 aulas**, **8 módulos**, **8 quizzes**, **32 questões** |
| **Curso AIOX Fundamentals** | [AIOX Fundamentals](cursos/AIOX-Fundamentals/README.md) — **12 aulas**, **3 módulos**, **3 quizzes**, **15 questões**, projeto final |
| **Curso design** | [AIOX Design](cursos/AIOX-Design/README.md) — **20 aulas**, **6 módulos**, **5 quizzes**, **20 questões**, capstone Storybook |
| **Curso Productização** | [AIOX Productização](cursos/AIOX-Productizacao/README.md) — **6 aulas**, **3 módulos**, **2 quizzes**, **8 questões**, capstone |
| **Curso squads** | [AIOX Advanced Squads](cursos/AIOX-Advanced-Squads/README.md) — **25 aulas** (intro + 1 por squad), **6 módulos**, **6 quizzes**, **24 questões** |
| **Mini Obsidian+IA** | [Obsidian + IA](cursos/Obsidian-IA/README.md) — **8 aulas**, ~90–120 min, gate de estudo na entrada + missão operacional depois do Core |
| **Operação** | Mapas de decisão, briefings copiáveis, exemplos de ativação, exercícios, critérios de evidência |
| **Agents (versionados)** | [AGENTS.md](AGENTS.md) · [CLAUDE.md](CLAUDE.md) · [guia de arquitetura](cursos/Introducao-a-Arquitetura-de-Sistemas/AGENT-GUIDE.md) · [guia do Core](cursos/AIOX-Fundamentals/AGENT-GUIDE.md) · [guia de Agent Engineering](cursos/AIOX-Agent-Engineering/AGENT-GUIDE.md) · [guia de design](cursos/AIOX-Design/AGENT-GUIDE.md) · [guia de Productização](cursos/AIOX-Productizacao/AGENT-GUIDE.md) · [guia de squads](cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md) |
| **Manifesto** | [`catalog.json`](catalog.json) — contagens, maturidade, aliases, proveniência |

**Integridade do curso (última hardening registrada):** 0 links quebrados / ambíguos / para fora de `cursos/`; sem paths absolutos de máquina na distribuição pública.

---

## Primeiros 15 minutos

| Min | Faça |
|-----|------|
| 0–2 | [Baixe](#baixar-o-material) o repositório (Git ou ZIP). |
| 2–5 | Abra a raiz como **vault no Obsidian** e entre por [00-HOME.md](00-HOME.md). |
| 5–8 | Abra [Como estudar — trilhas por caso](cursos/COMO-ESTUDAR.md) e identifique seu ponto de entrada. |
| 8–12 | Se termos técnicos travam, comece por [Introdução à Arquitetura de Sistemas](cursos/Introducao-a-Arquitetura-de-Sistemas/README.md); se quer instalar e conhecer os agents, abra [AIOX Fundamentals](cursos/AIOX-Fundamentals/README.md). |
| 12–15 | Leia o resultado, escopo e primeira aula da trilha escolhida; registre a evidência pedida pela aula. |

Se só tiver a pasta `cursos/`, o conteúdo pedagógico já é navegável — abra-a no Obsidian da mesma forma.

---

## Baixar o material

### Com Git

```bash
git clone https://github.com/oalanicolas/aiox-advanced-brain.git
cd aiox-advanced-brain
```

### Sem Git (ZIP)

1. Abra [github.com/oalanicolas/aiox-advanced-brain](https://github.com/oalanicolas/aiox-advanced-brain).
2. **Code → Download ZIP**.
3. Extraia a pasta e **abra no Obsidian** (estudo) e/ou no seu agent (execução).

### Validar o acervo (opcional)

Requer Python 3 e Node:

```bash
npm run validate
```

Valida todos os cursos e o roteamento de agents (`agent-router.json` + paridade skill/squad/aula).

Para a prova comportamental opcional em sessões limpas de Claude Code e Codex:

```bash
npm run smoke:routing:runtimes
```

O smoke usa somente ferramentas de leitura, limita o Claude por orçamento e mantém o Codex em sandbox `read-only`. Para testar apenas um runtime, acrescente `-- claude` ou `-- codex`.

---

## Navegar o conteúdo com o Obsidian

Os cursos usam **Markdown + wikilinks** (`[[Nome da nota]]`) — o formato nativo do [Obsidian](https://obsidian.md). **Recomendamos o Obsidian** para estudar aulas, módulos, glossário e mapas: clique nos links, use busca, backlinks e Graph view.

### Passo a passo

1. Instale o [Obsidian](https://obsidian.md) (gratuito para uso pessoal).
2. Clone ou extraia o ZIP.
3. **Open folder as vault**.
4. Escolha a pasta:

| Vault | Quando usar |
|-------|-------------|
| `cursos/AIOX Advanced/` | **Padrão recomendado** — estudar o método com grafo limpo (~2.000 links) |
| `cursos/AIOX-Agent-Engineering/` | Construir e operar capacidades agentic próprias |
| `cursos/AIOX-Design/` | Contrato visual e design system para IA |
| `cursos/AIOX-Productizacao/` | Transformar capacidade comprovada em oferta e experimento de mercado |
| `cursos/Introducao-a-Arquitetura-de-Sistemas/` | Aprender vocabulário e arquitetura de sistemas |
| `cursos/AIOX-Fundamentals/` | Instalar e operar o AIOX Core do zero ao primeiro ciclo |
| `cursos/AIOX-Advanced-Squads/` | Estudar o curso 1:1 dos squads |
| `cursos/` | Hub de todas as trilhas |
| Raiz do repositório | Estudo + `skills/` + `squads/` no mesmo vault (índice mais pesado) |

5. Abra o `README.md` do curso e navegue pelos links.
6. Opcional: **Graph view** no curso principal.

### Papéis: Obsidian vs agent

| Ferramenta | Papel |
|------------|--------|
| **Obsidian** | Navegar, estudar, reler conceitos, seguir wikilinks |
| **Agent** (Claude Code, Codex, …) | Escolher skill/squad, briefing, execução no *seu* projeto, gates |
| **Seu projeto** | Destino dos arquivos copiados de `skills/` e `squads/` |

Qualquer editor de Markdown funciona; o Obsidian é a **melhor superfície** para o segundo cérebro do curso.

### Graph colorido (Obsidian)

Abra a **raiz deste repositório** como vault. O Graph já vem com filtros por pasta (`.obsidian/graph.json`):

| Cor | O quê |
|-----|--------|
| Azul | Curso AIOX Advanced (método) |
| Roxo | Curso AIOX Advanced Squads |
| Ciano | Mini Obsidian + IA |
| Verde | `skills/` |
| Laranja | `squads/` |
| Âmbar | notas pessoais |
| Rosa | hubs (`#hub`) |

- **Tema:** padrão do Obsidian, sem dependência de tema de terceiros
- **Home:** [`00-HOME.md`](00-HOME.md)
- **Mapas:** [`cursos/MOC-Acervo-AIOX.md`](cursos/MOC-Acervo-AIOX.md) · [Skills](cursos/MOC-Skills.md) · [Squads](cursos/MOC-Squads.md)
- **Explorer colorido:** snippet `aiox-brain-folders` (Appearance → CSS snippets)
- **Orphans off** no Graph = some o anel de arquivos soltos; **on** = auditoria

### Usar este repositório como segundo cérebro

O acervo já é um vault de estudo. Para o agent **cuidar do grafo de aprendizado** (não só rotear squads), use as skills portáveis:

| Skill | Quando |
|-------|--------|
| [`aiox-brain`](skills/aiox-brain/SKILL.md) | Visão geral: como este repo funciona como segundo cérebro |
| [`obsidian-course-vault`](skills/obsidian-course-vault/SKILL.md) | Abrir vault, achar aula, trilha no Obsidian |
| [`course-moc`](skills/course-moc/SKILL.md) | Mapas de conteúdo / hubs (LYT-light) |
| [`study-capture`](skills/study-capture/SKILL.md) | Capturar insight **sem** editar aulas canônicas |
| [`teach`](skills/teach/SKILL.md) | Melhorar as aulas canônicas com rubrica didática + validação |

- **Canônico:** `cursos/**/lessons/`, `aulas/`, `modulos/` — material da turma.
- **Pessoal:** `notas/` (só o README é versionado; suas notas ficam no clone).
- **Operação AIOX:** gere um [Context Brief](cursos/Obsidian-IA/templates/context-brief.md), leve o menor asset ao projeto, execute, valide e devolva o aprendizado a `notas/retornos/`.
- **Roteamento:** continue com `skills/` + `squads/` e o [roteador de squads](cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md).

Isto **não** substitui um vault de vida/livros pessoal: é o segundo cérebro do **método e da operação AIOX**.

---

## Trilhas de estudo

Jornada canônica (detalhe e gates no [hub `cursos/`](cursos/README.md)):

```text
Obsidian + IA (estudar o acervo; diagnóstico se já domina o vault)
        ↓
Introdução à Arquitetura de Sistemas
        ↓
AIOX Fundamentals (Core, instalação e agents)
        ↓
AIOX Advanced (28 aulas de método)
        ↓
AIOX Advanced Squads (operar os especialistas)
```

Especializações laterais acionadas pelo gargalo do quarto degrau: **Agent Engineering**, **Design** e **Productização**. Elas aprofundam a missão; não alteram a ordem das cinco etapas.

| Trilha | Para quê | Comece em |
|--------|----------|-----------|
| **Obsidian + IA** | Navegar o vault, capturar e preparar um Context Brief para a próxima etapa | [cursos/Obsidian-IA/README.md](cursos/Obsidian-IA/README.md) |
| **Introdução à Arquitetura de Sistemas** | Ler sistemas, dados, contratos, fan-out/fan-in, confiabilidade, operação, segurança e agentes | [cursos/Introducao-a-Arquitetura-de-Sistemas/README.md](cursos/Introducao-a-Arquitetura-de-Sistemas/README.md) |
| **AIOX Fundamentals** | Instalar o Core, conhecer os 12 agents, escolher contexto e fechar a primeira story com evidência | [cursos/AIOX-Fundamentals/README.md](cursos/AIOX-Fundamentals/README.md) |
| **AIOX Advanced** | Mindset, contexto, SDC, determinismo e brownfield | [cursos/AIOX Advanced/README.md](cursos/AIOX%20Advanced/README.md) |
| **AIOX Advanced Squads** | Quando usar cada squad, briefing, ativação, evidência | [cursos/AIOX-Advanced-Squads/README.md](cursos/AIOX-Advanced-Squads/README.md) · [Mapa de decisão](cursos/AIOX-Advanced-Squads/Mapa-de-decisao.md) |
| **AIOX Agent Engineering (especialização lateral)** | Taxonomia, research, criação de squads, orquestração, harness e produção | [cursos/AIOX-Agent-Engineering/README.md](cursos/AIOX-Agent-Engineering/README.md) |
| **AIOX Design (especialização lateral)** | Repertório, contrato visual, Storybook, governança e qualidade de interface | [cursos/AIOX-Design/README.md](cursos/AIOX-Design/README.md) — entre quando a missão for visual |
| **AIOX Productização (especialização lateral)** | Wedge, oferta, ROI, distribuição, formato e estágio de monetização | [cursos/AIOX-Productizacao/README.md](cursos/AIOX-Productizacao/README.md) — exige capacidade comprovada |

Arquitetura e AIOX Fundamentals não são sinônimos: uma cria linguagem técnica universal; o outro ensina a operação básica do `aiox-core`.

**Ponte método ↔ squads:**
[`cursos/AIOX Advanced/ponte/`](cursos/AIOX%20Advanced/ponte/) · [`cursos/AIOX-Advanced-Squads/ponte/`](cursos/AIOX-Advanced-Squads/ponte/) · inventário em `catalog.json`.

Cada módulo do Advanced fecha com **evidência + quiz**. O curso não termina quando você “lê tudo” — termina quando o artefato funciona.

---

## Copiar skills e squads para o projeto

Este repo **não** usa `.claude/`, `.codex/` ou `.agents/` como layout canônico de distribuição. As pastas públicas são:

| Pasta | Conteúdo | No seu projeto |
|-------|----------|----------------|
| `skills/` | `SKILL.md` + recursos | `.claude/skills/`, `.codex/skills/` ou path da IDE |
| `squads/` | `config.yaml`, agents, tasks, workflows | `squads/` (ou path do monorepo AIOX) |
| `cursos/…` | Material pedagógico | Permanece no vault de estudo |

```bash
# exemplos
cp -R skills/tech-search /caminho/do/seu-projeto/.claude/skills/
cp -R squads/research /caminho/do/seu-projeto/squads/
```

Guia operacional completo (superfícies `$skill`, `@agent`, `*comando`, `/comando` e quando **não** inventar sintaxe):
[cursos/AIOX-Advanced-Squads/Guia-de-execucao.md](cursos/AIOX-Advanced-Squads/Guia-de-execucao.md).

---

## Maturidade (leia antes de executar)

Nem todo asset roda “do zero” neste repositório. A fonte de verdade é `catalog.json` → `skill_meta` / `squad_meta`.

| Label | Significado | O que fazer |
|-------|-------------|-------------|
| `study` | Anatomia, agentes, tasks — estudo e orientação | Ler, copiar, usar como referência; **não** prometer execução autônoma |
| `portable` | Roda com Node/Python + este repo (ou poucas deps) | Boa aposta para experimentar sem monorepo AIOX |
| `partial` | Parte roda; outras etapas pedem monorepo / infra no destino | Enumerar o que falta no projeto antes de executar |
| `runtime-aiox` | Exige AIOX completo (`.aiox-core`, SYNAPSE, etc.) | Usar no ambiente AIOX; aqui serve principalmente para estudo do procedimento |

### Snapshot real do catálogo (v0.6.0)

| Tipo | Distribuição de maturidade |
|------|----------------------------|
| **67 skills** | ver `skill_meta` em `catalog.json` (`portable` / `study` / `runtime-aiox` / camada `second-brain`) |
| **24 squads** | ~3 `study` · ~21 `partial` |

**Skills portáteis (bom ponto de partida sem runtime AIOX):**
`tech-search`, `tech-research`, `deep-strategic-planning`, `design-md`, `doc-rot`, `extract-session-heuristics`, `handoff`, `impeccable`, `skill-creator`, `slide-creator`, `survey-intel`.

**Regra de ouro:** presença no acervo ≠ “funciona sozinho no laptop”. Confira a label em `catalog.json`, a aula do squad e o `SKILL.md` / `config.yaml` antes de prometer entrega.

---

## Skill ou squad?

| | **Skill** | **Squad** |
|---|-----------|-----------|
| **Quando** | Objetivo específico, resultado claro | Missão multidisciplinar ou multi-etapa |
| **Forma** | Um procedimento especializado | Vários agentes + tasks + workflows |
| **Exemplos** | Validar story, tech-search, deploy | Marca, research multi-fonte, criar outro squad |
| **Ambos** | Skill wrapper abre o squad (`brand`, `research`, `copy`…) | |

**Comece pelo menor mecanismo suficiente.** Skill bem escolhida costuma ser mais rápida; squad cobre o que uma skill sozinha não fecha.

---

## Usar com Claude Code, Codex ou outro agent

O curso de squads e os bootstraps deste repo foram feitos para **humans e agents**.

### Prompt pronto

Depois de abrir o repositório no agent:

```text
Consulte cursos/AIOX-Advanced-Squads/Mapa-de-decisao.md e
cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md + agent-router.json.
Escolha o squad mais adequado para esta missão, confirme o anti-escopo
na aula correspondente, diga a maturidade, peça só o briefing que faltar
e me oriente com evidência de conclusão — sem inventar comandos do runtime.

Missão: {descreva o que precisa acontecer}
```

Versão mais curta:

```text
Consulte cursos/AIOX-Advanced-Squads/Mapa-de-decisao.md, escolha o squad
mais adequado para esta missão e use a aula correspondente para me orientar.
```

### O que o agent deve entregar

1. Squad (e por que **não** o vizinho).
2. Maturidade e dependências.
3. Briefing mínimo (só o que falta).
4. Como copiar/ativar no **seu** projeto.
5. Evidência esperada (artefato + gate) — não só “rodei o fluxo”.

### Runtime

| Runtime | Bootstrap neste repo | Cuidado |
|---------|----------------------|---------|
| **Claude Code** | [CLAUDE.md](CLAUDE.md) → [AGENTS.md](AGENTS.md) | Só use `$skill` / `@agent` / `*comando` / `/comando` se existirem no **seu** projeto |
| **Codex** | [AGENTS.md](AGENTS.md) | Não assuma superfícies `@` / `*` / `/` |
| **Outro** | [AGENTS.md](AGENTS.md) + [AGENT-GUIDE](cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md) | Use o `generic_prompt` de cada rota em `agent-router.json` |

**Contrato:** `AGENTS.md` e `CLAUDE.md` são **guias públicos versionados** (não ficam no `.gitignore`). Eles pedem ao agent atuar como **professor-especialista**: localizar material, conduzir estudo, rotear missões e exigir evidência. Overrides só em `AGENTS.local.md` / `CLAUDE.local.md`.

Referências: [Mapa de decisão](cursos/AIOX-Advanced-Squads/Mapa-de-decisao.md) · [Guia de execução](cursos/AIOX-Advanced-Squads/Guia-de-execucao.md) · [agent-router.json](cursos/AIOX-Advanced-Squads/agent-router.json).

---

## Missões frequentes

| Objetivo | Caminho sugerido |
|----------|------------------|
| Descobrir e planejar produto | `aiox-analyst` → `aiox-pm` → `aiox-sm` → `aiox-po` |
| Story completa (SDC) | `validate-story-draft` → … → `close-story`, ou `full-sdc` |
| Arquitetura e engenharia | `aiox-architect`, `aiox-dev`, `aiox-data-engineer`, `db-sage`, `aiox-devops` |
| Research rápido | skill `tech-search` (`portable`) |
| Research profundo / multi-fonte | `tech-research` · squad `research` |
| Brownfield (código) | `code-anatomist` · `domain-decoder` |
| Design system | criar: squad `design-system` · governar: `design-ops` · polish: `impeccable` |
| Criar skill / squad | `skill-creator` · `squad-chief` / squads `squad-creator` (+ `pro`) |
| Decisão de alto impacto | `roundtable` · `deep-strategic-planning` · `advisory-board` |
| Copy / vendas / conteúdo | skills + squads `copy`, `sales`, `conteudo`, `hormozi` |
| Claude Code | skill/squad `claude-code-mastery` |
| Slides | skill `slide-creator` · squad `slides-creator` |
| Agente em loop / pouco autônomo | squad `agent-autonomy` |
| Processo → ClickUp | squad `clickup-ops-squad` (depois do processo validado) |

Aula por squad: pasta [`cursos/AIOX-Advanced-Squads/aulas/`](cursos/AIOX-Advanced-Squads/aulas/).

---

## Estrutura do repositório

```text
.
├── 00-HOME.md                 # Dashboard do vault Obsidian
├── cursos/                    # Trilhas canônicas (minúsculo)
│   ├── README.md
│   ├── Introducao-a-Arquitetura-de-Sistemas/ # Base técnica (24 aulas)
│   ├── AIOX-Fundamentals/      # AIOX Core básico (12 aulas)
│   ├── AIOX Advanced/         # Método (28 aulas ativas)
│   ├── AIOX-Agent-Engineering/ # Capacidades agentic (28 aulas)
│   ├── AIOX-Design/           # Contrato visual (20 aulas, Storybook)
│   ├── AIOX-Productizacao/    # Oferta e mercado (6 aulas)
│   ├── AIOX-Advanced-Squads/  # Operação + agent-router
│   ├── Obsidian-IA/           # Vault + Context Brief + execução + retorno
│   └── MOC-*.md               # Hubs do Graph
├── notas/                     # Anotações dos alunos (âmbar; pessoal gitignored)
├── skills/                    # Skills (verde no Graph)
├── squads/                    # Squads (laranja)
├── .obsidian/                 # Graph limpo + snippet próprio
├── catalog.json
├── package.json
├── AGENTS.md / CLAUDE.md
├── CHANGELOG.md · NOTICE.md · LICENSE
└── .github/workflows/
```

---

## Guia das 67 skills

Inventário canônico = lista `skills` em `catalog.json`. Abaixo, o “use quando” de cada uma.

### Segundo cérebro (vault de estudo)

- [`aiox-brain`](skills/aiox-brain/SKILL.md) — Meta: usar este repo como segundo cérebro. **Use quando:** onboarding de estudo, Obsidian vs agent, ou dúvida de onde capturar notas.
- [`obsidian-course-vault`](skills/obsidian-course-vault/SKILL.md) — Operar `cursos/` no Obsidian. **Use quando:** abrir vault, achar aula, Graph, trilha.
- [`course-moc`](skills/course-moc/SKILL.md) — Mapas de conteúdo / hubs (LYT-light). **Use quando:** “como se conecta X e Y?” ou índice por dor/módulo.
- [`study-capture`](skills/study-capture/SKILL.md) — Captura pessoal ligada à aula. **Use quando:** anotar aprendizado sem editar o canônico (`notas/`).
- [`teach`](skills/teach/SKILL.md) — Melhoria didática do canônico (rubrica + validação). **Use quando:** “melhorar os cursos”, revisar didática de aula, criar exercício/quiz, padronizar navegação.

### Agentes fundamentais do AIOX

- [`aiox-analyst`](skills/aiox-analyst/SKILL.md) — Pesquisa mercado, concorrentes e usuários, conduz ideação, avalia viabilidade e descobre projetos brownfield. **Use quando:** existe uma pergunta de negócio ou produto que ainda precisa de evidência antes do PRD.
- [`aiox-architect`](skills/aiox-architect/SKILL.md) — Define arquitetura full-stack, APIs, infraestrutura, segurança, performance, stack e estratégia de deploy. **Use quando:** uma decisão técnica afeta várias partes do sistema ou exige trade-offs explícitos.
- [`aiox-data-engineer`](skills/aiox-data-engineer/SKILL.md) — Cuida de modelagem de dados, schemas, migrations, RLS e otimização de consultas dentro do ciclo AIOX. **Use quando:** a story altera banco, contratos de dados ou políticas de acesso.
- [`aiox-dev`](skills/aiox-dev/SKILL.md) — Implementa código, corrige bugs, refatora e aplica práticas de desenvolvimento. **Use quando:** requisitos e critérios de aceite já estão claros e chegou a hora de construir.
- [`aiox-devops`](skills/aiox-devops/SKILL.md) — Opera Git, GitHub, CI/CD, releases, MCPs e infraestrutura. **Use quando:** o trabalho envolve repositório, integração, publicação ou ambiente de execução.
- [`aiox-master`](skills/aiox-master/SKILL.md) — Governa o framework e coordena trabalho entre domínios e squads. **Use quando:** a missão atravessa fronteiras do AIOX, há conflito de autoridade ou é necessária uma decisão sistêmica.
- [`aiox-pm`](skills/aiox-pm/SKILL.md) — Cria PRDs, gerencia épicos, estratégia, roadmap e priorização MoSCoW/RICE. **Use quando:** é preciso decidir o que construir e por quê.
- [`aiox-po`](skills/aiox-po/SKILL.md) — Refina backlog, critérios de aceite, prioridades e planejamento de sprint. **Use quando:** o trabalho precisa ficar pronto e ordenado para execução.
- [`aiox-qa`](skills/aiox-qa/SKILL.md) — Define estratégia de testes, quality gates e avaliação de risco. **Use quando:** é preciso provar qualidade, cobertura e aderência aos critérios de aceite.
- [`aiox-sm`](skills/aiox-sm/SKILL.md) — Transforma PRDs e épicos em stories executáveis, organiza sprint e retrospectiva. **Use quando:** o escopo de produto precisa virar unidades pequenas de entrega.
- [`aiox-ux-designer`](skills/aiox-ux-designer/SKILL.md) — Cria fluxos, wireframes, protótipos, tokens e componentes acessíveis. **Use quando:** a solução depende da experiência do usuário ou da linguagem visual.

### Ciclo de desenvolvimento de stories

- [`validate-story-draft`](skills/validate-story-draft/SKILL.md) — Valida uma story em 12 passos, considera contexto do épico e corrige automaticamente problemas recomendados. **Use quando:** a story foi escrita, mas ainda não está pronta para desenvolvimento.
- [`develop-story`](skills/develop-story/SKILL.md) — Implementa todas as tarefas, verifica critérios de aceite e registra decisões do agente de desenvolvimento. **Use quando:** a story está validada e pronta para execução.
- [`review-story`](skills/review-story/SKILL.md) — Executa o quality gate completo, avalia riscos e prontidão de deploy e emite `PASS`, `CONCERNS`, `FAIL` ou `WAIVED`. **Use quando:** a implementação terminou e precisa de revisão independente.
- [`apply-qa-fixes`](skills/apply-qa-fixes/SKILL.md) — Corrige os achados registrados pelo quality gate. **Use quando:** a revisão encontrou problemas concretos que precisam ser eliminados antes do deploy.
- [`deploy-story`](skills/deploy-story/SKILL.md) — Detecta o tipo de deploy e executa publicação em Supabase, Docker Swarm, Vercel ou Railway. **Use quando:** a story foi aprovada e seu artefato deve chegar ao ambiente-alvo.
- [`verify-deploy`](skills/verify-deploy/SKILL.md) — Confirma de ponta a ponta que o estado real publicado corresponde ao artefato aprovado. **Use quando:** o deploy terminou, mas o valor ainda precisa ser provado no ambiente real.
- [`close-story`](skills/close-story/SKILL.md) — Verifica conclusão, deploy e governança, marca a story como concluída e atualiza o épico. **Use quando:** implementação e verificação já passaram e falta encerrar formalmente o ciclo.
- [`full-sdc`](skills/full-sdc/SKILL.md) — Orquestra todo o Story Development Cycle, da validação ao fechamento, com handoffs e checkpoints. **Use quando:** você quer executar uma única story de ponta a ponta com o fluxo AIOX completo.

### Pesquisa, estratégia e conhecimento

- [`tech-search`](skills/tech-search/SKILL.md) — Pesquisa técnica autocontida com decomposição, buscas paralelas, avaliação e síntese. **Use quando:** precisa responder uma pergunta técnica bem delimitada com rapidez e fontes.
- [`tech-research`](skills/tech-research/SKILL.md) — Conduz pesquisa técnica profunda, multi-wave, com scoring de cobertura, verificação de citações e fontes acadêmicas. **Use quando:** a decisão exige um dossier auditável e evidência graduada.
- [`roundtable`](skills/roundtable/SKILL.md) — Reúne revisores com perspectivas diferentes e produz consenso ou divergências explícitas. **Use quando:** uma decisão importante não deve depender de uma única leitura.
- [`deep-strategic-planning`](skills/deep-strategic-planning/SKILL.md) — Compara múltiplos futuros com lentes mentais, scoring e critérios de abandono. **Use quando:** arquitetura, investimento ou direção de produto têm alto impacto e alternativas reais.
- [`extract-session-heuristics`](skills/extract-session-heuristics/SKILL.md) — Extrai heurísticas operacionais de sessões de trabalho usando Pareto ao Cubo e GAH. **Use quando:** uma experiência contém aprendizados que devem virar regras reutilizáveis.
- [`doc-rot`](skills/doc-rot/SKILL.md) — Detecta documentação desatualizada, redundante ou enganosa. **Use quando:** documentos começaram a contradizer o sistema ou dificultar a busca pela fonte correta.
- [`handoff`](skills/handoff/SKILL.md) — Gera um handoff compatível com AIOX para outra IA retomar o trabalho. **Use quando:** haverá troca de sessão, agente ou janela de contexto sem perder decisões e estado.
- [`enhance-workflow`](skills/enhance-workflow/SKILL.md) — Encadeia discovery, research, roundtable e criação de épico para melhorias complexas. **Use quando:** uma feature ou evolução ainda precisa ser investigada e estruturada antes de virar execução.

### Design, marca, dados e conteúdo

- [`design-chief`](skills/design-chief/SKILL.md) — Faz triagem, roteamento e sequência do trabalho de design. **Use quando:** você sabe que o problema é de design, mas ainda não sabe qual especialista ou pipeline deve assumir.
- [`design-md`](skills/design-md/SKILL.md) — Extrai de uma URL pública um `DESIGN.md`, tokens, contrato de renderização, proveniência e relatório de drift. **Use quando:** precisa capturar ou comparar o sistema visual de uma referência existente.
- [`design-system`](skills/design-system/SKILL.md) — Assistente conversacional para componentes, páginas, decks, protótipos, dashboards e e-mails. **Use quando:** quer criar um artefato visual respeitando uma linguagem de design.
- [`impeccable`](skills/impeccable/SKILL.md) — Audita e refina interfaces em hierarquia, layout, acessibilidade, responsividade, conteúdo, movimento e acabamento. **Use quando:** a interface funciona, mas ainda precisa de qualidade visual e de experiência em nível profissional.
- [`brand`](skills/brand/SKILL.md) — Ativa os especialistas de naming, posicionamento, arquitetura e ativação de marca. **Use quando:** a missão é de branding e exige o squad `brand`.
- [`data`](skills/data/SKILL.md) — Ativa e coordena especialistas de analytics. **Use quando:** o problema envolve múltiplas disciplinas de dados ou o especialista correto ainda não está claro.
- [`db-sage`](skills/db-sage/SKILL.md) — Especialista profundo em PostgreSQL e Supabase, schemas, RLS, migrations, performance, operações e monitoramento. **Use quando:** o banco é o centro do problema e exige autoridade técnica especializada.
- [`slide-creator`](skills/slide-creator/SKILL.md) — Cria ou melhora apresentações com narrativa, direção visual, especificação slide a slide, notas e QA. **Use quando:** o entregável é um deck, pitch, aula, workshop ou apresentação executiva.
- [`survey-intel`](skills/survey-intel/SKILL.md) — Transforma CSV/XLSX de pesquisas, inscrições ou NPS em segmentos, avatares, briefing e dashboard. **Use quando:** decisões de comunicação, oferta ou evento dependem de entender uma audiência real.
- [`hormozi`](skills/hormozi/SKILL.md) — Ativa especialistas nas metodologias de Alex Hormozi. **Use quando:** a missão envolve oferta, leads, vendas, monetização ou escala segundo os frameworks `$100M`.

### Criação, governança e operação do ecossistema

- [`skill-creator`](skills/skill-creator/SKILL.md) — Orienta criação, empacotamento e validação de skills. **Use quando:** um procedimento recorrente merece virar uma capacidade invocável e reutilizável.
- [`squad-chief`](skills/squad-chief/SKILL.md) — Cria squads, agentes e workflows por templates e validação estrutural. **Use quando:** o problema precisa de uma nova equipe especializada, não apenas de uma skill.
- [`code-anatomist`](skills/code-anatomist/SKILL.md) — Faz engenharia reversa completa de software em nove fases: arquitetura, domínio, dados, API, dependências e infraestrutura. **Use quando:** precisa compreender um codebase inteiro antes de modificar, migrar ou documentar.
- [`decoder-chief`](skills/decoder-chief/SKILL.md) — Extrai regras de negócio, taxonomias e modelos de decisão de sistemas brownfield. **Use quando:** o código é conhecido, mas o domínio e suas regras ainda estão implícitos.
- [`telegram`](skills/telegram/SKILL.md) — Opera o AIOX Message Gateway: setup, deploy, canais, lifecycle, logs, health e webhooks. **Use quando:** agentes precisam funcionar por Telegram ou outros canais suportados pelo gateway.
- [`three-brain`](skills/three-brain/SKILL.md) — Roteia tarefas entre Claude, Codex, Gemini e CodeRabbit e impede autorrevisão. **Use quando:** qualidade, custo ou modalidade exigem escolher motores diferentes para executar e revisar.

### Entradas de squad (wrappers)

- [`aiox-squads`](skills/aiox-squads/SKILL.md) — Roteador universal dos 24 squads. **Use quando:** o usuário descreve uma missão sem saber qual squad escolher ou precisa de briefing e ativação segura por runtime.
- [`advisory-board`](skills/advisory-board/SKILL.md) — Porta de entrada do conselho estratégico. **Use quando:** decisão de alto impacto com múltiplas perspectivas.
- [`agent-autonomy`](skills/agent-autonomy/SKILL.md) — Porta de entrada para autonomia de agentes. **Use quando:** o agente entra em loops, depende de intervenção humana ou não avalia o próprio progresso.
- [`aiox-sop`](skills/aiox-sop/SKILL.md) — Porta de entrada para SOPs. **Use quando:** um processo precisa virar execução repetível e auditável.
- [`claude-code-mastery`](skills/claude-code-mastery/SKILL.md) — Porta de entrada do squad de domínio Claude Code. **Use quando:** hooks, skills, MCP e setup de projeto.
- [`clickup-ops-squad`](skills/clickup-ops-squad/SKILL.md) — Porta de entrada para ClickUp Ops. **Use quando:** um processo validado precisa virar Spaces, Lists, Fields e automações.
- [`conteudo`](skills/conteudo/SKILL.md) — Porta de entrada do squad de conteúdo social. **Use quando:** carrosséis, Reels, Stories e campanhas.
- [`copy`](skills/copy/SKILL.md) — Porta de entrada do squad de copy de conversão. **Use quando:** peças persuasivas e frameworks de copywriters.
- [`design-ops`](skills/design-ops/SKILL.md) — Porta de entrada para governança de design systems. **Use quando:** o sistema já existe e precisa de a11y, regressão, adoção ou controle de drift.
- [`domain-decoder`](skills/domain-decoder/SKILL.md) — Porta de entrada para regras de negócio brownfield. **Use quando:** o domínio está implícito no código.
- [`etl-ops`](skills/etl-ops/SKILL.md) — Porta de entrada para ETL. **Use quando:** dados precisam ser extraídos, transformados e carregados de forma repetível.
- [`research`](skills/research/SKILL.md) — Porta de entrada do squad unificado de research (sucessor de spy/deep-research). **Use quando:** bench, OSINT, discovery ou research multi-fonte.
- [`runner-ops`](skills/runner-ops/SKILL.md) — Porta de entrada para runners headless. **Use quando:** execução autônoma precisa operar fora da IDE com estado e observabilidade.
- [`sales`](skills/sales/SKILL.md) — Porta de entrada do squad de vendas. **Use quando:** funil completo (diagnose → close → scale).
- [`skill-creator-ops`](skills/skill-creator-ops/SKILL.md) — Porta de entrada para governança de skills. **Use quando:** várias skills precisam de lifecycle, testes e versionamento comuns.
- [`slides-creator`](skills/slides-creator/SKILL.md) — Porta de entrada para decks. **Use quando:** uma apresentação exige narrativa, visual, notas e QA coordenados.
- [`squad-creator`](skills/squad-creator/SKILL.md) — Porta de entrada para criação canônica de squads. **Use quando:** uma nova capacidade precisa de agentes, tasks e workflows.
- [`squad-creator-pro`](skills/squad-creator-pro/SKILL.md) — Porta de entrada para criação avançada de squads. **Use quando:** há clonagem mental, extração de DNA, model routing ou gates avançados.
- [`storytelling`](skills/storytelling/SKILL.md) — Porta de entrada para narrativa. **Use quando:** a mensagem depende de arco, tensão, emoção e memorabilidade.

---

## Guia dos 24 squads

Cada squad tem **aula 1:1** em `cursos/AIOX-Advanced-Squads/aulas/` (ver [índice](cursos/AIOX-Advanced-Squads/README.md)). Confira maturidade em `catalog.json` antes de executar.

- [`advisory-board`](squads/advisory-board/config.yaml) — Conselho estratégico com perspectivas alinhadas e complementares, devil's advocate e accountability. **Use quando:** precisa tomar uma decisão pessoal ou empresarial importante e quer reduzir vieses e groupthink.
- [`agent-autonomy`](squads/agent-autonomy/config.yaml) — Audita, cria, diagnostica e otimiza agentes autônomos com frameworks de autonomia real. **Use quando:** um agente depende demais de intervenção humana, entra em loops ou não sabe avaliar seu próprio progresso.
- [`aiox-sop`](squads/aiox-sop/config.yaml) — Cria, extrai, avalia e otimiza SOPs para humanos e agentes com referências de qualidade operacional. **Use quando:** um processo precisa sair da cabeça das pessoas e virar execução repetível e auditável.
- [`brand`](squads/brand/config.yaml) — Reúne especialistas em naming, fundamentos, posicionamento, arquitetura e ativação de marca. **Use quando:** a missão cobre a construção ou evolução completa de uma marca.
- [`claude-code-mastery`](squads/claude-code-mastery/config.yaml) — Especialistas em hooks, skills, subagentes, MCPs, plugins, agent teams e integração de projetos no Claude Code. **Use quando:** quer configurar, dominar ou evoluir o ambiente Claude Code.
- [`clickup-ops-squad`](squads/clickup-ops-squad/config.yaml) — Materializa processos validados em Spaces, Folders, Lists, Fields, automações, views e tasks no ClickUp. **Use quando:** o processo já foi mapeado e precisa virar operação real no ClickUp.
- [`code-anatomist`](squads/code-anatomist/config.yaml) — Equipe de engenharia reversa que recupera arquitetura, domínio, dados, APIs, dependências e infraestrutura. **Use quando:** um sistema completo precisa ser entendido por múltiplas lentes antes de uma transformação.
- [`conteudo`](squads/conteudo/config.yaml) — Produz conteúdo para Instagram: carrosséis, Reels, Stories, campanhas e pesquisa de concorrentes. **Use quando:** precisa operar um calendário ou campanha de conteúdo social.
- [`copy`](squads/copy/config.yaml) — Reúne copywriters especializados para peças de alta conversão. **Use quando:** o objetivo central é persuadir, converter ou vender por meio de texto.
- [`data`](squads/data/config.yaml) — Equipe de analytics para análises, métricas e decisões baseadas em dados. **Use quando:** a pergunta exige mais de uma especialidade analítica ou um pipeline completo de inteligência.
- [`db-sage`](squads/db-sage/config.yaml) — Especialistas em PostgreSQL e Supabase para arquitetura, migrations, RLS e performance. **Use quando:** a missão de banco é extensa, crítica ou combina desenho e operação.
- [`design-ops`](squads/design-ops/config.yaml) — Governa monitoramento, lifecycle, auditorias, acessibilidade, regressão visual, Storybook e Chromatic. **Use quando:** o design system já existe e precisa permanecer saudável, consistente e mensurável.
- [`design-system`](squads/design-system/config.yaml) — Constrói foundations, tokens, componentes, registry e metadata do design system. **Use quando:** é necessário criar ou evoluir tecnicamente a biblioteca visual; para governança contínua, use `design-ops`.
- [`domain-decoder`](squads/domain-decoder/config.yaml) — Decodifica regras, taxonomia e modelo de negócio presentes em software brownfield. **Use quando:** a prioridade é compreender o domínio escondido no código, e não mapear toda a arquitetura.
- [`etl-ops`](squads/etl-ops/config.yaml) — Opera pipelines ETL, collectors e APIs, incluindo fluxo progressivo para livros e capítulos. **Use quando:** precisa extrair, transformar e carregar dados de forma repetível usando a infraestrutura existente.
- [`hormozi`](squads/hormozi/config.yaml) — Conjunto de especialistas nos frameworks de ofertas, leads, vendas e escala de Alex Hormozi. **Use quando:** quer desenvolver uma oferta ou sistema comercial completo com essas metodologias.
- [`research`](squads/research/config.yaml) — Unifica pesquisa técnica, inteligência competitiva, discovery, benchmarking, OSINT e revisão sistemática. **Use quando:** a investigação atravessa fontes e disciplinas ou sustenta uma decisão de alto impacto.
- [`runner-ops`](squads/runner-ops/config.yaml) — Cria, integra, valida, monitora e governa runners headless e sua infraestrutura compartilhada. **Use quando:** pipelines autônomos precisam rodar fora da IDE com estado, orçamento, métricas e compliance.
- [`sales`](squads/sales/config.yaml) — Cobre diagnóstico, qualificação, prospecção, negociação, fechamento e escala comercial. **Use quando:** a missão envolve o funil de vendas completo, e não apenas uma peça de copy.
- [`skill-creator-ops`](squads/skill-creator-ops/config.yaml) — Governa o ciclo de vida de skills: criar, validar, testar, migrar, empacotar, depreciar e retirar. **Use quando:** há várias skills para manter com padrão, qualidade e versionamento consistentes.
- [`slides-creator`](squads/slides-creator/config.yaml) — Automatiza o ciclo completo de decks profissionais, do briefing à entrega validada. **Use quando:** uma apresentação exige especialistas coordenados em narrativa, conteúdo, visual e QA.
- [`squad-creator`](squads/squad-creator/config.yaml) — Meta-squad canônico para criar agentes, tasks, workflows e squads com templates e validação. **Use quando:** precisa construir uma nova capacidade organizacional dentro do AIOX.
- [`squad-creator-pro`](squads/squad-creator-pro/config.yaml) — Expande o `squad-creator` com clonagem mental, extração de DNA, delegação especializada, model routing e gates avançados. **Use quando:** a criação do squad exige especialistas baseados em mentes, maior profundidade ou otimização avançada.
- [`storytelling`](squads/storytelling/config.yaml) — Reúne mestres de narrativa para estruturar histórias poderosas. **Use quando:** a mensagem depende de arco, tensão, emoção e memorabilidade, em vez de apenas conversão direta.

---

## Nomes legados e aliases

Útil se você veio de turmas antigas, slides ou do monorepo com nomes anteriores:

| Mencionado | Neste acervo |
|------------|--------------|
| `aios-*` (analyst, dev, …) | `aiox-*` |
| `spy`, Spy/Bench, deep-research (squad unificado) | squad + skill `research` |
| `design` / design-squad | `design-ops` (+ `design-system` para construção) |
| skill `slides-creator` | skill **`slide-creator`** · squad **`slides-creator`** |
| `content-engine` | `conteudo` |
| `course-creator` | **não empacotado**; anatomia de referência → `squad-creator` |
| `sales-squad` / `negotiation-squad` | `sales` |
| `project-management-clickup-squad` | `clickup-ops-squad` |

Fonte completa: `catalog.json` → `aliases`, `renames`, `related_current_assets`.

---

## FAQ

**Preciso do AIOX Enterprise para usar isto?**
Não. Este acervo permite estudar o método e adaptar assets ao seu projeto. O Enterprise adiciona infraestrutura mantida e componentes proprietários de produção, que não estão empacotados aqui.

**Qual é o próximo passo depois do Fundamentals?**
Vá para o **AIOX Advanced** quando já conseguir instalar o Core, escolher o mecanismo correto e fechar uma story local com evidência reproduzível.

**Qual é o próximo passo depois do Advanced?**
Avance para **Advanced Squads** para operar um especialista publicado. Se a missão revelar uma lacuna, aprofunde-a com **Agent Engineering**, **Design** ou **Productização** e retome a execução. Se a competência já existe e o gargalo virou sustentar a base integrada, avalie o **AIOX Enterprise**.

**O Enterprise substitui o Advanced?**
Não. O Advanced constrói a competência do operador. O Enterprise oferece o ambiente mantido para aplicar essa competência com ativos de produção, governança e evolução contínua.

**O que eu ganho a mais ao entrar no AIOX Enterprise?**
Você passa de uma base montada e mantida por você para uma operação integrada e mantida. O Enterprise reúne repositório privado, Dashboard Enterprise, squads de produção, workspace, integrações disponíveis, monitoramento, auditoria, atualizações contínuas e acompanhamento.

**Como sei se chegou a hora do Enterprise?**
Quando você já entrega com o Advanced, mas remontar contexto, integrações, gates e monitoramento virou parte relevante do custo de cada projeto. O sinal não é querer mais conteúdo; é precisar sustentar a operação com menos fragmentação.

Veja a [comparação completa](JORNADA-AIOX.md) e confirme as condições na [página oficial](https://lp.aioxsquad.ai/enterprise).

**Por que copiar skills em vez de rodar daqui?**
Porque o destino canônico é o *seu* projeto/IDE. Este repo é fonte de distribuição; a execução usa o harness do projeto.

**Obsidian é obrigatório?**
Não, mas é a forma recomendada de navegar o grafo de wikilinks. No GitHub os arquivos abrem; o segundo cérebro funciona de verdade no vault.

**Qual a diferença entre os cursos?**
Introdução à Arquitetura de Sistemas = **linguagem técnica universal**. AIOX Fundamentals = **instalação e operação básica do `aiox-core`**, incluindo os 12 agents. Advanced = **método aprofundado**. Advanced Squads = **operação de cada squad**. Obsidian + IA conecta navegação e captura a Context Brief, execução validada no projeto e retorno ao vault.

**Posso pedir ao agent “roda o squad X” sem copiar?**
O agent pode **orientar** lendo a aula e o `config.yaml`. Execução real exige o asset no projeto (e runtime compatível). Maturidade `study`/`partial` limita o que é seguro prometer.

**Skill `slide-creator` vs squad `slides-creator`?**
Skill = procedimento de deck. Squad = time coordenado (narrativa, visual, QA). Nomes deliberadamente próximos; veja aliases.

**Os números do README mudaram?**
Confie em `catalog.json` (`library_version`, `counts`, `course`, `supplemental_courses`). Este README acompanha **0.6.0**.

**Posso redistribuir o link do repositório?**
Siga [NOTICE.md](NOTICE.md) e o combinado da turma. Frameworks/“minds” de terceiros são estudo metodológico — respeite direitos das obras originais.

---

## Documentação e licença

| Documento | Função |
|-----------|--------|
| [JORNADA-AIOX.md](JORNADA-AIOX.md) | Diferenças e próximos passos entre Fundamentals, Advanced e Enterprise |
| [cursos/README.md](cursos/README.md) | Hub das trilhas |
| [NOTICE.md](NOTICE.md) | Proveniência e o que **não** está no pacote |
| [CHANGELOG.md](CHANGELOG.md) | Histórico da biblioteca |
| [catalog.json](catalog.json) | Manifesto máquina (contagens, maturidade, aliases) |
| [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md) | Bootstrap agents |
| [LICENSE](LICENSE) | MIT + nota sobre material de terceiros |

**Licença:** MIT para o empacotamento e materiais originais deste repositório. Metodologias e “minds” de terceiros incluídos para estudo permanecem dos respectivos autores — ver [LICENSE](LICENSE) e [NOTICE.md](NOTICE.md).

Runtime enterprise multi-tenant **não** está empacotado neste repositório.
