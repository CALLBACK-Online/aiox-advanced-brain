---
type: course
course: aiox-advanced-squads
title: AIOX Advanced Squads
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
sharing_boundary: cursos
source: squads/ + skills/ + catalog.json
source_version: 1.2.0
curriculum_modules: 6
lessons: 25
tags: [curso, aiox-advanced, squads, layer/curso]
---

# AIOX Advanced Squads

> Da escolha do squad à evidência de uma execução real.

Este curso ensina a **usar os 24 squads** publicados neste acervo (`squads/`). Cada aula cobre um squad: quando escolher, quando evitar, que entrada preparar, como ativar, qual fluxo seguir e que evidência exigir.

**Aulas:** 25 (1 intro + 24 squads) · **Módulos:** 6 · **Quizzes:** 6 · **Projeto integrador:** 1

- [Guia de execução](Guia-de-execucao.md)
- [Mapa de decisão](Mapa-de-decisao.md)
- [Guia dos agentes (AGENT-GUIDE)](AGENT-GUIDE.md)
- [Roteador agent-readable](agent-router.json)
- [Avaliações](Assessments.md)
- [Projeto integrador](Projeto-Integrador.md)
- [Rubrica](Rubrica.md)
- [Fontes e snapshot](FONTES.md)
- [Pré-requisitos Advanced](ponte/pre-requisitos-advanced.md)

## Pré-requisito

Curso método: pasta `cursos/AIOX Advanced/`. Ponte: [Pré-requisitos no AIOX Advanced](ponte/pre-requisitos-advanced.md). Hub: `cursos/README.md`.

**Entrada esperada:** mission brief, critérios de aceite e domínio da taxonomia agent/task/skill/workflow/squad. Este curso não reensina instalação do Core nem o método; ele transforma essas bases em operação especializada.

Comece por [00 — Como usar este curso](aulas/00-como-usar-este-curso.md).

## Resultado do curso

Ao concluir, você consegue transformar uma missão em quatro decisões explícitas:

1. o squad certo para o problema;
2. o briefing mínimo que reduz retrabalho;
3. o modo de ativação no **seu** projeto (depois de copiar `squads/{nome}`);
4. a evidência que prova que o squad entregou valor.

**Saída da rota:** routing decision + briefings + artefatos + validation report + retrospectiva. Esse pacote prova que o método aprendido no Advanced virou operação especializada reproduzível; ele é a base para repetir a missão ou governá-la como operação recorrente.

## O próximo gargalo

Uma execução validada prova que você sabe operar um squad. Antes de buscar mais infraestrutura, repita a missão e confirme que o método se sustenta.

Quando vários squads, projetos e fontes de contexto exigem montagem e manutenção recorrentes, o problema muda. O desafio deixa de ser escolher o especialista e passa a ser governar a operação. Esse é o momento de comparar o acervo adaptável do Advanced com o ambiente mantido do **AIOX Enterprise**.

Vitrine diagnóstica: `cursos/AIOX-Enterprise/README.md`. Comparação completa: `JORNADA-AIOX.md` na raiz do repositório.

### Como ler a sinalização Enterprise nas aulas

As aulas dos squads que possuem uma conexão real com o workspace incluem a seção **O que muda no AIOX Enterprise**. Ela mostra o ganho operacional específico da integração. Também explica qual contexto o squad consome, onde o resultado continua e o que deixa de ser reconstruído manualmente.

A seção só aparece quando essa conexão existe no sistema de produção. Nos demais squads, o curso preserva o escopo do acervo em vez de prometer uma integração inexistente.

## Como este acervo se relaciona com o curso

Este repositório é **biblioteca de distribuição**, não runtime:

| Pasta | Uso |
|-------|-----|
| `squads/` | Fonte canônica dos 24 squads |
| `skills/` | Skills de entrada (quando existirem) para copiar à IDE |
| `cursos/AIOX-Advanced-Squads/` | Este curso (navegável e autocontido em `cursos/`) |

```bash
cp -R squads/research /caminho/do/seu-projeto/squads/
cp -R skills/research /caminho/do/seu-projeto/.claude/skills/   # se houver skill
```

## Módulos

