---
type: course-brief
course: aiox-productizacao
course_slug: aiox-productizacao
status: draft
materialization_state: partial
created_date: "2026-08-10"
instructor: "Equipe AIOX"
canonical_scope: cursos/AIOX-Productizacao
sharing_boundary: cursos
source: curadoria das aulas 62–66 do AIOX Advanced
tags: [curso, productizacao, service-as-software, distribuicao, monetizacao, layer/curso]
---

# COURSE BRIEF — AIOX Productização

> Da capacidade que funciona à oferta que alguém entende, testa e paga — sem construir SaaS antes da prova.

**Estado:** brief para aprovação. As cinco aulas-seed já possuem uma primeira materialização; este documento define a fronteira curricular e os gates necessários antes da publicação.

## 1. Decisão curricular

As aulas 62–66 do AIOX Advanced não pertencem ao núcleo de **Agent Engineering**. Elas deixam de responder “como construir e operar uma capacidade agentic?” e passam a responder “como transformar essa capacidade em valor econômico repetível?”.

Recomendação: criar um **mini-curso autocontido**, que também possa ser consumido como trilha opcional depois de Agent Engineering.

```text
Agent Engineering
capacidade confiável + evidência operacional
                    ↓
AIOX Productização
dor + oferta + distribuição + modelo + estágio
                    ↓
experimento comercial com critério de avanço
```

## 2. O que não colocar em Agent Engineering

| Tema | Por que sai de Agent Engineering | Dono curricular |
|------|----------------------------------|-----------------|
| Service-as-Software | Decide empacotamento e wedge comercial, não arquitetura do agente | AIOX Productização |
| Distribuição > Produto | Decide canal, feedback e alocação de tempo, não execução técnica | AIOX Productização |
| Dor, mecanismo, ROI e prova | Constrói proposta de valor e conversa comercial | AIOX Productização |
| Consultoria → App Web → SaaS | Escolhe modelo de entrega e gatilho de transição | AIOX Productização |
| Interno → cliente → produto | Decide estágio de monetização a partir de evidência de uso e pagamento | AIOX Productização |

### Fronteira objetiva

**Agent Engineering termina quando existe:**

- uma capacidade executável;
- entrada e saída definidas;
- runtime ou procedimento de execução conhecido;
- limites, observabilidade e gates;
- evidência de que o resultado funciona.

**AIOX Productização começa quando surge a pergunta:**

- para quem isso resolve uma dor importante?;
- qual parte repetível merece ser empacotada?;
- como traduzir resultado em promessa e ROI?;
- por qual canal testar demanda?;
- devo vender como consultoria, app ou SaaS?;
- já estou no estágio interno, cliente ou produto?

Deploy, harness, reliability, CI/CD e operação do agente continuam em `cursos/AIOX-Agent-Engineering/`. Productização recebe a capacidade pronta como entrada; não reensina sua engenharia.

## 3. Basic info

| Campo | Valor |
|-------|-------|
| **Título** | AIOX Productização |
| **Subtítulo** | Transforme uma capacidade agentic em serviço, oferta e experimento de monetização |
| **Slug** | `aiox-productizacao` |
| **Pasta** | `cursos/AIOX-Productizacao/` |
| **Categoria** | Estratégia de produto · oferta · distribuição · monetização |
| **Tipo** | Mini-curso prático, orientado a decisão e artefato |
| **Nível** | Intermediário |
| **Duração estimada** | 2h30–3h30, incluindo capstone |
| **Formato** | Self-paced em Markdown, legível por pessoa ou agente |
| **Relação prática/teoria** | 70/30 |

## 4. Problema que o curso resolve

### Dor superficial

“Construí algo com agentes, mas não sei como transformar isso em oferta ou produto.”

### Dor real

A pessoa confunde capacidade técnica com demanda. Investe em interface, automação e SaaS antes de provar dor, repetição, canal e disposição de pagamento.

### Dor profunda

O builder usa a construção como proteção contra o mercado: melhora o produto para evitar a conversa que poderia invalidar a tese.

### Antes → depois

| Antes | Depois |
|-------|--------|
| “Meu agente faz várias coisas” | “Este wedge resolve esta dor para este cliente e produz esta prova” |
| Features antes de conversas | Hipótese de canal e experimento com prazo |
| ROI inventado ou genérico | Baseline, premissas e prova identificados |
| SaaS como identidade | Consultoria, app ou SaaS escolhidos por evidência |
| Monetização como desejo | Estágio atual, veto e gate de passagem explícitos |

## 5. Público-alvo

- Alunos do AIOX que já construíram uma automação, workflow, skill, squad ou serviço assistido por IA.
- Consultores e agências que entregam trabalho recorrente e querem aumentar repetibilidade sem fingir que já possuem um SaaS.
- Founders e product builders que precisam escolher o próximo formato de entrega.
- Profissionais internos que provaram valor dentro da própria operação e querem testar um primeiro cliente.

**Não é o público primário:** quem ainda não possui um caso de uso, resultado demonstrável ou processo minimamente repetível. Nesse caso, a rota correta é Fundamentos/Agent Engineering antes de Productização.

