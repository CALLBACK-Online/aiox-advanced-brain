---
tags: [layer/curso, hub]
---

> Vault: [[00-HOME]] · [[cursos/MOC-Acervo-AIOX]] · [[cursos/entradas/README|entradas]]


# Cursos — AIOX Advanced Brain

Hub das trilhas educacionais deste repositório. Cada curso é **autocontido** (links internos resolvem dentro da própria pasta). Entre cursos, use os caminhos monoespaçados ou abra pelo arquivo indicado.

## Navegação recomendada: Obsidian

Os cursos usam Markdown com **wikilinks entre notas**. A forma recomendada de estudar é abrir esta pasta (ou um curso específico) como **vault no [Obsidian](https://obsidian.md)**:

1. Instale o Obsidian.
2. **Open folder as vault** → para o **Graph colorido completo** (cursos + skills + squads), abra a **raiz do repositório**. Alternativas: `cursos/`, `cursos/AIOX-Fundamentos-de-Arquitetura/`, `cursos/AIOX-Fundamentals/`, `cursos/AIOX Advanced/`, `cursos/AIOX-Advanced-Squads/` ou `cursos/Obsidian-IA/`.
3. Comece por `00-HOME.md` (raiz) ou pelo `README.md` do curso; use Graph view com as cores do acervo.
4. Mapas: `cursos/MOC-Acervo-AIOX.md`, `cursos/MOC-Skills.md`, `cursos/MOC-Squads.md`.

No GitHub ou em editores genéricos os arquivos abrem, mas o grafo de ~2.000 links do AIOX Advanced funciona melhor no Obsidian. Instruções completas: README na raiz do repositório.

## Trilhas

| Curso | Para quê | Comece em |
|-------|----------|-----------|
| **Obsidian + IA** | Mini: vault, captura, Context Brief, execução no projeto e retorno | `cursos/Obsidian-IA/README.md` |
| **Fundamentos de Arquitetura de Sistemas** | Base técnica: componentes, dados, comunicação, fan-out/fan-in, escala, operação, segurança e agentes | `cursos/AIOX-Fundamentos-de-Arquitetura/README.md` |
| **AIOX Fundamentals** | Core: instalação, anatomia, 12 agents, contexto, story e validação básica | `cursos/AIOX-Fundamentals/README.md` |
| **AIOX Advanced** | Método: mindset, SDC, taxonomia, determinismo, deploy | `cursos/AIOX Advanced/README.md` |
| **AIOX Advanced Squads** | Operação: um squad por aula, briefing e evidência | `cursos/AIOX-Advanced-Squads/README.md` |

## Ordem sugerida

1. **Obsidian + IA** (opcional, ~90–120 min + missão real) se o gargalo for estudar no vault com agent.
2. **Fundamentos de Arquitetura de Sistemas** — faça completo se os termos técnicos ainda travam; use o mapa de termos para revisão seletiva.
3. **AIOX Fundamentals** — instale/audite o Core, conheça os agents e conclua o primeiro ciclo local.
4. **AIOX Advanced — Rota Essencial** (ou, no mínimo, M1 + M5 + M7).
5. **AIOX Advanced Squads — aula 00** (como copiar e ativar).
6. Módulos do curso de Squads conforme a missão.
7. Voltar ao Advanced no Capstone / Projeto Integrador com os squads já escolhidos.

## Matriz método → squads

| Tema no AIOX Advanced | Aulas do método (pasta `lessons/`) | Aulas no curso Squads (`aulas/`) |
|----------------------|-------------------------------------|----------------------------------|
| O que é squad / anatomia | `23-…`, `28-…`, `33-…` | `00-como-usar-este-curso.md` + todas |
| Criar squad | `34-…`, `51-…`, `55-…` | `23-squad-creator.md`, `24-squad-creator-pro.md` |
| Research | `36-…`, `37-…`, `40-…` | `02-research.md` |
| Brownfield / código | `31-…`, `38-…`, `53-…` | `03-code-anatomist.md`, `04-domain-decoder.md` |
| Design system | `32-…`, `41-…`–`43-…` | `14-design-system.md`, `15-design-ops.md` |
| Runner / taxonomia | `28-…`–`30-…` | `09-runner-ops.md` |
| Mesa-redonda / decisão | `35-…` | `01-advisory-board.md` |
| Oferta / ROI | `62-…`, `64-…` | `19-copy.md`, `20-sales.md`, `21-hormozi.md` |
| Skills lifecycle | `28-…` | `22-skill-creator-ops.md` |

Sequência de pré-requisitos: `cursos/AIOX-Fundamentos-de-Arquitetura/README.md` → `cursos/AIOX-Fundamentals/README.md` → `cursos/AIOX Advanced/README.md`.

Matriz completa e pontes:  
`cursos/AIOX Advanced/ponte/pre-requisitos-arquitetura.md` · `cursos/AIOX Advanced/ponte/trilha-squads.md` · `cursos/AIOX-Advanced-Squads/ponte/pre-requisitos-advanced.md`

## Layout do acervo

| Pasta | Uso |
|-------|-----|
| `skills/` | Skills para copiar à IDE do projeto (inclui vault/ensino: `aiox-brain`, `obsidian-course-vault`, `course-moc`, `study-capture`, `teach`) |
| `squads/` | Squads para copiar ao projeto |
| `cursos/` | Cursos navegáveis (esta pasta) |
| `notas/` | Captura local do aluno (não polui aulas canônicas) |

Não há runtime AIOX completo neste repositório: estude aqui, leve um Context Brief + o menor asset ao projeto, execute lá e devolva o aprendizado. Segundo cérebro do acervo: `skills/aiox-brain/SKILL.md`.

## Graph / vault

- Home: `00-HOME.md` (raiz do repo)
- Pontes de skill: `cursos/entradas/`
- Anotações: `notas/`
- Graph limpo: orphans **off** (`.obsidian/graph.aiox-brain.json`)
