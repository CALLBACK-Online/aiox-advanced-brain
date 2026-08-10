---
type: quiz
course: introducao-arquitetura-sistemas
module: M3
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
questions: 4
---

# Quiz 3 — Contratos e comunicação

### 1. Quando uma interação síncrona é mais adequada?

A. Quando o chamador precisa da resposta para continuar e a espera é limitada  
B. Quando o trabalho pode levar horas sem manter conexão  
C. Quando nenhum resultado importa  
D. Quando o consumidor ainda não existe

### 2. Para que serve um webhook?

A. Consultar repetidamente um serviço a cada segundo  
B. Notificar outro sistema por HTTP quando um evento ocorre  
C. Substituir autenticação  
D. Criar índices no banco

### 3. Qual é o benefício central de uma fila?

A. Garantir que todo processamento será instantâneo  
B. Desacoplar produção e consumo, absorvendo diferença de ritmo  
C. Eliminar falhas de rede  
D. Impedir duplicatas por definição

### 4. Em pub/sub, o que muda em relação a uma fila simples de trabalho?

A. Um evento pode ser entregue a múltiplos assinantes interessados  
B. Não existem consumidores  
C. Toda mensagem vira arquivo  
D. O produtor chama cada função diretamente

<details>
<summary>Gabarito comentado</summary>

1. **A.** Sincronia combina com resposta imediata e orçamento claro de latência.  
2. **B.** O webhook é uma chamada iniciada pelo emissor após um acontecimento.  
3. **B.** A fila amortece picos e permite consumo independente, mas exige tratar falhas e duplicatas.  
4. **A.** Pub/sub distribui o mesmo fato a consumidores independentes.

</details>

## Transferência

Pegue uma automação real e escolha conscientemente entre chamada síncrona, webhook, fila e pub/sub. Registre latência, volume e tolerância a perda usados na decisão.

[Revisar o módulo](../modulos/M3-contratos-e-comunicacao.md) · [Próximo módulo](../modulos/M4-execucao-e-orquestracao.md)
