---
type: lesson
course: aiox-advanced
course_title: AIOX Advanced
lesson_id: apply-qa-fixes-loop
lesson_position: 49
title: 'Apply QA Fixes Loop: QA volta para Dev sem perder estado'
source: upstream monorepo/apps/aiox-courses
source_path: content/courses/aiox-advanced/lessons/49-apply-qa-fixes-loop/lesson.md
source_format: lesson.md
synced_at: '2026-08-09'
manual: true
concepts: []
tags:
- curso/aiox-advanced
- lesson
- course-brain
bloom: analyze
reading_minutes: 14
has_mermaid_map: true
map_source: auto-decision_graph
module: M3
sequence: M3.4
track: complete
status: canonical
canonical_scope: Cursos/AIOX Advanced
curated_at: '2026-08-09'
---

# [[Apply QA Fixes]] Loop: QA volta para Dev sem perder estado

← [[48-quality-gate-completo|Quality Gate: QA + Apply QA Fixes + CodeRabbit]] · ↑ [[modulos/Módulo 3 - Ciclo SDC|M3]] · ⌂ [[Cursos/AIOX Advanced/README|Curso]] · → [[06-code-rabbit-boost|Code Rabbit Boost]]

## Mapa desta aula

Decisão-chave da aula — O finding ainda cabe nesta Story?

```mermaid
%%{init: {
  "theme": "dark",
  "flowchart": {
    "curve": "basis",
    "nodeSpacing": 22,
    "rankSpacing": 36,
    "padding": 8,
    "htmlLabels": true,
    "useMaxWidth": true
  },
  "themeVariables": {
    "fontSize": "14px"
  }
}}%%
flowchart TB
  Q["O finding ainda cabe nesta Story?"]
  B0["Sim, é blocker do aceite<br/>Apply fix + re-gate na mesma PR."]
  B1["Sim, mas é nit<br/>Batch de nits no fim ou ignore document…"]
  B2["Não, é outra story<br/>Nova story; não infle a atual."]
  B3["Loop infinito<br/>Breaker: reabrir aceite, split ou redes…"]
  B4["Risco / waiver<br/>WAIVED com dono e data — nunca silêncio."]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
classDef core fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#e2e8f0
  classDef step fill:#0f172a,stroke:#6366f1,stroke-width:1.5px,color:#f1f5f9
  classDef gate fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#e2e8f0
  classDef good fill:#14532d,stroke:#4ade80,stroke-width:1.5px,color:#ecfdf5
  classDef bad fill:#450a0a,stroke:#f87171,stroke-width:1.5px,color:#fef2f2
  classDef warn fill:#422006,stroke:#fbbf24,stroke-width:1.5px,color:#fffbeb
```

> Leia o diagrama antes do texto longo. Depois volte e confira.

> Feedback loop curto: findings viram correção na mesma Story, com contexto e evidência intactos.

**Objetivos de aprendizagem:**
- Listar os quatro pedaços de estado que o loop deve preservar (story, PR, aceite, evidência). _(remember)_
- Explicar o que significa preservar estado da Story no loop QA→Dev e por que issue zumbi mata autonomia. _(understand)_
- Operar um ciclo Apply QA Fixes: findings → classificar → patch → re-run gate. _(apply)_
- Identificar quando o loop deve parar (waiver, re-split, redesign ou bloqueio). _(analyze)_

---

## O que você consegue no fim desta aula

*G · Destino*

Destino claro antes de qualquer lista de findings.

Ao final desta aula você vai conseguir três coisas concretas:

1. Descrever o loop **fail → fix → re-gate** sem abrir issue zumbi.
2. Classificar findings em **block / major / nit / outra-story** com critério.
3. Acionar o **circuit breaker** quando o mesmo erro volta sem delta real.

Se você sair daqui ainda "abrindo 12 tickets e torcendo", a aula falhou.
Autonomia sem loop curto é fábrica de meia-calça com board bonito.

- **Objetivos da aula** (Preservar estado (story/PR/aceite/evidência); Operar um ciclo completo de fixes; Saber quando parar o loop)
- **Resultado tangível**: Um ciclo documentado: findings classificados, ordem de patch, critério de re-gate e breaker.
- **Não é o destino**: Zero findings pra sempre. É feedback curto com contexto intacto.

