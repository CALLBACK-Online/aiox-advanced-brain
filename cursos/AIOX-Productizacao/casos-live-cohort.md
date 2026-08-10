---
type: reference
course: aiox-productizacao
status: canonical
canonical_scope: cursos/AIOX-Productizacao
source: síntese de lives Advanced (T2-aula-5, T1-aula-5) + padrões de campo; sem transcrição integral
tags: [curso, productizacao, casos, cohort]
---

# Casos live — Productização

Três vinhetas para enriquecer aulas e o capstone.  
**Não** substituem o Decision Pack; **alimentam** wedge, prova e veto.

Fontes históricas (fora deste curso, monoespaçado):  
`sinkra-hub/.../sources/TranscricaoT2/Aula5-T2.md`,  
`sinkra-hub/.../sources/transcricoesT1/aula-05-transcricao.md`.

---

## Caso 1 — “Era do serviço” (não do login SaaS)

**Aula âncora:** [01-service-as-software](aulas/01-service-as-software.md)

### Situação

O builder sonha com SaaS multi-tenant e dashboard. O comprador quer o **resultado** (aparecer, vender, operar) e muitas vezes **não usa** o login do produto.

### Decisão

Empacotar o **serviço produtivado** (job + prova + entrega), não a identidade “tenho um SaaS”.

### Portão

Você passa se consegue dizer em uma frase: *o que o cliente recebe sem precisar “morar” no seu app?*

### Veto

Não iniciar multi-tenant, billing e onboarding self-serve antes de 3 conversas com dor e baseline.

---

## Caso 2 — “Prova para técnico ≠ prova para comprador”

**Aula âncora:** [02-dor-e-roi](aulas/02-dor-e-roi.md)

### Situação

Demo rica: tokens, auditoria, arquitetura, “olha o sistema”. O stakeholder de negócio pergunta só: tempo, risco, dinheiro, prazo.

### Decisão

Separar **evidência de engenharia** (AE) de **evidência de valor** (Productização): baseline + hipótese + fórmula + o que ainda medir.

### Portão

ROI no pack tem premissas explícitas; “está otimizado” sozinho não conta.

### Veto

Não usar métricas só de dev (tokens, latência) como slide de venda sem traduzir para dor do cliente.

---

## Caso 3 — Brand Book / identidade sem confundir com oferta

**Aula âncora:** [01](aulas/01-service-as-software.md) · [04](aulas/04-caminhos-de-produto.md)  
**Ponte Design:** `cursos/AIOX-Design/` (Brand Book → tokens/contrato)  
**Ponte marca estratégica:** `squads/brand/` · Squads aula 13

### Situação

Live de Brand Book e engenharia reversa para DS (shadcn etc.). Identidade visual forte. Ainda não há wedge nem canal.

### Decisão

Brand Book **habilita** confiança e consistência; **não** substitui Decision Pack. Tradução visual → Design; posicionamento de marca → brand squad; monetização → este curso.

### Portão

No pack: anti-escopo “não vamos vender o DS como se fosse o produto, a menos que o wedge seja vender o DS”.

### Veto

Não chamar hormozi/copy só porque o brand book ficou bonito.

---

## Como usar

| Momento | Uso |
|---------|-----|
| Estudo | Ler o caso da aula âncora antes do exercício |
| Capstone | Citar qual caso se parece com o seu (A/B/C personas + 1/2/3 live) |
| Agent | “Critique meu pack: estou no Caso 1 (SaaS sem serviço)?” |

[FAQ de campo](FAQ-campo-cohort.md) · [Personas](personas-capstone.md) · [Projeto](Projeto-Integrador.md) · [⌂ Curso](README.md)
