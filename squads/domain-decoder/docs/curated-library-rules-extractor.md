# Biblioteca Curada — Squad "Rules Extractor"

> **Curadoria > Volume.** De ~60 livros pesquisados por 7 agentes em paralelo, selecionados os OURO para cada mind, alinhados ao workflow do squad.
>
> Pesquisa realizada em: 2026-02-18
> Metodologia: Deep Research paralela (7 agentes, WebSearch + WebFetch), classificacao ouro/bronze por relevancia para extracao de regras de negocio de sistemas legados.

---

## Contexto do Squad

```
DIAGNOSTICO (Tier 0: Ross + Evans)
  → "Que tipo de regra e essa? De qual dominio/contexto?"
EXTRACAO (Tier 1: Feathers + von Halle)
  → "Como entro nesse codigo legado? Como modelo a logica encontrada?"
FORMALIZACAO (Tier 2: Taylor + Fowler)
  → "Qual a decision table correta? Em que padrao de arquitetura vive?"
EXPRESSAO (Tier 3: Witt)
  → "Como escrevo isso sem ambiguidade?"
VALIDACAO (Tool: SBVR)
  → "A documentacao esta completa e padronizada?"
```

---

## TIER 0 — Fundacao & Diagnostico

### 1. Ronald G. Ross — "O pai das business rules"

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 1 | **Principles of the Business Rule Approach** | 2003 | Addison-Wesley | RuleSpeak completo (Cap. 8-12), taxonomia de regras (Cap. 10), teoria formal (Cap. 15-18) |
| 2 | **Building Business Solutions** (2nd ed.) — com Gladys Lam | 2015 | Business Rule Solutions | DecisionSpeak + Q-Charts (UNICOS neste livro), metodologia hands-on. IIBA Sponsored. |
| 3 | **Business Rule Concepts** (4th ed.) | 2013 | Business Rule Solutions | SBVR para practitioners, visao geral do ecossistema inteiro, ISBN 978-0-941049-14-6 |
| 4 | **Business Knowledge Blueprints** (2nd ed.) | 2020 | Business Rule Solutions | ConceptSpeak, concept models, vocabulario formal SBVR, ISBN 978-0-941049-17-7 |

**Mapeamento Framework → Livro:**

| Framework | Fonte Primaria | Fonte Secundaria | Recurso Gratuito |
|---|---|---|---|
| RuleSpeak | Principles (2003), Cap. 8-12 | Business Rule Concepts (2013) | RuleSpeak.com + Tabulation Primer (16pp) |
| DecisionSpeak | Building Business Solutions (2015) | Artigos BRJ (2011) | Decision Analysis Primer (49pp) |
| Q-Charts | Building Business Solutions (2015) | Artigos BRJ (2010, 2013) | Decision Analysis Primer (49pp) |
| SBVR | Business Knowledge Blueprints (2020) + Business Rule Concepts (2013) | BRG papers | BRG "Defining Business Rules" paper (free PDF) |
| Taxonomia de Regras | The Business Rule Book (1994/1997) + Principles (2003) Cap. 10 | Business Rule Concepts (2013) | Business Rules Manifesto (free, 18 linguas) |

**Recursos gratuitos OURO:**
- Decision Analysis Primer (49pp) — DecisionSpeak + Q-Charts completo
- TableSpeak Primer (121pp) — decision tables
- Business Rules Manifesto (2003) — 24 principios fundamentais
- BRG Paper "Defining Business Rules" (PDF gratuito)

---

### 2. Eric Evans — DDD

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 5 | **Domain-Driven Design: Tackling Complexity in the Heart of Software** | 2003 | Addison-Wesley | Ubiquitous Language (Cap. 2), Bounded Context (Cap. 14), Strategic Design (Cap. 14-17), Context Mapping (Cap. 14) |
| 6 | **DDD Reference** (FREE PDF) | 2014 | Dog Ear Publishing | Versao refinada por Evans apos decada de pratica. 75pp. CC license. |

**ISBN Blue Book:** 978-0321125217 (560pp)
**DDD Reference PDF:** domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf

**Capitulos criticos do Blue Book para extracao de regras:**
- Parte I, Cap. 2: Ubiquitous Language — framework para vocabulario compartilhado
- Parte IV, Cap. 14: Bounded Context + Context Mapping — fronteiras jurisdicionais das regras
- Parte IV, Cap. 15: Distillation — Core Domain vs Generic Subdomains (ONDE regras importam)
- Cap. 14: Anti-Corruption Layer — padrao arquitetural para extracao

---

