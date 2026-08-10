---
type: lesson
course: aiox-advanced
course_title: AIOX Advanced
lesson_id: storybook-para-variantes
lesson_position: 57
title: Storybook para derivar e testar variantes (a11y, dark mode, responsivo)
source: upstream monorepo/apps/aiox-courses
source_path: content/courses/aiox-advanced/aulas/57-storybook-para-variantes/lesson.md
source_format: lesson.md
synced_at: '2026-08-09'
manual: true
concepts: []
tags:
- curso/aiox-advanced
- lesson
- course-brain
bloom: apply
reading_minutes: 15
has_mermaid_map: true
map_source: auto-decision_graph
module: M9
sequence: M9.5
track: complete
status: canonical
canonical_scope: cursos/AIOX Advanced
curated_at: '2026-08-09'
---

# Storybook para derivar e testar variantes (a11y, dark mode, responsivo)

← [[56-tailwind-shadcn-storybook|Tailwind + ShadCN + Storybook]] · ↑ [[modulos/Módulo 9 - Design System|M9]] · ⌂ [[cursos/AIOX Advanced/README|Curso]] · → [[58-ralph-paralelizacao|Ralph: paralelização]]

## Mapa desta aula

> Gate visual: quando o catálogo cresce, [[Chromatic]] (ou similar) impede drift de pixels entre PRs.

Decisão-chave da aula — o que quebra de verdade?

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
 [[cursos/AIOX Advanced/README|Curso]]"14px"
  }
}}%%
flowchart TB
  Q["O que a mudança de UI pode quebrar de verdade?"]
  B0["Fluxo crítico<br/>Estados completos + a11y foco/nome + da…"]
  B1["Só visual de marketing<br/>Viewports + dark se tema global; a11y d…"]
  B2["Formulário<br/>Error/Empty/Loa[[58-ralph-paralelizacao|Ralph: paralelização de múltiplos agentes]]ressão com o caso exato ant…"]
  B4["Explosão combinatorial<br/>Cenários nomeados de produto — não 2^n …"]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