- [M0 — Escolha, pesquisa e domínio](modulos/M0-escolha-pesquisa-dominio.md)
- [M1 — Autonomia e operações](modulos/M1-autonomia-operacoes.md)
- [M2 — Dados e materialização](modulos/M2-dados-materializacao.md)
- [M3 — Marca, experiência e narrativa](modulos/M3-marca-experiencia-narrativa.md)
- [M4 — Aquisição, conteúdo e vendas](modulos/M4-aquisicao-conteudo-vendas.md)
- [M5 — Metacapacidades](modulos/M5-metacapacidades.md)

## Todas as aulas

### M0 — Escolha, pesquisa e domínio

0. [Como usar este curso e o acervo](aulas/00-como-usar-este-curso.md)
1. [Advisory Board — decisões sem groupthink](aulas/01-advisory-board.md)
2. [Research — inteligência e discovery multi-fonte](aulas/02-research.md)
3. [Code Anatomist — engenharia reversa completa](aulas/03-code-anatomist.md)
4. [Domain Decoder — regras de negócio no código](aulas/04-domain-decoder.md)
### M1 — Autonomia e operações

5. [Agent Autonomy — auditar e elevar autonomia](aulas/05-agent-autonomy.md)
6. [Claude Code Mastery — ambiente Claude Code](aulas/06-claude-code-mastery.md)
7. [AIOX SOP — processos repetíveis e auditáveis](aulas/07-aiox-sop.md)
8. [ETL Ops — extrair, transformar e carregar](aulas/08-etl-ops.md)
9. [Runner Ops — runners headless e governança](aulas/09-runner-ops.md)
### M2 — Dados e materialização

10. [Data — analytics e decisões com dados](aulas/10-data.md)
11. [DB Sage — PostgreSQL e Supabase com autoridade](aulas/11-db-sage.md)
12. [ClickUp Ops — materializar processo no ClickUp](aulas/12-clickup-ops-squad.md)
### M3 — Marca, experiência e narrativa

13. [Brand — fundamentos, posicionamento e ativação](aulas/13-brand.md)
14. [Design System — construir a biblioteca visual](aulas/14-design-system.md)
15. [Design Ops — governar o design system no tempo](aulas/15-design-ops.md)
16. [Storytelling — arco, tensão e memorabilidade](aulas/16-storytelling.md)
17. [Slides Creator — decks com narrativa e QA](aulas/17-slides-creator.md)
### M4 — Aquisição, conteúdo e vendas

18. [Conteúdo — Instagram e calendário social](aulas/18-conteudo.md)
19. [Copy — peças de alta conversão](aulas/19-copy.md)
20. [Sales — funil completo de vendas](aulas/20-sales.md)
21. [Hormozi — oferta, leads e escala $100M](aulas/21-hormozi.md)
### M5 — Metacapacidades

22. [Skill Creator Ops — ciclo de vida de skills](aulas/22-skill-creator-ops.md)
23. [Squad Creator — criar uma capacidade organizacional](aulas/23-squad-creator.md)
24. [Squad Creator Pro — DNA, mentes e gates avançados](aulas/24-squad-creator-pro.md)

## Antes de executar qualquer squad

1. Leia o [Guia de execução](Guia-de-execucao.md).
2. Use o [Mapa de decisão](Mapa-de-decisao.md) se ainda houver dúvida entre 2+ squads.
3. Copie o squad para o **seu** projeto; não espere o curso “rodar” o squad sozinho.
4. Confirme efeitos externos (deploy, ClickUp, e-mail, banco) com o operador humano.

## Pergunte diretamente ao seu agente

Você pode descrever a missão sem saber o nome do squad. Use o [Mapa de decisão](Mapa-de-decisao.md), escolha a aula correspondente e monte o briefing com o modelo do próprio curso.

Em outro runtime, use:

```text
Consulte o Mapa de decisão e as aulas deste curso. Escolha o squad mais adequado para a missão abaixo, explique por que não escolheu os vizinhos, monte o briefing mínimo e só sugira comandos que existam no runtime atual.

Missão: {descreva o que você quer alcançar}
```

## Navegação

[Guia de execução](Guia-de-execucao.md) · [Mapa de decisão](Mapa-de-decisao.md) · [Assessments](Assessments.md)
