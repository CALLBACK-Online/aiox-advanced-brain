---
tags: [layer/curso, hub]
---

> Vault: [[00-HOME]] · [[cursos/MOC-Acervo-AIOX]] · [[cursos/entradas/README|entradas]]


# Cursos — AIOX Advanced Brain

Hub das trilhas educacionais deste repositório. Cada curso é **autocontido** (links internos resolvem dentro da própria pasta). Entre cursos, use os caminhos monoespaçados ou abra pelo arquivo indicado.

## Padrão de pastas (português)

Todos os cursos usam a mesma convenção:

| Pasta | Uso |
|-------|-----|
| `aulas/` | Conteúdo das aulas (não `lessons/`) |
| `modulos/` | Índices de módulo (quando houver) |
| `avaliacoes/` | Quizzes e projeto (não `assessments/`) |
| `ponte/` | Pontes para outros cursos/assets |

Tooling de maintainer: `dev/` (não em `cursos/`). Regra: `AGENTS.md` § Superfície do aluno vs maintainer.

**Não sabe qual rota seguir?** Abra [Como estudar o acervo — trilhas por caso](COMO-ESTUDAR.md).

## Navegação recomendada: Obsidian

Os cursos usam Markdown com **wikilinks entre notas**. A forma recomendada de estudar é abrir esta pasta (ou um curso específico) como **vault no [Obsidian](https://obsidian.md)**:

1. Instale o Obsidian.
2. **Open folder as vault** → para o **Graph colorido completo** (cursos + skills + squads), abra a **raiz do repositório**. Alternativas: `cursos/`, `cursos/Introducao-a-Arquitetura-de-Sistemas/`, `cursos/AIOX-Fundamentals/`, `cursos/AIOX Advanced/`, `cursos/AIOX-Agent-Engineering/`, `cursos/AIOX-Design/`, `cursos/AIOX-Productizacao/`, `cursos/AIOX-Advanced-Squads/`, `cursos/AIOX-Enterprise/` ou `cursos/Obsidian-IA/`.
3. Comece por `00-HOME.md` (raiz) ou pelo `README.md` do curso; use Graph view com as cores do acervo.
4. Mapas: `cursos/MOC-Acervo-AIOX.md`, `cursos/MOC-Skills.md`, `cursos/MOC-Squads.md`.

No GitHub ou em editores genéricos os arquivos abrem, mas o grafo de ~2.000 links do AIOX Advanced funciona melhor no Obsidian. Instruções completas: README na raiz do repositório.

## Trilhas

| Curso | Para quê | Comece em |
|-------|----------|-----------|
| **Obsidian + IA** | Mini (9 aulas): vault, Graph colorido, captura, Context Brief, execução e retorno | `cursos/Obsidian-IA/README.md` |
| **Introdução à Arquitetura de Sistemas** | Base técnica: componentes, dados, comunicação, fan-out/fan-in, escala, operação, segurança e agentes | `cursos/Introducao-a-Arquitetura-de-Sistemas/README.md` |
| **AIOX Fundamentals** | Core: instalação, anatomia, 12 agents, contexto, story e validação básica | `cursos/AIOX-Fundamentals/README.md` |
| **AIOX Advanced** | Método: mindset, contexto, SDC, determinismo e brownfield | `cursos/AIOX Advanced/README.md` |
| **AIOX Advanced Squads** | Rota de aplicação: um squad publicado por aula, briefing e evidência | `cursos/AIOX-Advanced-Squads/README.md` |
| **AIOX Agent Engineering** | Rota de aplicação: projetar, construir, orquestrar e operar capacidades agentic | `cursos/AIOX-Agent-Engineering/README.md` |
| **AIOX Design** | Rota de aplicação: repertório → contrato → Storybook → governança e prova visual | `cursos/AIOX-Design/README.md` |
| **AIOX Productização** | Rota de aplicação: capacidade comprovada → oferta, distribuição, formato e monetização | `cursos/AIOX-Productizacao/README.md` |
| **AIOX Enterprise — Visão Operacional e Prontidão** | Preview: diagnosticar se a operação já pede infraestrutura mantida | `cursos/AIOX-Enterprise/README.md` |

## Jornada completa: núcleo comum + rotas de aplicação

`estudar o acervo → entender sistemas → operar o Core → aplicar o método → escolher a aplicação`

1. **Obsidian + IA** — faça o onboarding completo se o vault for novo; quem já domina Obsidian pode usar a evidência de entrada como diagnóstico.
2. **Introdução à Arquitetura de Sistemas** — faça completo se os termos técnicos ainda travam; use o mapa de termos para revisão seletiva.
3. **AIOX Fundamentals** — instale/audite o Core, conheça os agents e conclua o primeiro ciclo local.
4. **AIOX Advanced — 28 aulas / 6 módulos (5 de conteúdo + Capstone)** para dominar método, contexto, SDC, determinismo e brownfield.

Depois do núcleo comum, escolha uma ou combine rotas de aplicação:

- **AIOX Advanced Squads:** operar especialistas publicados.
- **AIOX Agent Engineering:** construir ou colocar uma capacidade agentic em produção.
- **AIOX Design:** materializar contrato visual, Storybook e governança.
- **AIOX Productização:** transformar uma capacidade comprovada em oferta e experimento de mercado.

Esses quatro cursos são partes canônicas da jornada atual. Eles não formam uma fila universal: o gate da missão decide a rota. Agent Engineering pode levar a Productização; Agent Engineering, Design e Productização podem terminar em Squads quando a execução pedir especialistas publicados.

Depois do Advanced e de uma execução real, o **preview AIOX Enterprise** ajuda a decidir se a operação já pede uma base mantida. Ele diagnostica integração, governança e observabilidade recorrentes. Não entrega componentes proprietários.

**Fronteira Agent Engineering × Productização (1 página):** `cursos/MOC-Agent-Engineering-vs-Productizacao.md` — o que não misturar entre capacidade técnica e mercado.

Diagnósticos permitem pular conteúdo já dominado; não mudam a responsabilidade de cada etapa nem fazem Arquitetura e AIOX Fundamentals virarem o mesmo curso.

## Da formação à operação

Há três momentos na jornada de produto:

`AIOX Fundamentals → AIOX Advanced → AIOX Enterprise`

- **Fundamentals:** concluir o primeiro ciclo no Core com evidência.
- **Advanced:** transformar intenção em sistema entregue, com método, contexto, SDC e gates.
- **Enterprise:** operar com infraestrutura proprietária mantida quando integrar e sustentar a base de produção já virou o gargalo.

Os oito cursos formativos deste acervo desenvolvem as duas primeiras capacidades. O Enterprise não é um curso com mais módulos. É o próximo contexto para quem já constrói e precisa sustentar a operação com menos fragmentação.

[Compare as três etapas](../JORNADA-AIOX.md) e faça o preview [AIOX Enterprise — Visão Operacional e Prontidão](AIOX-Enterprise/README.md).

## Contratos de passagem

| De → para | Você avança quando… | Artefato que atravessa a ponte |
|-----------|----------------------|-------------------------------|
| Obsidian + IA → Introdução à Arquitetura | localiza uma fonte, registra aprendizado e prepara uma missão de estudo | captura ou MOC justificado + Context Brief de estudo |
| Introdução à Arquitetura → AIOX Fundamentals | explica o fluxo, o estado, as falhas e os trade-offs de um sistema pequeno | arquitetura explicável + dúvidas abertas |
| AIOX Fundamentals → Advanced | instala/audita o Core, escolhe o agent e fecha uma story local | context pack + story + evidências + handoff |
| Advanced → Advanced Squads | domina taxonomia, briefing, gates e fronteiras de execução | mission brief + critérios de aceite |
| Advanced → Agent Engineering | domina o método e precisa construir/orquestrar uma capacidade própria | capability brief + caso representativo + critérios de operação |
| Advanced → AIOX Design | possui uma story visual e precisa impedir deriva | briefing de interface + estados + aceite visual |
| Advanced → Productização | já possui capacidade executável e evidência de valor | contrato da capacidade + prova + limitações |
| Agent Engineering → Productização | a capacidade executa e produz valor observável | contrato de execução + evidência + limitações |
| Agent Engineering / Design → Advanced Squads | a missão pede um especialista publicado para continuar | briefing específico + limites da capacidade ou do sistema visual |
| Productização → Advanced Squads | oferta e experimento pedem execução comercial especializada | decision pack + hipótese + canal + critério de parada |
| Advanced Squads → operação recorrente | escolhe e opera especialistas sem confundir orientação com runtime | routing decision + artefatos + validation report + retrospectiva reutilizável |
| Advanced + operação real → vitrine Enterprise | o gargalo passou de aprendizagem para recorrência, integração ou governança | retrospectiva + custo operacional + decisão de prontidão |

## Matriz método → rota de aplicação → operação

| Tema | Dono curricular | Operação publicada |
|------|-----------------|--------------------|
| Método, SDC, determinismo, brownfield | `AIOX Advanced/` | Capstone do próprio curso |
| Taxonomia, research, criação, routing, harness e produção | `AIOX-Agent-Engineering/` | Squads 01–09 e 22–24, conforme a missão |
| Contrato visual, taxonomia, variantes e quality gate visual | `AIOX-Design/` | Squads 13–15 |
| Oferta, ROI, distribuição e monetização | `AIOX-Productizacao/` | Squads 19–21, quando maturidade e briefing permitirem |
| Catálogo e uso dos 24 squads | `AIOX-Advanced-Squads/` | Asset correspondente em `squads/` |
| Prontidão para operação mantida | `AIOX-Enterprise/` (vitrine) | Decisão informada; componentes proprietários não estão neste acervo |

Núcleo comum: `cursos/Obsidian-IA/README.md` → `cursos/Introducao-a-Arquitetura-de-Sistemas/README.md` → `cursos/AIOX-Fundamentals/README.md` → `cursos/AIOX Advanced/README.md`. Depois: Squads, Agent Engineering, Design ou Productização conforme o gate da missão.

Matriz completa e pontes:  
`cursos/AIOX Advanced/ponte/pre-requisitos-arquitetura.md` · `cursos/AIOX Advanced/ponte/trilhas-de-aplicacao.md` · `cursos/AIOX-Advanced-Squads/ponte/pre-requisitos-advanced.md`

## Layout do acervo

| Pasta | Uso |
|-------|-----|
| `skills/` | Skills para copiar à IDE (67); inventário: `cursos/MAPA-SKILLS.md`; core no Fundamentals |
| `squads/` | Squads para copiar ao projeto |
| `cursos/` | Cursos navegáveis (esta pasta) |
| `notas/` | Captura local do aluno (não polui aulas canônicas) |

Não há runtime AIOX completo neste repositório: estude aqui, leve um Context Brief + o menor asset ao projeto, execute lá e devolva o aprendizado. Segundo cérebro do acervo: `skills/aiox-brain/SKILL.md`.

## Graph / vault

- Home: `00-HOME.md` (raiz do repo)
- Pontes de skill: `cursos/entradas/`
- Anotações: `notas/`
- Graph limpo: orphans **off** (`.obsidian/graph.aiox-brain.json`)