## TIER 1 — Masters

### 3. Michael Feathers — Legacy Code

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 7 | **Working Effectively with Legacy Code** | 2004 | Prentice Hall | Characterization Tests (Cap. 13), Seam Model (Cap. 4), 24 Dependency-Breaking Techniques (Cap. 25) |

**ISBN:** 978-0131177052 (464pp)

**Frameworks extraiveis:**
- **Characterization Tests** (Cap. 13): Testes que documentam O QUE o codigo faz (nao o que deveria). "Quando a spec oficial difere do comportamento observado, va com o comportamento."
- **Seam Model** (Cap. 4): "Um seam e um lugar onde voce pode alterar comportamento sem editar naquele lugar." 3 tipos: Preprocessing, Link, Object.
- **24 Dependency-Breaking Techniques** (Cap. 25): Adapt Parameter, Break Out Method Object, Extract Interface, Subclass and Override Method, etc.
- **Legacy Code Change Algorithm**: Identify change points → Cover with characterization tests → Make changes → Refactor
- **Sensing vs Separation** (Cap. 3): Duas razoes para quebrar dependencias
- **Scratch Refactoring** (Cap. 16): Refatorar para entender, depois descartar
- **Pinch Points** (Cap. 12): Pontos estreitos no grafo de dependencias

---

### 4. Barbara von Halle — The Decision Model

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 8 | **The Decision Model** — com Larry Goldberg | 2009 | Auerbach/CRC Press | 15 Principios Formais (7 estruturais, 3 declarativos, 5 integridade), Decision Model Normal Forms, Inferential Keys |
| 9 | **Business Rules Applied** | 2001 | John Wiley & Sons | Metodologia pratica 6 fases, Rule Track, taxonomia de regras, ISBN 978-0471412939 |

**ISBN The Decision Model:** 978-1420082814

**15 Principios do TDM (estrutura):**
- Principios Estruturais (1-7): Forma visual e organizacao (Tabular, Row, Connection)
- Principios Declarativos (8-10): Independencia tecnologica
- Principios de Integridade (11-15): Integridade estrutural, logica e de negocio

**Decision Model Normal Forms (analogas a normalizacao relacional):**
- 1NF: Logica de negocio atomica (obrigatorio)
- 2NF: Remove fact types de condicao irrelevantes
- 3NF: Remove dependencias transitivas entre condicoes
- 4NF/5NF: Descobertos em 2013 (coluna TDAN, nao no livro)

**Insight central:** "O que Codd fez para dados, feito para decisoes."

**Artigo OURO obrigatorio:** Coluna TDAN Jun 2013 — "Three Decision Model Normal Forms" (conteudo NAO presente no livro)

---

## TIER 2 — Systematizers

### 5. James Taylor — DMN

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 10 | **Real-World Decision Modeling with DMN** (2nd ed.) — com Jan Purchase | 2023 | JTonEDM Press | DMN 1.5 completo: DRDs, Decision Tables, FEEL, metodologia de discovery, integracao AI/ML |
| 11 | **Decision Management Systems** | 2011 | IBM Press | Blueprint arquitetural: como separar logica de decisao de logica de processo |

**ISBN Real-World DMN:** 978-8218234669 (470pp)
**ISBN DMS:** 978-0132884389 (308pp)

**Conteudo critico do Real-World DMN:**
- Decision Requirements Diagrams (DRDs): decomposicao hierarquica de decisoes
- Decision Tables: todos os hit policies e padroes
- FEEL Expressions: Friendly Enough Expression Language dentro do DMN 1.5
- Decision Modeling Methodology (Cap. 12): metodologia iterativa de discovery
- Business Architecture (Cap. 7): como decision models contribuem para arquitetura

---

### 6. Martin Fowler — Patterns

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 12 | **Patterns of Enterprise Application Architecture (PoEAA)** | 2002 | Addison-Wesley | ONDE regras vivem: Transaction Script vs Domain Model vs Table Module vs Service Layer (Cap. 2, 9) |
| 13 | **Analysis Patterns: Reusable Object Models** | 1996 | Addison-Wesley | O QUE regras parecem como modelos reutilizaveis: Accountability, Accounting, Posting Rules |
| 14 | **Refactoring** (2nd ed.) | 2018 | Addison-Wesley | COMO extrair regras: code smells como diagnostico (Cap. 3), mecanica de extracao (Cap. 6-10) |

**ISBNs:**
- PoEAA: 978-0-321-12742-6 (560pp)
- Analysis Patterns: 978-0-201-89542-1 (384pp)
- Refactoring: 978-0-13-475759-9 (448pp)

