---
type: quiz
course: introducao-arquitetura-sistemas
module: M7
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
questions: 4
---

# Quiz 7 — Segurança e fronteiras

### 1. Qual frase separa autenticação de autorização?

A. Autenticação identifica; autorização decide o que a identidade pode fazer  
B. Autenticação criptografa; autorização compacta  
C. São sempre a mesma operação  
D. Autorização ocorre apenas no frontend

### 2. Onde um segredo de produção deve ficar?

A. No README público  
B. Em um gerenciador de segredos com acesso mínimo e rotação  
C. Em uma captura de tela  
D. Dentro do prompt enviado a qualquer modelo

### 3. O que RLS protege?

A. A aparência de uma tabela  
B. O acesso a linhas do banco conforme políticas avaliadas para a identidade  
C. O limite de CPU  
D. A ordem do pipeline

### 4. Qual é um bom motivo para começar com monólito modular?

A. Eliminar a necessidade de fronteiras  
B. Manter operação simples enquanto separa responsabilidades no código  
C. Impedir qualquer escala futura  
D. Colocar todos os dados em uma variável global

<details>
<summary>Gabarito comentado</summary>

1. **A.** Saber quem é não implica permissão para executar toda ação.  
2. **B.** Segredos exigem armazenamento dedicado, menor privilégio, auditoria e rotação.  
3. **B.** RLS aplica isolamento perto dos dados, mas as políticas também precisam de testes.  
4. **B.** Modularidade cria limites conceituais sem assumir cedo o custo distribuído.

</details>

## Transferência

Modele dois tenants e três papéis. Especifique identidade, permissões, política de isolamento de dados e um teste negativo que prove a fronteira.

[Revisar o módulo](../modulos/M7-seguranca-e-fronteiras.md) · [Próximo módulo](../modulos/M8-sistemas-com-agentes.md)
