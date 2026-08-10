---
type: quiz
course: aiox-agent-engineering
module: M5
question_count: 4
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---
# Quiz M5 — Produção

[Módulo M5](../modulos/M5-producao.md) · [Avaliações](../Assessments.md)

### 1. Qual entrega caracteriza deploy verificável?

A. URL ou endpoint acessível, versão identificável e smoke test registrado
B. Build local bem-sucedido
C. README atualizado
D. Branch criada

### 2. O que CI/CD deve impedir?

A. Toda intervenção humana
B. Mudanças pequenas
C. Promoção de artefato sem gates e rastreabilidade
D. Rollback

### 3. Qual sinal indica prontidão de produção?

A. Demo perfeita uma vez
B. Limites, segurança, observabilidade, rollback e ownership definidos
C. Modelo mais recente
D. Ausência de incidentes antes do lançamento

### 4. Um segredo apareceu no log. Qual é a decisão correta?

A. Prosseguir se o ambiente for staging
B. Apenas apagar a captura
C. Ocultar o log do aluno
D. Bloquear promoção, rotacionar o segredo e corrigir a fronteira de logging

<details>
<summary>Gabarito comentado</summary>

1. **A.** Deploy é realidade acessível com prova de versão e saúde.
2. **C.** Pipeline existe para tornar promoção controlada e auditável.
3. **B.** Produção é um sistema operável, não uma demo.
4. **D.** Exposição de segredo é incidente e gate bloqueante.

</details>

## Transferência

Preencha um checklist de prontidão e identifique um bloqueio real antes do seu deploy.
