# Dashboard Design · sistema visual padrão + adaptação a brandbooks

Como construir o dashboard HTML standalone que materializa a análise.

## Princípio central

**O dashboard é um instrumento de decisão, não um relatório técnico.** Cada gráfico precisa responder a uma pergunta acionável. Se não responde, retira. Cada KPI precisa ter consequência. Se não tem, retira.

## Estética padrão (quando NÃO há brandbook fornecido)

**Editorial dark editorial.** Provado funcionar pra dados, gera autoridade visual, combina com screen share em Zoom.

### Tokens base

```css
:root {
  /* Surfaces */
  --bg: #0F0E0C;          /* canvas */
  --bg-soft: #1A1815;     /* secondary surface */
  --bg-card: #232019;     /* card */
  
  /* Text */
  --ink: #F5F1E8;         /* primary text - warm cream */
  --ink-soft: #B8B0A0;    /* secondary */
  --ink-mute: #7A7466;    /* tertiary / labels */
  
  /* Accent - escolha UMA cor */
  --accent: #E8A33D;      /* amber editorial */
  --hot: #D85A30;         /* warning/critical */
  --cool: #5D9B8C;        /* informational */
  
  /* Lines */
  --line: rgba(245, 241, 232, 0.08);  /* hairline */
}
```

### Tipografia padrão

```css
/* Display (h1, h2, números grandes) */
font-family: 'Fraunces', serif;
font-weight: 400;
font-style: italic;  /* opcional, dá caráter editorial */
letter-spacing: -0.03em;

/* Body */
font-family: 'Manrope', system-ui, sans-serif;
font-weight: 400;
line-height: 1.65;

/* HUD labels, números, mono */
font-family: 'JetBrains Mono', ui-monospace, monospace;
font-size: 0.65rem;
letter-spacing: 0.12em;
text-transform: uppercase;
```

### Componentes padrão

- **KPI grid** — 4 colunas, números grandes em display, label em mono uppercase, sub-info em sans
- **Chart cards** — fundo `--bg-card`, hairline border, padding generoso (28-32px)
- **Quotes** — italic em serif, border-left de 2px na cor do acento
- **Heatmaps** — células com gradiente de alpha no acento (0.10 a 0.80)

### Regras de ouro

1. **Hairline borders** (`rgba(255,255,255,0.08)`), não fills sólidos
2. **Sem drop shadows externos** — só inset rings em hover (`box-shadow: inset 0 0 0 1px`)
3. **Sem gradients meshy, sem glassmorphism**
4. **Square components por default** — pode arredondar cards (12px) mas não botões/inputs
5. **Acento usado com economia** — máximo 20% do espaço visual

## Adaptação a brandbook fornecido

Quando o usuário fornece um brandbook (CSS vars, design tokens, identidade), **substituir os tokens base** mas manter a **estrutura semântica**.

### Mapeamento canônico

| Token genérico | Equivalente no brandbook |
|----------------|--------------------------|
| `--bg` | canvas/background/surface escuro |
| `--bg-card` | surface elevada |
| `--ink` | primary text |
| `--accent` | primary accent (cor de marca) |
| `--font-display` | display/heading font |
| `--font-mono` | mono/HUD font |

### Estrutura semântica que NÃO muda

Mesmo com brandbook diferente, manter:
- Hero com KPIs lado a lado
- ToC sticky no topo
- Seções numeradas (01, 02, 03...)
- Chart cards em grid
- Heatmaps de cruzamento
- Footer com metadados

### Como inferir brandbook do usuário

Se o usuário cola design.md, frontmatter YAML, ou screenshots do brandbook:

1. Extrair as cores principais (canvas, surface, accent, text)
2. Extrair tipografia (display, sans, mono)
3. Identificar geometria (rounded vs square)
4. Identificar densidade (compacto vs amplo)
5. Identificar acentos especiais (glow, hover states)

Se o usuário NÃO fornece brandbook mas tem marca conhecida, **pergunte** antes de inferir. Não chutamos identidade visual.

## Estrutura canônica do dashboard