**PoEAA — Domain Logic Patterns (Cap. 9):**

| Pattern | Onde Regras Vivem |
|---|---|
| Transaction Script | Em scripts procedurais (1 por transacao). Regras tendem a duplicar. |
| Domain Model | Distribuidas em objetos interconectados. Regras vivem com os dados. |
| Table Module | Em modulos orientados a tabelas (1 classe por tabela). |
| Service Layer | NAO deve conter regras — so coordenacao. "All the key logic lies in the domain layer." |

**Analysis Patterns — Patterns que SAO business rules:**
- **Posting Rules** (Cap. 6): Regras como objetos de primeira classe — "quando X acontece, crie entrada Y"
- **Accountability** (Cap. 2): Regras organizacionais (quem reporta a quem)
- **Observation/Protocol** (Cap. 3): Regras sobre medicoes e qualidade de dados
- **Dual Time Record**: Regras temporais (valid time vs recording time)

**Refactoring — Code Smells como diagnostico de logica mal posicionada:**

| Smell | O Que Revela |
|---|---|
| Feature Envy | Logica no lugar errado |
| Long Function | Regras acumuladas sem decomposicao |
| Shotgun Surgery | Uma regra espalhada em muitas classes |
| Divergent Change | Multiplas regras em uma classe |
| Primitive Obsession | Conceitos de negocio como primitivos — regras espalhadas |

**Paper OURO obrigatorio:** Evans & Fowler — "Specification Pattern" (1997, PDF gratuito em martinfowler.com/apsupp/spec.pdf). Transforma business rules em objetos composiveis (AND/OR/NOT).

**Blog posts OURO (martinfowler.com):**
- AnemicDomainModel — diagnostico do anti-pattern mais comum
- RulesEngine — quando usar/nao usar rules engines
- "Domain Logic and SQL" — regras em stored procedures vs codigo
- "Refactoring to an Adaptive Model" — extracao de regras para sistemas data-driven

---

## TIER 3 — Specialist

### 7. Graham Witt — Expressao Natural

| # | Livro | Ano | Editora | Framework Principal |
|---|---|---|---|---|
| 15 | **Writing Effective Business Rules** | 2012 | Niobe Kaufmann | Constrained Natural Language, templates sintaticos, taxonomia Data/Activity/Party, guia pratico SBVR |

**ISBN:** 978-0-12-385051-5 (360pp)

**Metodologia core:**
- **Constrained Natural Language** — subconjunto restrito de ingles (sintaxe limitada + vocabulario controlado), analogo a comunicacao de controle aereo
- **Taxonomia de Rule Types:**
  - Data Rules: completude, significado, plausibilidade
  - Activity Rules: governam processos sem referencia a dados
  - Party Rules: permissoes/restricoes entre roles
- **Templates Sintaticos** — padroes exaustivos por tipo de regra, eliminando 6 fontes comuns de ambiguidade
- **Fact Model** — define E restringe o vocabulario das regras
- **Metodologia End-to-End:** Rule Discovery → Analysis → Vocabulary Development → Documentation → Quality Assurance → Publication → Maintenance

**Serie gratuita OURO:** 31 artigos expandindo o livro em BRCommunity.com

---

## Tabela Consolidada — 15 Livros OURO

| # | Mind | Livro | Ano | Editora | Tier |
|---|---|---|---|---|---|
| 1 | Ross | Principles of the Business Rule Approach | 2003 | Addison-Wesley | 0 |
| 2 | Ross | Building Business Solutions (2nd ed.) | 2015 | BRS | 0 |
| 3 | Ross | Business Rule Concepts (4th ed.) | 2013 | BRS | 0 |
| 4 | Ross | Business Knowledge Blueprints (2nd ed.) | 2020 | BRS | 0 |
| 5 | Evans | Domain-Driven Design | 2003 | Addison-Wesley | 0 |
| 6 | Evans | DDD Reference (FREE) | 2014 | Dog Ear | 0 |
| 7 | Feathers | Working Effectively with Legacy Code | 2004 | Prentice Hall | 1 |
| 8 | von Halle | The Decision Model | 2009 | Auerbach/CRC | 1 |
| 9 | von Halle | Business Rules Applied | 2001 | Wiley | 1 |
| 10 | Taylor | Real-World Decision Modeling with DMN (2nd) | 2023 | JTonEDM | 2 |
| 11 | Taylor | Decision Management Systems | 2011 | IBM Press | 2 |
| 12 | Fowler | PoEAA | 2002 | Addison-Wesley | 2 |
| 13 | Fowler | Analysis Patterns | 1996 | Addison-Wesley | 2 |
| 14 | Fowler | Refactoring (2nd ed.) | 2018 | Addison-Wesley | 2 |
| 15 | Witt | Writing Effective Business Rules | 2012 | Niobe Kaufmann | 3 |

