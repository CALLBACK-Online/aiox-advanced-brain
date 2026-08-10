---
documento: "{NOME_DESCRITIVO_DA_ANALISE}"
versao: "{X.Y}"
autor_analise: "Claude (Anthropic)"
preparado_para: "{NOME_DO_USUARIO_OU_TIME}"
data_analise: "{YYYY-MM-DD}"
fonte: "{Google Forms | Typeform | Tally | RD Station | export interno}"

dataset_atual:
  n_total: {NUMERO}
  n_substantivas_aberto: {NUMERO}
  preenchimento_geral: "{XX.X}%"
  janela_temporal: "{YYYY-MM-DD a YYYY-MM-DD}"

uso_primario:
  - injecao_em_projects_claude_como_contexto_base
  - geracao_automatizada_via_claude_code
  - apresentacao_humana

niveis_de_navegacao:
  - L1_overview: "seções 1-3"
  - L2_avatar: "seção 4"
  - L3_segmentos: "seção 5"
  - L4_inteligencia_aplicada: "seções 6-8"
  - L5_prompts: "seção 9"

aviso_de_uso:
  - "Citações entre aspas são literais — não inventar variações"
  - "Toda % vem com n absoluto"
  - "Avatar primário é o ICP — referência central"
  - "Vieses estão reportados na seção 11"
---

# {TITULO DA ANALISE}

## Resumo executivo de uma frase

{Síntese em 1-2 frases com o achado central. Exemplo:
"Dos {N} inscritos, {SUBGRUPO_DOMINANTE} ({PCT}%) tem dor predominantemente {COMERCIAL|TECNICA|OPERACIONAL} — o que muda o pitch de {O_QUE_SE_ESPERAVA} para {O_QUE_O_DADO_DIZ}."}

---

## 1. Visão estatística

### 1.1 Dataset

```yaml
n_total: {N}
campos_categoricos: {N}
campos_abertos: {N}
campos_meta: [email, utm_source, submitted_at]
preenchimento_geral: "{PCT}%"
qualidade: "{alta | media | baixa}"
janela_temporal: "{INICIO} a {FIM}"
dia_de_pico: "{DATA} ({N} = {PCT}%)"
```

### 1.2 Distribuições principais (KPIs)

```yaml
{campo_1}:
  - { id: P1, nome: "{categoria}", n: {N}, pct: {PCT}, ranking: 1 }
  - { id: P2, nome: "{categoria}", n: {N}, pct: {PCT}, ranking: 2 }
  # ...

{campo_2}:
  - { id: PR1, nome: "{categoria}", n: {N}, pct: {PCT}, ranking: 1 }
  # ...
```

---

## 2. Cruzamentos analíticos

### 2.1 {Campo A} × {Campo B}

| | Col1 | Col2 | Col3 | TOTAL |
|---|---|---|---|---|
| Linha1 | **{N} ({PCT}%)** | {N} | {N} | {N} |
| Linha2 | {N} | {N} | {N} | {N} |

> Célula quente: {LINHA × COLUNA} = {N} alunos ({PCT}%) → candidata a avatar primário (L6)

### 2.2 {Outro cruzamento relevante}

{Idem.}

---

## 3. Análise temática (se houver)

```yaml
analise_tematica:
  n_substantivas: {N}
  n_classificadas: {N}
  pct_cobertura: {PCT}
  metodologia: "Heurística por palavras-chave, não NLP profundo"
  nivel_de_confianca: media

temas:
  - tema: "{Nome do tema}"
    pct: {PCT}
    n_aprox: {N}
    keywords_usadas: [{kw1}, {kw2}, {kw3}]
    citacoes_canonicas:
      - "{citação literal 1}"
      - "{citação literal 2}"
      - "{citação literal 3}"
  # ...
```

---

## 4. AVATAR PRIMÁRIO

> **Atenção:** Esta seção só existe se L3 detectou célula quente clara (≥50% em uma linha + n≥50).

