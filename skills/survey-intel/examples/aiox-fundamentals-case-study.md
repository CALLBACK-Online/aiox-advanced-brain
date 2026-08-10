# Exemplo · caso AIOX Fundamentals (referência)

Este é o caso real que originou a skill. Use como referência para entender como as 8 camadas se aplicam na prática.

## Contexto

- **Cliente:** Alan Nicolas (Academia Lendária, AIOX)
- **Decisão-alvo:** Masterclass de venda do AIOX Fundamentals via Zoom
- **Dataset:** Pesquisa pré-aula (Google Forms)
- **Janela temporal:** 2 amostras (n=574 → n=726)
- **Brandbook fornecido:** AIOX cockpit (dark, kinetic limon, square components)

## Como cada camada se aplicou

### L1 · Diagnóstico

```yaml
n_total: 726
campos_categoricos: 4
campos_abertos: 3 
campos_meta: [email, utm_source, submitted_at]
preenchimento: 87.2%
qualidade: alta
janela_temporal: "2026-05-05 a 2026-05-13"
dia_de_pico: "2026-05-11 (515 = 71%)"
```

### L2 · Univariadas (KPI principais)

- Perfil: Construir s/ programar 251 (34.6%), Já tem negócio 191, Mudar carreira 187, Tarefas repetitivas 97
- Problema: **Vender IA 227 (31.3%)**, Sites/apps 165, Automatizar 136, Agentes 125, Conteúdo 73
- Tempo: 2-5h 285 (39.3%), +10h 158, <2h 146, 5-10h 137
- Ferramentas: **Claude Code 347 (47.8%)**, Só chat 277, Lovable 47, N8N 36, Nunca 19

### L3 · Cruzamentos · CÉLULA QUENTE

```
Mudar de carreira × Vender IA = 103 alunos (55%) ← CÉLULA QUENTE
```

Esse achado virou o ICP do produto e o avatar primário em L6.

### L4 · Análise temática · 633 respostas abertas

Top temas:
1. **Vendas / prospecção (23.2%)** — quase 4x maior que conhecimento técnico (6.2%)
2. Automação / processos (17.2%)
3. Conteúdo / criativos (10.0%)

**Insight derivado:** A dor da turma não é técnica, é comercial. Mudou todo o roteiro da masterclass.

### L5 · 7 segmentos acionáveis

```yaml
- AV_PRIMARIO: 103 (mudar carreira + vender IA)
- AV_PREMIUM: 34 (já negócio + Claude Code + 10h+)
- AV_AVANCADO_PRONTO: 119 (já negócio + Claude Code)
- AV_INICIANTE_ABSOLUTO: 93 (sem ferramenta + pouco tempo)
- AV_DESCOMPASSO: 82 (quer vender mas só chat)
- AV_CONSTRUTOR_NO_CODE: 102 (construir + sites/apps)
- AV_ICP_OPERACIONAL: 116 (vender + 5h+)
```

### L6 · Avatar primário em profundidade

**Persona "Rafael Costa"** — composição estatística dos 103:
- 34 anos (mediana implícita do segmento)
- Analista de operações (setor "Outro" + perfil mudar de carreira)
- Interior de SP (inferência razoável)
- 53% usa Claude Code (sub-distribuição do segmento)
- 58% tem 5h+/semana
- 71% veio de wa-grupo

**Jornada emocional em 5 estágios:** Sufocamento → Descoberta caótica → **Frustração (estágio de inscrição)** → Decisão → Compromisso.

**4 dores ranqueadas:**
1. Não sabe vender (crítica, 40%+)
2. Falta método (alta, ~20%)
3. Falta capital (média, ~8%)
4. Insegurança técnica residual (baixa, ~5%)

### L7 · Inteligência aplicada

**Frase de abertura otimizada:**
> "Tem 103 pessoas aqui hoje que mudaram de carreira pra trabalhar com IA — e a maior dificuldade não é entender Claude Code. É vender. Você sabe construir, mas não sabe quem é seu cliente, quanto cobrar, ou como começar a conversa. Eu vou falar pra vocês primeiro. Os outros 623 também vão aprender, mas hoje a porta de entrada é a sua."

**Linguagem que vende (top 5):**
- "Primeiro cliente em 30 dias"
- "Método pra prospectar"
- "Sair da CLT com previsibilidade"
- "Cobrar pelo que você entrega"
- "Saber o que vender"

**Linguagem que afasta (top 5):**
- "Fique milionário com Claude Code"
- "Trabalhe 4 horas por semana"
- "Sem esforço, sem código"
- "100k/mês" como promessa
- "private enterprise distribution" sem contexto

### L8 · Materialização

- Dashboard HTML standalone (17 seções, brandbook AIOX cockpit aplicado)
- Markdown estruturado v2.1 (12 seções, frontmatter YAML extensivo, prompts-template)
- Versionamento explícito (v1.0 → v2.0 → v2.1)

## Lições do caso

### O que funcionou

1. **Calibrar contexto na Etapa 0** salvou horas. Saber que era "masterclass de venda" definiu que a análise precisava chegar até L8.

2. **Procurar célula quente em L3 ativamente** foi o achado mais valioso. 103 alunos não apareceram na média — só no cruzamento.

3. **Citações literais > síntese parafraseada.** A frase "tem muito barulho de hypezinho nessa merda" sozinha desarma céticos melhor que qualquer paráfrase.

4. **Validar estabilidade entre amostras** quando a segunda chegou. Variações ≤1.3pp confirmaram que a análise qualitativa era robusta.

5. **Brandbook aplicado ao final** funcionou — a estrutura semântica das seções foi reusada, só os tokens visuais mudaram.

### O que poderia ter sido melhor

1. **Pular L4 inicialmente** foi engano — voltei depois pra extrair os temas das respostas abertas. Devia ter feito desde a primeira passada.

2. **Não pedir brandbook na Etapa 0** atrasou o output visual. Pra próximas, vou perguntar antes de gerar HTML.

3. **Cohort temporal e UTM** só foram analisados quando a segunda amostra chegou com esses campos. Era pra ter pedido na primeira.

## Como adaptar pra outros contextos

| Caso | Diferenças relevantes |
|------|----------------------|
| **Pesquisa de NPS de SaaS** | Pular L6-L7 (não tem avatar primário, não tem venda) |
| **Lançamento de curso (diferente de masterclass)** | Mesmas 8 camadas |
| **Pesquisa de mercado pra investidor** | Pular L7 (sem copy), L8 vira pitch deck |
| **Onboarding cohort fechado** | L1-L6 sem L7 (não há copy de venda) |
| **Survey de feature em SaaS** | Pular L6, L7 (não há avatar de venda) |

A estrutura se ajusta. O método não.
