# Statistical Honesty · regras de integridade analítica

A diferença entre análise útil e análise enganosa é honestidade estatística. Quase tudo nessa skill depende de seguir essas regras.

## Regra de ouro

**Toda % deve vir com n absoluto.** Sem exceção.

❌ Ruim: "42% querem ganhar 100k/mês"
✅ Bom: "42% dos 36 alunos que escreveram um valor explícito querem 100k/mês"

Sem o n absoluto, percentuais mentem por omissão. "42% de 36" é diferente de "42% de 726".

## Níveis de confiança

Cada insight/conclusão recebe um nível explícito:

```yaml
nivel_de_confianca: muito_alta | alta | media | media_baixa | baixa
```

| Nível | Critério | Como reportar |
|-------|----------|---------------|
| **Muito alta** | Frequência direta com n≥100, confirmada em 2+ amostras | "Confirmado em amostras independentes" |
| **Alta** | Frequência direta com n≥50, ou cruzamento principal | Padrão pra L1, L2, L3 |
| **Média** | Análise temática heurística, cruzamento secundário | Padrão pra L4 |
| **Média-baixa** | Persona narrativa, estimativa de subgrupo, arquétipo | Padrão pra L6 narrativo |
| **Baixa** | Especulação fundamentada, inferência indireta | Marcar como "hipótese a validar" |

**Exemplo de aplicação:**

```yaml
insights:
  - id: I01
    afirmacao: "A dor real é comercial, não técnica"
    evidencia: "Vendas lidera respostas abertas com 23.2%; conhecimento técnico aparece em 6.2%"
    nivel: muito_alta
    base: "n=633 respostas abertas, confirmada em 2 amostras (574 e 726)"
  
  - id: I05
    afirmacao: "Persona Rafael Costa representa o avatar primário"
    evidencia: "Composição narrativa baseada em padrões agregados dos 103 alunos"
    nivel: media_baixa
    base: "Construção interpretativa, não pessoa real"
```

## Vieses conhecidos a reportar SEMPRE

### 1 · Viés de auto-seleção

Quem responde não é representativo de quem se inscreveu. Quem se inscreveu não é representativo de quem viu o convite.

**Como reportar:**
```yaml
vies_auto_selecao: |
  Apenas 87% preencheu campos abertos. Os 13% que pularam podem
  ter perfil sistematicamente diferente (mais apressado, menos
  engajado, ou com menos clareza). Análise reflete o subgrupo
  que se dedicou a responder.
```

### 2 · Viés de aspiração

Em campos abertos com pergunta "qual seu objetivo financeiro?", quem está em sobrevivência tem **vergonha de admitir números baixos**. O viés é sistemático e SEMPRE puxa pra cima.

**Como reportar:**
```yaml
vies_aspiracao_financeira: |
  Apenas 36 dos 726 (5%) escreveu um valor explícito.
  A "maioria silenciosa" provavelmente tem ambição mais baixa
  do que os 42% que escreveram 100k+. Pricing realista deve
  considerar nível 1 da pirâmide (5-15k) como mediana provável.
```

### 3 · Viés de auto-classificação

Perfis declarados ("Quero mudar de carreira") são auto-atribuídos. Pessoas se descrevem aspiracionalmente, não factualmente.

**Como reportar:**
```yaml
vies_auto_classificacao: |
  "Quero mudar de carreira pra IA" pode incluir gente que está
  só explorando + gente que já está em transição ativa. 
  Combine com "tempo disponível" pra refinar.
```

### 4 · Viés de UTM perdido

UTMs perdidos não são aleatórios. Geralmente são tráfego direto, indicação boca-a-boca, ou bio do Instagram — comportamentos sistematicamente diferentes.

**Como reportar:**
```yaml
vies_utm_perdido: |
  34% dos inscritos não têm UTM. Provavelmente vieram de bio
  do Instagram ou indicação direta — perfil possivelmente
  mais "quente" que mídia paga. Não generalize a análise de
  canal pros 100% da turma.
```

## Anti-padrões estatísticos comuns