```yaml
avatar_primario:
  id: AV_PRIMARIO
  nome: "{Nome descritivo curto}"
  definicao_estatistica: '{campo_A} = "{valor}" AND {campo_B} = "{valor}"'
  n_absoluto: {N}
  pct_da_turma: {PCT}

  demografia:
    {sub_distribuicao_1}: { {cat_1}: {PCT}, {cat_2}: {PCT} }
    {sub_distribuicao_2}: { ... }

  comparativo_com_media:
    - "{PCT}% acima da média em {EIXO}"
    - "{PCT}% abaixo em {EIXO}"

  persona_canonica:
    nome: "{Nome próprio inventado}"
    idade: {NUMERO}
    cidade: "{Inferida do setor + perfil}"
    ocupacao: "{Inferida}"
    status_emocional: "{exausto | esperançoso | desconfiado | impaciente | ...}"
    fala_canonica: |
      "{Destilação fiel de 3-5 respostas abertas reais.
      Não inventar do zero — preservar tom e vocabulário do avatar.}"
    o_que_quer: ["{ambição 1}", "{ambição 2}"]
    o_que_trava: ["{barreira 1}", "{barreira 2}"]
    comportamento_compra:
      preco_aceitavel: "{faixa}"
      objecao_principal: "{texto}"
      gatilho_principal: "{texto}"

  dores_ranqueadas:
    - { id: D1, nome: "{dor}", intensidade: critica, pct: {PCT}, citacao: "{literal}" }
    - { id: D2, nome: "{dor}", intensidade: alta,    pct: {PCT}, citacao: "{literal}" }
    - { id: D3, nome: "{dor}", intensidade: media,   pct: {PCT}, citacao: "{literal}" }
    - { id: D4, nome: "{dor}", intensidade: baixa,   pct: {PCT}, citacao: "{literal}" }

  jornada_emocional:
    - { estagio: 1, nome: "{nome do estágio}", emocao_dominante: "{emoção}", descricao: "{texto}" }
    # ... 4-6 estágios

  gatilhos_de_compra: ["{gatilho 1}", "{gatilho 2}", "{gatilho 3}"]
  objecoes_esperadas: ["{objeção 1}", "{objeção 2}", "{objeção 3}"]
```

---

## 5. Outros segmentos acionáveis

```yaml
segmentos:
  - id: AV_PREMIUM
    criterio: '{SQL-like}'
    n: {N}
    pct: {PCT}
    abordagem_comercial: "{texto curto}"
    porque_existe: "{texto curto}"

  - id: AV_AVANCADO_PRONTO
    criterio: '{SQL-like}'
    n: {N}
    pct: {PCT}
    abordagem_comercial: "{texto curto}"

  - id: AV_INICIANTE_ABSOLUTO
    criterio: '{SQL-like}'
    n: {N}
    pct: {PCT}
    abordagem_comercial: "{texto curto}"

  - id: AV_DESCOMPASSO
    criterio: '{SQL-like}'
    n: {N}
    pct: {PCT}
    abordagem_comercial: "{texto curto}"

sobreposicoes_relevantes:
  AV_PRIMARIO_x_AV_DESCOMPASSO: {N} alunos ({PCT}% do avatar primário)
```

---

## 6. Glossário linguagem (vende vs afasta)

```yaml
linguagem_que_vende:
  - termo: "{frase literal}"
    porque_funciona: "{razão baseada em insight da análise}"
    tag: "#dor_X · #aspiracao_Y"
    contexto_de_uso: "pitch | landing | email | orgânico"
  # ... 6-10 itens

linguagem_que_afasta:
  - termo: "{frase a evitar}"
    porque_afasta: "{qual segmento isso ativa negativamente}"
    quando_pode_usar: "nunca"
  # ... 6-10 itens
```

---

## 7. Banco de citações tageado

```yaml
banco_citacoes:
  citacoes_ouro:
    - id: Q01
      texto: "{citação literal de alto impacto}"
      tags: ["#dor_X", "#avatar_primario"]
      uso_recomendado: "Abertura / desarmar cético"
    # ... 5-8 ouro

  por_tag:
    "#dor_X":
      - "{citação literal}"
      - "{citação literal}"
      # ... 5-8 por tag
    "#aspiracao_Y":
      - "..."
    "#objecao_Z":
      - "..."
    # mínimo 6 tags
```