---

## A fábrica de issue zumbi

*P · Onde você está*

Empatia com o ponto de partida real do operador.

Cara, o pior anti-pattern de QA: achar 12 problemas, abrir 12 issues, Dev esquece
o contexto, story morre em "later". O board fica rico. O produto fica podre.

Apply QA Fixes é o oposto: o achado volta pro Dev **na mesma story**, com o
mesmo aceite, o mesmo PR, o mesmo thread de evidência. Feedback loop curto.

Se você está aqui, provavelmente já sentiu um destes sintomas:

- QG falhou, criaram ticket novo, a story original foi pra limbo.
- Mesmo finding volta três vezes e ninguém relê o aceite.
- Nits e blockers na mesma pilha — tudo "urgente" e nada priorizado.
- "Corrige depois" vira merge com dívida invisível.

Beleza. A partir daqui a gente troca limbo por **esteira**: o QG deixa de ser
muro e vira loop com estado.

**Onde a maioria trava**
- 12 findings → 12 issues zumbis
- Patch em branch paralela sem vínculo
- Re-gate sem saber o que mudou

**Onde o operador vai**
- Findings na mesma story/PR
- Classificar antes de patchar
- Delta explícito a cada ciclo

---

## O subprocesso que faz o SDC respirar

*S · Rota*

Invisível quando funciona. Fatal quando some.

O ciclo da story (aula 47) e o [[Quality Gate]] (aula 48) só fecham se existir um
subprocesso entre FAIL e o próximo PASS: **Apply QA Fixes**.

Sequência canônica:

findings → classificar (block/major/nit/outra) → patch na mesma trilha → re-run QG
→ PASS ou próximo ciclo → breaker se teimosia.

Prior-art: [[CodeRabbit]] (aula 06) joga findings no colo; o gate completo (48)
exige veredito; o [[Ciclo do Story|ciclo do story]] (10/47) exige estado. Este loop é a **costura**
entre os três — sem drama de "processo novo", com disciplina de não perder o fio.

- **4**: pedaços de estado
- **↻**: loop até PASS ou breaker
- **0**: espaço pra limbo 'later'

- **status**: apply qa fixes
- **meta**: preserve=story+pr+aceite
- **meta**: loop=fail→fix→re-gate
- **ready**: ready to loop

**Legenda de cores**

O que cada cor sinaliza nesta aula

- **Estado** (signal): o que não pode se perder entre ciclos
- **Finding** (insight): achado classificado, não novelinha
- **Delta** (bench): mudança desde o último FAIL
- **Re-gate** (action): prova de novo com evidência
- **Zumbi** (pain): trabalho expulso da story atual

**Como ler esta aula**

1. **Estado**: O que preservar a cada volta.
2. **Mecânica**: Coletar → priorizar → patch → re-gate.
3. **Breaker**: Quando parar com dignidade.
4. **Prática**: Simular um ciclo com classificação.

---

## Os quatro pedaços que não podem morrer

Preservar estado não é slogan — é checklist.

Estado a preservar a cada volta do loop:

1. **Story id + aceite** — o contrato não muda no meio sem cerimônia.
2. **Branch / PR** — correção no mesmo trilho, não fork sentimental.
3. **Findings** — lista priorizada, versionada, não novelinha no Slack.
4. **Evidência** — o que passou / o que ainda falha (log, screenshot, check).

Então o que acontece se você perde um pedaço? Perde o **porquê** do patch.
Dev corrige o sintoma que lembra. QA redescobre o mesmo buraco. O modelo
alucina contexto que existia no thread morto.

Olha só: "preservar estado" é o oposto de "abrir ticket e rezar". Ticket novo
só quando o finding é **outra story** de verdade — e aí você nomeia isso.

- **1. Contrato**: Story + aceite intactos (ou reabertura formal). [aceite]
- **2. Trilho**: Mesma branch/PR e lista de findings. [pr]
- **3. Prova**: Evidência do que ainda falha e o que já passou. [qg]

> **Issue zumbi é falha de processo**: Se o achado não cabe na story atual, ou a story está mal cortada, ou o achado é outro trabalho — nomeie. Não empurre pra limbo.

---

