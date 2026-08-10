# L1-L8 · As 8 camadas de análise

Cada camada tem: **entrada** (o que assume), **saída** (o que produz), **gatilho** (quando rodar), **anti-gatilho** (quando pular).

---

## L1 · Diagnóstico do dataset

**Entrada:** CSV/XLSX bruto recebido.

**Saída:** Bloco YAML com qualidade do dataset.

**Gatilho:** Sempre — primeira ação após receber o arquivo.

**Anti-gatilho:** Nenhum.

**Como rodar:**

```python
import pandas as pd
df = pd.read_csv(path)

# Diagnóstico
print(f"Total: {len(df)}")
print(f"Colunas: {df.columns.tolist()}")
print(f"Preenchimento:")
for col in df.columns:
    pct = 100 * df[col].notna().sum() / len(df)
    print(f"  {col}: {pct:.1f}%")

# Detectar tipos de campo
for col in df.columns:
    n_unique = df[col].nunique()
    if n_unique <= 10:
        print(f"  {col} → categórico ({n_unique} níveis)")
    elif df[col].dtype == object:
        avg_len = df[col].dropna().astype(str).str.len().mean()
        if avg_len > 30:
            print(f"  {col} → texto aberto (avg {avg_len:.0f} chars)")
        else:
            print(f"  {col} → identificador ou curto")
```

**Output esperado:**

```yaml
dataset:
  n_total: 726
  campos_categoricos: 4
  campos_abertos: 3
  campos_meta: [email, utm_source, submitted_at]
  preenchimento_geral: 87%
  qualidade: alta
  janela_temporal: "2026-05-05 a 2026-05-13"
```

**Decisão pós-L1:** Se preenchimento <50% em campos críticos, **pare e pergunte ao usuário** se quer prosseguir com a fatia preenchida ou ajustar.

---

## L2 · Distribuições univariadas

**Entrada:** Campos categóricos identificados em L1.

**Saída:** YAML por campo com `{categoria, n, pct}` ordenado por frequência.

**Gatilho:** Sempre.

**Anti-gatilho:** Nenhum.

**Regra:** Cada distribuição vem com **ranking explícito** e **delta vs amostra anterior** (se houver).

**Output esperado:**

```yaml
perfil:
  - { id: P1, nome: "...", n: 251, pct: 34.6, ranking: 1 }
  - { id: P2, nome: "...", n: 191, pct: 26.3, ranking: 2 }
```

**Atenção crítica:** Sempre dê IDs (`P1`, `P2`, `PR1`, etc) às categorias. Vai precisar deles em L3 e L5 pra construir critérios de segmento.

---

## L3 · Cruzamentos 2D

**Entrada:** 2+ campos categóricos chave.

**Saída:** Matrizes de contagem com células % por linha.

**Gatilho:** Sempre que houver 2+ categóricos. **Sempre.**

**Anti-gatilho:** Dataset com apenas 1 categórico relevante.

**Como rodar:**

```python
# Matriz absoluta
ct = pd.crosstab(df['perfil'], df['problema'])

# Matriz % por linha (revela células dominantes dentro de cada perfil)
ct_pct = pd.crosstab(df['perfil'], df['problema'], normalize='index') * 100
```

**Cruzamentos canônicos pra qualquer pesquisa de público:**
- Perfil × Problema
- Perfil × Maturidade técnica
- Setor × Problema
- Tempo/disponibilidade × Problema
- Canal de aquisição (UTM) × Perfil
- Maturidade × Problema (revela descompassos)

**Procura ativa da célula quente:**

A célula com `pct_por_linha > 50%` em uma linha é candidata a avatar primário. Se houver, marca-la imediatamente.

**Anti-padrão crítico:** Não fazer cruzamento de variáveis que se sobrepõem semanticamente (ex: "perfil de carreira" × "perfil profissional" — vão correlacionar artificialmente).

---

## L4 · Análise temática qualitativa

**Entrada:** Campos abertos com >100 respostas substantivas (>40 chars cada).

**Saída:** Ranking de temas com % e citações canônicas por tema.

**Gatilho:** Sempre que critério de entrada for satisfeito.