classDef core fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#e2e8f0
  classDef step fill:#0f172a,stroke:#6366f1,stroke-width:1.5px,color:#f1f5f9
  classDef gate fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#e2e8f0
  classDef good fill:#14532d,stro```mermaid
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
  Q["O que a mudança de UI pode quebrar de verdade?"]
  B0["Fluxo crítico<br/>Estados completos + a11y foco/nome + da…"]
  B1["Só visual de marketing<br/>Viewports + dark se tema global; a11y d…"]
  B2["Formulário<br/>Error/Empty/Loading + teclado + mobile."]
  B3["Já quebrou em prod<br/>Story de regressão com o caso exato ant…"]
  B4["Explosão combinatorial<br/>Cenários nomeados de produto — não 2^n …"]
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
```book só no happy path light desktop, a aula falhou.
Happy path é demo. Variante é engenharia.

- **Objetivos da aula** (Matriz de eixos (não lista infinita); Stories que provam tema/viewport/a11y; Priorizar falha de variante)
- **Resultado tangível**: Um componente com stories de estado + dark + 1 viewport + nota a11y.
- **Não é o destino**: Gerar 200 stories automáticas sem critério. Isso é ruído com branding de cobertura.

---

## O erro do default eterno

*P · Onde você está*

Empatia com quem só testou o botão no centro da tela.

Cara, o Storybook vira portfolio. Screenshot lindo no default. Merge.
Segunda-feira: cliente no dark mode, contraste zero no label. Ou teclado
preso no modal. Ou layout estourado no iPhone SE.

Não é "falta de capricho". É **matriz não desenhada**. O default engana
porque é o estado que o autor olhou enquanto codava.

Se você está aqui, provavelmente já sentiu:

- "No meu monitor tava ok."
- Addon de a11y vermelho e ninguém lê.
- Dark mode = inverter cores e torcer.
- Responsivo só no DevTools no dia do deploy.

A partir daqui: variante é cidadã de primeira classe — não "depois a gente vê".

**Onde a maioria trava**
- Uma story Default e paz
- a11y addon instalado, zero gate
- Dark mode 'depois do launch'

**Onde o operador vai**
- Matriz mínima por componente crítico
- Falha de contraste bloqueia merge
- Viewport e tema no mesmo PR da feature

---

## Quatro eixos que pagam o aluguel

*S · Rota*

Estado, tema, viewport, a11y — o resto é opcional até doer.

Storybook pra variante não é "mais tela no menu lateral". É **gerar e
inspecionar o espaço de estados** que produção vai encontrar.

Quatro eixos que eu cobro primeiro:

1. **Estado** — default, hover/focus, disabled, loading, error, empty.
2. **Tema** — light/dark (e high-contrast se o produto exige).
3. **Viewport** — mobile / tablet / desktop nos breakpoints reais.
4. **a11y** — nome acessível, contraste, foco, teclado, aria onde couber.

Combinatória total explode. Por isso você **escolhe interseções que doem**,
não o produto cartesiano de marketing.

Prior-art: a 56 plantou a stack. Aqui o museu vira **bateria de prova**.

Lembrete brutal: Storybook que ninguém abre no PR é museu fechado.
Variante sem dono de review é dívida com iluminação bonita.

- **4**: eixos prioritários
- **1**: matriz por componente
- **0**: cobertura só no default

- **status**: storybook-variantes
- **meta**: eixos=estado+tema+viewport+a11y
- **meta**: regra=intersecao que dói
- **ready**: ready to matrix

**Legenda de cores**

O que cada cor sinaliza nesta aula

- **Story** (signal): caso nomeado e reproduzível
- **Eixo** (insight): dimensão de variação intencional
- **Interseção** (bench): estado×tema×viewport que importa
- **Gate** (action): falha bloqueia ou vira ticket
- **Explosão** (pain): matriz sem critério = ruído

**Como ler esta aula**

1. **Eixos**: O que variar e por quê.
2. **Matriz**: Como cortar sem cegar.
3. **Caso**: Componente real quebrando.
4. **Priorizar**: Do fail à correção.

---

## Da cohort: efeito composto da qualidade visual

*T1 + T2 · WhatsApp*

Realidade do grupo Advanced — cicatriz, não slide.

Alan: quando DS e gates acumulam, o efeito composto **impede** de entregar
código ruim. Storybook de variantes (dark, a11y, responsive) é onde isso vira
bateria — não catálogo de vaidade.

A turma manda print de tela 'quase certa'. Esta aula responde com matriz: se não
passa nas variantes, não é pronto. O Advanced ensinou isso no susto do review,
não no Figma perfeito.

> **Âncora de campo**: Happy path no light mode não é qualidade — é sorte amostral.

> **Materiais / FAQ**: Ligar QG visual ao 48 [[Quality Gate]] quando o produto for UI

---

## Como montar a matriz sem explodir

Cobertura inteligente > cobertura teatral.

Regra prática — **matriz mínima viável por criticidade**:

- **Componente de fluxo** (Button, Input, Dialog, Nav): estados completos
  + dark + mobile + a11y de foco/nome.
- **Componente de layout** (Card, Section): 2–3 densidades de conteúdo +
  viewports; dark se tokens de superfície.
- **Componente raro**: default + 1 edge que já quebrou uma vez.

Técnicas que funcionam no Storybook moderno:

- **Args/controls** pra variantes de prop (size, variant, disabled).
- **Decorators** de tema (dark class / provider).
- **Viewport addon** com breakpoints do [[DESIGN md|DESIGN.md]] — não genéricos de blog.
- **a11y addon** com falhas lidas no PR, não no "um dia".

Anti-padrão: gerar story pra cada prop booleano. Isso é snapshot de orgulho.
Prefira cenários nomeados: `CheckoutSubmitLoading`, `FormErrorMobileDark`.

Quando a IA gera UI, a matriz vira **prompt de restrição**: "implemente só
o que as stories cobrem; se faltar estado, abra story antes de inventar CSS".
Sem isso, o agent recria o default eterno e você volta pro portfolio.

- **Story nomeada**: Cenário com intenção de produto, não só prop dump.
- **Eixo**: Dimensão controlada (estado, tema, viewport, a11y).
- **Interseção crítica**: Combinação que já falhou ou é alta frequência de uso.
- **Cobertura teatral**: Muitas stories que ninguém roda nem lê no review.

> **Lei da interseção**: Priorize estado_ruim × dark × mobile. É onde o usuário real sofre e o autor nunca olhou.

- **Muitas stories** != **Boa cobertura**: Sem gate e sem critério, volume é ruído.
- **Addon instalado** != **QA ativo**: Addon sem bloquear merge é enfeite.

---

## Caso: modal perfeito no default, armadilha no teclado

Como a matriz pega o que o olho não pega.

Time entregou Dialog de confirmação de delete. Story Default: lindo.
Light, desktop, mouse. Code review visual passou.

Produção: usuário só teclado. Foco escapava pro fundo. Screen reader lia
"botão" sem nome no close. Dark: texto muted no fundo muted — contraste
falhou. Mobile: botões empilhavam e o cancel ficava fora da dobra.

Matriz mínima que teria pegado:
1. Default + OpenFocusTrap (teclado)
2. DarkDangerConfirm
3. MobileStackedActions
4. a11y scan no Open

Custo de escrever as quatro stories: menor que uma hora de suporte.
Custo de não escrever: ticket P1 e desculpa em público.

Então o que acontece se você só snapshot visual? Você congela o default
e deixa o comportamento acessível no escuro.

Checklist de review que eu coloco no PR de UI[[Quality Gate]]novas/alteradas listadas no body do PR
- [ ] Dark rodado no componente tocado
- [ ] a11y addon sem critical aberto (ou waiver escrito)
- [ ] Viewport mobile se o fluxo é mobile-first ou misto
- [ ] Story de regressão se o PR corrige bug reportado

**Do fail à prioridade**

1. **Rodar**: Stories + a11y no PR
2. **Classificar**: a11y / dark / RWD / estado
3. **Impacto**: bloqueia fluxo? legal?
4. **Fix ou ticket**: P0 no PR ou backlog com story
5. **Regredir**: story fica como prova

---

## Qual variante escrever agora?

Árvore curta pra não virar fábrica de story inútil.

**Árvore de decisão**
_Escolha pela superfície de risco, não pela facilidade de args._

```mermaid
%%{init: {"theme": "dark", "flowchart": {"useMaxWidth": true, "htmlLabels": true, "nodeSpacing": 22, "rankSpacing": 36, "padding": 8}}}%%
flowchart TB
  Q["O que a mudança de UI pode quebrar de verdade?"]
  B0["Fluxo crítico<br/>Estados completos + a11y foco/nome + dark + mobile."]
  B1["Só visual de marketing<br/>Viewports + dark se tema global; a11y de heading/contr…"]
  B2["Formulário<br/>Error/Empty/Loading + teclado + mobile."]
  B3["Já quebrou em prod<br/>Story de regressão com o caso exato antes do fix."]
  B4["Explosão combinatorial<br/>Cenários nomeados de produto — não 2^n stories."]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
