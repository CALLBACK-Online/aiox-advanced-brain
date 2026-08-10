---
type: module-quiz
course: aiox-advanced
module: M3
status: canonical
canonical_scope: cursos/AIOX Advanced
passing_score: 80
question_count: 5
source_version: 1.0.0
tags: [curso/aiox-advanced, avaliacao, quiz]
---

# Quiz M3 — Ciclo SDC

Eu respondo sem consultar as aulas. Depois abro o gabarito, explico cada erro com minhas palavras e volto à evidência do módulo. Minha referência de domínio é 80%.

## Questões

### 1. A ordem canônica das etapas antes do código é:

- A. Deploy → Story → Briefing
- B. Briefing → PRD → Stories
- C. Story → PRD → Briefing
- D. PRD → Deploy → Briefing

### 2. No ciclo de vida da Story, desenvolver em draft é:

- A. Boa prática de velocidade
- B. Obrigatório no AIOX
- C. Anti-padrão — ready é o contrato antes do Dev
- D. Só permitido com Opus

### 3. Durante o loop de Quality Gate / Apply QA Fixes, o status da task deve:

- A. Permanecer in_progress até o loop fechar
- B. Ir para completed ao entrar no QG
- C. Ser apagado do board
- D. Virar deploy automaticamente

### 4. Quality Gate 'de verdade' implica:

- A. Comment opcional no PR sem bloquear merge
- B. Revisão só no final do mês
- C. Apenas like no diff
- D. Bloqueio físico de merge até PASS (ou waiver assinado)

### 5. Done da Story e deploy:

- A. São sempre o mesmo evento
- B. Podem ser ciclos distintos — done ≠ necessariamente produção
- C. Deploy deve ocorrer em draft
- D. Done proíbe qualquer QA

<details>
<summary>Gabarito comentado</summary>

**1. B** — Intenção → planta → unidades executáveis. PRD não é Story.

**2. C** — Draft é rascunho; ready passou validate. Codar draft assina retrabalho.

**3. A** — Learning real da cohort T2: completed no meio do QG é mentira de processo.

**4. D** — Sem bloqueio, gate é enfeite. Coleira = critério + remediação + review.

**5. B** — Fechar a unidade de trabalho ≠ promover ambiente; DevOps pode ser outro ciclo.

</details>

## Transferência

Eu produzo esta evidência no meu projeto: Story com critérios de aceite, resultado do gate, correções realizadas e estado final registrado.

## Navegação

↑ [[modulos/Módulo 3 - Ciclo SDC|M3]] · [[Assessments|Todas as avaliações]]
