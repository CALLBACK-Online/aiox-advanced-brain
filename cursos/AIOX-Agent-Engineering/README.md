---
type: course
course: aiox-agent-engineering
title: AIOX Agent Engineering
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
sharing_boundary: cursos
source: curadoria de 27 aulas da edição 1 do AIOX Advanced + capstone novo
source_version: 1.1.0
curriculum_modules: 7
lessons: 28
quizzes: 6
questions: 24
tags: [curso, agentes, orquestracao, runtime, producao, layer/curso]
---

# AIOX Agent Engineering

> Projetar, construir, orquestrar, escalar e colocar em produção uma capacidade agentic verificável.

Essa é a promessa única do curso. Research reduz incerteza; arquitetura e construção materializam a capacidade; orquestração, runtime e produção provam que ela funciona fora da sessão do autor.

**Aulas:** 28 · **Módulos:** 6 + Capstone · **Quizzes:** 6 · **Questões:** 24

- [Brief do curso](COURSE-BRIEF.md)
- [Avaliações](Assessments.md)
- [Projeto integrador](Projeto-Integrador.md)
- [Rubrica](Rubrica.md)
- [Fontes](FONTES.md) · [Proveniência](PROVENIENCIA.md)
- [Guia para agentes](AGENT-GUIDE.md)

## Para quem

- Quem já concluiu o núcleo comum até o AIOX Advanced — ou prova o mesmo gate com uma story fechada por método e evidência.
- Quem precisa criar ou adaptar agents, squads, workflows e runners.
- Quem quer tirar uma capacidade da IDE e operá-la por harness, API ou pipeline.

## Resultado do curso

Ao concluir, você consegue:

1. escolher a unidade correta entre task, skill, agent, workflow, squad e runner;
2. reduzir incerteza com research, prior art e engenharia reversa;
3. construir uma capacidade mínima com papéis, contratos e gates;
4. decidir sequência, paralelismo, routing e dependências;
5. expor a capacidade fora da IDE;
6. entregar URL, pipeline e checklist de prontidão com limites conhecidos.

## Não é

- Curso básico de instalação ou primeiro ciclo AIOX — isso pertence ao AIOX Fundamentals.
- Catálogo de squads publicados — isso pertence ao AIOX Advanced Squads.
- Curso de contrato visual — isso pertence ao AIOX Design.
- Curso de oferta, vendas ou monetização — isso pertence ao AIOX Productização.

## Depois da capacidade

Quando a capacidade tem evidência e a pergunta vira “para quem / por quanto / por qual canal?”, saia pela ponte:

- Ponte de saída: [saída para Productização](ponte/saida-para-productizacao.md)
- Mini-curso: `cursos/AIOX-Productizacao/README.md`
- Fronteira em uma página: `cursos/MOC-Agent-Engineering-vs-Productizacao.md`

A escada técnica deste curso (script → runner → API) **não** substitui a decisão comercial de Productização.

## Módulos

1. [M0 — Arquitetura da capacidade](modulos/M0-arquitetura-da-capacidade.md) — aulas 01–06
2. [M1 — Discovery e research](modulos/M1-discovery-e-research.md) — aulas 07–12
3. [M2 — Construção de capacidade](modulos/M2-construcao-de-capacidade.md) — aulas 13–16
4. [M3 — Orquestração e escala](modulos/M3-orquestracao-e-escala.md) — aulas 17–20
5. [M4 — Runtime fora da IDE](modulos/M4-runtime-fora-da-ide.md) — aulas 21–23
6. [M5 — Produção](modulos/M5-producao.md) — aulas 24–27
7. [Capstone](modulos/MC-capstone.md) — aula 28

## Sequência

```text
arquitetura → research → construção → orquestração → runtime → produção → capstone
```

O curso inteiro é a rota principal. Quem já possui uma capacidade pronta pode diagnosticar a entrada pelo checkpoint de cada módulo.

## Todas as aulas

### M0 — Arquitetura da capacidade

1. [Pipeline ETL com agentes](aulas/01-pipeline-etl-com-agentes.md)
2. [Taxonomia Task, Skill, Agent, Workflow e Runner](aulas/02-taxonomia-da-capacidade.md)
3. [Sub-agents × Swarm-agents](aulas/03-subagents-vs-swarm.md)
4. [Runner determinístico](aulas/04-runner-deterministico.md)
5. [Mapear entidades antes do Squad](aulas/05-entidade-e-ciclo-de-vida.md)
6. [Workflow × comando manual](aulas/06-workflow-vs-comando.md)

### M1 — Discovery e research

7. [Mesa-redonda e Advisory Board](aulas/07-mesa-redonda-e-advisory-board.md)
8. [Tech Research](aulas/08-tech-research.md)
9. [Spy/Bench](aulas/09-spy-bench.md)
10. [Code Anatomy e Domain Decoder](aulas/10-code-anatomy-e-domain-decoder.md)
11. [Pasta OS](aulas/11-pasta-os.md)
12. [Research ao PRD](aulas/12-research-ao-prd.md)

### M2 — Construção de capacidade

13. [REUSE > ADAPT > CREATE](aulas/13-reuse-adapt-create.md)
14. [Triagem de squad](aulas/14-triagem-de-squad.md)
15. [Anatomia de squad](aulas/15-anatomia-de-squad.md)
16. [Squad Creator](aulas/16-squad-creator.md)

### M3 — Orquestração e escala

17. [Ralph](aulas/17-ralph.md)
18. [Paralelo vs sequencial](aulas/18-paralelo-vs-sequencial.md)
19. [Routing de modelos](aulas/19-routing-de-modelos.md)
20. [Wave Execute](aulas/20-wave-execute.md)

### M4 — Runtime fora da IDE

21. [Harness](aulas/21-harness.md)
22. [Squad fora da IDE](aulas/22-squad-fora-da-ide.md)
23. [Escada progressiva](aulas/23-escada-progressiva.md)

### M5 — Produção

24. [Supabase via data engineer](aulas/24-supabase-via-data-engineer.md)
25. [Vercel Deploy](aulas/25-vercel-deploy.md)
26. [CI/CD](aulas/26-cicd.md)
27. [Prontidão de produção](aulas/27-prontidao-de-producao.md)

### Capstone

28. [Capstone: capacidade agentic em produção](aulas/28-capstone-capacidade-em-producao.md)

## Evidência de conclusão

Uma cadeia verificável: **Research → PRD → capacidade → orquestração → harness/API → deploy → evidências**, avaliada pela rubrica. Sem credenciais ou autorização para produção, o aluno deve provar o resultado local e registrar o bloqueio; não pode simular URL ou deploy.
