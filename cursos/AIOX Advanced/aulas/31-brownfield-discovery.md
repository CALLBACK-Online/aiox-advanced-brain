---
type: lesson
course: aiox-advanced
course_title: AIOX Advanced
lesson_id: brownfield-discovery
lesson_position: 31
title: 'Brownfield Discovery: entrar num projeto que já existe'
source: upstream monorepo/apps/aiox-courses
source_path: content/courses/aiox-advanced/aulas/31-brownfield-discovery/lesson.md
source_format: lesson.md
synced_at: '2026-08-09'
manual: true
concepts:
- Brownfield Discovery
tags:
- curso/aiox-advanced
- lesson
- course-brain
bloom: apply
reading_minutes: 23
has_mermaid_map: true
map_source: auto-decision_graph
module: M4
sequence: 25
track: core
status: canonical
canonical_scope: cursos/AIOX Advanced
curated_at: '2026-08-09'
---

# [[Brownfield Discovery]]: entrar num projeto que já existe

## Conceitos

- [[Brownfield Discovery]]

## Mapa desta aula

Decisão-chave da aula — O código já existe e você não o escreveu?

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
  Q["O código já existe e você não o escreveu?"]
  B0["Brownfield vivo<br/>Discovery completo"]
  B1["Greenfield<br/>Desenho direto"]
  B2["Legado abandonado<br/>Descarte / isolamento"]
  B3["Patch pontual<br/>Discovery focado"]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
classDef core fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#e2e8f0
  classDef step fill:#0f172a,stroke:#6366f1,stroke-width:1.5px,color:#f1f5f9
  classDef gate fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#e2e8f0
  classDef good fill:#14532d,stroke:#4ade80,stroke-width:1.5px,color:#ecfdf5
  classDef bad fill:#450a0a,stroke:#f87171,stroke-width:1.5px,color:#fef2f2
  classDef warn fill:#422006,stroke:#fbbf24,stroke-width:1.5px,color:#fffbeb
