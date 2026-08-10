---
type: glossary-term
course: aiox-advanced
tags:
- glossario
- aiox
- course-brain
updated: '2026-08-10'
status: reference
canonical_scope: cursos/AIOX Advanced
freq:
  aiox_advanced: 58
  aiox_advanced_squads: 2
  total: 60
  counted_at: '2026-08-10'
---
# MCP

Model Context Protocol: padrão para conectar ferramentas e dados externos ao agente por uma interface controlada. O que estiver ativo entra na janela de contexto; escolher MCPs é engenharia de contexto.

## Como é usado

Antes de ativar um **MCP**, defina a tarefa, os recursos e ferramentas permitidos, o ambiente, os dados que podem sair e a evidência esperada. Mantenha conectores específicos fora do carregamento global quando não forem necessários.

**Exemplo prático:** na aula [[17-engenharia-de-contexto]], habilite um MCP somente leitura para consultar tickets de staging, busque um ticket e registre a resposta; não deixe uma ferramenta de escrita em production ativa por conveniência.

**Não confunda:** **MCP** não é o agente, nem contexto grátis ou autorização ampla. Ele expõe capacidades; escopo, credenciais, ambiente e validação continuam sendo responsabilidade do desenho do processo.

**Frequência nos cursos:** **60** menções (AIOX Advanced: 58 · AIOX Advanced Squads: 2).

## Aulas

- [[17-engenharia-de-contexto]]
- [[05-ambientes-local-staging-production]]

## Ver também

- [[Engenharia de Contexto]]
- [[Janela de Contexto]]
- [[Hook]]
- [[Glossário AIOX Advanced]]
