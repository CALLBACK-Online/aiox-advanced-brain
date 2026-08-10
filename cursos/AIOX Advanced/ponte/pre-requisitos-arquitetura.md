---
type: bridge
course: aiox-advanced
status: canonical
canonical_scope: cursos/AIOX Advanced
title: Pré-requisitos de arquitetura
---

# Ponte — arquitetura → AIOX Fundamentals → AIOX Advanced

O AIOX Advanced continua sendo o curso canônico do **método AIOX**. A linguagem técnica geral usada pelo método agora tem uma trilha própria em:

`cursos/Introducao-a-Arquitetura-de-Sistemas/README.md`

O path aparece como texto, não como link, para preservar este curso como unidade autocontida.

Entre a base técnica e o método existe a trilha operacional do Core:

`cursos/AIOX-Fundamentals/README.md`

Ela cobre instalação, anatomia do `aiox-core`, os 12 agents e o primeiro ciclo por story. Assim, esta ponte separa duas perguntas:

- **entendo o sistema?** → Introdução à Arquitetura de Sistemas;
- **consigo operar o Core?** → AIOX Fundamentals.

## Quando fazer a base antes

Use a trilha de Fundamentos primeiro se você ainda confunde dois ou mais destes pares:

- frontend × backend;
- estado × evento;
- fila × pub/sub;
- task × job × worker × runner;
- workflow × pipeline;
- concorrência × paralelismo;
- fan-out × fan-in;
- autenticação × autorização;
- runtime × harness;
- deploy × release × rollback.

Se já consegue explicar os pares com um exemplo próprio, avance para o AIOX Fundamentals. Se também já instala o Core, escolhe agents e fecha uma story com evidência, pode entrar direto na Rota Essencial.

## O que foi reaproveitado e reposicionado

| Extensão aplicada no Advanced | Base canônica no novo curso |
|---|---|
| [[14-anatomia-do-agente|Anatomia de um agente]] e [[16-janela-de-contexto|Janela de contexto]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/22-modelo-contexto-memoria-tool-skill.md` |
| [[18-yaml-markdown-json-sweet-spot|YAML, Markdown e JSON para LLM]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/07-json-yaml-markdown-contratos.md` |
| [[24-entidade-como-unidade-de-processo|Entidade como unidade de processo]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/04-estado-entidade-ciclo-de-vida.md` |
| [[52-workflow-vs-comando-manual|Workflow vs comando manual]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/11-workflow-pipeline-batch-stream.md` |
| [[58-ralph-paralelizacao|Ralph e paralelização]] e [[59-quando-paralelizar-vs-sequencial|Paralelizar vs sequencial]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/12-concorrencia-paralelismo-fanout-fanin.md` |
| [[67-harness-ambiente-execucao|Harness do agente]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/17-runtime-harness-ambiente-container.md` |
| [[71-vercel-deploy|Deploy na Vercel]] e [[72-cicd-pipeline-completa|CI/CD completa]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/18-cicd-deploy-rollback.md` |
| [[73-prontidao-de-producao|Prontidão de produção]] | `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/24-capstone-arquitetura-agentic.md` |

“Base canônica” significa: o novo curso ensina o conceito sem exigir AIOX. A aula antiga permanece porque mostra como o conceito muda uma decisão real dentro do AIOX.

## Rota mínima de nivelamento

Para entrar no Advanced sem fazer as 24 aulas, estude estas seis no curso de Fundamentos:

1. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/01-sistema-componentes-fronteiras.md`
2. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/04-estado-entidade-ciclo-de-vida.md`
3. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/11-workflow-pipeline-batch-stream.md`
4. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/12-concorrencia-paralelismo-fanout-fanin.md`
5. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/17-runtime-harness-ambiente-container.md`
6. `cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/22-modelo-contexto-memoria-tool-skill.md`

Depois, no AIOX Fundamentals, confirme ao menos:

1. `cursos/AIOX-Fundamentals/lessons/01-fundamentos/1.4-instalacao-e-primeiro-valor.md`
2. `cursos/AIOX-Fundamentals/lessons/02-sinais-e-contexto/2.2-escolher-o-agente-certo.md`
3. `cursos/AIOX-Fundamentals/lessons/03-validacao-basica/3.4-evidencia-doctor-e-handoff.md`

## Pergunte ao seu agente

```text
Consulte cursos/Introducao-a-Arquitetura-de-Sistemas/AGENT-GUIDE.md,
cursos/AIOX-Fundamentals/AGENT-GUIDE.md e esta ponte.
Diagnostique quais pré-requisitos realmente me faltam para a aula do AIOX
Advanced que quero aplicar. Indique no máximo três aulas de nivelamento,
faça uma pergunta de checagem por conceito e depois retome a aula aplicada.
```

## Evidência de prontidão

Você está pronto para voltar ao Advanced quando consegue:

- desenhar o fluxo principal do sistema;
- nomear onde estado muda e quem é responsável;
- justificar sequência, fan-out e fan-in;
- distinguir orientação de uma execução disponível no runtime;
- instalar ou auditar o Core e escolher o agent correto;
- definir uma evidência que prove conclusão.

← [[cursos/AIOX Advanced/README|Curso]] · → [[ponte/trilha-squads|Trilha de squads]]