---

## Ordem de Leitura Alinhada ao Workflow

```
DIAGNOSTICO (Tier 0) — "O QUE e e DE ONDE vem?"
  1. Ross — Business Rule Concepts (visao geral rapida)
  2. Ross — Principles (RuleSpeak + taxonomia)
  3. Evans — DDD Reference (FREE, 75pp, vocabulario DDD)
  4. Evans — Blue Book, Parte I + IV (UL, BC, Strategic Design)

EXTRACAO (Tier 1) — "COMO entro e COMO modelo?"
  5. Feathers — Working Effectively with Legacy Code
  6. von Halle — The Decision Model
  7. von Halle — Business Rules Applied

FORMALIZACAO (Tier 2) — "QUAL notacao e EM QUE padrao?"
  8. Taylor — Real-World Decision Modeling with DMN
  9. Fowler — PoEAA (Cap. 2, 9)
  10. Fowler — Refactoring (Cap. 3, 6-10)

EXPRESSAO (Tier 3) — "COMO escrevo sem ambiguidade?"
  11. Witt — Writing Effective Business Rules
  12. Ross — Business Knowledge Blueprints (vocabulario formal)
```

---

## Descobertas Bonus — Fontes que surgiram em multiplas pesquisas

Livros que apareceram como complementos OURO em 2+ pesquisadores independentes:

| Livro | Autor | Ano | Editora | Apareceu Em | Para Que |
|---|---|---|---|---|---|
| Architecture Modernization | Nick Tune | 2024 | Manning | Evans, Feathers | Legacy modernization end-to-end (DDD + EventStorming + Wardley) |
| Learning DDD | Vlad Khononov | 2021 | O'Reilly | Evans, Feathers | DDD moderno para brownfield, "THE DDD book of this decade" |
| DMN Method and Style (3rd) | Bruce Silver | 2024 | Cody-Cassidy | Taylor, Witt | FEEL + decision tables em profundidade tecnica |
| Your Code as a Crime Scene (2nd) | Adam Tornhill | 2024 | Pragmatic | Feathers | Hotspot analysis — ONDE olhar primeiro no legado |
| Knowledge Automation | Alan Fish | 2012 | Wiley | Taylor | Inventou DRA (Decision Requirements Analysis), precursor do DRD |
| Domain Storytelling | Hofer & Schwentner | 2022 | Addison-Wesley | Evans | Tecnica de workshop para extracao de regras |
| Software Design X-Rays | Adam Tornhill | 2018 | Pragmatic | Feathers | Analise organizacional do codigo |
| Smart (Enough) Systems | Taylor & Raden | 2007 | Prentice Hall | Taylor | Conceito original de "hidden decisions" em sistemas legados |

---

## TOOL — SBVR Checklist

| Recurso | Descricao | Acesso |
|---|---|---|
| SBVR Specification v1.5 | Standard OMG completo | omg.org/spec/SBVR (free PDF) |
| Witt's Writing Effective Business Rules | Guia pratico do SBVR (livro #15) | ISBN 978-0-12-385051-5 |
| Ross's SBVR Speaks series | 6 artigos (Aug 2019 - Mar 2020) | BRCommunity.com (free) |
| BRG "Defining Business Rules" paper | Paper seminal com classificacao original | businessrulesgroup.org (free PDF) |

---

## Gaps Identificados

1. **Nenhum livro cobre o pipeline completo** "encontrar regras no codigo → extrair → modelar → migrar → documentar para negocio." Minimo 3 livros necessarios (Feathers + Fowler + Evans/Khononov).
2. **AI-assisted rule extraction** e area emergente sem livro definitivo.
3. **Literatura academica** existe (Sneed & Verhoef, Putrycz & Kark) em papers, nao em livros acessiveis.
4. **COBOL/mainframe-specific** extracao tem literatura propria com baixa aplicabilidade a stacks modernas.
5. **EventStorming** (Alberto Brandolini) — livro inacabado ha ~10 anos, mas secao Big Picture e completa (Leanpub).

---

*Curadoria > Volume. 15 livros ouro + 8 bonus = 23 fontes com rastreabilidade completa.*
*Pesquisa: 7 agentes paralelos, ~350k tokens processados, ~60 livros avaliados.*
