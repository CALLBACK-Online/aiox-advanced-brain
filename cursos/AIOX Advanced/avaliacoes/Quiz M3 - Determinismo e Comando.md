---
type: quiz
course: aiox-advanced
module: M3
question_count: 8
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX Advanced
---
# Quiz M3 — Determinismo e comando

### 1. Quando preferir fluxo determinístico?
A. Quando regras e validações podem ser codificadas
B. Quando toda etapa exige julgamento aberto
C. Quando não há critério de aceite
D. Quando o prompt é curto

### 2. O que diferencia Goal de Loop?
A. Goal nunca usa agente
B. Loop sempre é paralelo
C. Goal define o resultado; loop itera estado e feedback até um stop condition
D. Não há diferença

### 3. Qual autonomia é saudável?
A. A máxima disponível
B. A menor que alcança o resultado dentro do risco aceito
C. A que elimina logs
D. A que não permite interrupção

### 4. Quando operar em Rider mode?
A. Quando o sistema já é totalmente determinístico
B. Quando não existe impacto
C. Quando o resultado é irrelevante
D. Quando decisões ambíguas precisam de elicitação do operador

### 5. Você rodou /goal “melhorar as aulas até ficarem excelentes” e o agente trabalha há horas relatando progresso sem terminar. Qual é o problema?
A. Faltou usar um modelo mais forte no loop
B. Faltou paralelizar o goal em subagentes
C. O goal era longo demais para uma sessão só
D. O DONE WHEN é vago: sem condição verificável, VERIFY e stop rules, o loop não tem como terminar

### 6. Uma feature grande está para ser pedida e você quer mandar tudo de uma vez para ganhar tempo. O que diz o determinismo progressivo?
A. Quebre em 30 (esqueleto), 60 (corpo) e 90 (acabamento), com gate entre estágios: o erro de estrutura aparece quando consertar é barato
B. Peça tudo de uma vez e revise no fim: economiza turnos
C. Especifique cada linha antes de pedir qualquer coisa
D. Rode duas versões em paralelo e escolha a melhor

### 7. Um agent de LLM converte formato de arquivo toda noite e de vez em quando a saída varia. Qual é a correção certa?
A. Melhorar o prompt com mais exemplos de saída
B. Reduzir a temperatura do modelo para variar menos
C. Mover a tarefa para um script determinístico: regra que fecha sozinha é trabalho de código, não de IA
D. Colocar um segundo agent revisando a saída do primeiro

### 8. Seu loop tem um passo que dropa schema em ambiente real e outro que só formata código. Onde colocar elicit (rider)?
A. Nos dois passos: segurança em primeiro lugar
B. No passo irreversível, com contexto e confirmação não-trivial; o passo mecânico e reversível roda em silêncio
C. Em nenhum: o Quality Gate no fim do loop já protege
D. Só no fim do loop, para não quebrar o ritmo

<details><summary>Gabarito</summary>

**1. A** · **2. C** · **3. B** · **4. D** · **5. D** · **6. A** · **7. C** · **8. B**
</details>

## Transferência
Defina stop condition e escalonamento humano para um loop.
