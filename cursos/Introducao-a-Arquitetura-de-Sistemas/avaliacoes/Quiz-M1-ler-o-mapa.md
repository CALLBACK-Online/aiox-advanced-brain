---
type: quiz
course: introducao-arquitetura-sistemas
module: M1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
questions: 4
---

# Quiz 1 — Ler o mapa de um sistema

### 1. Em um checkout, qual componente deve decidir o valor final da compra?

A. O botão no frontend  
B. O serviço no backend responsável pelo pedido  
C. O navegador do cliente  
D. O arquivo CSS

### 2. O que melhor descreve uma fronteira de sistema?

A. Uma pasta com muitos arquivos  
B. O limite onde responsabilidade, dados ou confiança mudam  
C. Qualquer função com mais de dez linhas  
D. Um sinônimo de banco de dados

### 3. Em HTTP, o que é uma resposta `404`?

A. Um método de escrita  
B. Um evento assíncrono  
C. Uma resposta informando que o recurso não foi encontrado  
D. Uma confirmação de persistência

### 4. Qual é o melhor primeiro passo ao receber um diagrama desconhecido?

A. Escolher microserviços imediatamente  
B. Identificar atores, componentes, fronteiras e fluxo principal  
C. Trocar toda a stack  
D. Criar uma fila para cada seta

<details>
<summary>Gabarito comentado</summary>

1. **B.** Regras críticas pertencem ao lado confiável da fronteira.  
2. **B.** A fronteira torna explícita a mudança de responsabilidade, dado ou nível de confiança.  
3. **C.** O status comunica o resultado da requisição; `404` indica recurso não encontrado.  
4. **B.** Primeiro se compreende o mapa; padrões e tecnologias vêm depois do problema.

</details>

## Transferência

Escolha um produto que você usa. Desenhe cliente, servidor, dados, uma fronteira de confiança e uma interação HTTP. Peça ao agente para apontar uma suposição não declarada.

[Revisar o módulo](../modulos/M1-ler-o-mapa.md) · [Próximo módulo](../modulos/M2-dados-e-estado.md)
