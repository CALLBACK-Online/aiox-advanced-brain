---
type: quiz
course: aiox-advanced
module: M4
question_count: 8
passing_score: 80
status: canonical
canonical_scope: cursos/AIOX Advanced
---
# Quiz M4 — Método e brownfield

### 1. O que vem primeiro em brownfield?
A. Reescrita
B. Reconstrução do sistema real e de suas fronteiras
C. Nova arquitetura ideal
D. Escolha de framework

### 2. Por que modelar uma entidade?
A. Para ligar estados, eventos, regras e ownership ao processo
B. Para criar mais tabelas
C. Para evitar discovery
D. Para substituir stories

### 3. Quando um squad é justificável?
A. Quando o nome é atraente
B. Quando existe qualquer tarefa
C. Quando múltiplos papéis e handoffs são necessários para o resultado
D. Quando uma skill basta

### 4. Qual enhancement é mais seguro?
A. O maior possível
B. O que troca toda a stack
C. O que ignora regressões
D. A menor fatia integrada, com baseline e testes de regressão

### 5. Seu squad tem oito agentes e fica bonito no terminal, mas você não sabe dizer qual saída ele produz nem quem paga por ela. O que fazer?
A. Definir a saída concreta e quem paga ou usa; se a resposta continuar vaga, cortar o squad
B. Adicionar mais agentes operacionais para gerar entrega
C. Manter: a organização em squad já é valor por si
D. Transformar o squad em app antes de definir a saída

### 6. O Dev quer começar a entidade “pedido” criando a tabela com id, nome e status. Qual é o movimento certo?
A. Deixar seguir: campos primeiro, processo depois
B. Adicionar mais campos agora para prever estados futuros
C. Mapear antes o ciclo de vida — como nasce, que estados percorre, como morre — e derivar os campos do ciclo
D. Pedir para a IA inferir os estados a partir do schema

### 7. O sistema roda em produção, você não escreveu o código e a mudança toca regiões com dependências desconhecidas. O que fazer antes de propor?
A. Um patch direto com bons testes unitários
B. Propor a reescrita do módulo para eliminar o legado
C. Discovery focado só na região da mudança
D. Discovery completo: legado vivo que você não entende pede o pipeline inteiro antes de qualquer proposta

### 8. O enhancement toca auth e billing — núcleo do sistema. Qual é o kit mínimo de evidência antes do merge?
A. Testes do módulo e smoke do fluxo
B. ADR, feature flag, Quality Gate reforçado e plano de rollback
C. Canary com checklist de consumidores, como em mudança transversal
D. CI verde no caminho novo já basta

<details><summary>Gabarito</summary>

**1. B** · **2. A** · **3. C** · **4. D** · **5. A** · **6. C** · **7. D** · **8. B**
</details>

## Transferência
Mapeie uma entidade e uma fatia mínima de enhancement.