## 6. Pré-requisitos

### Mínimo

- Uma capacidade real que produza alguma saída observável.
- Um caso de uso ou dor candidata.
- Disponibilidade para conversar com usuários ou clientes; leitura isolada não conclui o curso.

### Recomendado

- Entender a diferença entre skill, workflow, squad e produto.
- Ter uma execução documentada com entrada, saída, tempo, custo e limitações.
- Saber que “funciona tecnicamente” não prova demanda.

Não é necessário concluir todo Agent Engineering. É necessário chegar com **uma capacidade e uma evidência**, não apenas uma ideia.

## 7. Objetivos de aprendizagem

Ao concluir, a pessoa consegue:

1. **Identificar** o wedge mais doloroso, repetível e comprovável de um serviço habilitado por agentes.
2. **Traduzir** capacidade técnica em dor, mecanismo, promessa, ROI e prova sem inventar números.
3. **Definir** uma hipótese de distribuição com canal, público, mensagem, ação e métrica.
4. **Escolher** entre consultoria, app web e SaaS usando repetição, margem, variabilidade e demanda.
5. **Classificar** a iniciativa nos estágios interno, cliente ou produto e aplicar vetos antes de avançar.
6. **Entregar** um pacote de decisão de productização que diga o que testar agora e o que deliberadamente não construir.

Bloom dominante: **Analyze → Evaluate → Create**.

## 8. Estrutura curricular

### M1 — Oferta antes do produto

**Resultado:** wedge e oferta de uma página com dor, mecanismo, ROI e prova.

1. [Service-as-Software: a era do serviço produtivado](aulas/01-service-as-software.md)
2. [Vender pela dor e ROI, não pela tecnologia](aulas/02-dor-e-roi.md)

**Quiz M1:** 4 questões de cenário.  
**Evidência:** one-pager da oferta + tabela de premissas de ROI.

### M2 — Distribuição, formato e monetização

**Resultado:** experimento de distribuição, caminho de produto e estágio atual com gates.

3. [Distribuição > Produto](aulas/03-distribuicao-vs-produto.md)
4. [Três caminhos: Consultoria → App Web → SaaS](aulas/04-caminhos-de-produto.md)
5. [Três estágios: interno → cliente → produto](aulas/05-estagios-de-monetizacao.md)

**Quiz M2:** 4 questões de cenário.  
**Evidência:** plano de experimento + cartão de caminho + cartão de estágio.

### Ordem adaptada

A fonte original segue 62 → 63 → 64 → 65 → 66. O mini-curso adota **62 → 64 → 63 → 65 → 66**:

1. definir o serviço produtizado;
2. expressar a dor e o valor;
3. levar a hipótese ao mercado;
4. escolher o formato de entrega;
5. reconhecer o estágio de monetização.

Oferta vem antes de canal; canal vem antes de software mais pesado.

## 9. Capstone — Productization Decision Pack

O aluno escolhe uma capacidade real e entrega um pacote único com seis partes:

1. **Wedge card** — cliente, dor, job repetível, entrada, saída e limite.
2. **Oferta de uma página** — dor → mecanismo → promessa → prova → anti-escopo.
3. **ROI auditável** — baseline, hipótese, fórmula, premissas e o que ainda precisa ser medido.
4. **Experimento de distribuição** — canal, público, mensagem, ação, prazo e métrica.
5. **Decisão de formato** — consultoria, app ou SaaS agora; alternativa recusada e gatilho de revisão.
6. **Cartão de estágio** — interno, cliente ou produto; prova atual, veto e próximo gate.

### Gate de aprovação

O capstone passa quando:

- todas as afirmações de valor estão ligadas a evidência ou marcadas como hipótese;
- existe um único wedge prioritário;
- o experimento pode gerar aprendizado em até 14 dias;
- a escolha de formato cita pelo menos três critérios operacionais;
- o aluno nomeia algo que não construirá agora;
- o próximo estágio exige prova, não entusiasmo.

## 10. Avaliação

| Artefato | Critério |
|----------|----------|
| Quiz M1 | Distinguir capacidade, wedge, dor, mecanismo, ROI e prova |
| Quiz M2 | Escolher canal, formato e estágio diante de cenários ambíguos |
| Práticas das aulas | Um artefato pequeno e verificável por aula |
| Capstone | Decisão integrada com hipótese, evidência, veto e próximo teste |

**Regra:** acertar quiz sem conversar com o mercado não conclui o curso. O quiz mede julgamento; o capstone mede transferência.

## 11. Didática e leitura por agentes

Cada aula deve conter:

1. objetivo verificável;
2. mapa da decisão;
3. caso com antes/depois;
4. distinções e anti-padrões;
5. router de próxima ação;
6. prática com template copiável;
7. portão de conclusão;
8. prompt para feedback do agente;
9. origem curricular e navegação interna.

### Contrato para Claude Code, Codex ou agente genérico

O futuro `AGENT-GUIDE.md` deve rotear para este curso quando a pessoa disser, por exemplo:

- “Como transformo este workflow em serviço?”
- “Devo fazer consultoria ou SaaS?”
- “Como provo ROI sem inventar?”
- “Tenho produto, mas ninguém conhece.”
- “Isso já está pronto para vender?”
- “Uso interno já conta como produto?”

Anti-sinais que devem permanecer em Agent Engineering:

- “Meu agente entra em loop.”
- “Como desenho o workflow?”
- “Preciso de runner, harness ou fila.”
- “Como faço deploy, CI/CD ou observabilidade?”

## 12. Voz

**Tom:** direto, comercialmente sóbrio, baseado em evidência e sem teatro de startup.

**Usar:** dor observável, hipótese, baseline, prova, wedge, canal, repetição, margem, gate, veto e próximo teste.

**Evitar:** “escala infinita”, “renda passiva”, TAM fabricado, ROI sem premissa, “é só virar SaaS”, jargão de growth sem comportamento observável e promessa financeira.

## 13. Fontes e propriedade curricular

| Aula nova | Seed no AIOX Advanced |
|-----------|-----------------------|
| 01 — Service-as-Software | `cursos/AIOX Advanced/lessons/62-service-as-software.md` |
| 02 — Dor e ROI | `cursos/AIOX Advanced/lessons/64-vender-pela-dor-e-roi.md` |
| 03 — Distribuição | `cursos/AIOX Advanced/lessons/63-distribuicao-vs-produto.md` |
| 04 — Caminhos de produto | `cursos/AIOX Advanced/lessons/65-tres-caminhos-de-produto.md` |
| 05 — Estágios de monetização | `cursos/AIOX Advanced/lessons/66-tres-estagios-de-monetizacao.md` |

Após estabilização:

- AIOX Productização torna-se o dono canônico dos conceitos comerciais.
- As aulas 62–66 permanecem no Advanced como extensões aplicadas/ponte, preservando paths e wikilinks.
- Agent Engineering não duplica as cinco aulas; recebe apenas uma ponte na saída da capacidade técnica.
- O módulo M11 do Advanced separa claramente 62–66 (estratégia comercial) de 67–68 (engenharia/runtime).

## 14. Pontes operacionais

Este curso ensina **julgamento e artefato**. Execução especializada permanece nos assets existentes:

- `cursos/AIOX-Advanced-Squads/aulas/19-copy.md` — mensagem e conversão;
- `cursos/AIOX-Advanced-Squads/aulas/20-sales.md` — processo comercial;
- `cursos/AIOX-Advanced-Squads/aulas/21-hormozi.md` — oferta e aquisição sob framework específico;
- `skills/copy/`, `skills/sales/`, `skills/hormozi/` — procedimentos no projeto destino.

O curso não simula ativação desses assets nem transforma o capstone em operação de CRM.

## 15. Anti-escopo

- Engenharia de agentes, prompts, context window, tools, memória ou orquestração.
- Tutorial de deploy, billing, Stripe, Supabase ou stack SaaS.
- Curso completo de vendas, copywriting, pricing ou growth.
- Plano de negócio, valuation, captação ou modelagem financeira.
- Pesquisa de mercado extensa sem uma decisão de productização delimitada.
- Promessa de receita ou ROI não sustentada por dados do aluno.

## 16. Métricas de sucesso curricular

- 100% das aulas com objetivo, prática, portão e evidência.
- 5/5 aulas com origem rastreada nas seeds 62–66.
- 0 conteúdo comercial duplicado em Agent Engineering.
- 2 quizzes, 8 questões, gabarito balanceado A/B/C/D.
- 1 capstone com rubrica e decisão go/no-go.
- 100% dos links resolvendo dentro de `cursos/AIOX-Productizacao/`.
- Bootstrap em `AGENTS.md` e `CLAUDE.md` roteando perguntas comerciais ao curso.
- `npm run validate` verde antes de publicar.

## 17. Sequência para finalizar a materialização

1. Aprovar este brief e a ordem adaptada das aulas.
2. Criar `README.md`, módulos M1/M2, quizzes, rubrica, projeto e `AGENT-GUIDE.md`.
3. Curar as cinco aulas: remover navegação herdada de M11 e adicionar prompts/evidências do novo curso.
4. Criar validador próprio e integrar em `npm run validate`.
5. Marcar 62–66 no Advanced como `applied-extension` com owner em AIOX Productização.
6. Remover 62–66 do outline de Agent Engineering e adicionar ponte de saída.
7. Atualizar hub, catálogo, MOCs e pacote; validar.

## 18. Decisões pedidas ao revisor

- [ ] Aprovar o nome **AIOX Productização** e o slug `aiox-productizacao`.
- [ ] Aprovar o formato de mini-curso: 2 módulos, 5 aulas, 2 quizzes e 1 capstone.
- [ ] Aprovar a ordem adaptada 62 → 64 → 63 → 65 → 66.
- [ ] Confirmar que conversa/experimento real é requisito de conclusão.
- [ ] Confirmar que as aulas 62–66 saem do escopo de Agent Engineering.

**Recomendação do brief:** aprovar o mini-curso com cinco aulas. O recorte é pequeno, coerente e fecha numa decisão real; adicionar conteúdo genérico de marketing diluiria a proposta.