```

> Leia o diagrama antes do texto longo. Depois volte e confira.

> [[Greenfield]] começa do zero. Brownfield começa de um código que já roda e que você não escreveu. A regra muda: antes de propor, você decifra. Discovery é o ritual que evita refatorar no escuro.

**Objetivos de aprendizagem:**
- Nomear o que distingue um projeto brownfield de um greenfield no AIOX. _(remember)_
- Distinguir discovery (decifrar) de intervenção (propor mudança) num código legado. _(understand)_
- Escolher quando rodar discovery completo antes de tocar em qualquer linha. _(apply)_
- Explicar por que mapear a estrutura real evita refatorar no escuro. _(understand)_

---

## Brownfield: o código já roda e você não escreveu

*Discovery AIOX · entrar num projeto que já existe*

Greenfield é uma folha em branco. Brownfield é uma casa habitada: tem paredes, tem encanamento, tem decisões antigas que você precisa respeitar. Antes de propor mudança, você decifra. Quem pula o discovery refatora no escuro.

- **10**: fases de discovery brownfield
- **1**: regra: decifrar antes de propor
- **0**: refatoração no escuro

- **status**: [[Brownfield Discovery|brownfield discovery]]
- **meta**: greenfield=comeca do zero
- **meta**: brownfield=codigo que ja roda
- **meta**: regra=decifra antes de propor
- **ready**: ready to map

**Legenda de cores**

Mapa semantico do Brownfield Discovery

- **Brownfield** (signal): projeto que ja existe e voce nao escreveu
- **Discovery** (insight): o ritual de decifrar antes de propor
- **Mapa** (bench): a estrutura real do codigo, nao a suposta
- **Intervencao** (action): a mudanca proposta depois de entender
- **Erro comum** (pain): refatorar no escuro, sem discovery

---

## Comece pela pergunta certa

Antes de listar as fases do discovery, fixe a pergunta única: o código já existe e você não o escreveu? Se sim, é território brownfield, e a primeira ação é decifrar, não propor. Todo o resto deriva daí.

**Como ler esta aula**

1. **A pergunta aparece**: Uma frase separa começar do zero de entrar num código que já roda.
2. **Cada peça mostra a cara**: Discovery decifra a estrutura real. Intervenção só vem depois de entender.
3. **Vê o caso real**: /processo de mapeamento AIOX e code-anatomist são primitivos reais do AIOX, apontáveis no repo.
4. **Decide**: Dado um projeto, você aponta se merece discovery completo antes de tocar no código.

- **Objetivos da aula** (Nomear o que distingue brownfield de greenfield no AIOX.; Distinguir discovery (decifrar) de intervenção (propor mudança).; Escolher quando rodar discovery completo antes de tocar no código.; Explicar por que mapear a estrutura real evita refatorar no escuro.)
- **Onde você está?** (Começando: foque Mapa Simples e a analogia da casa habitada.; Já usa AIOX: foque Casos Reais e a Decisão.; Vai mapear: foque as 10 Fases e as Métricas.)
- **Leitura prática**: Em cada bloco, procure uma resposta: estou decifrando o que já existe ou propondo mudança? Quando cada um ajuda e quando atrapalha?

**Ritmo da aula**

A distinção fica clara quando cada peça tem definição curta, exemplo real do framework e o gosto de quando usar.

- G **Pergunta antes do detalhe**: Primeiro o critério que separa, depois cada fase por dentro.
- 1 **Analogia que ancora**: Greenfield é terreno baldio. Brownfield é casa habitada que pede planta antes da reforma.
- 2 **Caso real**: /processo de mapeamento AIOX e code-anatomist são apontáveis no AIOX, não teoria.
- 3 **Recap com decisão**: A aula fecha com o aluno decidindo se um projeto dele merece discovery completo.

---

## A diferença sem jargão

Antes dos termos técnicos, a diferença é só isto: greenfield você desenha do nada; brownfield você herda um código que já roda e precisa entender antes de mudar.

> **Em uma frase**: Greenfield começa do zero: nenhuma decisão antiga te limita. Brownfield começa de código que já roda e que você não escreveu. A regra muda: antes de propor mudança, você decifra a estrutura real. Discovery primeiro, intervenção depois.

- **Brownfield é código herdado** -> Um projeto que já existe, já roda em produção, e você não foi quem escreveu. Tem decisões antigas embutidas.
- **Discovery decifra** -> O ritual de mapear a estrutura real: arquitetura, domínio, dados, dependências. Entender antes de tocar.
- **O mapa é a marca** -> Você sai do discovery com a estrutura real desenhada, não com a suposta. Sem mapa, não houve discovery.
- **Intervenção vem depois** -> Só depois de entender você propõe mudança. A proposta nasce do mapa, não do palpite.
- **O erro caro** -> Refatorar no escuro: mexer antes de decifrar. Você quebra o que não entendeu e descobre tarde demais.

**Diagrama principal: do código herdado à intervenção**

1. **Brownfield**: O código já existe e roda. Você herdou, não escreveu.
2. **Discovery**: O ritual que decifra a estrutura real antes de qualquer mudança.
3. **Mapa**: A estrutura real desenhada: arquitetura, domínio, dados, dependências.
4. **Intervenção**: A mudança proposta a partir do mapa, não do palpite.

**O que o discovery evita**
- Refatorar antes de entender a estrutura real.
- Tratar brownfield como se fosse greenfield.
- Propor mudança a partir de palpite, não de mapa.
- Quebrar dependências que você não sabia que existiam.

**O que ele força**
- Decifrar arquitetura, domínio e dados antes de tocar.
- Respeitar as decisões antigas embutidas no código.
- Propor intervenção a partir do mapa desenhado.
- Rodar discovery completo antes da primeira linha.

---

## A analogia da casa habitada

A forma mais rápida de fixar a diferença: greenfield é terreno baldio onde você constrói livre; brownfield é casa habitada onde você reforma. Reformar sem a planta da fiação derruba a parede errada.

- **Greenfield = terreno baldio**: Você constrói do zero. Nenhuma parede te limita, nenhuma tubulação te surpreende. Liberdade total, mas também zero contexto herdado.
- **Brownfield = casa habitada**: Você herda paredes, encanamento e fiação que alguém instalou. Antes de reformar, precisa da planta: onde passa o cano, onde está a viga estrutural.
- **Discovery = levantar a planta**: O ritual de mapear a casa antes da obra. Onde está cada cano, cada viga, cada decisão antiga. A planta evita derrubar a parede que segura o teto.
- **Intervenção = a reforma certa**: Com a planta na mão, você reforma o que precisa sem quebrar o que sustenta. A mudança nasce do mapa, não do palpite.

> **E quando misturar?**: Um projeto pode ter alas greenfield (módulos novos do zero) e alas brownfield (código legado herdado). O erro é tratar a ala habitada como terreno baldio e reformar sem planta. Discovery na parte herdada, liberdade na parte nova.

---

## Greenfield versus Brownfield: o critério legado

Esta é a confusão mais cara do início de projeto. Os dois falam de construir software, então parecem o mesmo trabalho. O critério legado separa os dois de vez: existe código herdado ou não?

**Greenfield (terreno baldio)**
- Começa do zero, sem código herdado.
- Liberdade de arquitetura total.
- Nenhuma decisão antiga te limita.
- Discovery curto: você define tudo.

**Brownfield (casa habitada)**
- Começa de código que já roda.
- Arquitetura herdada que você respeita.
- Decisões antigas embutidas no código.
- Discovery completo: você decifra tudo antes.

> **A pergunta que separa**: Pergunte: existe código que já roda e que eu não escrevi? Se não, é greenfield: desenhe livre. Se sim, é brownfield: decifre antes de propor. Greenfield é a folha em branco; brownfield é o manuscrito alheio que você precisa ler antes de editar.

- **Brownfield com greenfield**: Os dois constroem software, então parecem o mesmo trabalho.
- **Discovery com refatoração**: Os dois tocam no código legado, então parecem a mesma etapa.
- **Brownfield com legado abandonado**: Os dois lidam com código antigo, então parecem o mesmo caso.

---

## O discovery existe de verdade no AIOX

A distinção não é teoria. O discovery brownfield é apontável no framework. Estes dois casos mostram os primitivos reais do AIOX que decifram um código que você não escreveu.

- **Onde o discovery vive no AIOX**: O AIOX tem dois primitivos de discovery: code-anatomist (9 fases de engenharia reversa de software) e /processo de mapeamento AIOX (7 fases de mapeamento de processo, iniciando em Discovery). O discovery não é abstração: tem skill, tem fases nomeadas e tem ordem de leitura. Players: code-anatomist, /processo de mapeamento AIOX, 9 fases reverse engineering, 7 fases process mapping, fase Discovery.
- **O que muda a decisão**: A pergunta não é se o projeto é importante. É se existe código ou processo herdado que você não escreveu. Brownfield com valor vivo pede discovery completo. Greenfield e legado abandonado, não.

**Cada conceito num eixo**

A distinção vira sistema quando cada conceito tem definição, lar no framework e o tipo de projeto que resolve.

- **Brownfield**: Código ou processo que já roda e você não escreveu. Tem decisões antigas embutidas.
- **Discovery**: O ritual de decifrar a estrutura real. code-anatomist e /processo de mapeamento AIOX são os primitivos.
- **Mapa**: A estrutura real desenhada: arquitetura, domínio, dados, dependências.
- **Intervenção**: A mudança proposta a partir do mapa, depois do discovery.

**Colunas:** Conceito | Decifra ou muda? | Sinal de uso certo | Sinal de erro

- Brownfield: Decifra ou muda? | Reconhecido como código herdado com decisões antigas. | Tratado como greenfield, reformado sem planta.
- Discovery: Decifra ou muda? | code-anatomist ou /processo de mapeamento AIOX rodando antes da mudança. | Pulado por pressa, intervenção no escuro.
- Mapa: Decifra ou muda? | Estrutura real desenhada fase a fase. | Estrutura suposta, baseada em palpite.
- Intervenção: Decifra ou muda? | Mudança nascida do mapa, depois do discovery. | Mudança proposta antes de entender a estrutura.

### Caso: O code-anatomist faz a engenharia reversa

O discovery não é uma metáfora de aula: o AIOX tem a skill code-anatomist, um pipeline de 9 fases que faz engenharia reversa de software cobrindo arquitetura, domínio, dados, API, dependências e infra.

- Começou como: Um código herdado que rodava, mas cuja estrutura real ninguém tinha mapeado.
- Virou: Um mapa completo da arquitetura, domínio e dependências, fase a fase, antes de qualquer mudança.
- Prova: A skill code-anatomist (renomeada de domain-decoder, RT-DD-V2-001) existe no AIOX com 9 fases de reverse engineering documentadas.
- Lição: Discovery é primitivo real: tem skill, tem fases nomeadas, tem ordem de leitura do código.

### Caso: O /processo de mapeamento AIOX abre pela fase Discovery

Na visão de processo, o discovery é a primeira fase de um pipeline maior: /processo de mapeamento AIOX é um pipeline de 7 fases que começa exatamente em Discovery antes de qualquer arquitetura.

- Começou como: Um processo recorrente brownfield que ninguém tinha mapeado nem decomposto em fases.
- Virou: Um mapeamento de 7 fases iniciado pelo Discovery, que decifra o processo antes de desenhar a solução.
- Prova: A skill /processo de mapeamento AIOX existe no AIOX com 7 fases: Discovery, Architecture, Executors, Workflows, Tasks, QA Gates, Infra.
- Lição: Discovery não é opcional: é a fase de entrada que sustenta todas as outras seis.

---

## As 10 fases do discovery brownfield

O discovery brownfield não é um olhar genérico no código. É um pipeline de fases nomeadas, da leitura da arquitetura à proposta de intervenção. Cada fase fecha antes da próxima abrir.

**Pipeline de discovery brownfield**
As fases ordenadas que decifram um código herdado antes de qualquer intervenção.
- **1. Contexto**: Entender por que o projeto existe e que valor ele sustenta hoje.
- **2. Arquitetura**: Mapear a estrutura macro: camadas, módulos, fronteiras.
- **3. Domínio**: Decifrar as regras de negócio embutidas no código.
- **4. Dados**: Levantar schema real, tabelas com conteúdo, fluxo de dados.
- **5. Dependências**: Mapear o que o código consome e o que depende dele.
- **6. Síntese**: Desenhar o mapa consolidado da estrutura real.

**discovery fecha antes da intervenção abrir**

1. **Leitura**: O discovery lê o código herdado em camadas ordenadas, sem mudar nada.
2. **Mapa**: Arquitetura, domínio, dados e dependências viram um mapa consolidado.
3. **Gate**: O discovery fecha com checkpoint antes de qualquer proposta.
4. **Intervenção**: A mudança proposta nasce do mapa, fase por fase.

---

## Como discovery, mapa e intervenção se combinam

Discovery, mapa e intervenção não são rivais; são camadas em sequência. O discovery decifra, o mapa registra, a intervenção muda. Entender a direção evita propor mudança antes de entender.

- **1. Decifrar (Discovery)**: Quem lê o código herdado. O discovery roda as fases sem mudar nada. É a única etapa que apenas observa. [WHY, decifra, observa]
- **2. Registrar (Mapa)**: O que ficou entendido. A estrutura real desenhada: arquitetura, domínio, dados, dependências. O artefato que sobrevive ao discovery. [WHAT, estrutura, mapa]
- **3. Mudar (Intervenção)**: Como o código vira outro. A proposta de mudança que nasce do mapa. Zero palpite, máxima rastreabilidade. [HOW, proposta, do mapa]

---

## Quando rodar discovery completo?

Antes de tocar no código, decida se o projeto merece discovery completo. O critério economiza tempo quando você escolhe pelo legado vivo, não pela vontade de mexer logo.

**Árvore de decisão**
_Responda pelo legado antes de pensar em quanto vai mudar._

```mermaid
%%{init: {"theme": "dark", "flowchart": {"useMaxWidth": true, "htmlLabels": true, "nodeSpacing": 22, "rankSpacing": 36, "padding": 8}}}%%
flowchart TB
  Q["O código já existe e você não o escreveu?"]
  B0["Brownfield vivo<br/>Discovery completo"]
  B1["Greenfield<br/>Desenho direto"]
  B2["Legado abandonado<br/>Descarte / isolamento"]
  B3["Patch pontual<br/>Discovery focado"]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
