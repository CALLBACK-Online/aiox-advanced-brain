---
name: survey-intel
description: Transforma pesquisas pré-evento, formulários de inscrição, NPS, ou qualquer dataset tabular com respostas humanas em briefings acionáveis com dashboards visuais e markdown estruturado para LLM. Use quando o usuário enviar CSV/XLSX de pesquisa, formulário, inscrição, NPS, customer survey, ou pedir "análise de público", "perfil de audiência", "quem está na sala", "briefing pra masterclass", "avatar do meu lançamento", "análise do meu formulário", "estudo de público pré-evento". Especialmente útil para lançamentos digitais, masterclasses, workshops, eventos de venda, onboarding de cohorts, segmentação de leads, e qualquer momento em que decisões de comunicação/oferta dependem de entender quem é a audiência. Produz análise quantitativa em camadas, cruzamentos de variáveis, segmentos acionáveis, citações qualitativas tageadas, avatar primário em profundidade, dashboard HTML visual standalone, e markdown estruturado para reuso em Projects/Claude Code.
user-invocable: true
version: "1.0.0"
---

# Survey Intel · análise de pesquisa em camadas progressivas

Pesquisas de público são tratadas como aprendizado estatístico que serve a uma **decisão concreta** — não como relatório técnico. O objetivo nunca é "descrever os dados". O objetivo é responder: *o que esse público pede que eu entregue?*

## Princípio central

**Análise em camadas progressivas, não pipeline linear.** Cada camada é gatilhada pelo que a anterior revelou. Pular camadas é OK quando o dataset não pede; forçar todas é pior que parar cedo.

```
L1 · Diagnóstico do dataset           ← sempre
L2 · Distribuições univariadas        ← sempre
L3 · Cruzamentos 2D                   ← se houver 2+ variáveis categóricas chave
L4 · Análise temática qualitativa     ← se houver campos abertos com >100 respostas substantivas
L5 · Segmentação acionável            ← se a decisão final exige falar com subgrupos
L6 · Avatar primário em profundidade  ← se houver UMA célula claramente dominante no cruzamento
L7 · Inteligência aplicada            ← se o uso for comunicação/venda/copy (não pesquisa acadêmica)
L8 · Materialização visual            ← se há audiência além do próprio analista
```

## Quando usar esta skill

**Triggers explícitos:**
- Upload de CSV/XLSX/JSON de pesquisa, formulário, inscrição, NPS, survey
- "Analisa essa pesquisa"
- "Quem é meu público?"
- "Faz um briefing dessa turma"
- "Avatar do meu lançamento"
- "Análise pré-aula"

**Triggers implícitos (use mesmo sem pedido explícito):**
- Dataset com campos como `email`, `perfil`, `interesse`, `problema`, `dor`, `objetivo`, `setor`, `disponibilidade` + colunas de texto livre
- Conversas onde o usuário menciona masterclass, lançamento, cohort, workshop e tem dados sobre os inscritos
- Pedidos de "copy", "landing", "email pra esses leads" — análise vem ANTES da geração

## Workflow

### Etapa 0 · Calibração do contexto (obrigatório · ~2 min)

Antes de tocar nos dados, **descobrir 3 coisas**:

1. **Qual decisão depende desta análise?** Não pergunte "o que você quer". Pergunte "o que você vai fazer com isso". Respostas comuns:
   - Vender em masterclass/lançamento → ênfase em segmentos comerciais, dores, objeções
   - Onboarding/operação de cohort → ênfase em capacidade, expectativa, segmentos pedagógicos
   - Pesquisa de mercado → ênfase em distribuições e cluster analysis
   - Construir oferta nova → ênfase em dor + ambição + linguagem

2. **Quem vai consumir o output?** O analista sozinho, equipe, LLMs, audiência externa? Isso decide o formato final (notebook bruto, markdown estruturado, dashboard visual, ou tudo).

3. **Tem identidade visual obrigatória?** Se sim, pedir o brandbook/design tokens antes de gerar artefato. Se não, escolher estética editorial dark como default (provado funcionar pra dados).

**NÃO PULE essa etapa.** Análise sem decisão-alvo vira relatório descritivo inútil. A diferença entre "62% querem X" e "62% querem X, então o pitch precisa abrir com Y" é toda a diferença.

### Etapa 1 · Camadas de análise (executar em ordem, mas só as necessárias)

Consulte `references/L1-L8_layers.md` para o método detalhado de cada camada. Resumo:

**L1 · Diagnóstico** — n total, preenchimento por campo, qualidade dos campos abertos, presença de UTM/timestamp/email. Define o teto da análise.

**L2 · Univariadas** — frequência de cada categoria. Saída em YAML estruturado, não em prosa.

**L3 · Cruzamentos 2D** — matrizes perfil×problema, problema×setor, ferramentas×problema. **Procure ativamente pela célula dominante** — é onde nasce o avatar primário (L6).

**L4 · Análise temática** — agrupar respostas abertas por tema dominante via palavras-chave. Para datasets >500 respostas e campos com substância, é mandatório. Vide `references/thematic-coding.md`.

**L5 · Segmentação** — definir 5-10 segmentos com critério estatístico explícito (`SQL-like`: `perfil = X AND tempo >= Y`). Cada segmento deve ser acionável — gerar uma decisão diferente.