## Como o loop roda na prática

Classificar é metade do trabalho. Patch sem prioridade é teatro.

Loop canônico:

1. **Coletar** — QG, CodeRabbit, QA humano: lista única.
2. **Priorizar** — block → major → nit. Outra-story sai do loop atual.
3. **Patch** — Dev (ou agente Dev) corrige na mesma branch, blockers primeiro.
4. **Re-gate** — roda de novo; anota **delta** (o que mudou desde o FAIL).
5. **PASS** ou volta ao 2. **Breaker** se o mesmo finding volta 3x sem aprendizado.

Classificação que salva o time:

- **Block** — sem isso, done é mentira (aceite, segurança, teste do caminho).
- **Major** — qualidade séria, ainda na story, mas depois dos blocks.
- **Nit** — cosmético; batch no fim ou ignore documentado.
- **Outra story** — escopo novo disfarçado; não infle a atual.

Sem delta entre ciclos, não é loop — é **teimosia com git**.

**Loop canônico**

1. **Coletar**: QG/CR/QA listam findings numa lista só.
2. **Priorizar**: Blockers primeiro; nits no fim ou ignore com dono.
3. **Patch**: Dev corrige na mesma branch/PR.
4. **Re-gate**: Roda de novo com delta explícito.

- **Block**: Impede done honesto: aceite, segurança, caminho crítico.
- **Major**: Defeito sério ainda no escopo da story, não cosmético.
- **Nit**: Ajuste de qualidade menor; batch ou ignore com dono.
- **Delta**: O que mudou desde o último FAIL — prova de que o ciclo aprendeu.

> **Prior-art**: Aula 48 monta a coleira (QG). Aula 06 joga findings do CodeRabbit. Aula 47/10 guardam o estado da story. Este loop é a costura operacional entre FAIL e PASS.

---

## Caso: o finding que voltou três vezes

Quando patch cosmético mascara design errado.

Story: "fallback se API de dica cair no passo 2". FAIL 1: tela branca. Patch:
try/catch que engole o erro. FAIL 2: usuário fica preso sem UI. Patch: toast
genérico. FAIL 3: toast existe, mas o fluxo não deixa seguir o onboarding.

Três ciclos, zero reler de aceite. O aceite pedia **continuar o fluxo** com
fallback — não "não crashar". O loop saudável no ciclo 2 já teria:

- classificado como **block de aceite** (não nit de UX);
- forçado reabrir a implementação do caminho alternativo;
- ou **breaker**: se o design da story está torto, split/redesign, não maquiagem.

Então o que acontece sem breaker? Você industrializa o puxadinho **dentro** do
QG — a coleira vira coleira de enfeite com mais commits.

**Loop com breaker**

1. **FAIL**: Findings + evidência
2. **Classificar**: Block/major/nit/outra
3. **Patch**: Mesma PR
4. **Re-gate**: Delta explícito
5. **PASS|Break**: Fechar ou redesenhar

- **Loop curto** != **Teimosia**: Loop tem delta e classificação; teimosia repete o mesmo patch.
- **Outra story** != **Debt escondida**: Se saiu do aceite, nomeie story nova — não 'depois'.

---

## Continuar o loop ou parar?

Escopo do aceite é a cerca.

**Árvore de decisão**
_Escopo do aceite é a cerca — não a urgência do comment._

```mermaid
%%{init: {"theme": "dark", "flowchart": {"useMaxWidth": true, "htmlLabels": true, "nodeSpacing": 22, "rankSpacing": 36, "padding": 8}}}%%
flowchart TB
  Q["O finding ainda cabe nesta Story?"]
  B0["Sim, é blocker do aceite<br/>Apply fix + re-gate na mesma PR."]
  B1["Sim, mas é nit<br/>Batch de nits no fim ou ignore documentado."]
  B2["Não, é outra story<br/>Nova story; não infle a atual."]
  B3["Loop infinito<br/>Breaker: reabrir aceite, split ou redesign."]
  B4["Risco / waiver<br/>WAIVED com dono e data — nunca silêncio."]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
```

- **Sim, é blocker do aceite** — Sem isso, done é mentira.
  → _Apply fix + re-gate na mesma PR._
  Ex.: Teste do caminho feliz falha.
