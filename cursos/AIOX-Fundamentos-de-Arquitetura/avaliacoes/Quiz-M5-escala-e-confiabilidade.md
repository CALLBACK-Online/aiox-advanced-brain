---
type: quiz
course: aiox-fundamentos-arquitetura
module: M5
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
questions: 4
---

# Quiz 5 — Escala e confiabilidade

### 1. Qual sinal justifica considerar escala horizontal?

A. O nome do projeto mudou  
B. Uma instância atingiu limite mensurável e o trabalho pode ser distribuído  
C. Existe um único usuário  
D. O README ficou longo

### 2. Quando um retry é perigoso?

A. Quando a operação não é idempotente e pode repetir efeito  
B. Quando há backoff  
C. Quando existe observabilidade  
D. Quando o erro é transitório

### 3. Para que serve rate limiting?

A. Definir um limite de consumo por identidade ou período  
B. Garantir zero latência  
C. Substituir autorização  
D. Sincronizar bancos automaticamente

### 4. Qual é a função de um circuit breaker?

A. Repetir falhas sem limite  
B. Interromper temporariamente chamadas a uma dependência degradada e testar recuperação  
C. Duplicar todos os eventos  
D. Balancear arquivos CSS

<details>
<summary>Gabarito comentado</summary>

1. **B.** Escala responde a gargalo observado e arquitetura distribuível, não a estética.  
2. **A.** Sem idempotência ou chave de deduplicação, repetir pode cobrar, enviar ou gravar duas vezes.  
3. **A.** O limite protege capacidade e equidade, mas não decide permissão funcional.  
4. **B.** O circuito reduz falhas em cascata e volta a testar após um intervalo.

</details>

## Transferência

Escolha uma dependência real. Defina timeout, condições de retry, backoff, limite de tentativas e comportamento após abertura do circuito.

[Revisar o módulo](../modulos/M5-escala-e-confiabilidade.md) · [Próximo módulo](../modulos/M6-operacao-e-observabilidade.md)
