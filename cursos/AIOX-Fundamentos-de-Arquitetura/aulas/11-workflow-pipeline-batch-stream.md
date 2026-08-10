---
type: lesson
course: aiox-fundamentos-arquitetura
lesson_id: workflow-pipeline-batch-stream
lesson_position: 11
module: M4
sequence: M4.2
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
difficulty: foundation
adapted_from: cursos/AIOX Advanced/lessons/52-workflow-vs-comando-manual.md
source_refs: [azure-architecture-styles]
---

# Workflow, pipeline, batch e stream

## Resultado

Você desenha a topologia do trabalho e escolhe entre lote e fluxo contínuo sem chamar qualquer sequência de pipeline.

## Mapa visual

```text
WORKFLOW: regras de ordem, decisão, espera e aprovação
       ├── PIPELINE: entrada passa por estágios de transformação
       ├── BATCH: lote finito começa e termina
       └── STREAM: registros continuam chegando e sendo processados
```

## Modelo mental

**Workflow** é o conjunto de estados e regras que coordena trabalho até um resultado. Pode conter decisões, retornos, espera humana e caminhos alternativos.

**Pipeline** enfatiza estágios de transformação: extrair → normalizar → validar → publicar. Uma saída alimenta a próxima etapa.

**Batch** processa um conjunto delimitado, como os pedidos do dia. **Stream** processa um fluxo potencialmente contínuo, como cliques ou transações chegando em tempo real.

Um pipeline pode rodar em batch ou stream. Um workflow pode envolver vários pipelines. Nomear a topologia ajuda a escolher estado e recuperação.

## Quando usar — e quando não usar

Use workflow quando a operação possui estados, branches, aprovações ou retomada. Use pipeline para transformação sequencial. Prefira batch quando latência permite agrupar; stream quando o valor exige reação contínua e a operação aceita complexidade maior.

Não automatize um processo instável só para chamá-lo de workflow. Não escolha stream para atualizar um relatório diário. E não esconda decisões humanas dentro de um estágio sem estado de espera.

## Caso rápido

Publicar conteúdo é workflow: briefing, produção, revisão, aprovação e agendamento. Gerar formatos de imagem pode ser pipeline. Processar o calendário de amanhã é batch. Consumir eventos de publicação para analytics é stream.

Anti-padrão: pipeline sem contrato de entrada/saída por estágio. Quando quebra, ninguém sabe qual item avançou.

## Prática

Desenhe um processo real. Marque:

- estados do workflow;
- estágios de transformação;
- branches e gates humanos;
- batch ou stream;
- checkpoint e evidência por etapa.

## Pergunte ao seu agente

```text
Classifique este processo: workflow, pipeline, batch, stream ou composição. Desenhe estados, stages, branches, checkpoints e gates. Aponte onde uma receita manual ainda é mais segura que automação.
```

## Evidência de conclusão

Diagrama em que cada etapa tem entrada, saída, executor, estado e critério de avanço; lote/stream está justificado por latência e volume.

Fonte: [Azure Architecture Center — Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/). Proveniência: [mapeamento](../PROVENIENCIA.md).

[Anterior](10-processo-task-job-worker-runner.md) · [Próxima: fan-out e fan-in](12-concorrencia-paralelismo-fanout-fanin.md)