```

- **Fluxo crítico** — Login, pagamento, delete, submit.
  → _Estados completos + a11y foco/nome + dark + mobile._
  Ex.: Confirm delete account.
- **Só visual de marketing** — Landing, hero, seção estática.
  → _Viewports + dark se tema global; a11y de heading/contraste._
  Ex.: Hero da home.
- **Formulário** — Inputs, validação, erro, disabled.
  → _Error/Empty/Loading + teclado + mobile._
  Ex.: Cadastro multi-step.
- **Já quebrou em prod** — Bug reportado em tema/viewport.
  → _Story de regressão com o caso exato antes do fix._
  Ex.: Label some no dark iOS.
- **Explosão combinatorial** — 10 props booleanas.
  → _Cenários nomeados de produto — não 2^n stories._
  Ex.: Table com 12 toggles.

**Gate:** Você consegue nomear 3 interseções que um usuário real toca esta semana? — _Se só consegue nomear Default, ainda está em modo portfolio._

#### Rota matriz mínima
Por componente crítico.
1. **Listar eixos: Estado, tema, viewport, a11y.
2. **Cortar: 3–6 interseções que doem.
3. **Nomear: Stories de cenário, não prop soup.
4. **Gate: PR mostra falhas lidas.

#### Rota regressão
Bug virou prova.
1. **Repro: Condições exatas do bug.
2. **Story: Congela o caso falho.
3. **Fix: Verde na mesma story.
4. **Keep: Nunca apagar a prova.

#### Rota review
PR de UI com disciplina.
1. **Diff: Código + stories novas.
2. **Rodar: a11y + dark no componente.
3. **Classificar: Block vs follow-up.
4. **Aceite: Só com interseções cobertas.

---

## Matriz de um componente real (15 min)

Papel ou arquivo de story — mas escrito.

Escolhe um componente que o usuário toca de verdade. Cronometra quinze minutos.

- 1. **Escolha**: Um componente (Button, Dialog, FormField, NavItem…).
- 2. **Eixos**: Liste estados, temas, viewports e checks a11y relevantes.
- 3. **Corte**: Marque 4–6 interseções críticas (não o produto cartesiano).
- 4. **Stories**: Nomeie cada story como cenário de produto.
- 5. **Prioridade**: Se só puder implementar 2 amanhã, quais? Por quê?

**Funcionou se:**

- A matriz tem eixos explícitos e interseções nomeadas.
- Pelo menos uma interseção envolve dark OU mobile OU a11y.
- Você justificou a prioridade das 2 primeiras stories.

---

## Glossário sem jargão de vaidade

- **Variante**: Instância intencional de um componente sob eixos (estado, tema, viewport).
- **Matriz de stories**: Conjunto planejado de interseções — não lista infinita de props.
- **Interseção crítica**: Combinação de eixos de alto risco ou alta frequência de uso.
- **Story de regressão**: Caso que congela um bug passado como prova permanente.
- **Cobertura teatral**: Muitas stories sem gate, leitura ou critério de risco.
- **Addon sem gate**: Ferramenta de a11y/visual instalada mas que não bloqueia nem gera ticket.

---

## Portão da aula

Você passou quando um componente crítico tem matriz com estados + pelo
menos um eixo de tema/viewport/a11y, e o PR trata falha de variante como
sinal — não como "detalhe visual".

Storybook sem variantes é folder de screenshots. Com variantes é fábrica
barata de verdade antes da produção.

> **Próximo na trilha**: Da UI estável a gente sobe pra escala de execução: aula 58 — Ralph e paralelização de múltiplos agentes sem colidir o repo.

> **GATE-MODULE (auto)**: GPS Goal/Position/Steps presentes · caso + do/dont · decisão · prática com evidência · glossário. Alvo DL ≥70 atingido na construção enrich-W3.

***

---

## Navegação

← [[43-design-md-novo-contrato|DESIGN.md: o novo contrato que a IA lê antes de gerar tela]] · ↑ [[modulos/Módulo 9 - Design System|M9]] · ⌂ [[cursos/AIOX Advanced/README|Curso]] · → [[58-ralph-paralelizacao|Ralph: paralelização de múltiplos agentes]]
[[DESIGN md|DESIGN.md]]`CheckoutSubmitLoading``FormErrorMobileDark````mermaid
%%{init: {"theme": "dark", "flowchart": {"useMaxWidth": true, "htmlLabels": true, "nodeSpacing": 22, "rankSpacing": 36, "padding": 8}}}%%
flowchart TB
  Q["O que a mudança de UI pode quebrar de verdade?"]
  B0["Fluxo crítico<br/>Estados completos + a11y foco/nome + dark + mobile."]
  B1["Só visual de marketing<br/>Viewports + dark se tema global; a11y de heading/contr…"]
  B2["Formulário<br/>Error/Empty/Loading + teclado + mobile."]
  B3["Já quebrou em prod<br/>Story de regressão com o caso exato antes do fix."]
  B4["Explosão combinatorial<br/>Cenários nomeados de produto — não 2^n stories."]
  Q --> B0
  B0 --> B1
  B1 --> B2
  B2 --> B3
  B3 --> B4