---

## 8. Frase de abertura otimizada

> "Tem {N} pessoas aqui hoje que {característica do avatar primário} — e a maior dificuldade não é {skill aparente}. É {skill real identificada na análise}. Você sabe {o que o avatar já é bom em}, mas não sabe {o que falta concretamente}. Eu vou falar pra vocês primeiro. Os outros {N restante} também vão aprender, mas hoje a porta de entrada é a sua."

**Rationale:**
- "{N} pessoas" → autoridade quantitativa
- "{característica}" → reconhecimento (avatar se identifica)
- "Não é {aparente}, é {real}" → reframing — desinstala expectativa errada
- "Você sabe X, não sabe Y" → validação + dor nomeada
- "Vou falar pra vocês primeiro" → prioridade — diminui resistência

---

## 9. Prompts-template pra Claude Code / Projects

### 9.1 `gerar_copy_whatsapp_pos_evento`

```
Considerando o briefing {NOME_DA_ANALISE} anexo, gere sequência de 3-4 mensagens
de WhatsApp pós-masterclass seguindo:

AVATAR DE REFERÊNCIA: AV_PRIMARIO
CONSTRAINTS:
- Use linguagem da seção 6.linguagem_que_vende
- Evite TODA linguagem de 6.linguagem_que_afasta
- Cada mensagem endereça uma dor específica (D1-D4 da seção 4)
- Tom: direto, conversacional, sem hype
- Comprimento: máx 4 linhas por mensagem
OUTPUT: 3-4 mensagens numeradas com timestamps sugeridos
```

### 9.2 `gerar_headline_landing`

```
{Idem, com OUTPUT: 5 variações de headline + sub-headline}
```

### 9.3 `gerar_sequencia_email_pre_evento`

```
{Idem, com OUTPUT: 5 emails D-7, D-5, D-3, D-1, D-0}
```

### 9.4 `analisar_lead_individual`

```
Considerando o briefing {NOME_DA_ANALISE} anexo, classifique este lead:
{COLAR_RESPOSTA_DO_LEAD}

OUTPUT:
- segmento_provavel: {AV_PRIMARIO | AV_PREMIUM | ...}
- nivel_de_calor: {alto | médio | baixo}
- dor_dominante: {D1-D4}
- abordagem_recomendada: {texto 2-3 linhas}
```

---

## 10. Insights táticos numerados

```yaml
insights:
  - id: I01
    titulo: "{título curto}"
    evidencia: "{dado + n + %}"
    nivel_de_confianca: muito_alta
    implicacao: "{o que fazer com isso}"

  - id: I02
    titulo: "{...}"
    evidencia: "{...}"
    nivel_de_confianca: alta
    implicacao: "{...}"
  # ... 5-10 insights
```

---

## 11. Limitações e notas metodológicas

```yaml
limitacoes_da_analise:
  - "{Não há dado de X — persona usa estimativa baseada em Y}"
  - "{Cohort temporal cobre Z dias — não captura comportamento de longo prazo}"

vieses_reportados:
  - tipo: auto_selecao
    descricao: "Apenas {PCT}% preencheu campos abertos. Os {PCT}% que pularam podem ter perfil sistematicamente diferente."
  - tipo: aspiracao_financeira
    descricao: "Apenas {N} de {N} ({PCT}%) escreveu valor explícito. A maioria silenciosa provavelmente tem ambição mais baixa."
  - tipo: auto_classificacao
    descricao: "Perfis declarados são auto-atribuídos. Pessoas se descrevem aspiracionalmente."

niveis_de_confianca:
  L1_L2_L3: alta a muito_alta
  L4_tematica: media (heurística por keywords, não NLP)
  L6_persona: media_baixa (composição interpretativa, não pessoa real)
```

---

## Changelog

```yaml
versoes:
  v1_0:
    data: "{YYYY-MM-DD}"
    n: {N}
    descricao: "Análise inicial"
    autor: "Claude + {USUARIO}"
  # versões subsequentes quando novas amostras chegarem
```
