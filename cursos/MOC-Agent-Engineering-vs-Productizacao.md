---
tags: [hub, moc, layer/curso, agent-engineering, productizacao]
aliases: [AE vs Productização, Agent Engineering vs Productização, fronteira comercial]
---

# MOC — Agent Engineering × Productização

> Uma página para **não misturar** “como o agente funciona” com “como vira oferta”.

Vault: `00-HOME.md` · Hub: `cursos/README.md`

| Curso | Path | Dono de |
|-------|------|---------|
| **AIOX Agent Engineering** | `cursos/AIOX-Agent-Engineering/` | Capacidade agentic confiável, runtime, produção |
| **AIOX Productização** | `cursos/AIOX-Productizacao/` | Oferta, distribuição, formato e estágio de monetização |

---

## Pergunta-mestre

| Se a dúvida é… | Curso |
|----------------|--------|
| Como **construir / operar / provar** a capacidade? | Agent Engineering |
| Como **empacotar / distribuir / monetizar** o valor? | Productização |

```text
Agent Engineering
  capacidade com entrada, saída, runtime, gates e evidência
                 │
                 │ handoff (capacidade + prova)
                 ▼
AIOX Productização
  wedge → oferta/ROI → canal → formato → estágio
                 │
                 │ decisão fechada
                 ▼
Squads comerciais (copy / sales / hormozi) — operação, não julgamento
```

---

## O que **não** entra em Agent Engineering

| Tema | Por quê | Aula Productização |
|------|---------|-------------------|
| Service-as-Software / wedge | Empacotamento comercial | `aulas/01-service-as-software.md` |
| Dor, promessa, ROI auditável | Proposta de valor | `aulas/02-dor-e-roi.md` |
| Distribuição > produto | Canal e alocação de tempo | `aulas/03-distribuicao-vs-produto.md` |
| Consultoria → App → SaaS | Formato de entrega **comercial** | `aulas/04-caminhos-de-produto.md` |
| Interno → cliente → produto | Estágio de monetização | `aulas/05-estagios-de-monetizacao.md` |
| Decision Pack (capstone) | Decisão go/no-go de mercado | `aulas/06-capstone-decisao-de-productizacao.md` |

Seeds históricas (Advanced M11): 62–66 — dono canônico agora é Productização.

---

## O que **fica** em Agent Engineering

| Tema | Exemplos de aula AE |
|------|---------------------|
| Taxonomia task / skill / workflow / squad / runner | M0 |
| Research, prior-art, anatomy | M1 |
| Criar/adaptar squad (critério técnico) | M2 |
| Paralelismo, routing, waves | M3 |
| Harness, API, escada **técnica** de industrialização | M4 (`21`–`23`) |
| Deploy, CI/CD, readiness | M5 |

**Nuance:** a “escada progressiva” do AE amarra **maturidade de industrialização** (script → runner → API). A “escada comercial” (consultoria → SaaS, interno → produto) é **Productização**. Não são a mesma escada.

---

## Handoff mínimo (AE → Productização)

Só avance se conseguir preencher:

```yaml
capacidade:
  entrada: ""
  saída: ""
  usuário_atual: ""
  evidência: ""          # artefato ou métrica observável
  tempo_e_custo: ""
  falhas_conhecidas: []
  limites: []
```

Detalhe: `cursos/AIOX-Productizacao/ponte/agent-engineering.md`  
Espelho AE: `cursos/AIOX-Agent-Engineering/ponte/saida-para-productizacao.md`

Se o YAML não fecha → **volte à engenharia**. Se fecha → comece Productização pela aula 01 (wedge).

---

## Sinais para o agent-professor

| Frase do aluno | Rota |
|----------------|------|
| “Agente em loop / workflow / harness / deploy” | AE |
| “Como viro isso em serviço / oferta?” | Productização 01–02 |
| “Consultoria ou SaaS?” | Productização 04 |
| “Ninguém conhece meu produto” | Productização 03 |
| “Uso interno já conta como produto?” | Productização 05 |
| “Já decidi a oferta; quero copy/sales” | Squads 19–21 (`ponte/squads-comerciais.md`) |
| “UI feia / DESIGN.md” | AIOX Design (outra rota de aplicação) |

---

## Ordem na jornada do acervo

Agent Engineering, Productização, Design e Squads são **rotas de aplicação canônicas** depois do núcleo comum:

```text
Obsidian-IA → Arquitetura → Fundamentals → Advanced
                              ├─ Squads — especialistas publicados
                              ├─ Agent Engineering — capacidade em produção
                              ├─ Design — contrato visual
                              └─ Productização — oferta e mercado
Squads + operação real → Enterprise — vitrine de prontidão
```

Entrada típica em Productização: **depois** de ter capacidade + evidência (AE ou Advanced + prática real).

---

## Links rápidos

- Productização: `cursos/AIOX-Productizacao/README.md` · brief: `COURSE-BRIEF.md`
- FAQ de campo (cohort): `cursos/AIOX-Productizacao/FAQ-campo-cohort.md`
- Personas de capstone: `cursos/AIOX-Productizacao/personas-capstone.md`
- Agent Engineering: `cursos/AIOX-Agent-Engineering/README.md`
- Squads comerciais: `cursos/AIOX-Advanced-Squads/aulas/19-copy.md` …
- Hub: `cursos/README.md`
