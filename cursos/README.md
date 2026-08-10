---
tags: [layer/curso, hub]
---

> Vault: [[00-HOME]] · [[cursos/MOC-Acervo-AIOX]] · [[cursos/entradas/README|entradas]]


# Cursos — AIOX Advanced Brain

Hub das trilhas educacionais deste repositório. Cada curso é **autocontido** (links internos resolvem dentro da própria pasta). Entre cursos, use os caminhos monoespaçados ou abra pelo arquivo indicado.

## Navegação recomendada: Obsidian

Os cursos usam Markdown com **wikilinks entre notas**. A forma recomendada de estudar é abrir esta pasta (ou um curso específico) como **vault no [Obsidian](https://obsidian.md)**:

1. Instale o Obsidian.
2. **Open folder as vault** → para o **Graph colorido completo** (cursos + skills + squads), abra a **raiz do repositório**. Alternativas: `cursos/`, `cursos/Introducao-a-Arquitetura-de-Sistemas/`, `cursos/AIOX-Fundamentals/`, `cursos/AIOX Advanced/`, `cursos/AIOX-Design/`, `cursos/AIOX-Advanced-Squads/` ou `cursos/Obsidian-IA/`.
3. Comece por `00-HOME.md` (raiz) ou pelo `README.md` do curso; use Graph view com as cores do acervo.
4. Mapas: `cursos/MOC-Acervo-AIOX.md`, `cursos/MOC-Skills.md`, `cursos/MOC-Squads.md`.

No GitHub ou em editores genéricos os arquivos abrem, mas o grafo de ~2.000 links do AIOX Advanced funciona melhor no Obsidian. Instruções completas: README na raiz do repositório.

## Trilhas

| Curso | Para quê | Comece em |
|-------|----------|-----------|
| **Obsidian + IA** | Mini: vault, captura, Context Brief, execução no projeto e retorno | `cursos/Obsidian-IA/README.md` |
| **Introdução à Arquitetura de Sistemas** | Base técnica: componentes, dados, comunicação, fan-out/fan-in, escala, operação, segurança e agentes | `cursos/Introducao-a-Arquitetura-de-Sistemas/README.md` |
| **AIOX Fundamentals** | Core: instalação, anatomia, 12 agents, contexto, story e validação básica | `cursos/AIOX-Fundamentals/README.md` |
| **AIOX Advanced** | Método: mindset, SDC, taxonomia, determinismo, deploy | `cursos/AIOX Advanced/README.md` |
| **AIOX Design** | Contrato visual e design system para IA (`DESIGN.md`, taxonomia, variantes) | `cursos/AIOX-Design/README.md` |
| **AIOX Advanced Squads** | Operação: um squad por aula, briefing e evidência | `cursos/AIOX-Advanced-Squads/README.md` |

## Jornada canônica

`estudar o acervo → entender sistemas → operar o Core → aplicar o método → operar especialistas`

1. **Obsidian + IA** — faça o onboarding completo se o vault for novo; quem já domina Obsidian pode usar a evidência de entrada como diagnóstico.
2. **Introdução à Arquitetura de Sistemas** — faça completo se os termos técnicos ainda travam; use o mapa de termos para revisão seletiva.
3. **AIOX Fundamentals** — instale/audite o Core, conheça os agents e conclua o primeiro ciclo local.
4. **AIOX Advanced — Rota Essencial até M12** (ou, no mínimo, M1 + M5 + M7 antes da primeira missão com squad).
5. **AIOX Advanced Squads — aula 00**, módulo alinhado à missão e uma execução com evidência.
6. Voltar ao **Capstone / Projeto Integrador do Advanced** para consolidar método + especialistas.

**Especialização lateral:** AIOX Design entra após M9 quando a missão envolver UI, `DESIGN.md` ou deriva visual; ele prepara especialmente as aulas 13–15 de Squads, mas não substitui nenhuma das cinco etapas canônicas.

Diagnósticos permitem pular conteúdo já dominado; não mudam a responsabilidade de cada etapa nem fazem Arquitetura e AIOX Fundamentals virarem o mesmo curso.

## Da formação à operação

Há três momentos na jornada de produto:

`AIOX Fundamentals → AIOX Advanced → AIOX Enterprise`

- **Fundamentals:** concluir o primeiro ciclo no Core com evidência.
- **Advanced:** transformar intenção em sistema operável, com método, squads e gates.
- **Enterprise:** operar com infraestrutura proprietária mantida quando integrar e sustentar a base de produção já virou o gargalo.

Os cursos deste acervo desenvolvem as duas primeiras capacidades. O Enterprise não é um curso com mais módulos: é o próximo contexto operacional para quem já constrói e precisa reduzir fragmentação, governar a execução e acompanhar a evolução do sistema.

[Compare as três etapas e diagnostique o seu próximo passo](../JORNADA-AIOX.md).

## Contratos de passagem

| De → para | Você avança quando… | Artefato que atravessa a ponte |
|-----------|----------------------|-------------------------------|
| Obsidian + IA → Arquitetura | localiza uma fonte, registra aprendizado e prepara uma missão de estudo | captura + MOC + Context Brief de estudo |
| Arquitetura → AIOX Fundamentals | explica o fluxo, o estado, as falhas e os trade-offs de um sistema pequeno | arquitetura explicável + dúvidas abertas |
| AIOX Fundamentals → Advanced | instala/audita o Core, escolhe o agent e fecha uma story local | context pack + story + evidências + handoff |
| Advanced → Advanced Squads | domina taxonomia, briefing, gates e fronteiras de execução | mission brief + critérios de aceite |
| Advanced Squads → Capstone Advanced | escolhe e opera especialistas sem confundir orientação com runtime | routing decision + artefatos + validation report |

## Matriz método → squads

| Tema no AIOX Advanced | Aulas do método (pasta `lessons/`) | Aulas no curso Squads (`aulas/`) |
|----------------------|-------------------------------------|----------------------------------|
| O que é squad / anatomia | `23-…`, `28-…`, `33-…` | `00-como-usar-este-curso.md` + todas |
| Criar squad | `34-…`, `51-…`, `55-…` | `23-squad-creator.md`, `24-squad-creator-pro.md` |
| Research | `36-…`, `37-…`, `40-…` | `02-research.md` |
| Brownfield / código | `31-…`, `38-…`, `53-…` | `03-code-anatomist.md`, `04-domain-decoder.md` |
| Design system | `32-…`, `41-…`–`43-…` (ponte) | **Curso `AIOX-Design/`** + `14-design-system.md`, `15-design-ops.md` |
| Runner / taxonomia | `28-…`–`30-…` | `09-runner-ops.md` |
| Mesa-redonda / decisão | `35-…` | `01-advisory-board.md` |
| Oferta / ROI | `62-…`, `64-…` | `19-copy.md`, `20-sales.md`, `21-hormozi.md` |
| Skills lifecycle | `28-…` | `22-skill-creator-ops.md` |

Sequência de pré-requisitos: `cursos/Obsidian-IA/README.md` → `cursos/Introducao-a-Arquitetura-de-Sistemas/README.md` → `cursos/AIOX-Fundamentals/README.md` → `cursos/AIOX Advanced/README.md` → `cursos/AIOX-Advanced-Squads/README.md`.

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
