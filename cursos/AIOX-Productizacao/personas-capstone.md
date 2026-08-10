---
type: reference
course: aiox-productizacao
status: canonical
canonical_scope: cursos/AIOX-Productizacao
source: padrões de campo cohort Advanced T1+T2, personas sintéticas (sem PII)
tags: [curso, productizacao, capstone, personas]
---

# Personas de capstone — Productização

Use **uma** persona se ainda não tiver capacidade real própria.  
São **compósitos** de padrões da cohort — não são pessoas reais.

Preencha o [Decision Pack](templates/decision-pack.md) como se fosse o seu negócio.  
Dados sensíveis: invente números **plausíveis** e marque como hipótese.

---

## Persona A — “Ops interno que virou máquina”

### Contexto

Dono de operação pequena/média. Migrar planilhas e rotinas manuais para fluxos AIOX (relatórios, follow-ups, ClickUp/Notion). A capacidade **roda todo dia** e economiza horas da equipe.

### Capacidade (entrada do curso)

| Campo | Valor sintético |
|-------|-----------------|
| Entrada | CSV/planilha semanal + regras de status |
| Saída | Relatório + tasks atualizadas no board |
| Evidência | 6 semanas rodando; ~8h/semana de trabalho manual a menos (hipótese medida por diário de tempo) |
| Falhas | Quebra quando coluna muda de nome; precisa de 1 revisão humana |

### Armadilha típica

Achar que “já montei na empresa” = produto SaaS multi-tenant.

### Foco do Decision Pack

- Estágio: **interno** (aula 05)  
- Wedge se for a mercado: “relatório operacional semanal sem caçar planilha” para **mesmo tipo de operação**, não “ERP com IA”  
- Formato default: **piloto/consultoria** (aula 04) até 3 conversas com pares  
- Experimento ≤14 dias: 5 conversas com donos de operação similar; métrica = reuniões agendadas + “pagaria por isso?”

### Aulas âncora

01 · 02 · 05 · 06

---

## Persona B — “Vitrine do primeiro sistema”

### Contexto

Builder em transição. Primeiro sistema “de verdade” para um conhecido/familiar ou caso próximo (ex.: operação no exterior, CRM de nicho). Objetivo misturado: **aprender** + **portfólio** + “talvez vender depois”.

### Capacidade

| Campo | Valor sintético |
|-------|-----------------|
| Entrada | Briefing de pedidos + planilha de clientes |
| Saída | Dashboard + rascunhos de proposta |
| Evidência | 1 protótipo usado por 1 usuário; 3 iterações em 2 semanas |
| Falhas | Design muda a cada geração; usuário ainda valida tudo manualmente |

### Armadilha típica

Precificar SaaS ou “produto global” com amostra N=1 e sem baseline de dor em reais/horas.

### Foco do Decision Pack

- Separar **aprendizado** de **wedge comercial**  
- Oferta de uma página para um ICP estreito (ex.: “agências de viagem com 50–200 leads/mês”), não “CRM para todos”  
- Se UI for o gargalo de confiança: desviar 1 sprint para `cursos/AIOX-Design/` (DESIGN.md), **sem** abandonar o experimento comercial  
- Formato: **consultoria de implantação** do fluxo, app só se 3 clientes pedirem o mesmo job

### Aulas âncora

01 · 02 · 04 · 06 (+ Design se necessário)

---

## Persona C — “Serviços densos virando pacote”

### Contexto

Consultor, mentor ou criador com **horas de material** (lives, PDFs, gravações) e vários serviços custom. Quer “productizar” e, em paralelo, pensa em squad de copy/conteúdo/hormozi.

### Capacidade

| Campo | Valor sintético |
|-------|-----------------|
| Entrada | Transcrições + pasta de aulas + briefing do cliente |
| Saída | Roteiro de diagnóstico + checklist de 30 dias + 1 deliverable semanal |
| Evidência | 4 clientes em 6 meses no modelo 100% custom; NPS alto; zero produto fixo |
| Falhas | Cada proposta reinventa o escopo; onboarding come 40% da margem de tempo |

### Armadilha típica

Acionar squad de copy/sales **antes** de escolher um wedge e provar dor; “mentoria + app + comunidade” no mesmo release.

### Foco do Decision Pack

- Inventário de jobs → **um** wedge (ex.: “diagnóstico de 7 dias com checklist acionável”)  
- ROI: horas de custom vs pacote fixo; baseline de tempo de proposta  
- Distribuição: 8 conversas com ex-leads da base (não só post em rede)  
- Formato: **serviço empacotado** agora; app/SaaS só com gate de repetição  
- Squads 19–21 só depois do pack aprovado pela [Rubrica](Rubrica.md)

### Aulas âncora

01 · 02 · 03 · 04 · 06 · [squads-comerciais](ponte/squads-comerciais.md)

---

## Como usar no Projeto Integrador

1. Escolha A, B ou C (ou o seu caso real — preferível).  
2. Complete os templates **sem** copiar a tabela acima como “fato” — adapte e marque hipóteses.  
3. Critique com o [AGENT-GUIDE](AGENT-GUIDE.md).  
4. Passe na [Rubrica](Rubrica.md).  
5. Execute o experimento no mundo real; registre perseverar / ajustar / matar.

## O que estas personas **não** são

- Briefing para inventar startup sem capacidade.  
- Licença para usar nomes ou dados da cohort.  
- Substituto de Agent Engineering (se a capacidade não roda, volte à engenharia).

[Projeto integrador](Projeto-Integrador.md) · [FAQ de campo](FAQ-campo-cohort.md) · [⌂ Curso](README.md)
