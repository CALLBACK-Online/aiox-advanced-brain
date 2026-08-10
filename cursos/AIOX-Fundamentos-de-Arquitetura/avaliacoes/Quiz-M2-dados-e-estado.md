---
type: quiz
course: aiox-fundamentos-arquitetura
module: M2
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
questions: 4
---

# Quiz 2 — Dados, estado e persistência

### 1. Qual opção representa melhor uma entidade de negócio?

A. Uma cor do tema  
B. Um pedido com identidade e ciclo de vida  
C. Um comentário no código  
D. Uma aba aberta no navegador

### 2. Qual é a função principal de uma transação no banco?

A. Comprimir imagens  
B. Fazer um conjunto de mudanças confirmar ou falhar como unidade  
C. Substituir toda validação  
D. Tornar qualquer consulta instantânea

### 3. Quando um cache é apropriado?

A. Como única fonte de verdade de pagamentos  
B. Para acelerar leituras quando atraso ou expiração controlados são aceitáveis  
C. Para esconder ausência de modelo de dados  
D. Para armazenar qualquer segredo permanentemente

### 4. Qual afirmação diferencia JSON, YAML e Markdown corretamente?

A. Os três são bancos de dados  
B. JSON e YAML estruturam dados; Markdown prioriza conteúdo legível  
C. Markdown substitui toda API  
D. YAML é sempre mais seguro que JSON

<details>
<summary>Gabarito comentado</summary>

1. **B.** Entidade combina identidade, estado e transições relevantes ao domínio.  
2. **B.** A transação protege a unidade lógica contra confirmação parcial.  
3. **B.** Cache troca frescor e complexidade por menor latência ou custo.  
4. **B.** A escolha depende do contrato: dados estruturados ou explicação humana.

</details>

## Transferência

Modele uma entidade do seu contexto com estados válidos, transições e fonte de verdade. Marque um dado que poderia ser cacheado e explique a política de expiração.

[Revisar o módulo](../modulos/M2-dados-e-estado.md) · [Próximo módulo](../modulos/M3-contratos-e-comunicacao.md)
