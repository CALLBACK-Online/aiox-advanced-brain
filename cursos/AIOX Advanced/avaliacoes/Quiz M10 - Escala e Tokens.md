---
type: module-quiz
course: aiox-advanced
module: M10
status: canonical
canonical_scope: Cursos/AIOX Advanced
passing_score: 80
question_count: 4
source_version: 1.0.0
tags: [curso/aiox-advanced, avaliacao, quiz]
---

# Quiz M10 — Escala e tokens

Eu respondo sem consultar as aulas. Depois abro o gabarito, explico cada erro com minhas palavras e volto à evidência do módulo. Minha referência de domínio é 80%.

## Questões

### 1. Alan no campo: Ralph costuma ser usado para:

- A. Qualquer feature de produto sem partição
- B. Apagar branches
- C. ETL e trabalhos com ownership claro — não dev solto
- D. Só UI

### 2. Paralelizar vs sequencial decide-se por:

- A. Grafo de dependências e paths — medindo wall-clock
- B. Número de monitores
- C. Sempre paralelo
- D. Sempre sequencial

### 3. Model routing bem feito pode reduzir custo na ordem de:

- A. 0%
- B. 100% — grátis para sempre
- C. Aumentar 200%
- D. cerca de 40–60% (Haiku explore / Sonnet implement / Opus reason)

### 4. Há três Stories independentes e uma migração da qual todas dependem. Qual plano de execução faz sentido?

- A. Paralelizar tudo desde o primeiro minuto
- B. Executar a migração em sequência, abrir as três Stories em paralelo e medir wall-clock e custo
- C. Executar tudo sequencialmente por segurança
- D. Usar o mesmo modelo para todas as tarefas

<details>
<summary>Gabarito comentado</summary>

**1. C** — Citação de operação da cohort.

**2. A** — Dependência mata speedup.

**3. D** — Número de campo/ensino Advanced.

**4. B** — Paralelismo começa depois da dependência compartilhada e só vale quando o ganho é medido.

</details>

## Transferência

Eu produzo esta evidência no meu projeto: Plano de partição, modelo por tarefa, limites de concorrência, baseline e comparação do tempo final.

## Navegação

↑ [[modulos/Módulo 10 - Escala e Tokens|M10]] · [[Assessments|Todas as avaliações]]