- **Sim, mas é nit** — Qualidade, não correção de contrato.
  → _Batch de nits no fim ou ignore documentado._
  Ex.: Nome de variável feio.
- **Não, é outra story** — Escopo novo disfarçado de finding.
  → _Nova story; não infle a atual._
  Ex.: Refator de módulo inteiro no meio do botão.
- **Loop infinito** — Mesmo erro 3x sem delta real.
  → _Breaker: reabrir aceite, split ou redesign._
  Ex.: Flaky + patch cosmético eterno.
- **Risco / waiver** — Não dá pra fixar agora, mas o risco é conhecido.
  → _WAIVED com dono e data — nunca silêncio._
  Ex.: Check flaky catalogado; merge com flag.

**Gate:** Você sabe o número do ciclo e o que mudou desde o último FAIL? — _Sem delta, não é loop — é teimosia._

#### Loop saudável
Curto e com delta.
1. **Findings: Lista única classificada.
2. **Patch: Blockers na mesma PR.
3. **Re-gate: Evidência do delta.
4. **PASS: Fecha a borda da story.

#### Breaker
Parar com dignidade.
1. **3x mesmo fail: Sem aprendizado.
2. **Reler aceite: Contrato ainda faz sentido?
3. **Split ou redesign: Não maquiar.
4. **Nova rota: Story nova ou arquitetura.

#### Exportar trabalho
Quando não é desta story.
1. **Nomear: Finding = outra unidade.
2. **Criar story: Com aceite próprio.
3. **Não bloquear: Só se for risco real.
4. **Seguir QG: Story atual fecha o que é dela.

---

## Simule um ciclo (15 min)

Findings reais ou inventados com honestidade.

Vamos lá. Sem isso a aula vira podcast. Usa findings reais de uma PR ou inventa
cinco achados críveis de uma feature que você conhece.

- 1. **Findings**: Liste 5 achados (reais ou simulados) de uma PR.
- 2. **Classifique**: block / major / nit / outra-story para cada um.
- 3. **Ordem**: Escreva a ordem de patch e o que fica de fora desta story.
- 4. **Re-gate**: Defina o critério de PASS do próximo ciclo (uma frase).
- 5. **Breaker**: Escreva a condição de parada (ex.: 3x mesmo block).

**Funcionou se:**

- Nenhum blocker virou 'depois' sem justificativa.
- Pelo menos um item foi marcado como outra story ou nit com dono.
- Há critério explícito de re-gate e de parada do loop.
- Você sabe quais 4 pedaços de estado preservaria nesse ciclo.

---

## Glossário sem jargão de vaidade

- **Apply QA Fixes**: Subprocesso que devolve findings ao Dev na mesma story/PR até re-gate.
- **Estado preservado**: Story, aceite, PR, findings e evidência intactos entre ciclos.
- **Issue zumbi**: Trabalho expulso da story atual para limbo de tickets sem contexto.
- **Circuit breaker**: Parada deliberada do loop após repetição sem aprendizado.
- **Delta**: Mudança observável desde o último FAIL — prova de progresso do ciclo.
- **Feedback loop curto**: Tempo mínimo entre achado e correção com contexto ainda quente.

---

## Portão da aula

Você passou quando opera QA→Dev sem perder story, PR e evidência — e sabe quando
o loop deve virar breaker. Feedback curto é o oxigênio da autonomia.

A IA é a seta. O X é seu — inclusive **não abrir limbo** só pra board ficar limpo.

> **Trilha M3 neste bloco**: Órbitas (45) → etapas (46) → ciclo story (47) → QG (48) → este loop (49). Daqui o trilho de repo/CI continua a amarrar a infraestrutura.

> **GATE-MODULE (auto)**: GPS Goal/Position/Steps presentes · caso + do/dont · decisão · prática com evidência · glossário. Alvo DL ≥70 atingido na construção enrich-W1.

***


---

## Navegação

← [[48-quality-gate-completo|Quality Gate: QA + Apply QA Fixes + CodeRabbit]] · ↑ [[modulos/Módulo 3 - Ciclo SDC|M3]] · ⌂ [[Cursos/AIOX Advanced/README|Curso]] · → [[06-code-rabbit-boost|Code Rabbit Boost]]