```

- **Brownfield vivo** — O código já roda em produção, sustenta valor e você não o escreveu.
  → _Discovery completo_
  Ex.: Rode discovery completo via code-anatomist ou /processo de mapeamento AIOX antes de propor.
- **Greenfield** — Você começa do zero, sem código herdado nem decisões antigas.
  → _Desenho direto_
  Ex.: Não precisa de discovery de legado. Desenhe livre a arquitetura.
- **Legado abandonado** — Código antigo que ninguém usa e pode ser descartado sem custo.
  → _Descarte / isolamento_
  Ex.: Não vale discovery completo. Avalie só se descarta ou isola.
- **Patch pontual** — Uma mudança mínima e isolada num código que você já conhece bem.
  → _Discovery focado_
  Ex.: Discovery leve, focado só na região tocada. Não precisa do pipeline inteiro.

**Gate:** Qual é o gate? — _Sem gate, você roda discovery por reflexo ou pula por pressa. Responda: existe código herdado vivo que você não entende? Se sim, discovery completo. Se não, desenho direto, descarte ou discovery focado._

> **Regra do critério único**: A escolha não é pela importância do projeto; é pelo legado vivo. Se existe código herdado que importa e você não entende, discovery completo é a peça. Se é greenfield ou legado morto, discovery completo é overengineering. Mexer em brownfield vivo sem discovery é refatorar no escuro, o erro mais caro do início.

---

## Rotas de discovery

Cada tipo de projeto brownfield tem um modo típico de discovery. Saber a rota evita decidir certo pelo discovery e materializar com a ferramenta errada.

#### Discovery de código herdado
Quando o brownfield é um software que já roda e você precisa entender a estrutura.
1. **Sinal: código em produção que você não escreveu.
2. **Pergunta: você entende a arquitetura real ou está supondo?
3. **Ação: rodar code-anatomist para as 9 fases de engenharia reversa.
4. **Resultado: mapa de arquitetura, domínio, dados e dependências.

#### Discovery de processo recorrente
Quando o brownfield é um processo de negócio que existe mas ninguém mapeou.
1. **Sinal: processo recorrente sem documentação formal.
2. **Pergunta: você conhece as fases reais ou está adivinhando?
3. **Ação: rodar /processo de mapeamento AIOX começando pela fase Discovery.
4. **Resultado: processo decomposto em 7 fases a partir do discovery.

#### Discovery focado para mudança pontual
Quando a mudança é pequena e isolada num código que você já conhece.
1. **Sinal: mudança mínima numa região conhecida do código.
2. **Pergunta: a região tocada tem dependências que você não vê?
3. **Ação: discovery focado só na região e suas dependências diretas.
4. **Resultado: mapa local suficiente sem o pipeline inteiro.

**Discovery de código**
Use quando o brownfield é software herdado e você precisa decifrar a estrutura.
- `code-anatomist`: roda as 9 fases de engenharia reversa do código.
- `mapear dependências`: levantar o que o código consome e o que depende dele.

**Discovery de processo**
Use quando o brownfield é um processo recorrente sem mapa formal.
- `/processo de mapeamento AIOX`: abre o pipeline de 7 fases pela fase Discovery.
- `fechar checkpoint`: validar o discovery antes de avançar para Architecture.

**Discovery focado**
Use quando a mudança é pontual e a região do código é conhecida.
- `mapear região`: decifrar só a parte tocada e suas dependências diretas.
- `validar fronteiras`: confirmar que a mudança não vaza para fora do mapeado.

---

## Modelos para ler melhor

Visualizações rápidas para o aluno comparar greenfield, brownfield e patch, os riscos de cada escolha e o grau de discovery que cada um exige.

- **Brownfield vivo**: alto (código herdado que importa pede discovery completo.)
- **Patch pontual**: médio (discovery focado na região tocada.)
- **Greenfield**: baixo (sem legado, quase nada a decifrar.)

- **Brownfield sem discovery**: brownfield (refatorar no escuro e quebrar o que não viu.)
- **Greenfield com discovery pesado**: greenfield (gastar tempo mapeando o que não existe.)
- **Patch sem checar dependências**: patch (mudança pontual vazando para fora do esperado.)

**Matriz de Decisão do Aluno**

Em dúvida, escolha a célula que melhor descreve o seu projeto.

- **Código herdado vivo**: Discovery completo. code-anatomist antes de propor.
- **Processo recorrente sem mapa**: /processo de mapeamento AIOX pela fase Discovery.
- **Começando do zero**: Greenfield. Desenhe livre, sem discovery de legado.
- **Mudança pontual conhecida**: Discovery focado só na região tocada.
- **Legado que ninguém usa**: Avalie descarte ou isolamento, não discovery.
- **Não sabe ainda**: Pergunte: o código já roda e você não escreveu? Sim, discovery.

- **Sinal de discovery saudável**: estrutura real mapeada antes de qualquer mudança / discovery focado na região da mudança pontual / intervenção proposta sem mapa, no escuro
- **Separação de etapas**: discovery decifra, mapa registra, intervenção muda / discovery e proposta em rodadas separadas e rastreáveis / mudança no código durante a fase de leitura

---

## O que cada peça carrega

Cada peça do discovery tem uma anatomia mínima. Saber o que cada uma guarda ajuda a reconhecer quando você está pulando uma fase ou usando a ferramenta errada.

- **Brownfield: o herdado**: Código ou processo que já roda e você não escreveu. Carrega decisões antigas embutidas.
- **Discovery: o ritual**: As fases que decifram a estrutura real sem mudar nada. Leitura ordenada, não palpite.
- **code-anatomist: a skill**: O pipeline de 9 fases de engenharia reversa de software, da arquitetura à infra.
- **/processo de mapeamento AIOX: o mapa**: O pipeline de 7 fases que abre pela fase Discovery, com checkpoint antes de avançar.
- **Intervenção: a mudança**: A proposta que nasce do mapa. Nunca vem antes do discovery, sempre depois.

---

## Métricas do discovery

Sem telemetria, a saúde do discovery vira fé. Estas perguntas separam um discovery confiável de um olhar superficial disfarçado de mapeamento.

**Colunas:** Métrica | Pergunta | Sinal saudável | Sinal de risco

- Cobertura de estrutura: Arquitetura, domínio, dados e dependências foram mapeados? | As quatro camadas têm mapa, não suposição. | Uma camada ficou no palpite, refatoração quebra ali.
- Ordem das fases: O discovery rodou na ordem, da arquitetura à síntese? | Cada fase fechou antes da próxima abrir. | Pulou direto para a mudança, sem fechar o mapa.
- Separação de etapas: A leitura ficou separada da mudança? | Discovery decifrou sem alterar o código. | Refatoração começou durante a fase de leitura.
- Rastreabilidade: A intervenção aponta para o mapa que a justifica? | Cada mudança traça de volta a uma fase do discovery. | Mudança proposta sem âncora no que foi mapeado.

---

## Quando resistir ao discovery completo

A distinção ajuda mais quando você resiste ao reflexo de rodar discovery completo em tudo. O discovery tem custo: tempo de leitura, mapeamento, checkpoint. Vale só quando o legado vivo paga.

**Quando rodar discovery completo**
- O código já roda em produção e sustenta valor real.
- Você não escreveu a estrutura e não a entende.
- A mudança toca regiões com dependências desconhecidas.
- O custo de quebrar no escuro é alto.

**Quando não rodar**
- É greenfield: começa do zero, nada a decifrar.
- É legado morto que pode ser descartado sem custo.
- A mudança é pontual numa região que você já domina.
- O custo do discovery completo supera o risco da mudança.

---

## Exercício: decida o discovery

Pegue um projeto real seu e aplique o critério. O objetivo não é mapear tudo; é apontar se o projeto exige discovery completo antes de tocar em qualquer linha.

**Um projeto, cinco perguntas**
```yaml
discovery:
  projeto: "o que voce vai mexer?"
  herdado: "codigo ja roda e voce nao escreveu? sim | nao"
  peca: "discovery_completo | desenho_direto | discovery_focado"
  ferramenta: "code_anatomist | aiox_map_process | discovery_focado"
  gate: "por que nao a outra rota? (se discovery, quais camadas mapeia antes?)"