### 1 · Confundir frequência com causalidade

❌ "48% usam Claude Code, então a turma é técnica"
✅ "48% declararam usar Claude Code. Não sabemos se usam profissionalmente ou apenas testaram."

### 2 · Generalizar de subgrupo pequeno

❌ "Os 36 que citaram valor querem 100k — a turma quer 100k"
✅ "36 escreveram valor. Esse subgrupo tem viés aspiracional. Não generalize pra os 690 que não escreveram."

### 3 · Confundir % alta com importância

❌ "Setor Outro com 22% é o segundo mais importante"
✅ "'Outro' é uma caixa preta — agrupa muitas categorias não capturadas. Não tratar como segmento real."

### 4 · Cherry-picking de citações

❌ Pegar 3 citações dramáticas e tratar como tendência
✅ Reportar n de cada tema + amostra representativa, não só os "highlights"

### 5 · Inferir intenção de palavras

❌ "Quem escreveu 'liberdade' quer libertinagem financeira"
✅ "Quem escreveu 'liberdade' pode referir-se a liberdade financeira, geográfica, ou de tempo. Ambíguo — usar contexto da resposta inteira."

### 6 · Tratar correlação como segmentação

❌ "Quem usa Claude Code também quer vender IA, então CC = vontade de vender"
✅ Reporte a correlação como dado, não como causa. Pode ser que ambos sejam consequência de "perfil sério".

### 7 · Subnotificação de sobreposição em segmentos

Segmentos sobrepõem. Sempre. Se você diz "AV_PRIMARIO = 103 e AV_PREMIUM = 34", o leitor assume disjuntos. **Diga explicitamente** que segmentos podem se sobrepor e em quanto.

```yaml
sobreposicoes_relevantes:
  AV_PRIMARIO_x_AV_AVANCADO_PRONTO: 0 alunos
  AV_PRIMARIO_x_AV_DESCOMPASSO: 41 alunos (40% do avatar primário)
  AV_PREMIUM_x_AV_AVANCADO_PRONTO: 34 alunos (premium é subgrupo do avançado pronto)
```

### 8 · Falsa precisão

❌ "23.2156% das respostas mencionam vendas"
✅ "23% das respostas mencionam vendas (147 de 633)"

Arredonde % a 1 casa decimal no máximo. Mais que isso simula precisão que a heurística não tem.

### 9 · Comparações de amostras sem contexto

❌ "Vendas caiu de 23.0% pra 23.2% — aumentou marginalmente"
✅ "Variação de 0.2pp está dentro da margem de erro com n=633. Estável."

Toda comparação precisa de **margem de erro estimada** ou pelo menos noção do que conta como mudança real.

## Quando reportar "não sei"

Há perguntas que a pesquisa não responde. **Diga isso explicitamente.**

```yaml
limitacoes_da_analise:
  - "Não há dado de idade — persona usa estimativa baseada em setor"
  - "Não há dado de renda atual — pirâmide financeira é declarativa"
  - "Não há dado de geografia além de 'Outro' — não dá pra mapear regiões"
  - "Cohort temporal cobre 9 dias — não captura comportamento de longo prazo"
```

## Auditoria final

Antes de entregar a análise, perguntas a fazer:

- [ ] Toda % tem n absoluto associado?
- [ ] Cada insight tem nível de confiança explícito?
- [ ] Vieses conhecidos estão reportados?
- [ ] Subgrupos pequenos (n<20) estão marcados como "indicativo"?
- [ ] Citações são literais, não inventadas?
- [ ] Sobreposições entre segmentos estão reportadas?
- [ ] Há seção `limitacoes_da_analise`?
- [ ] Persona narrativa está marcada como "construção interpretativa"?
- [ ] Precisão decimal não é falsa?
- [ ] Comparações de amostra têm contexto de margem de erro?

## Lembrete final

**É melhor entregar análise menor e honesta do que análise grande e enganosa.** Quando em dúvida, reporte o limite. O usuário sempre prefere saber o que NÃO sabe do que descobrir depois que estava sendo enganado.
