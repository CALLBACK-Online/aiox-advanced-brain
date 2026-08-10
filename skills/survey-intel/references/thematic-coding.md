# Thematic Coding · análise de respostas abertas

Como transformar 500+ respostas dissertativas em ranking de temas acionável.

## Quando usar

- **Sim:** Campos abertos com >100 respostas substantivas (>40 chars de média).
- **Não:** Campos abertos com <50 respostas, ou respostas todas curtas/genéricas.
- **Caso intermediário:** 50-100 respostas → fazer análise, mas reportar `confianca: media_baixa`.

## Método em 4 passos

### Passo 1 · Inspecionar amostra crua

Antes de qualquer codificação, leia 30-50 respostas aleatórias. **Não tente categorizar ainda.** Só observe:
- Que temas aparecem repetidamente?
- Que palavras-gatilho indicam cada tema?
- Há respostas vazias/genéricas demais ("nada", ".", "...")?

```python
import pandas as pd
df = pd.read_csv(path)

# Filtre substantivas
substantivas = df['campo_aberto'].dropna()
substantivas = substantivas[substantivas.str.len() > 40]

# Amostra aleatória
sample = substantivas.sample(min(40, len(substantivas)), random_state=42)
for s in sample:
    print(f"  → {s.strip()[:200]}")
```

### Passo 2 · Definir 8-12 temas candidatos

A partir da inspeção, defina temas com **keywords detectáveis**. Pra contextos de pesquisa de público de IA/negócios, esses são os 12 temas canônicos que tendem a aparecer:

```python
TEMAS_PUBLICO_IA_NEGOCIOS = {
    'Vendas / prospecção / clientes': ['vend', 'prospec', 'cliente', 'lead', 'capt', 'comercial', 'fech', 'negocia'],
    'Automação / processos repetitivos': ['automa', 'processo', 'repetitiv', 'manual', 'fluxo'],
    'Criação de conteúdo / criativos': ['conteúd', 'conteud', 'post', 'criativ', 'design', 'imagem'],
    'Tempo / produtividade': ['tempo', 'produtividade', 'rápid', 'demora', 'agilid'],
    'Criar sites / apps / sistemas': ['site', 'app ', 'aplicat', 'sistema', 'plataform'],
    'Conhecimento / aprender': ['conhecimento', 'aprender', 'entender', 'saber', 'clareza', 'passo a passo', 'começar'],
    'Escala / replicar': ['escala', 'escalar', 'replicar', 'multipl'],
    'Não tem negócio ainda': ['não tenho', 'nao tenho', 'sem negócio', 'comecando', 'iniciar', 'começando'],
    'Marketing / tráfego': ['marketing', 'tráfego', 'trafego', 'anúncio', 'anuncio', 'ads'],
    'Agentes IA / squads': ['agente', 'squad', 'crew', 'orquestr'],
    'Recursos / dinheiro': ['dinheiro', 'recurso', 'capital', 'investim', 'custo', 'orçament'],
    'Foco / organização': ['foco', 'organiz', 'gestão', 'gestao', 'rotina'],
}
```

**Para outros contextos**, adapte com keywords específicas do domínio:

| Domínio | Temas candidatos |
|---------|------------------|
| Saúde/Wellness | sintomas, peso, ansiedade, energia, alimentação, sono |
| Educação | nota, vestibular, profissão, dificuldade, professor, conteúdo |
| Finanças | dívida, investir, aposentadoria, salário, gasto, planejamento |
| E-commerce | conversão, abandono, frete, descrição, foto, anúncio |
| B2B SaaS | integração, time, métricas, churn, onboarding, scale |

### Passo 3 · Atribuir e contar

```python
def tag_response(text, temas):
    text_lower = text.lower()
    matched = []
    for tema, keywords in temas.items():
        if any(kw in text_lower for kw in keywords):
            matched.append(tema)
    return matched

# Aplicar
results = []
for resp in substantivas:
    tags = tag_response(resp, TEMAS_PUBLICO_IA_NEGOCIOS)
    results.append({'text': resp, 'tags': tags})

# Contar tema dominante (primeiro match) e múltiplos
from collections import Counter

dominante_count = Counter()
total_mentions = Counter()
for r in results:
    if r['tags']:
        dominante_count[r['tags'][0]] += 1
        for t in r['tags']:
            total_mentions[t] += 1

# Ranking por dominante
for tema, n in dominante_count.most_common():
    pct = 100 * n / len(substantivas)
    print(f"  {tema}: {n} ({pct:.1f}%)")
```

**Decisão importante:** Use `dominante` (primeiro match) para o ranking principal. `total_mentions` (qualquer match) pra mostrar sobreposição quando relevante.

### Passo 4 · Extrair citações canônicas

Pra cada tema top 5-7, extraia 3-5 citações literais que representem bem o tema:

```python
TOP_N_QUOTES = 5

for tema in dominante_count:
    matches = [r['text'] for r in results if r['tags'] and r['tags'][0] == tema]
    # Preferir tamanhos médios (60-200 chars) - mais "limpas"
    matches.sort(key=lambda x: abs(len(x) - 120))
    canonicas = matches[:TOP_N_QUOTES]
    
    print(f"\n{tema} ({len(matches)} respostas):")
    for c in canonicas:
        print(f"  • {c.strip()}")
```

## Critérios de qualidade

**Boa análise temática:**
- Cobre ≥80% das respostas substantivas (não deixa 30%+ "sem tema")
- Tema #1 tem ≥10% das respostas (concentração observável)
- Top 5 temas somam ≥60%
- Temas são mutuamente distinguíveis (sem ambiguidade entre eles)

**Análise temática problemática:**
- Top tema tem <8% → distribuição uniforme demais, talvez os temas estão mal definidos
- "Outros / não classificado" >30% → faltam temas
- Dois temas com >50% sobreposição → mesclar

## Reportagem honesta

Sempre incluir no output:

```yaml
analise_tematica:
  n_substantivas: 633
  n_classificadas: 581
  pct_cobertura: 91.8
  metodologia: "Heurística por palavras-chave, não NLP profundo"
  nivel_de_confianca: media
  observacao: |
    Análise por keywords pode confundir contexto (ex: "não vendi nada" 
    é classificado em vendas mas é negação). Para precisão maior, 
    considerar embedding clustering.
```

## Quando vale subir pra NLP profundo

Se o usuário pede precisão maior, considere:
- **Embeddings + clustering** (sentence-transformers + HDBSCAN)
- **Topic modeling** (BERTopic, especialmente bom pra português)
- **LLM-as-classifier** (passar cada resposta pra GPT/Claude classificar)

Reporte trade-off: NLP profundo é mais preciso mas leva 10-100x mais tempo e requer pipeline adicional. Heurística por keywords é boa o suficiente pra 90% dos casos de pesquisa de público (<2000 respostas).

## Anti-padrões

- **Não use stemming agressivo** ("venda" → "vend") sem testar — pode pegar "vendaval", "vendados", etc.
- **Não force "outros / não classificado" como tema.** É reporting honesto, não tema.
- **Não invente citações.** Use só o que está literal nas respostas. Pode normalizar pontuação, não conteúdo.
- **Não traduza tema pra inglês** se o público é PT-BR. As keywords precisam casar com o idioma das respostas.
