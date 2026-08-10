# Segment Archetypes · padrões reutilizáveis de segmentação

Catálogo de **arquétipos de segmento** que aparecem em quase toda pesquisa de público comercial. Use como **ponto de partida** em L5 — adapte os critérios ao dataset real.

## Como usar este catálogo

1. Após L1-L4, leia os critérios abaixo e identifique quais ARQUÉTIPOS o seu dataset suporta (precisa ter os campos correspondentes).
2. Para cada arquétipo aplicável, **adapte o critério SQL-like** aos nomes reais das colunas + categorias do seu dataset.
3. Calcule n absoluto e %.
4. Reporte sobreposições explicitamente (segmentos podem se sobrepor — é normal).
5. **Se o arquétipo não couber (ex: não há dado de tempo disponível), pule.** Não force.

## Princípio central

Cada segmento existe **se gera uma decisão diferente**. Se dois segmentos têm a mesma abordagem comercial, **mescle**. Se um segmento tem n<20, é **indicativo, não conclusivo** — reporte como tal.

---

## Arquétipo 1 · AV_PRIMARIO (ICP claro)

**Quando aparece:** Há célula quente em L3 (≥50% em uma linha + n≥50).

**Critério canônico:**
```sql
{perfil_aspiracional} = "{categoria dominante}"
AND {problema_central} = "{categoria dominante}"
```

**Como saber se é o primário:**
- É a célula com maior % em uma linha de cruzamento canônico
- Tem n absoluto ≥ 50 (sustenta narrativa)
- A combinação dos dois eixos faz sentido semântico (não é correlação artificial)

**Abordagem comercial:**
- Foco principal do pitch
- Headline e frase de abertura citam este avatar literalmente
- Recebe persona narrativa em L6

**Anti-padrão:** Forçar um avatar primário quando a distribuição é uniforme. Se nenhuma célula passa de 35-40%, **não há primário** — use só os outros segmentos.

---

## Arquétipo 2 · AV_PREMIUM (high-ticket)

**Quando aparece:** Há subgrupo pequeno com **alta capacidade + alta vontade**.

**Critério canônico:**
```sql
{perfil_negocio} = "Já tem negócio"
AND {ferramenta_tecnica} IN ("Claude Code", "{ferramenta avançada}")
AND {tempo_disponivel} >= "10h+"
```

**Características:**
- n geralmente pequeno (20-50 em pesquisa média)
- Não compra o produto entry-level — compra a oferta high-ticket
- Linguagem rejeitada: tudo aspiracional ("muda de vida"). Linguagem que vende: técnica e específica.

**Abordagem comercial:**
- Oferta paralela ao produto principal
- Não dilua o pitch principal pra agradá-los — tenha um upsell claro
- Email/WhatsApp dedicado pós-evento

**Anti-padrão:** Inflar para sustentar pricing premium. Se n<20, é **sinalização de mercado, não segmento operacional**.

---

## Arquétipo 3 · AV_AVANCADO_PRONTO (executores ativos)

**Quando aparece:** Subgrupo com capacidade técnica + negócio em andamento, mas que ainda não é premium.

**Critério canônico:**
```sql
{perfil_negocio} = "Já tem negócio"
AND {ferramenta_tecnica} = "{ferramenta avançada}"
```

**Características:**
- Sabem o que precisam, querem a solução, não a teoria
- Movem-se rápido quando o pitch é direto

**Abordagem comercial:**
- Hands-on demos, casos concretos
- Mostre o atalho, não o método completo
- Conversão alta com call-to-action específico

---

## Arquétipo 4 · AV_INICIANTE_ABSOLUTO

**Quando aparece:** Subgrupo sem ferramenta + pouco tempo + sem negócio.

**Critério canônico:**
```sql
{ferramenta_tecnica} = "Nunca usei"
AND {tempo_disponivel} <= "<2h"
```

**Características:**
- Risco real de **desconectar** durante o evento se o nível for alto demais
- Geralmente vieram por marketing aspiracional

**Abordagem comercial:**
- Não é o foco do pitch primário, mas precisa de **um acolhimento explícito** ("se você nunca usou X, esta sessão também serve pra você porque...")
- Produto de entrada (pré-curso, intro) é a oferta natural pra eles
- Se vc não tem produto de entrada, **não venda nada agressivamente** — gere goodwill

