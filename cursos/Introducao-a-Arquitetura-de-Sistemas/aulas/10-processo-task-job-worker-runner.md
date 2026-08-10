---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: processo-task-job-worker-runner
lesson_position: 10
module: M4
sequence: M4.1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [azure-background-jobs, docker-container]
reading_minutes: 5
---

# Processo, task, job, worker e runner

## Resultado

Você nomeia corretamente trabalho, executor e ambiente, evitando chamar tudo de agente ou processo.

## Mapa visual

```text
Workflow define a ordem
  └── cria Jobs persistíveis
       └── divididos em Tasks delimitadas
            └── Worker consome e executa
                 └── Runner materializa regras no Runtime
                      └── Processo está rodando no sistema operacional
```

## Modelo mental

- **Processo:** instância de programa em execução, com recursos do sistema operacional.
- **Task:** unidade delimitada de trabalho com entrada e saída.
- **Job:** trabalho persistível, agendado ou enfileirado, que pode conter tasks e status.
- **Worker:** executor que busca ou recebe trabalho.
- **Runner:** mecanismo que transforma uma definição de workflow/job em execução concreta dentro de um runtime.

As palavras variam entre produtos. O importante é não misturar três perguntas: “qual é o trabalho?”, “quem executa?” e “onde/como executa?”.

## Quando usar — e quando não usar

Use a taxonomia para definir ownership, retry, timeout e observabilidade. Se um worker cai, o job deve continuar reconhecível e retomável.

Não transforme toda task em job persistido. Uma função local de milissegundos não precisa de fila e painel. Não chame o LLM de worker quando ele também planeja e escolhe tools; executor determinístico e agente possuem graus de liberdade diferentes.

## Caso rápido

“Processar 100 PDFs” é um job. Cada PDF pode ser uma task. Quatro workers consomem tasks. Um runner controla concorrência, timeout e checkpoint. Cada worker é um processo ou container no runtime escolhido.

Anti-padrão: guardar o board apenas no contexto do agente. Se a sessão termina, o sistema perde jobs e estados.

## Prática

Pegue um trabalho recorrente e escreva:

- job e seu identificador;
- tasks;
- worker responsável;
- runtime;
- checkpoint;
- critérios de retry e done.

## Pergunte ao seu agente

```text
Converta este trabalho em job e tasks. Separe definição, executor, runner e runtime. Aponte qual estado precisa persistir para retomar após queda. Prefira execução determinística quando raciocínio não for necessário.
```

## Evidência de conclusão

Ficha de execução que permite matar um worker e responder onde o trabalho ficou, quem retoma e como evita perda ou duplicação.

Fontes: [Azure — Background jobs](https://learn.microsoft.com/en-us/azure/architecture/best-practices/background-jobs) e [Docker — containers](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).


## Âncora no acervo

- [Glossário](../Glossario.md)
- [Mapa de termos](../Mapa-de-termos.md)

## Navegação

- Curso: [README](../README.md)
- Módulo: [M4](../modulos/M4-execucao-e-orquestracao.md)
- Anterior: [09-webhook-fila-evento-pubsub.md](09-webhook-fila-evento-pubsub.md)
- Próxima: [11-workflow-pipeline-batch-stream.md](11-workflow-pipeline-batch-stream.md)
