---
type: lesson
course: aiox-fundamentos-arquitetura
lesson_id: json-yaml-markdown-contratos
lesson_position: 7
module: M3
sequence: M3.1
status: canonical
canonical_scope: cursos/AIOX-Fundamentos-de-Arquitetura
difficulty: foundation
adapted_from: cursos/AIOX Advanced/lessons/18-yaml-markdown-json-sweet-spot.md
source_refs: [openapi, mcp]
---

# JSON, YAML e Markdown como contratos

## Resultado

Você escolhe formato pelo consumidor e pelo tipo de validação, não por preferência estética.

## Mapa visual

```text
Máquina ↔ máquina, schema rígido  → JSON
Humano configura estrutura        → YAML
Humano lê raciocínio e instrução  → Markdown
Documento + metadados             → Markdown com frontmatter
```

## Modelo mental

Formato é parte do contrato porque define como informação será lida e validada.

- **JSON:** estrutura explícita e amplamente suportada por APIs. Ótimo para dados; ruim para comentários e narrativa longa.
- **YAML:** configuração legível com comentários e menos pontuação. Exige cuidado com indentação e tipos implícitos.
- **Markdown:** texto humano com hierarquia, links, exemplos e código. Excelente para instruções e conhecimento; fraco como contrato rígido sem convenção adicional.

Combinar formatos pode ser correto: frontmatter YAML para metadados e corpo Markdown para explicação. A pergunta é sempre “quem consome e como detecta erro?”.

## Quando usar — e quando não usar

Use JSON quando outro programa precisa validar ou trocar payload. Use YAML para configuração revisada por pessoas. Use Markdown para ensinar, justificar e operar procedimentos.

Não coloque lógica executável escondida em prosa quando um runner precisa de campos determinísticos. Não use YAML para transportar dados não confiáveis sem parser seguro. Não gere JSON “quase válido” com comentários ou vírgulas sobrando.

## Caso rápido

Um squad pode ter `config.yaml` para inventário e `agents/*.md` para comportamento. Já a resposta de uma API precisa de JSON validável. Forçar a personalidade inteira do agente em JSON gera strings gigantes; deixar o identificador e permissões apenas em Markdown impede validação automática.

Anti-padrão: duplicar o mesmo campo em YAML, JSON e Markdown sem declarar fonte canônica. Drift é inevitável.

## Prática

Pegue três artefatos reais — payload de API, configuração de workflow e guia de operação — e escolha o formato. Para cada um, registre consumidor, validação, fonte canônica e erro mais provável.

## Pergunte ao seu agente

```text
Para cada artefato, recomende JSON, YAML, Markdown ou composição. Justifique pelo consumidor, necessidade de schema, revisão humana e risco de drift. Não converta nada antes de declarar a fonte canônica.
```

## Evidência de conclusão

Tabela formato × consumidor × validação × fonte canônica; outra pessoa sabe qual arquivo editar e qual é derivado.

Fontes: [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) e [MCP primitives](https://modelcontextprotocol.io/specification/2025-06-18/server/index). Proveniência: [mapeamento](../PROVENIENCIA.md).

[Anterior](06-cache-arquivos-object-storage.md) · [Próxima: síncrono e assíncrono](08-sincrono-assincrono.md)
