---
type: quiz
course: aiox-fundamentos-arquitetura
module: M6
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
questions: 4
---

# Quiz 6 — Operação e observabilidade

### 1. Qual combinação ajuda a responder “onde e por que esta requisição ficou lenta?”

A. Apenas comentários  
B. Métricas para detectar, traces para localizar e logs para explicar detalhes  
C. Somente o nome do container  
D. Apenas o histórico do Git

### 2. Qual é a diferença entre liveness e readiness?

A. Liveness indica se deve reiniciar; readiness, se pode receber tráfego  
B. São sinônimos exatos  
C. Readiness mede custo; liveness mede receita  
D. Ambas substituem testes

### 3. O que um container empacota?

A. Uma imagem do ambiente e suas dependências para executar um processo de forma consistente  
B. Todo o datacenter  
C. A estratégia de produto  
D. A identidade do usuário final

### 4. Qual característica torna um rollback confiável?

A. Ser improvisado após a falha  
B. Ter versão anterior identificável, dados compatíveis e procedimento testado  
C. Apagar todos os logs  
D. Ignorar migrações de banco

<details>
<summary>Gabarito comentado</summary>

1. **B.** Os três sinais se complementam: tendência, caminho e contexto detalhado.  
2. **A.** Um processo pode estar vivo, mas temporariamente incapaz de servir tráfego.  
3. **A.** Container melhora portabilidade do runtime; não elimina diferenças de infraestrutura.  
4. **B.** Reversão é capacidade projetada e ensaiada, especialmente quando há mudanças de dados.

</details>

## Transferência

Defina para um serviço: três métricas, campos mínimos de log, um trace crítico, probes de saúde e o gatilho objetivo de rollback.

[Revisar o módulo](../modulos/M6-operacao-e-observabilidade.md) · [Próximo módulo](../modulos/M7-seguranca-e-fronteiras.md)
