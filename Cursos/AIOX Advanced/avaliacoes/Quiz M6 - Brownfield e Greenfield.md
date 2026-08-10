---
type: module-quiz
course: aiox-advanced
module: M6
status: canonical
canonical_scope: Cursos/AIOX Advanced
passing_score: 80
question_count: 4
source_version: 1.0.0
tags: [curso/aiox-advanced, avaliacao, quiz]
---

# Quiz M6 — Workflows brownfield e greenfield

Eu respondo sem consultar as aulas. Depois abro o gabarito, explico cada erro com minhas palavras e volto à evidência do módulo. Minha referência de domínio é 80%.

## Questões

### 1. Brownfield Discovery deve vir:

- A. Depois de refatorar tudo
- B. Somente se o cliente pedir PDF
- C. Antes de propor mudança — decifrar o que já roda
- D. Nunca em AIOX

### 2. Workflow vs comando vs runner escolhe-se por:

- A. Maturidade do processo e variação (rodinha → pedal → estrada)
- B. Cor do logo
- C. Sempre runner
- D. Sempre comando manual

### 3. Enhancement em legado exige:

- A. Big-bang rewrite sempre
- B. Desligar testes
- C. Force push na main
- D. Menor diff + evidência de não-regressão

### 4. Você precisa adicionar uma feature a um sistema legado cuja arquitetura e testes são desconhecidos. Qual é a primeira decisão responsável?

- A. Abrir uma branch e começar pela tela
- B. Executar discovery brownfield, mapear restrições e só então desenhar o enhancement
- C. Reescrever tudo como greenfield
- D. Pedir um deploy para descobrir o comportamento

<details>
<summary>Gabarito comentado</summary>

**1. C** — Mapa real > hipótese no escuro.

**2. A** — Bicicleta com rodinha até estabilizar.

**3. D** — Adicionar sem quebrar.

**4. B** — Brownfield exige diagnóstico do terreno antes da mudança; enhancement sem mapa aumenta risco invisível.

</details>

## Transferência

Eu produzo esta evidência no meu projeto: Diagnóstico do terreno, riscos, prior art, estratégia escolhida e plano de mudança com gates.

## Navegação

↑ [[modulos/Módulo 6 - Brownfield e Greenfield|M6]] · [[Assessments|Todas as avaliações]]
