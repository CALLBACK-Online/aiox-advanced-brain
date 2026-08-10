---
type: quiz
course: aiox-advanced
module: M2
question_count: 8
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX Advanced
---
# Quiz M2 — SDC e qualidade

### 1. O que torna uma story executável?
A. Título curto
B. Estimativa precisa
C. Contexto, critérios de aceite, escopo e evidência esperada
D. Um agente atribuído

### 2. Qual é o papel do Quality Gate?
A. Produzir parecer com evidência e bloquear falha crítica
B. Substituir testes
C. Aprovar toda entrega
D. Aumentar o diff

### 3. Por que QA devolve o trabalho ao Dev?
A. Para mudar o escopo
B. Para preservar separação entre diagnóstico e correção
C. Para evitar automação
D. Para reescrever o PRD

### 4. Quando a story termina?
A. Quando o código existe
B. Quando o agente para
C. Quando o diff é pequeno
D. Quando critérios e validações estão comprovados no artefato real

### 5. O CodeRabbit apareceu no bootstrap do projeto, mas o QA humano vive corrigindo lint, imports quebrados e edge cases óbvios. Qual é o diagnóstico?
A. O QA está fraco e precisa de treinamento
B. O gate provavelmente está desligado: confira o enable no core-config, porque sujeira mecânica deveria cair no filtro automático
C. Está tudo normal: o reviewer automático só atua no PR final
D. Falta adicionar uma quarta passagem de review

### 6. Você vai amarrar um repositório novo ao ciclo antes de o agente tocar no código. Qual é a ordem correta?
A. CI/CD primeiro, para garantir o deploy desde o início
B. CodeRabbit primeiro: review automático é o que mais protege
C. A ordem não importa, desde que as quatro fases existam
D. Detect Repo, GitHub, CodeRabbit e CI/CD, avançando só com a fase anterior fechada

### 7. O pedido é “coloca IA no onboarding”. Você já sabe a dor e o outcome, mas ninguém decidiu stack, limites nem o que fica fora de escopo. Em que etapa você está?
A. Briefing: volte ao porquê e ao público
B. Story: quebre direto em unidades com aceite
C. PRD: o porquê está fechado, falta a planta de construção
D. Dev: comece a codar e ajuste pelo diff

### 8. O QA encontrou 12 findings na story e o Dev quer abrir 12 issues para resolver depois. O que o Apply QA Fixes Loop manda fazer?
A. Devolver ao Dev, na mesma story, branch e PR, os findings que cabem no aceite; issue nova só quando o achado é outra story de verdade
B. Abrir as 12 issues: cada finding rastreado separadamente
C. Corrigir só os nits agora e deixar os blockers para a próxima sprint
D. Fazer o merge e tratar os findings como dívida documentada

<details><summary>Gabarito</summary>

**1. C** · **2. A** · **3. B** · **4. D** · **5. B** · **6. D** · **7. C** · **8. A**
</details>

## Transferência
Reescreva um critério subjetivo como evidência verificável.
