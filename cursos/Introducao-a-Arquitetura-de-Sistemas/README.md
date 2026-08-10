---
type: course
course: introducao-arquitetura-sistemas
title: Introdução à Arquitetura de Sistemas
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
sharing_boundary: cursos
source: adaptação curricular do AIOX Advanced + documentação técnica primária
source_version: 1.0.0
curriculum_modules: 8
lessons: 24
quizzes: 8
questions: 32
tags: [curso, arquitetura, sistemas, ia, fundamentos, layer/curso]
---

# Introdução à Arquitetura de Sistemas

> Entenda o sistema antes de pedir para a IA construí-lo.

Curso introdutório para quem usa Claude Code, Codex ou outro agente para criar software, mas quer compreender o vocabulário, os diagramas e os trade-offs por trás das sugestões técnicas.

**Aulas:** 24 · **Módulos:** 8 · **Quizzes:** 8 · **Questões:** 32 · **Projeto integrador:** 1

- [Mapa de termos](Mapa-de-termos.md)
- [Guia para agentes](AGENT-GUIDE.md)
- [Avaliações](Assessments.md)
- [Projeto integrador](Projeto-Integrador.md)
- [Rubrica](Rubrica.md)
- [Glossário](Glossario.md)
- [Fontes primárias](FONTES.md)
- [Proveniência e reaproveitamento](PROVENIENCIA.md)

## Para quem

- Profissionais não técnicos que já constroem com agentes.
- Product builders que precisam conversar com devs e arquitetos.
- Alunos do AIOX Advanced que encontram termos como fila, cache, runtime, fan-in ou RLS no meio da execução.
- Pessoas técnicas que querem organizar fundamentos antes de avançar para sistemas agentic.

## Resultado do curso

Ao concluir, você consegue:

1. ler um diagrama de arquitetura e explicar o caminho de uma requisição;
2. distinguir estado, dados, cache, fila, evento, processo e worker;
3. decidir entre síncrono/assíncrono e sequencial/paralelo;
4. reconhecer mecanismos básicos de escala, confiabilidade, observabilidade e segurança;
5. comparar monólito modular e microsserviços sem escolher por moda;
6. desenhar um sistema com agentes, ferramentas, memória, guardrails e intervenção humana;
7. questionar uma arquitetura proposta por IA usando evidências e trade-offs.

## Não é

- Bootcamp de programação ou preparação para entrevista de system design.
- Receita para começar com microsserviços, Kubernetes ou qualquer cloud específica.
- Substituto do AIOX Fundamentals ou Advanced: este curso ensina o vocabulário universal; Fundamentals ensina o Core e Advanced ensina o método.
- Autorização para um agente executar deploy, banco ou efeitos externos sem confirmação.

## Como estudar

Cada aula ensina uma decisão pequena. Leia o mapa, faça a prática e mostre sua resposta ao agente para receber feedback imediato. O curso funciona em Markdown, GitHub ou Obsidian.

**Entrada recomendada:** ter concluído o gate de estudo de Obsidian + IA (`cursos/Obsidian-IA/README.md`) ou conseguir localizar, capturar e explicar uma fonte sem depender do agent para navegar.

**Saída para a próxima etapa:** leve ao AIOX Fundamentals sua arquitetura explicável, os trade-offs defendidos e as dúvidas ainda abertas. Aqui você prova que entende o sistema; no próximo curso aprenderá a operar o Core.

Rota padrão:

```text
M1 mapa do sistema → M2 estado → M3 comunicação → M4 execução
        → M5 confiabilidade → M6 operação → M7 fronteiras → M8 agentes
```

Quem já trabalha com software pode fazer os quizzes de M1–M3. Se acertar pelo menos 10 de 12 questões e conseguir explicar os erros, pode iniciar no M4.

## Módulos

1. [M1 — Ler o mapa de um sistema](modulos/M1-ler-o-mapa.md)
2. [M2 — Dados, estado e persistência](modulos/M2-dados-e-estado.md)
3. [M3 — Contratos e comunicação](modulos/M3-contratos-e-comunicacao.md)
4. [M4 — Execução e orquestração](modulos/M4-execucao-e-orquestracao.md)
5. [M5 — Escala e confiabilidade](modulos/M5-escala-e-confiabilidade.md)
6. [M6 — Operação e observabilidade](modulos/M6-operacao-e-observabilidade.md)
7. [M7 — Segurança e fronteiras](modulos/M7-seguranca-e-fronteiras.md)
8. [M8 — Arquitetura de sistemas com agentes](modulos/M8-sistemas-com-agentes.md)

