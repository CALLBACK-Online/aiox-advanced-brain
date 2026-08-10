---
type: quiz
course: aiox-fundamentos-arquitetura
module: M4
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
questions: 4
---

# Quiz 4 — Execução e orquestração

### 1. O que melhor define um worker?

A. Um processo que retira e executa unidades de trabalho  
B. Um documento de requisitos  
C. Um banco relacional  
D. Um usuário administrador

### 2. Qual é a diferença mais útil entre workflow e pipeline?

A. Não existe nenhuma diferença de uso  
B. Workflow coordena estados e decisões; pipeline enfatiza transformação por etapas  
C. Pipeline só funciona com agentes  
D. Workflow nunca possui etapas

### 3. O que é fan-out?

A. Reunir resultados em uma síntese  
B. Distribuir um trabalho em ramos que podem avançar independentemente  
C. Cancelar toda execução concorrente  
D. Repetir a mesma tarefa indefinidamente

### 4. O que torna o fan-in seguro?

A. Aceitar qualquer saída sem contrato  
B. Um ponto de convergência com critérios de completude, conflito e falha parcial  
C. Usar o maior número possível de agentes  
D. Ocultar resultados divergentes

<details>
<summary>Gabarito comentado</summary>

1. **A.** Worker consome unidades de trabalho; runner fornece o mecanismo ou ambiente que as executa.  
2. **B.** Os termos se sobrepõem, mas destacam problemas diferentes.  
3. **B.** Fan-out abre ramos independentes para reduzir o caminho crítico ou ampliar cobertura.  
4. **B.** Fan-in precisa saber o que esperar e como reconciliar resultados, conflitos e ausências.

</details>

## Transferência

Desenhe um processo seu com três etapas. Marque dependências reais, um fan-out possível e o contrato de fan-in. Se não houver independência, explique por que manteria a sequência.

[Revisar o módulo](../modulos/M4-execucao-e-orquestracao.md) · [Próximo módulo](../modulos/M5-escala-e-confiabilidade.md)
