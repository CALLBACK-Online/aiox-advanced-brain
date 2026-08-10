---
creation_mode: brownfield
status: approved
course_slug: aiox-fundamentals
created_date: "2026-08-10"
instructor: "Equipe AIOX"
mmos_persona:
  enabled: false
token_estimation_log:
  operation: "upgrade aios -> aiox-fundamentals"
  estimated_tokens: 95000
  projected_usage: "seguro"
  user_choice: 1
  timestamp: "2026-08-10"
---

# COURSE BRIEF — AIOX Fundamentals

## 1️⃣ Basic Info

**Título do Curso:**
```
AIOX Fundamentals
```

**Subtítulo:**
```
Base mental e operacional para orquestrar IA com contexto, processo e evidência
```

**Slug:**
```
aiox-fundamentals
```

**Duração total estimada do curso:** 7h45, incluindo três quizzes e projeto final.

**Categoria Principal:** Tecnologia / AI Orchestration.

**Tipo:** [x] MISTO — conceitual, técnico e prático.

**Ferramenta:** Framework AIOX (`@aiox-squads/core`).

**Nível:** Iniciante.

**Pré-requisitos:** computador com Node.js 18+, npm 9+, Git e uma IDE/CLI suportada. Não exige experiência profissional em programação. Introdução à Arquitetura de Sistemas é a base recomendada; o aluno pode usar seu projeto integrador como diagnóstico e revisar apenas as lacunas.

## 2️⃣ Público-alvo (ICP)

**Idade principal:** 25–60 anos.

**Ocupação atual:** desenvolvedores, empreendedores, profissionais de produto, criativos e pessoas não técnicas com uma ideia concreta para materializar.

**Momento atual do avatar:** usa IA de forma fragmentada, depende de tentativa e erro ou não sabe qual agente/processo escolher.

**Estado mental/emocional predominante:** curiosidade acompanhada de sobrecarga, receio do terminal ou frustração com ferramentas desconectadas.

**Dor superficial:** não sabe por onde começar no AIOX.

**Dor real:** perde contexto, escolhe o executor errado e não consegue provar que uma entrega está correta.

**Dor profunda:** sente que a complexidade técnica o impede de transformar visão em algo funcional e sob seu controle.

**Estado atual (ANTES do curso):**
```
Faz pedidos isolados para IA, confunde ferramenta com método e aceita respostas sem evidência.
```

**Estado desejado (DEPOIS do curso):**
```
Lê o contexto, escolhe uma rota AIOX proporcional, executa por story e fecha com validação reproduzível.
```

## 3️⃣ Learning Objectives e Outline

Ao final do curso, o aluno será capaz de:

1. Explicar a proposta do framework AIOX, a prioridade CLI First e o modelo de planejamento mais desenvolvimento.
2. Instalar o core, ativar um agent e confirmar first-value em uma IDE compatível.
3. Comparar agent, task, skill, workflow e squad para selecionar a menor unidade que resolve o problema.
4. Aplicar o ciclo story-driven com contexto, autoridade e handoffs explícitos.
5. Avaliar uma entrega usando quality gates, diagnósticos e evidência reproduzível.

**Framework pedagógico:** Backward Design + Microlearning + Bloom, estruturado em GPS e Didática Lendária.

**Relação prática/teoria:** 60/40.

**MÓDULO 1: Fundamentos**
- O que é AIOX.
- CLI First e as duas fases.
- Anatomia do framework.
- Instalação e primeiro valor.

**MÓDULO 2: Sinais e contexto**
- Ler o contexto antes de agir.
- Escolher o agent certo.
- Task, skill, workflow ou squad.
- Greenfield, brownfield e story.

**MÓDULO 3: Validação básica**
- Qualidade em três camadas.
- Autoridade e permissões.
- Ciclo da story na prática.
- Evidência, doctor e handoff.

## 4️⃣ Voice

**Usar clone MMOS como instrutor?** Não.

**Instrutor editorial:** Equipe AIOX.

**Tom:** técnico-objetivo, direto, acolhedor com iniciantes e sem hype.

**Estilo:** começa pelo porquê, explica jargão na primeira ocorrência, usa analogias concretas e termina com aplicação CLI First.

**Vocabulário preferido:** criador, orquestração, framework AIOX, CLI First, agent, task, workflow, squad, Constitution.

**Evitar:** AIOS como nome atual, “plataforma AIOX”, promessas absolutas e simplificação que esconda trade-offs.

## 5️⃣ Format & Delivery

**Formato principal:** curso self-paced em Markdown.

**Estrutura:** 3 módulos, 12 aulas, 3 quizzes e 1 projeto final.

**Duração por aula:** 30 minutos, combinando leitura, exercício e prática de recuperação.

**Táticas de engajamento:** diagramas textuais, cenários, checklists, ação rápida, reflexão e prática sem assistência de IA.

**Avaliações:** quiz por módulo e projeto de condução de uma mudança pequena de ponta a ponta.

## 6️⃣ Commercial

**Estratégia de monetização:** fora do escopo deste artefato; curso técnico de suporte ao ecossistema AIOX.

**Preço sugerido:** não definido. Nenhuma decisão financeira foi inferida.

**Posicionamento:** primeira camada de compreensão operacional antes de cursos especializados ou AIOX Advanced.

## 7️⃣ Success Metrics & Constraints

**Métricas de sucesso:**
- 100% das aulas vinculadas a fontes canônicas do AIOX Core.
- 100% das aulas com objetivo, contexto, passos, exemplo, erro comum e prática.
- Pelo menos um objetivo de Bloom em Apply ou nível superior.
- Projeto final com evidência de contexto, execução e validação.

**Restrições:**
- Não ensinar comandos que não existam no snapshot de origem.
- Não misturar recursos comerciais do Pro com o core open source.
- Não assumir paridade total de hooks entre IDEs.
- Não fazer afirmações financeiras ou de performance sem fonte canônica.

## 8️⃣ Sources & Approval

**Fonte técnica:** checkout rastreado de `SynkraAI/aiox-core`, commit `a68bd88f45e560f606e9bdc8a0f663570bdcef88`, pacote `@aiox-squads/core` versão `5.2.9`.

**Fonte de ICP e voz:** contexto canônico do negócio AIOX em modo somente leitura.

**Aprovação curricular:** arquitetura de três módulos herdada do registro `aiox-fundamentals` em `apps/aiox-design-system/current/course-manifest.yaml`; o pedido do usuário autorizou a modernização do conteúdo brownfield.

**Manifesto de fontes:** `sources/SOURCE-MANIFEST.yaml`.
