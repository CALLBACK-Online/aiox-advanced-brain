---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: modelo-contexto-memoria-tool-skill
lesson_position: 22
module: M8
sequence: M8.1
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
adapted_from: cursos/AIOX Advanced/archive/migrated/aulas/14-anatomia-do-agente.md + cursos/AIOX Advanced/aulas/16-janela-de-contexto.md
source_refs: [anthropic-effective-agents, openai-agents, mcp]
reading_minutes: 5
---

# Modelo, contexto, memória, tool e skill

## Resultado

Você desmonta um “agente” em componentes verificáveis e sabe qual camada mudar quando ele erra.

## Mapa visual

```text
Modelo: raciocina e escolhe
Contexto: informação disponível nesta execução
Memória: estado recuperável entre execuções
Tool: capacidade de ler ou agir no mundo
Skill: instrução/procedimento reutilizável
Harness: combina tudo com limites e ambiente
```

## Modelo mental

O **modelo** produz decisões e linguagem. O **contexto** é sua mesa de trabalho atual: instruções, conversa, arquivos e resultados de tools disponíveis agora. Mais contexto não é sempre melhor; ruído compete com sinais.

**Memória** é estado que pode ser persistido e recuperado depois. Não é a mesma coisa que a janela de contexto. **Tool** é uma função exposta para buscar informação ou causar efeito. **Skill** é procedimento e conhecimento que orientam quando e como agir; só executa se o runtime oferecer as tools necessárias.

Um agente útil é sistema, não apenas prompt: modelo + harness + tools + ambiente + estado.

## Quando usar — e quando não usar

Diagnostique pela camada: conhecimento ausente pode pedir contexto; repetição entre sessões, memória; incapacidade de agir, tool; processo inconsistente, skill/workflow; decisão fraca, modelo ou instrução.

Não dê tool poderosa para corrigir prompt ruim. Não carregue toda biblioteca em cada turno. Não trate memória como verdade sem origem, validade e permissão. E não prometa que `$skill` existe em runtime que não a instalou.

## Caso rápido

Um agente responde corretamente sobre ClickUp, mas não cria nada. Ele possui conhecimento, não tool/credencial. Outro possui tool, mas escolhe campos errados porque não recebeu o processo. Problemas de camadas diferentes exigem correções diferentes.

Anti-padrão: contexto infinito. Instruções contraditórias e milhares de arquivos reduzem recuperação do que importa.

## Prática

Escolha um agente e preencha: objetivo, modelo, contexto mínimo, memória, tools, skills, permissões, ambiente e evidência. Remova uma camada supérflua e justifique.

## Pergunte ao seu agente

```text
Faça uma anatomia deste agente por camadas: modelo, contexto, memória, tools, skills, harness e ambiente. Para cada falha relatada, indique a camada provável e a menor correção. Não assuma integração instalada.
```

## Evidência de conclusão

Diagrama em que toda capacidade e todo estado têm uma camada responsável; você consegue explicar por que “trocar o modelo” não resolve qualquer falha.

Fontes: [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/agents/) e [MCP](https://modelcontextprotocol.io/specification/2025-06-18/server/index). Proveniência: [mapeamento](../PROVENIENCIA.md).

[Anterior](21-monolito-modulos-microsservicos.md) · [Próxima: orquestração agentic](23-orquestrador-squad-human-in-loop.md)
