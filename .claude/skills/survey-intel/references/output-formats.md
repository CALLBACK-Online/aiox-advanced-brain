# Output Formats · estruturas canônicas de markdown e HTML

Como entregar a análise final em formato consumível.

## Markdown estruturado (briefing.md)

Otimizado para 2 usos: **injeção em Projects como contexto base** e **consumo por LLM via Claude Code**.

### Frontmatter YAML obrigatório

```yaml
---
documento: "Nome descritivo da análise"
versao: "X.Y"
autor_analise: "Claude (Anthropic)"
preparado_para: "Nome do usuário"
data_analise: "YYYY-MM-DD"
fonte: "Descrição da fonte (Google Forms, Typeform, etc)"

dataset_atual:
  n_total: número
  n_substantivas_aberto: número
  preenchimento_geral: porcentagem
  janela_temporal: "YYYY-MM-DD a YYYY-MM-DD"

uso_primario:
  - injecao_em_projects_claude_como_contexto_base
  - geracao_automatizada_via_claude_code
  - apresentacao_humana

niveis_de_navegacao:
  - L1_overview: "seções 1-3"
  - L2_avatar: "seção 4"
  - L3_segmentos: "seção 5"
  - ...

aviso_de_uso:
  - "Citações entre aspas são literais - não inventar variações"
  - "Toda % vem com n absoluto"
  - "Avatar primário é o ICP - referência central"
---
```

### Estrutura de seções numeradas

```markdown
# Título da análise

## Resumo executivo de uma frase

[Síntese em 1-2 frases com o achado central]

---

## 1. Visão estatística

### 1.1 Dataset
[YAML estruturado]

### 1.2 Distribuições principais (KPIs)
[YAML por campo categórico]

---

## 2. Cruzamentos analíticos

### 2.1 Perfil × Problema (matriz)
[Markdown table com célula quente em **negrito**]

### 2.2 [Outros cruzamentos relevantes]
[Idem]

---

## 3. Análise temática (se houver)

[YAML ranking de temas com n_aprox e pct]

---

## 4. AVATAR PRIMÁRIO (se houver célula quente)

[Estrutura completa de L6 - vide L1-L8_layers.md]

---

## 5. Outros segmentos acionáveis

[YAML de segmentos com ID, critério, n, abordagem]

---

## 6-7-8 · Inteligência aplicada (se contexto for venda)

- Glossário linguagem (vende vs afasta)
- Banco de citações tageado
- Frase de abertura otimizada

---

## 9 · Prompts-template pra Claude Code

[Markdown blocks com cada prompt nomeado e parametrizado]

---

## 10 · Insights táticos numerados

[Cada um: id, título, evidência, confiança, implicação]

---

## 11 · Limitações e notas metodológicas

[Lista honesta de vieses e níveis de confiança]
```

### Tags semânticas em citações

Sempre acompanhar citações de tags pra busca dirigida:

```yaml
banco_citacoes:
  por_tag:
    "#dor_X":
      - "..."
    "#aspiracao_Y":
      - "..."
```

### Changelog ao final

Sempre versionar mudanças:

```yaml
versoes:
  v1_0:
    data: "..."
    n: 574
    descricao: "Análise inicial"
  v2_0:
    data: "..."
    n: 726
    descricao: "Nova amostra + análise UTM"
```

---

## Dashboard HTML standalone

Vide `./dashboard-design.md` para sistema visual completo.

### Estrutura mínima

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{TITULO}</title>
  
  <!-- Fontes via Google Fonts ou CDN -->
  <link href="..." rel="stylesheet">
  
  <!-- Chart.js -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
  
  <style>
    /* Tokens CSS */
    :root { /* ... */ }
    
    /* Reset */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    /* Componentes */
    /* ... */
    
    /* Responsive */
    @media (max-width: 900px) { /* ... */ }
    
    /* Print */
    @media print { /* ... */ }
  </style>
</head>
<body>

  <!-- Top nav sticky -->
  <nav class="top-nav">...</nav>
  
  <!-- Hero com KPIs -->
  <section class="hero">...</section>
  
  <!-- Seções numeradas -->
  <section id="overview">...</section>
  <section id="cruzamentos">...</section>
  <!-- ... -->
  
  <!-- Footer -->
  <footer>...</footer>
  
  <!-- Chart.js initialization -->
  <script>
    (function(){
      // Charts setup
    })();
  </script>
</body>
</html>
```

### Requisitos não-negociáveis

1. **Standalone** — funciona offline (exceto fontes/Chart.js via CDN)
2. **Single file** — todo HTML/CSS/JS no mesmo arquivo
3. **Responsivo** — funciona em mobile
4. **Print-friendly** — CSS print incluído
5. **Sem dependências de framework** — vanilla CSS/JS
6. **Acessibilidade básica** — `<canvas role="img" aria-label="...">`

### Naming convention dos arquivos

```
{contexto}_{tipo}_{versao}.{ext}

Exemplos:
  pesquisa_aulax_briefing_v2_1.md
  pesquisa_aulax_dashboard_v2_1.html
  lancamento_2026_briefing_v1_0.md
```

---

## Notebook Python (opcional)

Quando o usuário pede pra reproduzir/auditar, gere também:

```python
"""
Análise de pesquisa - {CONTEXTO}
Versão: {VERSAO}
Data: {DATA}
N: {N}

Reproduz os números do briefing.
"""

import pandas as pd
from collections import Counter

# === L1: Diagnóstico ===
df = pd.read_csv("path/to/data.csv")
print(f"Total: {len(df)}")
# ...

# === L2: Univariadas ===
# ...

# === L3: Cruzamentos ===
# ...

# === L4: Temática (se aplicável) ===
TEMAS = { ... }
# ...

# === L5: Segmentos ===
segmentos = {
    'AV_PRIMARIO': df[(df['perfil'] == '...') & (df['problema'] == '...')],
    # ...
}
for nome, sub in segmentos.items():
    print(f"{nome}: {len(sub)} ({100*len(sub)/len(df):.1f}%)")
```

---

## Quando entregar qual artefato

| Cenário | Artefatos |
|---------|-----------|
| Apresentação humana | Dashboard HTML |
| Reuso por LLM | Markdown estruturado |
| Auditoria/reprodutibilidade | Notebook Python |
| Lançamento completo | Todos os 3 |
| NPS interno rápido | Só notebook ou só YAML |

**Default:** Markdown + Dashboard. Se o usuário não especificar, entregar os dois.

---

## Versionamento

Toda análise nova versiona:

- **v1.0:** análise inicial
- **v1.1:** correções menores, mesmo dataset
- **v2.0:** nova amostra com recalculação
- **v3.0:** mudança de método ou nova decisão-alvo

Reporte explicitamente no frontmatter e changelog.