```
*O acerto não é mapear tudo. É provar que você escolheu a rota pelo critério legado vivo e sabe justificar por que a outra custaria mais sem entregar mais segurança.*

**Exemplo preenchido: herdar um SaaS legado versus criar um módulo novo**

- **Projeto A**: Herdei um SaaS em producao que nao escrevi e preciso adicionar uma feature.
- **Herdado A**: Sim. O codigo ja roda e tem decisoes antigas que eu nao conheco.
- **Peça A**: Discovery completo. Rodo code-anatomist para mapear arquitetura, dominio, dados e dependencias antes de tocar.
- **Projeto B**: Vou criar um modulo novo do zero, sem dependencia de codigo legado.
- **Peça B**: Desenho direto. Greenfield: nao ha legado a decifrar, desenho a arquitetura livre.
- **Gate B**: Discovery completo nao se aplica: nao existe estrutura herdada para mapear, entao a leitura pesada seria mapear o vazio.

- 1. **Projeto**: Descreva em uma frase o projeto ou processo em que você vai mexer.
- 2. **Herdado?**: Responda: o código já roda e você não o escreveu, ou começa do zero?
- 3. **Peça**: Aponte discovery completo (brownfield vivo), desenho direto (greenfield) ou discovery focado (patch).
- 4. **Ferramenta**: Diga como rodaria: code-anatomist para código, /processo de mapeamento AIOX para processo, discovery focado para patch.
- 5. **Gate**: Justifique por que não escolheu a outra rota. Para discovery, diga quais camadas vai mapear antes de propor.

**Funcionou se:**

- O aluno escolhe a rota pelo critério legado vivo, não pela vontade de mexer logo.
- O aluno separa decifrar (discovery) de propor mudança (intervenção).
- O aluno define quais camadas vai mapear quando escolhe discovery completo.

---

## Glossário do Brownfield Discovery

Tradução dos termos para alguém que está vendo a distinção greenfield versus brownfield pela primeira vez.

- **Brownfield**: Projeto que já existe, já roda e que você não escreveu. Tem decisões antigas embutidas que você precisa respeitar.
- **Greenfield**: Projeto que começa do zero, sem código herdado nem decisões antigas. Liberdade total de arquitetura.
- **Discovery**: O ritual de decifrar a estrutura real de um código herdado antes de propor mudança. Lê em fases ordenadas sem alterar nada.
- **code-anatomist**: A skill do AIOX que faz engenharia reversa de software em 9 fases: arquitetura, domínio, dados, API, dependências, infra. Renomeada de domain-decoder.
- **/processo de mapeamento AIOX**: O pipeline de 7 fases do AIOX para mapear processos recorrentes. Abre pela fase Discovery, com checkpoint antes de avançar.
- **Mapa**: A estrutura real desenhada pelo discovery: arquitetura, domínio, dados e dependências. O artefato que sobrevive à leitura.
- **Intervenção**: A mudança proposta a partir do mapa. Nasce do discovery, nunca antes dele.
- **Refatorar no escuro**: O anti-padrão de mudar código herdado sem discovery. Quebra o que não foi entendido e descobre tarde demais.

> **Portão da aula**: A aula só está no padrão quando o aluno nomeia o que distingue brownfield de greenfield, distingue o discovery (decifrar a estrutura real) da intervenção (propor mudança) e consegue apontar, para um projeto real, se ele exige discovery completo (brownfield vivo, via code-anatomist ou /processo de mapeamento AIOX) ou desenho direto (greenfield) antes de tocar em qualquer linha.

***

---

## Operar isto na prática

Esta aula é pré-requisito no curso de squads — quando a missão for real, siga para: Code Anatomist: `cursos/AIOX-Advanced-Squads/aulas/03-code-anatomist.md` · Domain Decoder: `cursos/AIOX-Advanced-Squads/aulas/04-domain-decoder.md`

## Navegação

← [[aulas/24-entidade-como-unidade-de-processo|Entidade como unidade de processo: nasce, vive, morre]] · ↑ [[modulos/Módulo 4 - Método e Brownfield|M4 — Método e brownfield]] · ⌂ [[cursos/AIOX Advanced/README|Curso]] · → [[aulas/53-brownfield-enhancement|Brownfield Enhancement: como adicionar feature em código legado]]