**Anti-padrão:** Ignorá-los. São maioria silenciosa em muitos lançamentos.

---

## Arquétipo 5 · AV_DESCOMPASSO (querem X mas não têm capacidade)

**Quando aparece:** Subgrupo com **alta vontade comercial** mas **baixa capacidade técnica/operacional**.

**Critério canônico:**
```sql
{problema_central} = "Vender com IA"
AND {ferramenta_tecnica} = "Só uso chat"
```

**Características:**
- Querem o resultado (vender), mas não têm a ferramenta pra produzir o que vão vender
- Subgrupo emocionalmente carregado — alta urgência, baixa capacidade
- Sobrepõe muito com AV_PRIMARIO (frequente: ~40% do primário também é descompasso)

**Abordagem comercial:**
- Nomear o descompasso **antes** do pitch ("Você quer vender, mas ainda não sabe construir. Vou te mostrar como resolver os dois.")
- Sequência educativa pré-venda + produto que cobre o gap técnico
- **Não** trate só com discurso comercial — eles vão sentir que falta substância

---

## Arquétipo 6 · AV_CONSTRUTOR_NO_CODE

**Quando aparece:** Subgrupo focado em **construir produtos** com ferramentas no-code/low-code.

**Critério canônico:**
```sql
{perfil_aspiracional} = "Construir sem programar"
AND {problema_central} = "Criar sites/apps/sistemas"
```

**Características:**
- Foco em **fazer**, não em vender
- Vocabulário próprio: "Lovable", "Bolt", "Cursor", "v0"
- Linguagem que afasta: tudo que sugere "marketing/copy/funil"

**Abordagem comercial:**
- Demos técnicas, screen-share, casos antes/depois
- Conteúdo orgânico do tipo "construí X em Y minutos"

---

## Arquétipo 7 · AV_ICP_OPERACIONAL (ICP de execução)

**Quando aparece:** Subgrupo que combina **dor + capacidade** suficiente pra executar.

**Critério canônico:**
```sql
{problema_central} = "{problema do produto}"
AND {tempo_disponivel} >= "5h+"
```

**Características:**
- Não é o mais sexy emocionalmente, mas é quem **executa**
- Conversão alta + retenção alta

**Abordagem comercial:**
- Pricing realista
- Estrutura de cohort/turma fechada
- Suporte com expectativa de resultado em 30-60 dias

---

## Arquétipo 8 · AV_INDECISO_EXPLORADOR

**Quando aparece:** Subgrupo que escreve respostas vagas, sem dor clara, sem objetivo claro.

**Critério (qualitativo):**
- Campos abertos com respostas <40 chars ou genéricas ("quero aprender", "saber mais", "ver como funciona")
- Nenhum problema dominante declarado

**Abordagem comercial:**
- **Não persegua agressivamente.** Eles vão decidir em 2-3 ciclos
- Conteúdo de nutrição (newsletter, podcast)
- Não diluir o pitch primário pra agradá-los

---

## Checklist de segmentação saudável

- [ ] 5-10 segmentos definidos (não menos, não mais)
- [ ] Cada um tem **ID curto único** (AV_*, usado consistentemente)
- [ ] Cada um tem **critério SQL-like** parametrizado, não prosa
- [ ] Cada um tem **abordagem comercial diferente** (se igual, mescle)
- [ ] **n absoluto reportado** em todos
- [ ] Subgrupos com n<20 marcados como "indicativo"
- [ ] **Sobreposições explícitas** reportadas (especialmente AV_PRIMARIO × AV_DESCOMPASSO)
- [ ] **AV_PRIMARIO definido OU explicitamente declarado ausente** (não inventar)

## Quando NÃO usar este catálogo

- Pesquisa de NPS interno (sem segmentação comercial)
- Survey de feature em SaaS (segmentação por uso da feature, não por avatar)
- Pesquisa acadêmica (segmentação metodológica diferente)

Nestes casos, **defina segmentos do zero** baseado nas variáveis do dataset, não force os arquétipos canônicos.

---

*Survey Intel · segment-archetypes v1.0*