## Todas as aulas

### M1 — Ler o mapa de um sistema

1. [Sistema, componente, fronteira e dependência](aulas/01-sistema-componentes-fronteiras.md)
2. [Cliente, servidor, frontend e backend](aulas/02-cliente-servidor-frontend-backend.md)
3. [HTTP, request, response, API e endpoint](aulas/03-http-request-response-api.md)

### M2 — Dados, estado e persistência

4. [Estado, entidade e ciclo de vida](aulas/04-estado-entidade-ciclo-de-vida.md)
5. [Banco, schema, índice e transação](aulas/05-banco-schema-indice-transacao.md)
6. [Cache, arquivos e object storage](aulas/06-cache-arquivos-object-storage.md)

### M3 — Contratos e comunicação

7. [JSON, YAML e Markdown como contratos](aulas/07-json-yaml-markdown-contratos.md)
8. [Comunicação síncrona e assíncrona](aulas/08-sincrono-assincrono.md)
9. [Webhook, fila, evento e pub/sub](aulas/09-webhook-fila-evento-pubsub.md)

### M4 — Execução e orquestração

10. [Processo, task, job, worker e runner](aulas/10-processo-task-job-worker-runner.md)
11. [Workflow, pipeline, batch e stream](aulas/11-workflow-pipeline-batch-stream.md)
12. [Concorrência, paralelismo, fan-out e fan-in](aulas/12-concorrencia-paralelismo-fanout-fanin.md)

### M5 — Escala e confiabilidade

13. [Escala vertical, horizontal e load balancing](aulas/13-escala-load-balancing.md)
14. [Timeout, retry, backoff e rate limit](aulas/14-timeout-retry-backoff-rate-limit.md)
15. [Idempotência, deduplicação e circuit breaker](aulas/15-idempotencia-deduplicacao-circuit-breaker.md)

### M6 — Operação e observabilidade

16. [Logs, métricas, traces e health checks](aulas/16-logs-metricas-traces-health-checks.md)
17. [Runtime, harness, ambiente e container](aulas/17-runtime-harness-ambiente-container.md)
18. [CI/CD, deploy e rollback](aulas/18-cicd-deploy-rollback.md)

### M7 — Segurança e fronteiras

19. [Autenticação, autorização e secrets](aulas/19-autenticacao-autorizacao-secrets.md)
20. [Multi-tenancy, isolamento e RLS](aulas/20-multitenancy-isolamento-rls.md)
21. [Monólito, módulos, microsserviços e acoplamento](aulas/21-monolito-modulos-microsservicos.md)

### M8 — Arquitetura de sistemas com agentes

22. [Modelo, contexto, memória, tool e skill](aulas/22-modelo-contexto-memoria-tool-skill.md)
23. [Orquestrador, squad, human-in-the-loop e quality gate](aulas/23-orquestrador-squad-human-in-loop.md)
24. [Capstone: desenhar e defender uma arquitetura agentic](aulas/24-capstone-arquitetura-agentic.md)

## Pergunte diretamente ao seu agente

```text
Leia o AGENT-GUIDE.md e o Mapa-de-termos.md deste curso. Explique o termo abaixo no nível iniciante, usando uma analogia, um diagrama pequeno e um exemplo do meu projeto. Depois faça uma pergunta de cenário para verificar se eu entendi. Não invente comandos nem recomende tecnologia antes de explicar o trade-off.

Termo ou dúvida: {escreva aqui}
```

## Evidência de conclusão

Você passa quando entrega o [Projeto Integrador](Projeto-Integrador.md): um diagrama de sistema, fluxo de uma operação crítica, decisões de dados/comunicação/confiabilidade/segurança, arquitetura agentic e três trade-offs defendidos pela [Rubrica](Rubrica.md).

## Ordem com as outras trilhas

```text
Obsidian + IA → Introdução à Arquitetura de Sistemas → AIOX Fundamentals → AIOX Advanced
                                                                    ├─ Advanced Squads
                                                                    ├─ Agent Engineering
                                                                    ├─ Design
                                                                    └─ Productização
Advanced + operação real → AIOX Enterprise (vitrine de prontidão)
```

Alunos experientes podem usar o diagnóstico e entrar direto no AIOX Fundamentals; quem já opera o Core pode seguir ao Advanced. Próximo curso canônico: `cursos/AIOX-Fundamentals/README.md`. Hub geral: `cursos/README.md`.
