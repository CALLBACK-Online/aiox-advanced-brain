# Anti-Patterns · armadilhas comuns na análise de pesquisa

Esses são os erros que matam análises de pesquisa. Aprendi todos eles fazendo no contexto AIOX/Alan. Universalizando.

## Os 10 piores anti-padrões

### 1 · Pular a Etapa 0 (calibração de contexto)

**Sintoma:** Você lê o CSV e já começa a calcular distribuições.

**Por que mata:** Análise sem decisão-alvo vira descritiva inútil. "62% querem X" não move ninguém.

**Como evitar:** Sempre pergunte primeiro: *o que você vai fazer com essa análise?* Onboarding? Venda? Pricing? Cada um pede análise diferente.

---

### 2 · Listar todas as variáveis sem hierarquizar

**Sintoma:** Output de 47 distribuições univariadas, todas com mesmo peso visual.

**Por que mata:** O leitor não sabe o que importa. Análise vira reference manual, não decisão.

**Como evitar:** Sempre ranqueie. As 3-4 distribuições que mudam decisão recebem destaque visual + interpretação. As outras vão pra apêndice ou nem aparecem.

---

### 3 · Inventar persona sem base estatística

**Sintoma:** "Maria, 32, gerente de marketing em São Paulo" — chutada do nada.

**Por que mata:** Persona inventada não conecta com os respondentes reais. Vira ficção genérica.

**Como evitar:** Persona só após L6 com célula quente clara. Nome inventado, mas idade/cidade/ocupação baseadas no setor dominante do subgrupo. Fala canônica destila 3-5 respostas reais.

---

### 4 · % sem n absoluto

**Sintoma:** "42% querem 100k+/mês"

**Por que mata:** "42% de 36 que escreveram número" é completamente diferente de "42% dos 726". A primeira é viés aspiracional, a segunda seria insight real.

**Como evitar:** Toda % vem com n. Regra inquebrantável.

---

### 5 · Promessa numérica como conclusão

**Sintoma:** "A turma quer faturar 100k/mês"

**Por que mata:** É wish do respondente que escreveu, não dado real sobre a turma. Confunde aspiração com diagnóstico.

**Como evitar:** Separe sempre `quem responde escreveu X` de `a turma quer X`. Reporte viés de aspiração explicitamente.

---

### 6 · Dashboard como objeto decorativo

**Sintoma:** Gráfico que ninguém olha 2 vezes. Insight que ninguém usa.

**Por que mata:** Confunde "bonito" com "útil". Gera trabalho descartável.

**Como evitar:** Pergunta pra cada gráfico: *qual decisão isso muda?* Se não muda decisão, retira.

---

### 7 · Análise temática por keywords sem inspeção prévia

**Sintoma:** Você define 12 temas baseado em chute, roda matching, reporta números.

**Por que mata:** Keywords mal escolhidas pegam contexto errado ("não vendi" classifica em vendas). Cobertura ruim. Temas mutuamente sobreponíveis.

**Como evitar:** Sempre **leia 30-50 respostas aleatórias antes**. Defina temas baseado no que VIU, não no que imagina.

---

### 8 · Inflar segmentos pequenos

**Sintoma:** "28 alunos premium representam o público high-ticket"

**Por que mata:** Subgrupo de 28 não sustenta estratégia. Margem de erro grande, viés provável.

**Como evitar:** Subgrupos com n<30 são **indicativos, não conclusivos**. Reporte como tal. Decisões de pricing/oferta não devem depender deles.

---

### 9 · Forçar todas as 8 camadas em todos os casos

**Sintoma:** NPS interno trimestral com persona narrativa + jornada emocional + frase de abertura.

**Por que mata:** Material irrelevante dilui o que importa. Tempo perdido.

**Como evitar:** Pule camadas conforme `./L1-L8_layers.md` indica. Análise se ajusta ao dataset, não o contrário.

---

### 10 · Identidade visual genérica

**Sintoma:** Dashboard com gradientes roxos de SaaS quando o usuário tem brandbook industrial.

**Por que mata:** O artefato visual deve REFORÇAR a marca da pessoa que vai apresentar. Genérico = não-pertencente.

**Como evitar:** Sempre pergunte sobre brandbook antes. Se não houver, use o editorial dark padrão (provado funcionar). Não chute paletas.

---

## Anti-padrões por camada

### Em L1 (Diagnóstico)
- Não reportar preenchimento de campos abertos antes de prometer análise temática
- Ignorar timestamps quando estão disponíveis (perde cohort analysis)

### Em L2 (Univariadas)
- Não dar IDs únicos às categorias (impossibilita L5 SQL-like)
- Pie chart com 7+ categorias (use horizontal bar ranqueada)

### Em L3 (Cruzamentos)
- Não procurar célula quente (perde o achado mais importante)
- Cruzar variáveis semanticamente sobrepostas (correlação artificial)

### Em L4 (Temática)
- Não validar cobertura (top tema com 4% indica temas mal definidos)
- Reportar como "análise NLP" quando é heurística por keyword

### Em L5 (Segmentação)
- Segmentos disjuntos quando na realidade sobrepõem
- Sem critério SQL-like (impossibilita reuso programático)

### Em L6 (Avatar)
- Forçar avatar quando distribuição é uniforme
- Persona com características fora do setor dominante (gerente de TI na agricultura — combina mal)

### Em L7 (Copy)
- Linguagem que vende "em geral", não específica do avatar
- Citações inventadas/parafrazeadas em vez de literais

### Em L8 (Visual)
- Forçar gráfico 3D ou animação ostentosa
- Não testar responsividade mobile
- Esquecer print-friendly (limita uso prático)

---

## Sintomas de análise problemática

Se você notar qualquer um desses, **pause e revise**:

- O output está enorme mas o usuário não sabe o que fazer com ele
- Insights são todos "alta" confiança — não há margem de erro
- Citações soam genéricas, podem ser de qualquer pesquisa
- Persona não tem nome próprio inventado ou tem características inconsistentes
- Dashboard tem 3+ cores saturadas
- KPIs sem n absoluto associado
- Análise temática com cobertura <70%
- Nenhuma seção de "limitações da análise"

---

## Lembrete final

A diferença entre análise útil e análise impressionante é grande. Análise útil é **menor, mais honesta, mais opinativa**. Análise impressionante é maior, mais cautelosa, mais descritiva.

Esta skill busca análise útil. Tudo aqui está orientado a isso.
