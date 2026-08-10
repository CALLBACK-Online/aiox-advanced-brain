---
type: glossary
course: introducao-arquitetura-sistemas
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
---

# Glossário de arquitetura sem jargão

[Mapa de termos](Mapa-de-termos.md) · [Curso](README.md)

- **API:** contrato pelo qual um software oferece operações a outro.
- **Assíncrono:** o emissor entrega trabalho sem esperar o resultado final na mesma chamada.
- **Autenticação:** prova de quem é a identidade.
- **Autorização:** decisão sobre o que essa identidade pode fazer.
- **Backend:** parte que executa regras, integrações e acesso a dados fora da interface do usuário.
- **Backoff:** espera progressivamente maior entre novas tentativas.
- **Batch:** conjunto finito de itens processado como lote.
- **Cache:** cópia derivada e mais rápida de um dado cuja verdade vive em outro lugar.
- **Circuit breaker:** mecanismo que interrompe chamadas a uma dependência persistentemente falha.
- **CI:** integração frequente com build, testes e verificações automatizadas.
- **CD:** entrega ou implantação automatizada após gates definidos.
- **Cliente:** componente que inicia uma solicitação a outro componente.
- **Componente:** parte do sistema com responsabilidade e interface reconhecíveis.
- **Concorrência:** múltiplos trabalhos progridem no mesmo intervalo de tempo.
- **Container:** processo isolado empacotado com arquivos e dependências necessários.
- **Contrato:** forma, significado e regras de uma interação entre componentes.
- **Deploy:** colocar uma versão em um ambiente de execução.
- **Endpoint:** endereço e operação específicos expostos por uma API.
- **Entidade:** coisa do domínio com identidade e ciclo de vida.
- **Evento:** fato ocorrido e publicado para possíveis interessados.
- **Fan-in:** ponto de convergência que reúne e valida resultados paralelos.
- **Fan-out:** distribuição de um trabalho em vários ramos independentes.
- **Frontend:** interface executada perto do usuário e responsável pela interação.
- **Guardrail:** validação ou limite aplicado antes, durante ou depois de uma ação agentic.
- **Harness:** conjunto de instruções, ferramentas, permissões e controles que envolve um agente ou programa.
- **Health check:** diagnóstico de inicialização, vida ou prontidão de um componente.
- **HTTP:** protocolo de aplicação baseado em mensagens de request e response.
- **Idempotência:** propriedade de repetir uma operação sem multiplicar seu efeito final.
- **Índice:** estrutura auxiliar que acelera certos acessos ao banco em troca de espaço e custo de escrita.
- **Job:** unidade de trabalho agendada ou enfileirada para execução.
- **Load balancer:** distribuidor de tráfego entre recursos capazes de atender à solicitação.
- **Log:** registro de um evento discreto ocorrido no sistema.
- **Memória do agente:** estado persistido ou recuperado para influenciar execuções futuras; não é sinônimo de contexto atual.
- **Métrica:** medição numérica agregável capturada durante a execução.
- **Microsserviço:** serviço implantável de forma independente, delimitado por uma capacidade de negócio.
- **Monólito modular:** aplicação implantada como unidade, mas internamente dividida por fronteiras explícitas.
- **Multi-tenancy:** arquitetura em que uma plataforma atende organizações ou clientes distintos com isolamento definido.
- **Object storage:** armazenamento de objetos/blobs endereçados por chave, adequado a arquivos grandes.
- **Orquestrador:** componente que decide ou coordena ordem, delegação e convergência.
- **Pipeline:** sequência de estágios que transforma uma entrada em uma saída.
- **Pub/sub:** publicação de eventos para assinantes sem acoplamento direto a um único consumidor.
- **Quality gate:** verificação que precisa passar antes de avançar o estado da entrega.
- **Queue/fila:** buffer ordenado de mensagens ou trabalhos aguardando consumidores.
- **Rate limit:** limite de operações aceitas em uma janela de tempo.
- **Request:** mensagem de solicitação enviada por um cliente.
- **Response:** mensagem de resposta produzida após uma request.
- **Retry:** nova tentativa de uma operação que falhou de forma potencialmente transitória.
- **RLS:** políticas no banco que filtram linhas de acordo com identidade e regra de acesso.
- **Rollback:** retorno controlado a uma versão ou estado anterior conhecido.
- **Runner:** executor que materializa um workflow em um runtime.
- **Runtime:** ambiente concreto que carrega e executa um programa ou agente.
- **Schema:** estrutura e restrições que dão forma aos dados.
- **Secret:** credencial ou material sensível que concede acesso e precisa de ciclo de vida controlado.
- **Servidor:** componente que recebe solicitações e oferece respostas ou recursos.
- **Síncrono:** o chamador espera a resposta da operação na mesma interação.
- **Squad:** conjunto coordenado de especialistas, tarefas e gates para uma missão.
- **Stateless:** componente que não depende de memória local entre solicitações para manter a verdade do negócio.
- **Stream:** fluxo potencialmente contínuo de registros processados ao chegar.
- **Task:** unidade delimitada de trabalho com entrada e saída esperadas.
- **Tenant:** organização ou cliente isolável dentro de uma plataforma compartilhada.
- **Timeout:** limite de espera após o qual uma operação é tratada como não concluída.
- **Trace:** trajetória correlacionada de uma operação através de componentes.
- **Transação:** grupo de mudanças de dados tratado como unidade de consistência.
- **Webhook:** chamada HTTP enviada quando um evento ocorre.
- **Worker:** executor que consome tarefas delimitadas.
- **Workflow:** ordem e regras que coordenam tarefas até uma entrega.
