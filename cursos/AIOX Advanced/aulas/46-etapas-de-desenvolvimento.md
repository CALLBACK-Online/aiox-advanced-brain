---
type: lesson
course: aiox-advanced
course_title: AIOX Advanced
lesson_id: etapas-de-desenvolvimento
lesson_position: 46
title: 'Briefing, PRD, Stories: as 3 etapas antes do código'
source: upstream monorepo/apps/aiox-courses
source_path: content/courses/aiox-advanced/aulas/46-etapas-de-desenvolvimento/lesson.md
source_format: lesson.md
synced_at: '2026-08-09'
manual: true
concepts: []
tags:
- curso/aiox-advanced
- lesson
- course-brain
bloom: apply
reading_minutes: 14
has_mermaid_map: true
map_source: auto-decision_graph
module: M2
sequence: 17
track: core
status: canonical
canonical_scope: cursos/AIOX Advanced
curated_at: '2026-08-09'
---

# Briefing, [[PRD]], Stories: as 3 etapas antes do código

Priorização no PRD: use [[MoSCoW]] (Must/Should/Could/Won't) e, quando precisar de score comparável, [[RICE]] (Reach, Impact, Confidence, Effort).

## Mapa desta aula

Decisão-chave da aula — O que ainda está confuso?

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
  Q["O que ainda está confuso?"]
  B0["Não sei o porquê / pra quem<br/>Volta pro Briefing. Proibido PRD e códi…"]
  B1["Sei o porquê, não o como<br/>PRD — stack, limites, trade-offs, fora."]
  B2["Planta ok, execução vaga<br/>Quebrar em Stories com aceite testável."]
  B3["Já estou codando<br/>Pare. Reconstrua o mínimo viável de pla…"]
  B4["Story pronta e validada<br/>Dev — só agora. Não reabra PRD no meio …"]
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

> Por que pular essas etapas vira puxadinho atrás de puxadinho — e como nunca mais confundir PRD com [[Story]].

**Objetivos de aprendizagem:**
- Listar o que cada etapa (Briefing, PRD, Story) trava e o que proíbe pular. _(remember)_
- Diferenciar Briefing, PRD e Story em uma feature real sem misturar os artefatos. _(understand)_
- Aplicar as três etapas em ordem em um pedido de feature do próprio projeto. _(apply)_
- Detectar quando o time pulou etapa e o sintoma vira puxadinho industrializado. _(analyze)_

---

## O que você consegue no fim desta aula

*G · Destino*

Destino claro antes de qualquer template de PRD.

Ao final desta aula você vai conseguir três coisas concretas:

1. Olhar um pedido de feature e **nomear em qual etapa ele está** (ou se ainda não está em nenhuma).
2. Separar em arquivo (mesmo rascunho curto) **Briefing ≠ PRD ≠ Story** sem reaproveitar o mesmo parágrafo.
3. Recusar com critério o "só manda pro Claude" quando a planta não existe.

Se você sair daqui ainda chamando de "PRD" um post-it de duas linhas, a aula falhou.
Velocidade sem as três etapas não é produtividade — é **puxadinho com CI verde**.

- **Objetivos da aula** (Listar o que cada etapa trava; Diferenciar os três artefatos num pedido real; Aplicar a ordem brief → prd → stories)
- **Resultado tangível**: Uma feature sua com 3 caixas preenchidas e a próxima ação nomeada.
- **Não é o destino**: Escrever PRD de 40 páginas. É fechar a planta mínima que um sênior construiria igual.

---

## A mansão com sete puxadinhos

*P · Onde você está*

Empatia com o ponto de partida real do operador.

Cara, eu mesmo já errei feio nisso. Fazia "PRD" que era story disfarçada. Ou pior:
abria o Claude e mandava construir com uma frase solta. O modelo é rápido. Então
você não ganha um puxadinho — ganha uma **favela em velocidade de startup**.

A maioria começa a comandar IA sem especificação. Sem briefing, sem detalhamento,
sem quebra em tarefas. Aí vira o quê? Mansãozinha bonita no pitch e, na prática,
varanda enferrujada do lado, garagem improvisada, banheiro no quintal. O pior:
**continua funcionando** — e você se acostuma com a porcaria.

Se você está aqui, provavelmente já sentiu um destes sintomas:

- Cliente pediu "coloca IA aí" e o diff já saiu genial e inútil.
- "PRD" de três linhas e story de romance (ou o inverso).
- Aceite inventado no meio do PR porque ninguém escreveu o contrato.

Beleza. A partir daqui a gente troca vibe de execução por **ordem de especificação**.

**Onde a maioria trava**
- Uma frase vira implementação
- PRD e Story no mesmo arquivo sem fronteira
- Aceite mental ('você vai entender')

**Onde o operador vai**
- Briefing fecha o porquê antes da planta
- PRD fecha a planta antes da ordem de serviço
- Story fecha o pedaço executável com aceite testável

---

## As três etapas que separam operador de torcedor

*S · Rota*

Não é burocracia — é barreira barata antes do custo caro.

Decora a trinca:

1. **Briefing** — o que e por quê (dor, ICP, não-negociáveis).
2. **PRD** — planta operacional (escopo, stack, trade-offs, fora de escopo).
3. **Stories** — unidades mastigáveis com aceite e dono.

PRD não é Story. Story não é briefing. Misturar os três é industrializar gambiarra.

Essa trinca não nasceu em slide. Ela nasceu ao vivo, na abertura do cohort, quando o Alan abriu o capô do próprio fluxo:

> **Alan Nicolas (aula-01 L453-457)**: "Eu separei aqui como três etapas principais: ter o briefing ali, onde você vai entender o que você quer fazer; fazer o detalhamento profundo, que seria aquele PRD, separar isso por etapas; e depois quebrar aqui em tarefas. Isso já é uma coisa que pouca gente faz. Só que daí existem muitas sub-etapas nesse processo aqui, que são essenciais."

Guarda a última frase. Ter as três etapas já te coloca à frente da maioria; as **sub-etapas** (validar o draft, quebrar o épico na hora certa) são onde o jogo vira — e é exatamente isso que o resto desta aula opera.

Prior-art: a aula 07 (etapas de desenvolvimento AIOX) plantou o sintoma do puxadinho
e a trinca canônica. Aqui a gente **instancia o roteamento operacional** — em qual
etapa você está de verdade, e o que falta pra avançar sem pular.

- **3**: etapas canônicas
- **1**: ordem obrigatória
- **0**: espaço pra frase-solta-no-chat

- **status**: brief → prd → stories
- **meta**: anti=frase-solta-no-chat
- **meta**: regra=artefato em arquivo
- **meta**: fonte=aula-01 + t2-aula-2
- **ready**: ready to stage

**Legenda de cores**

O que cada cor sinaliza nesta aula

- **Briefing** (signal): intenção: dor, ICP, outcome
- **PRD** (insight): planta: escopo, stack, fora
- **Story** (bench): unidade com aceite verificável
- **Ordem** (action): só avança com artefato da etapa
- **Puxadinho** (pain): código sem planta ou aceite

**Como ler esta aula**

1. **Sintoma**: Reconhecer o puxadinho industrializado.
2. **As 3**: O que cada etapa trava (e o anti-papel).
3. **Ordem**: Por que a sequência é barata e o pulo é caro.
4. **Prática**: Passar uma feature real pelas três caixas.

---

## Briefing, PRD, Stories — o que cada um trava

Memoriza a trava, não o template.

**Briefing** trava ambiguidade de **intenção**. Se você não sabe a dor, não tem o que
detalhar. Pergunta-mãe: "pra quem e que mudança de vida isso gera?"

**PRD** trava ambiguidade de **construção**. Stack, limites, integrações, o que NÃO
entra. Pergunta-mãe: "se um sênior lesse isso, construiria a mesma coisa que eu?"

> **Pedro Valerio Lopez (aula-01 L659)**: "E o PRD vai ditar quais são os objetivos, o que vai ser desenvolvido, até qual stack. Tudo isso é definido no PRD."

**Story** trava ambiguidade de **execução**. Aceite testável, paths, fora. Pergunta-mãe:
"dá pra marcar done sem opinião?"

> **Adriano De Marqui (t2-aula-2 L977)**: "Story é a unidade menor de entrega que eu posso medir: se foi feito, se foi bem feito, se foi validado."

E quando a IA "não corrige" o que você pediu? Quase nunca é o modelo:

> **Adriano De Marqui (t2-aula-2 L981)**: "'Adriano, eu estou pedindo para me corrigir, mas não corrige.' Por que está quebrando? Porque a Story tem ambiguidades."

Então o que acontece se o PRD nasce torto? A story nasce torta. Se a story nasce torta,
o Claude Code constrói torto — e constrói **rápido**. Velocidade multiplica erro de planta.

Olha só: se o teu "PRD" é um parágrafo e a "story" é um romance de escopo, você não tem
etapas — tem confusão com nome de cargo.

> **PRD não é Story**: PRD é a planta do prédio. Story é a ordem de serviço do andar. Usar um no lugar do outro é pedir pro pedreiro improvisar a arquitetura.

Uma pegadinha de granularidade que o campo revelou: PRD é do **produto**, não da feature. O Alan confessou ao vivo que fazia errado — "eu, erroneamente, até hoje fazia muitos PRDs para features" [SOURCE: aula-01 L1749] — e o Pedro fechou a regra:

> **Pedro Valerio Lopez (aula-01 L3407)**: "Você não fica criando PRD toda hora. Você cria um grande PRD de início, e depois você vai fazendo enhancement naquilo."

Enhancement pode ser new feature, melhoria de algo que já existe ou bug fix [SOURCE: aula-01 L3407-3413] — mas todos entram como épico e stories pendurados no PRD que já existe, não como um PRD novo por capricho.

- **1. Briefing**: Dor, ICP, outcome, não-negociáveis. Fecha o porquê. [intenção]
- **2. PRD**: Escopo, stack, trade-offs, fora de escopo. Fecha a planta. [planta]
- **3. Stories**: Unidades com aceite, paths, dono de ciclo. Fecha a execução. [unidade]

- **Briefing**: Clareza de intenção: dor, ICP, outcome, restrições — sem stack ainda.
- **PRD**: Planta operacional: escopo, decisões, trade-offs, fora de escopo.
- **Story**: Unidade executável com aceite verificável e dono de ciclo.
- **Puxadinho**: Correção em cima de correção sem planta — velocidade sem fundação.

- **PRD curto e claro** != **Story incompleta**: Planta boa não desculpa unidade sem aceite.
- **Story detalhada** != **PRD disfarçado**: Se a story redefine stack e escopo do produto, sobrou PRD.

---

## Por que a sequência é barata e o pulo é caro

Custo de especificar vs custo de desfazer.

Beleza. Então o que acontece quando você pula?

- Pula **briefing** → otimiza a feature errada com elegância.
- Pula **PRD** → cada story inventa uma arquitetura diferente.
- Pula **story** → o Dev (humano ou IA) decide o aceite no diff.

E o pior anti-pattern moderno: **pular as três** e mandar uma frase no chat.
O modelo entrega. Você sente progresso. Duas sprints depois você está pagando
a dívida com juros de contexto perdido.

A ordem brief → prd → stories não é ritual de consultoria. É o caminho em que
o erro barato (texto) vem **antes** do erro caro (código + merge + hábito).

Prior-art reforça: [[Determinismo Progressivo|determinismo progressivo]] (aula 09) diz a mesma coisa em outra
linguagem — trave o caminho antes de soltar a IA solta. Aqui a trava é a etapa.

O Pedro amarra a cadeia inteira num fôlego só, com as palavras dele:

> **Pedro Valerio Lopez (aula-01 L2911-2913)**: "Você vai para o desenvolvimento, cria um bom PRD. Do bom PRD você quebra em etapas executáveis, em épicos, e os épicos em Stories. Mas você não deixa ele executar o draft do Story: você faz um Validate Story Draft, que vai mais uma vez comparar aquilo com o template, comparar com os documentos, com o core-config, e vai validar aquele Story."

### Caso de campo: a etapa que o Alan pulava fazia seis meses

No dia 1 do cohort, o Alan mostrou o fluxo antigo dele: pegava o PRD, quebrava em épicos, gerava de uma vez a sequência inteira de stories do épico e "botava os bichos pra trabalhar". Revisava o épico inteiro no final e dava um push de tudo pro GitHub. Funcionava — esse é o perigo. O Pedro cortou: não, é um por um. O Alan reclamou ("é muito maçante"), mas aceitou fazer story por story, "até para poder mapear, porque eu vou deixar isso tudo automatizado". [SOURCE: aula-01 L1867-1871]

Horas depois, na demonstração do ciclo, caiu a ficha de qual sub-etapa ele vinha pulando. O Pedro anunciou: "O importante é validar Story. Hoje o Alan entendeu muito por que validar Story." [SOURCE: aula-01 L2075] E o Alan assumiu na frente da turma:

> **Alan Nicolas (aula-01 L2077-2081)**: "Essa era uma etapa que eu não fazia, pessoal. Eu fazia um Quality Gate com o QA, fazia outras coisas, mas eu não fazia o validar da história. Quando eu entendi o valor disso aqui, eu revi minha vida. Pensei: é por isso que quando eu fiz tal e tal coisa, lá quebrou. É por isso que eu tive que ficar com dor de cabeça. Então tudo aqui tem um motivo para existir."

Seis meses de uso diário e o puxadinho ainda crescia em silêncio — porque a sequência estava quase certa. Quase. O pulo era numa sub-etapa barata (validar o draft antes do Dev), e a conta chegava sempre cara: código quebrado depois do merge, dor de cabeça sem causa aparente.

> **Regra do arquivo**: Se o artefato da etapa não existe em arquivo (mesmo rascunho de 8 linhas), a etapa não aconteceu. Memória de reunião não conta.

**Fluxo canônico pré-código**

1. **Briefing**: Fecha intenção
2. **PRD**: Fecha planta
3. **Stories**: Quebra + aceite
4. **Validate**: draft → ready
5. **Dev**: Só na unidade ready

---

## Caso: 'coloca IA no onboarding'

O mesmo pedido em três etapas — e o desastre de pular.

Pedido do cliente: "coloca IA no onboarding pra engajar mais."

**Sem etapas:** Claude gera wizard com chat, embeddings, três providers e um
dashboard. Bonito. Ninguém sabe o outcome. Em duas semanas o time discute
"qual modelo" em vez de "qual dor".

**Com etapas:**

- **Briefing:** ICP = trial de 14 dias; dor = abandono no passo 2; outcome =
  +X% completar onboarding; não-negociável = sem treinar modelo próprio.
- **PRD:** escopo = checklist + dica contextual no passo 2; stack = LLM via
  API já usada; fora = chat livre, analytics novo, fine-tune.
- **Story 1:** "Dado trial no passo 2, quando usuário hesita 30s, então mostra
  dica com base no perfil — aceite: teste e2e + fallback se API cair."

Então o que acontece? O Dev (ou o agente) recebe **ordem de serviço**, não
romance de produto. O QG depois consegue provar o aceite — porque o aceite existe.

> **Prior-art**: Aula 07 mostra o puxadinho como cultura. Esta aula opera o antídoto: três caixas, ordem, e recusa de Dev sem artefato. As duas se complementam.

### E como é um Story bom de verdade, em produção?

Na abertura do cohort, o Pedro abriu um Story real do sistema da Offluence — não exemplo de slide, código rodando: "Olha, isso aqui é um Story. Como gerente de produção de operações da Offluence, eu quero que briefings de clientes sejam automaticamente tokenizados em JSON estruturado e vídeos validados por IA, para que a equipe de produção tenha checklists claros e feedback automático de conformidade, reduzindo o trabalho em sessenta por cento. Isso aqui é um bom Story." [SOURCE: aula-01 L1939-1945]

Repara a anatomia. O Story tem overview, contexto de negócio ("briefings textuais são ambíguos e difíceis de processar automaticamente"), contexto técnico, trigger explícito (webhook do ClickUp quando o status muda de "briefing" para "analisar briefing"), integrações nomeadas (ClickUp API, Gemini para análise de vídeo, Supabase) e um task breakdown em fases — task 1.1, 1.2, 1.3 — que o Dev segue passo a passo sem inventar moda. [SOURCE: aula-01 L1947-1971]

É o mesmo formato "como papel, eu quero capacidade, para que outcome mensurável" da Story 1 do onboarding acima. A distância entre o exemplo didático e o de produção é zero — e é exatamente esse o ponto.

**Mesmo pedido, três densidades**

- **Briefing (5–10 linhas)**: Pra quem, dor, outcome, não-negociáveis
- **PRD (1–3 páginas úteis)**: Escopo, stack, trade-offs, fora
- **Story (1 unidade)**: Aceite testável + paths + dono
- **Anti-padrão**: Um único blob chamado 'spec' com tudo misturado

---

## Em qual etapa você está de verdade?

A confusão aponta a etapa — não o desejo de codar.

**Árvore de decisão**
_A confusão aponta a etapa — não a urgência emocional de abrir o editor._

```mermaid
%%{init: {"theme": "dark", "flowchart": {"useMaxWidth": true, "htmlLabels": true, "nodeSpacing": 22, "rankSpacing": 36, "padding": 8}}}%%
flowchart TB
  Q["O que ainda está confuso?"]
  B0["Não sei o porquê / pra quem<br/>Volta pro Briefing. Proibido PRD e código."]
  B1["Sei o porquê, não o como<br/>PRD — stack, limites, trade-offs, fora."]
  B2["Planta ok, execução vaga<br/>Quebrar em Stories com aceite testável."]
  B3["Já estou codando<br/>Pare. Reconstrua o mínimo viável de planta (mesmo retr…"]
  B4["Story pronta e validada<br/>Dev — só agora. Não reabra PRD no meio do diff sem cer…"]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
```

- **Não sei o porquê / pra quem** — Dor e outcome nebulosos.
  → _Volta pro Briefing. Proibido PRD e código._
  Ex.: Cliente: 'coloca IA aí'.
- **Sei o porquê, não o como** — Outcome ok, planta fraca.
  → _PRD — stack, limites, trade-offs, fora._
  Ex.: Quer onboarding, sem decidir auth.
- **Planta ok, execução vaga** — PRD existe, ninguém sabe o próximo diff.
  → _Quebrar em Stories com aceite testável._
  Ex.: PRD de 8 páginas, zero story ready.
- **Já estou codando** — Diff rolando sem artefato.
  → _Pare. Reconstrua o mínimo viável de planta (mesmo retroativo)._
  Ex.: Branch com 40 arquivos e aceite mental.
- **Story pronta e validada** — Aceite claro, ready.
  → _Dev — só agora. Não reabra PRD no meio do diff sem cerimônia._
  Ex.: Story com DoD e paths definidos.

**Gate:** Você consegue apontar o artefato atual (brief / PRD / story) e o que falta pra avançar? — _Se o artefato não existe em arquivo, a etapa não aconteceu._

#### Rota Briefing
Intenção antes de planta.
1. **Nomear dor: Uma frase mensurável.
2. **ICP: Pra quem isso muda a vida.
3. **Outcome: O que 'melhor' significa em número ou comportamento.
4. **Não-negociáveis: Restrições que matam o projeto se violadas.

#### Rota PRD
Planta antes de story.
1. **Escopo: O que entra nesta fatia.
2. **Stack / decisões: O sênior não deveria adivinhar.
3. **Trade-offs: O que você abriu mão e por quê.
4. **Fora: Lista explícita do que NÃO entra.

#### Rota Stories
Unidades com aceite.
1. **Quebrar: Fatias que cabem num ciclo.
2. **Aceite: Testável sem opinião.
3. **Validate: draft → ready (próxima aula aprofunda).
4. **Só então Dev: Implementação na unidade ready.

---

## Uma feature, três caixas (15 min)

Papel, vault ou board — mas escrito.

Vamos lá. Sem isso a aula vira podcast. Cronometra quinze minutos. Escolhe
algo real — até pedido que você "já quase codou" serve pra auditar o que faltou.

- 1. **Feature**: Escolha um pedido real do teu projeto (mesmo pequeno).
- 2. **Briefing**: 5–10 linhas: dor, ICP, outcome, não-negociáveis.
- 3. **PRD mínimo**: 10–20 linhas: escopo, stack/decisões, trade-offs, fora.
- 4. **Uma Story**: 1 unidade com aceite testável em uma frase + paths se souber.
- 5. **Auditoria**: Marque o que estava misturado antes (PRD dentro da story, etc.).

**Funcionou se:**

- Você separou os três artefatos sem reutilizar o mesmo bloco de texto.
- A story tem aceite testável em uma frase.
- Você sabe qual etapa estava pulando no fluxo antigo.
- Consegue nomear a próxima ação (voltar etapa / validar / dev) sem 'vamos vendo'.

---

## Da cohort: as dúvidas que todo mundo tem na primeira semana

Três cenas reais da segunda turma, porque a tua dúvida provavelmente é uma delas.

**"Um bug simples pode ir direto pro Dev, né?"** Não. Quando o Thiago levantou a sequência no chat, o Adriano fechou a porta:

> **Adriano De Marqui (t2-aula-2 L2097-2101)**: "Tem que ter um ciclo de story, mesmo que seja uma correção de um bug muito fácil. Porque aquilo que não foi feito dentro de uma Story, o sistema já não conhece mais. Não sabe quem fez, não sabe como surgiu, não sabe em que momento foi pedido, por quem foi pedido — não sabe da existência daquilo. Ele não vai conseguir mapear aquilo."

E emendou a sequência canônica: "Você tem que criar com o SM o Story, o PO tem que validar o Story, daí o Dev vai implementar. Tem que passar pelo Quality Assurance e tem que passar pelo DevOps" — com commits pontuais o tempo todo, documentando o que foi feito para aquela Story específica. "Não vai juntar aquele monte de Stories para depois fazer commit, para depois fazer push." [SOURCE: t2-aula-2 L2109-2129]

**"Já fiz o PRD, os Stories, a documentação... montei até um portal."** A Cris França contou que criou um portal com toda a documentação do que construiu [SOURCE: t2-aula-2 L6009]. O Adriano devolveu a hierarquia real dos artefatos:

> **Adriano De Marqui (t2-aula-2 L6013-6029)**: "A maior documentação para o AIOX são as Stories. Porque nas Stories ele tem documentado tudo que foi feito, e ele está amarrado com o PRD. O épico é só a coleção. Se perder a documentação que você criou e precisar de uma nova, ele consegue reconstruir muito facilmente."

Ou seja: o portal é vitrine; a fonte de verdade são as Stories penduradas no PRD.

**"Por que tanta gente quebra?"** O diagnóstico do Adriano para quem chega no avançado atropelando etapa: "Tem um monte de gente quebrando [...] que está fazendo as coisas direto com o Dev. Sem Story. Não sabe para que serve o Story, qual é a estrutura do Story, a importância de validar um Story, quais são as etapas do Story, os Gates do Story — não está olhando para nada disso. E aí está olhando que a solução está quebrando, que a solução não funciona." [SOURCE: t2-aula-2 L965-969]

Se você se reconheceu em alguma das três cenas, a resposta é a mesma: volta pra caixa que ficou vazia — briefing, PRD ou Story — antes de tocar em código.

---

## Glossário sem jargão de vaidade

- **Briefing**: Artefato de intenção: dor, ICP, outcome e restrições antes de qualquer planta técnica.
- **PRD**: Product Requirements / planta operacional: escopo, decisões, trade-offs e fora de escopo.
- **Story**: Unidade de trabalho com aceite verificável; ordem de serviço, não romance de produto.
- **Puxadinho**: Camada de gambiarra em cima de base fraca — velocidade aparente, dívida real.
- **Aceite testável**: Critério de done que dá pra provar sem 'acho que tá bom'.
- **Regra do arquivo**: Etapa só conta se o artefato existe fora da memória da conversa.

---

## Portão da aula

Você passou quando, sem cheatsheet, diferencia Briefing, PRD e Story num pedido
real e recusa começar Dev sem a etapa certa existir em arquivo.

A IA é a seta. O X é seu — inclusive **não soltar a seta** antes da planta.

> **Próximo na trilha**: Com as etapas claras, o ciclo de vida da Story (draft→done) vira o trilho onde o bastão passa de agente pra agente (posição 47).

> **GATE-MODULE (auto)**: GPS Goal/Position/Steps presentes · caso + do/dont · decisão · prática com evidência · glossário. Alvo DL ≥70 atingido na construção enrich-W1.

***

---

## Operar isto na prática

Esta aula é pré-requisito no curso de squads — quando a missão for real, siga para: Data: `cursos/AIOX-Advanced-Squads/aulas/10-data.md`

## Navegação

← [[aulas/19-ciclo-do-repositorio|Ciclo do repositório: Detect Repo, GitHub, CodeRabbit, CI/CD]] · ↑ [[modulos/Módulo 2 - SDC e Qualidade|M2 — SDC e qualidade]] · ⌂ [[cursos/AIOX Advanced/README|Curso]] · → [[aulas/48-quality-gate-completo|Quality Gate: QA + Apply QA Fixes + CodeRabbit]]
