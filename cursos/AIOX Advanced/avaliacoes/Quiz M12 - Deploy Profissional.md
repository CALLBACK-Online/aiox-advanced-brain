---
type: module-quiz
course: aiox-advanced
module: M12
status: canonical
canonical_scope: cursos/AIOX Advanced
passing_score: 80
question_count: 5
source_version: 1.0.0
tags: [curso/aiox-advanced, avaliacao, quiz]
---

# Quiz M12 — Deploy profissional

Eu respondo sem consultar as aulas. Depois abro o gabarito, explico cada erro com minhas palavras e volto à evidência do módulo. Minha referência de domínio é 80%.

## Questões

### 1. Na escada Script→…→SaaS, pular degraus:

- A. É teleporte arriscado — sobe com evidência de estabilidade
- B. É sempre a melhor estratégia
- C. É obrigatório no AIOX
- D. Só importa o logo SaaS

### 2. RLS no Supabase é:

- A. Opcional se a UI for bonita
- B. Só para Postgres local
- C. Substituto de senha de email
- D. Obrigatório em multi-user — banco recusa linha indevida

### 3. CI/CD com Quality Gate pré-merge exige:

- A. Badge verde opcional
- B. Required status checks + bloqueio de merge no vermelho
- C. Só review por like
- D. Deploy sem build

### 4. Checklist de prontidão de produção:

- A. É chato e deve ser ignorado
- B. Só conta URL pública
- C. Go/no-go com itens verdes/vermelhos e dono — segurança vermelha é no-go
- D. Substitui testes

### 5. O sistema funciona localmente, mas não tem RLS, smoke test nem rollback. Como classificá-lo?

- A. Ainda não pronto; é preciso fechar segurança, deploy, smoke, observabilidade e recuperação
- B. Pronto para produção porque o caminho feliz funciona
- C. Pronto se o repositório estiver privado
- D. Pronto depois de trocar o domínio

<details>
<summary>Gabarito comentado</summary>

**1. A** — Cada degrau paga escola.

**2. D** — service_role no client é vazamento.

**3. B** — Lei do repo, não enfeite.

**4. C** — Produção é checklist, não empolgação.

**5. A** — Localhost prova construção; produção exige proteção, validação e recuperação operacional.

</details>

## Transferência

Eu produzo esta evidência no meu projeto: URL, smoke test, Quality Gate pré-merge, segurança mínima, rollback e limites conhecidos.

## Navegação

↑ [[modulos/Módulo 12 - Deploy Profissional|M12]] · [[Assessments|Todas as avaliações]]