**L6 · Avatar primário** — SE houver célula dominante clara em L3. Aprofundar com: estatística do subgrupo, persona narrativa (com nome/idade/cidade), 4 dores ranqueadas, jornada emocional em estágios, gatilhos vs objeções.

**L7 · Inteligência aplicada** — SÓ se uso for comunicação/venda. Inclui: glossário de linguagem que vende vs afasta, citações ouro tageadas, frase de abertura otimizada, prompts-template pra reuso. Vide `references/copy-intelligence.md`.

**L8 · Materialização** — markdown estruturado + dashboard HTML. Vide `references/output-formats.md`.

### Etapa 2 · Honestidade estatística (obrigatório)

Sempre incluir:
- **n absoluto** ao lado de toda %
- **viés de auto-seleção** explicitado (quem não preencheu pode ser diferente)
- **nível de confiança** por insight (alta/média/baixa)
- **células com n<20**: marcar como "indicativo, não conclusivo"

Vide `references/statistical-honesty.md` para anti-padrões comuns.

### Etapa 3 · Iteração baseada em feedback

A primeira versão raramente é a final. Espere e prepare-se para:
- "Aprofunda no avatar" → expandir L6 com mais profundidade narrativa
- "Mais cruzamentos" → voltar a L3 com combinações não óbvias
- "Faz com identidade X" → reestilizar L8 com tokens de marca
- "Nova amostra chegou" → recalcular L1-L5 e **validar estabilidade** entre amostras (se ≤2pp de variação, análise qualitativa permanece válida)

## Outputs canônicos

A skill produz combinações de 3 artefatos, escolhidos conforme o caso:

1. **Markdown estruturado** (`{nome}_briefing.md`) — frontmatter YAML extensivo, seções numeradas, tags semânticas em citações, prompts-template no final. Otimizado pra injeção em Projects/Claude Code.

2. **Dashboard HTML** (`{nome}_dashboard.html`) — standalone, dark editorial por default ou identidade fornecida. Chart.js inline. Print-friendly. Vide `references/dashboard-design.md` e `assets/dashboard-template.html`.

3. **Notebook de análise** (`{nome}_analysis.py` ou similar) — quando o usuário pede pra reproduzir/auditar.

**Default:** se o usuário não especificar, gerar markdown + dashboard. Se houver brandbook, dashboard primeiro.

## Estética padrão (quando não há brandbook)

Vide `references/dashboard-design.md` em detalhe. Resumo:
- Fundo dark (`#0F0E0C` ou similar), alto contraste
- 1 acento saturado, máximo 2 cores funcionais (lime/orange/amber)
- Hairline borders, square components
- Tipografia editorial: serif para títulos, sans para corpo, mono para HUD
- Sem gradientes, sem drop shadows externos, sem rounded corners em utilitários

**Nunca use:** roxos genéricos de SaaS, gradientes meshy, glassmorphism, emojis nos dados.

## Anti-padrões comuns

Vide `references/anti-patterns.md` para a lista completa. Os 5 piores:

1. **Listar todas as variáveis sem hierarquizar.** A turma não precisa ler 47 distribuições — precisa entender as 3-4 que mudam decisão.

2. **Inventar persona sem base estatística.** Persona narrativa só após L6 — antes disso é ficção, não análise.

3. **Usar % sem n absoluto.** "42% querem 100k+/mês" é mentira se n=36 de 726.

4. **Promessa numérica como conclusão.** "Faturar 100k" não é insight de pesquisa, é wish do respondente — separe sempre `quem responde` de `quem é a maioria silenciosa`.

5. **Dashboard como objeto decorativo.** Cada gráfico precisa responder a uma pergunta acionável. Se não responde, retira.

## Validação cruzada entre amostras

Quando uma segunda amostra chega (e isso acontece em quase todo lançamento real):
1. Recalcule L1-L5 do zero
2. Compare proporções: variação ≤2pp em todas as categorias = **análise qualitativa validada**
3. Reporte estabilidade no frontmatter: `estabilidade_entre_amostras: confirmada`
4. Avatar primário pode crescer/encolher proporcionalmente, mas IDs e narrativa permanecem

## Estrutura dos arquivos de referência

- `references/L1-L8_layers.md` · método detalhado de cada camada
- `references/thematic-coding.md` · como agrupar respostas abertas
- `references/copy-intelligence.md` · linguagem que vende, citações tageadas, prompts-template
- `references/dashboard-design.md` · sistema visual padrão + adaptação a brandbooks
- `references/statistical-honesty.md` · níveis de confiança, viés, anti-padrões estatísticos
- `references/anti-patterns.md` · armadilhas comuns
- `references/output-formats.md` · estrutura canônica do markdown e do HTML
- `scripts/analyze_survey.py` · script template pra análise inicial
- `assets/dashboard-template.html` · template base do dashboard
- `assets/markdown-template.md` · template base do briefing
- `examples/` · exemplos completos (anonimizados)

## Lembrete final

Esta skill substitui análise rasa de pesquisa por análise em camadas. **Mas não substitui julgamento.** Quando os dados não pedem L6 (porque não há célula dominante), pare em L5. Quando o uso é interno e não precisa visualização, pule L8. O método se ajusta ao dataset — não o contrário.