```
1. Top nav (sticky)
   - Brand glyph
   - Título do briefing
   - ToC clicável (atalhos pras seções)
   - Status live (n total)

2. Hero
   - Tag de contexto (mono, com border)
   - H1 grande (display, 3 linhas máx)
   - Subtítulo (sans, 1-2 linhas)
   - Stats panel à direita (4 números-chave)

3. Seção 01 · Overview
   - 4 KPIs principais
   - 2-3 gráficos univariados (donut, barras horizontais)
   - 1 chart "amplo" se houver análise temática (barras verticais ou horizontais com 10+ categorias)

4. Seção 02 · Cruzamentos
   - 1-2 heatmaps (perfil × problema, setor × problema)
   - Cada heatmap com note interpretativa abaixo

5. Seção 03 · Segmentos
   - Grid 2x3 ou 2x4 de cards de segmento
   - Cada card: ID, n absoluto, %, nome, critério em mono, abordagem

6. Seção 04 · Avatar primário (SE houver)
   - Card destacado com border lime/accent
   - Tag "AVATAR PRIMÁRIO"
   - Stats do avatar específico (4 mini-KPIs)
   - Persona card (avatar + nome + idade + fala + 4 quadrantes)

7. Seção 05 · Dores ranqueadas
   - Lista vertical com numeração grande
   - Cada item: dor, intensidade, descrição, citação canônica

8. Seção 06 · Sinais emocionais (se houver L4 robusta)
   - Grid 2x3 ou 3x2
   - Cada signal: número de menções, nome, descrição

9. Seção 07 · Pirâmide de ambição (SE houver dados financeiros)
   - 3 linhas (nível 1, 2, 3)
   - Cada linha: faixa, título, descrição, uso recomendado (allow/deny)

10. Seção 08 · Jornada emocional (SE contexto for venda)
    - 5 cards horizontais (estágios 1-5)
    - Card 3 destacado (momento de inscrição)
    - Insight crítico abaixo

11. Seção 09 · Arquétipos (SE houver)
    - Grid 3x2
    - Cada arquétipo: ID, nome, citação canônica, "como falar"

12. Seção 10 · Citações ouro
    - Grid 2 colunas
    - Cada citação: texto em italic, tag em mono

13. Seção 11 · Glossário linguagem
    - 2 colunas (vende vs afasta)
    - Cor verde/teal pra vende, vermelho/coral pra afasta

14. Seção 12 · Frase de abertura
    - Card destacado com border de cor de acento
    - Texto em display, citações específicas em accent
    - Rationale embaixo

15. Seção 13 · Gatilhos × objeções
    - 2 colunas com listas

16. Seção 14 · Aquisição (SE houver UTM)
    - Grid 3 colunas (canal 1, canal 2, sem-utm)
    - Cohort temporal abaixo (barras dia a dia)

17. Seção 15 · Insights (8 numerados)
    - Grid 2x4
    - Cada insight: ID, título, evidência

18. Seção 16 · Estratégia
    - Lista vertical com 3 movimentos

19. Seção 17 · Roteiro (SE evento ao vivo)
    - Blocos timestamped
    - Cada bloco: tempo grande, título, descrição, target

20. Footer
    - Citação grande (display)
    - Metadados (n, versão, data, preparado para)
```

**Adapte conforme o caso.** Não force seções que o dataset não pede.

## Chart.js · configuração padrão

```javascript
Chart.defaults.font.family = "'Manrope', system-ui, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#B8B0A0';

// Tooltip padrão
{
  backgroundColor: '#1A1815',
  borderColor: 'rgba(245,241,232,0.1)',
  borderWidth: 1,
  padding: 12,
  titleFont: { family: "'JetBrains Mono', monospace", size: 10 },
  bodyFont: { family: "'JetBrains Mono', monospace", size: 11 }
}

// Grid lines
grid: { color: 'rgba(245, 241, 232, 0.05)', drawBorder: false }
```

## Responsividade

Mobile fallback obrigatório:
- KPI grid 4 colunas → 2 colunas
- Chart grids 2-3 colunas → 1 coluna
- Heatmaps com `overflow-x: auto`
- Top nav: esconder ToC clicável
- Hero stats: stack vertical

## Print-friendly

CSS específico:
```css
@media print {
  body { background: white; color: black; }
  section { page-break-inside: avoid; padding: 30px 0; }
  .top-nav { position: relative; }  /* tira sticky */
}
```

Permite usuário gerar PDF do dashboard via Ctrl+P.

## Carregamento de assets

**Mínimo necessário:**
- Chart.js via CDN (cdnjs.cloudflare.com)
- Google Fonts pra tipografia (Manrope, Fraunces ou equivalentes, JetBrains Mono)

**Evitar:**
- Frameworks JS (React, Vue) — overhead desnecessário pra dashboard estático
- Bibliotecas de UI (Bootstrap, Tailwind) — escrever CSS direto é mais limpo
- Imagens externas — tudo SVG inline ou CSS puro

## Anti-padrões visuais

1. **Múltiplas cores saturadas** — gera ruído. Use 1 acento + grays + 1 cor de warning/critical.

2. **Pie charts com >5 categorias** — vira ilegível. Use barras horizontais ranqueadas.

3. **Heatmap com gradient rainbow** — confunde. Use gradient de alpha do acento.

4. **Gráficos 3D** — sempre piores que 2D pra leitura. Banir.

5. **Animações exageradas** — distraem da informação. Transitions sutis (`0.2s ease`) só em hover.

6. **Densidade visual exagerada** — espaçamento generoso (32-48px padding em cards) > apertar tudo.

7. **Tipografia decorativa em corpo de texto** — display só pra h1/h2/números. Body sempre sans legível.

8. **Emojis nos dados** — visualmente ruidoso, age datas o material, sinaliza falta de profissionalismo.

## Checklist final do dashboard

- [ ] Todas as seções têm headline + intro + componente visual?
- [ ] Cada KPI tem n absoluto + contexto?
- [ ] Cada gráfico tem título + sub (mono) + chart?
- [ ] Heatmap tem nota interpretativa abaixo?
- [ ] Avatar primário tem persona card narrativa?
- [ ] Citações estão em italic, atribuídas via tag?
- [ ] Frase de abertura está destacada visualmente?
- [ ] Footer tem metadados (n, versão, data)?
- [ ] Responsivo testado em <900px?
- [ ] Print-friendly?
- [ ] Sem dependências externas além de Chart.js + fontes?