**Anti-gatilho:** Campos abertos com <50 respostas ou todas curtas (<40 chars). Aí não há substância pra análise temática.

**Método:** Vide `thematic-coding.md` em detalhe. Resumo:

1. Defina 8-12 temas candidatos com keywords
2. Atribua cada resposta ao tema dominante (uma resposta pode contar pra múltiplos temas)
3. Rankeie por frequência
4. Para cada tema top 5, extraia 3-5 citações literais canônicas

**Output esperado:**

```yaml
temas:
  - tema: "Vendas / prospecção / clientes"
    pct: 23.2
    n_aprox: 147
    keywords_usadas: [vender, prospec, cliente, lead, captação]
    citacoes_canonicas:
      - "Como eu faço para prospectar, automatizar e vender isso na prática"
      - "Acredito que não tenho um processo comercial bem definido"
```

**Atenção:** Análise temática por keywords é **heurística, não NLP profundo**. Reporte isso em `nivel_de_confianca: media`. Para NLP profundo (embeddings, clustering semântico), avise o usuário que requer pipeline adicional.

---

## L5 · Segmentação acionável

**Entrada:** Cruzamentos de L3 + análise temática de L4.

**Saída:** 5-10 segmentos com critério estatístico, n, abordagem comercial.

**Gatilho:** Sempre que o uso for comunicação/venda/produto.

**Anti-gatilho:** Pesquisa puramente descritiva/acadêmica.

**Regras:**

1. **Cada segmento tem ID curto** (`AV_PRIMARIO`, `AV_PREMIUM`, etc) usado consistentemente nos outputs subsequentes.

2. **Critério é SQL-like, não prosa:**
```yaml
- id: AV_PRIMARIO
  criterio: 'perfil = "Mudar de carreira" AND problema = "Vender IA"'
  n: 103
  pct: 14.2
```

3. **Segmentos podem sobrepor.** Um aluno pode estar em 3 segmentos. Reporte isso explicitamente.

4. **Cada segmento gera UMA decisão diferente.** Se dois segmentos têm a mesma abordagem comercial, mescle.

5. **Sempre incluir:**
   - O segmento que é o ICP claro
   - O segmento "descompasso" (querem X mas não têm capacidade)
   - O segmento "iniciante absoluto" (risco de desconectar)
   - O segmento "premium" (não compra o produto X, compra Y)

**Vide `./segment-archetypes.md` para padrões reutilizáveis.**

---

## L6 · Avatar primário em profundidade

**Entrada:** Célula quente identificada em L3 (≥50% em uma linha + n absoluto ≥50).

**Saída:** Perfil completo do subgrupo com persona narrativa.

**Gatilho:** Existência de célula quente. **Importante:** se não houver, NÃO INVENTE avatar primário. Use só os segmentos de L5.

**Anti-gatilho:** Distribuição uniforme entre células. Aí o público é fragmentado por design e não tem "avatar primário".

**Estrutura obrigatória:**

```yaml
avatar_primario:
  id: AV_PRIMARIO
  nome: "Nome descritivo curto"
  definicao_estatistica: "fórmula SQL-like"
  n_absoluto: X
  pct_da_turma: X
  
  demografia:
    # subdistribuições do próprio avatar (não confundir com média da turma)
    maturidade_tecnica: {...}
    tempo_disponivel: {...}
    setor: {...}
    canal_aquisicao: {...}  # se houver UTM
  
  comparativo_com_media:
    # quanto o avatar difere da média da turma em cada eixo
    - "X% acima da média em Y"
    - "Z% abaixo em W"
  
  persona_canonica:
    nome: "Nome próprio"
    idade: número
    cidade: "..."
    ocupacao: "..."
    status_emocional: "..."
    fala_canonica: |
      "Citação narrativa de 2-4 frases que destila o que esse avatar diria"
    o_que_quer: [...]
    o_que_trava: [...]
    comportamento_compra: {...}
  
  dores_ranqueadas:
    # 3-5 dores em ordem de intensidade observada nas respostas abertas
    - { id: D1, nome, intensidade, pct, citacao }
    - ...
  
  jornada_emocional:
    # SÓ se o contexto for venda/onboarding
    # 4-6 estágios narrativos
    - { estagio, nome, emocao_dominante, descricao }
  
  gatilhos_de_compra: [...]
  objecoes_esperadas: [...]
```

**Regras pra persona canônica:**

1. **Persona = composto estatístico, não pessoa real.** Nome inventado, mas características baseadas no agregado.

2. **Idade/cidade** baseadas no setor + perfil. Não invente "São Paulo capital" se o setor é "agricultura interior".

3. **Fala canônica** deve ser **destilação fiel** de 3-5 respostas abertas reais misturadas. Não inventar do zero.

4. **Status emocional** deve refletir os sinais detectados em L4 (urgência, exaustão, ambição, etc).

**Vide `./persona-construction.md` para o método detalhado.**

---

## L7 · Inteligência aplicada

**Entrada:** Tudo anterior + decisão-alvo definida em Etapa 0.

**Saída:** Material direto pra uso (copy, pitch, anti-padrões).

**Gatilho:** Decisão-alvo for comunicação/venda/copy.

**Anti-gatilho:** Pesquisa descritiva pura.

**Componentes obrigatórios:**

1. **Glossário linguagem que vende vs afasta** — 6-10 termos de cada lado, baseados no que o avatar primário escreve E no que os céticos rejeitam.

2. **Banco de citações tageado** — citações literais agrupadas por tag semântica (`#dor_X`, `#objecao_Y`, `#aspiracao_Z`). Mínimo 6 tags, 5-8 citações por tag.

3. **Frase de abertura otimizada** — uma frase que:
   - Cita um número específico do avatar primário
   - Nomeia a dor #1
   - Valida o que o avatar já é bom em
   - Nomeia explicitamente o que falta
   - Cria sensação de prioridade

4. **Anti-padrões explícitos** — o que NÃO falar. LLM gera melhor com restrições explícitas.

5. **Prompts-template** pra geração subsequente:
   - copy WhatsApp pós-evento
   - headline de landing
   - sequência de email pré-evento
   - script de Reels/Shorts
   - análise de lead individual

**Vide `./copy-intelligence.md` para esquemas completos.**

---

## L8 · Materialização visual

**Entrada:** Tudo anterior estruturado.

**Saída:** Markdown estruturado + dashboard HTML standalone.

**Gatilho:** Audiência além do analista (apresentação, equipe, LLMs externos).

**Anti-gatilho:** Análise interna rápida, exploratória.

**Defaults:**

- **Markdown:** sempre que houver análise estruturada. Vide `../assets/markdown-template.md`.
- **Dashboard:** sempre que houver audiência humana. Vide `../assets/dashboard-template.html`.
- **Notebook Python:** sob pedido explícito ("quero reproduzir") ou se o usuário é analista.

**Vide `./output-formats.md` para estrutura canônica e `./dashboard-design.md` para estética.**

---

## Decisões de pular camadas

| Caso | Camadas | Justificativa |
|------|---------|---------------|
| NPS interno trimestral | L1, L2, L4 | Não precisa segmentação acionável |
| Pesquisa de mercado pra investidor | L1-L5, L8 | Sem persona/copy |
| Lançamento de produto | L1-L8 | Todas |
| Onboarding cohort fechado | L1-L6 | Sem L7 (não há copy de venda) |
| Survey de feature em SaaS | L1-L4 | Sem persona/segmento amplo |
| Pesquisa pré-evento de venda | **L1-L8 todas** | Caso canônico AIOX |

## Checklist final antes de entregar

- [ ] L1 reportou qualidade do dataset?
- [ ] L2 tem IDs únicos pras categorias?
- [ ] L3 procurou ativamente célula quente?
- [ ] L4 reportou nível de confiança da análise temática?
- [ ] L5 tem 5-10 segmentos com critério SQL-like?
- [ ] L6 só foi feito SE havia célula quente?
- [ ] L7 só foi feito SE uso é comunicação?
- [ ] L8 respeita brandbook (se houver) ou estética padrão?
- [ ] Toda % vem com n absoluto?
- [ ] Vieses estão explicitados?
- [ ] Anti-padrões estatísticos foram evitados?
