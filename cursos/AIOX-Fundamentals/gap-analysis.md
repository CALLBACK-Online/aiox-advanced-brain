# Análise de lacunas brownfield

**Origem analisada:** curso legado `aios`, publicado em 2024, com 19 módulos e 73 aulas.

**Destino:** `aiox-fundamentals`, alinhado ao snapshot do AIOX Core 5.2.9 e à arquitetura canônica de três módulos.

## Lacunas críticas encontradas

- Identidade antiga “AIOS” e expansão incorreta do acrônimo.
- Namespace npm anterior à consolidação em `@aiox-squads/core`.
- Conteúdo anterior ao suporte atual de Claude Code, Gemini CLI, Codex CLI, Cursor, Copilot e AntiGravity.
- Comandos documentados como visão de design, sem garantia de implementação.
- Conteúdo sem acentuação em PT-BR.
- Escopo enciclopédico que colidia com a proposta “Fundamentals”.
- Ausência do contrato atual de lesson slug, `COURSE-BRIEF`, `curriculum.yaml`, assessments e rastreabilidade por commit.
- QA de 2024 não representava a base atual.

## Decisões de correção

- Reconstruir, em vez de fazer substituição textual sobre afirmações obsoletas.
- Reduzir o escopo a 12 aulas fundamentais e remeter temas avançados à trilha própria.
- Usar apenas comandos confirmados nos arquivos do snapshot.
- Separar identidade pública limpa (`lesson_id`) de nomes numerados no filesystem.
- Adicionar quizzes, projeto final, manifests e relatórios de validação.

## Completude após correção

- Basic info: completa.
- ICP: completo e cruzado com o contexto canônico AIOX.
- Objetivos: cinco objetivos mensuráveis, com progressão Bloom.
- Voz: definida como editorial genérica, sem simular pessoa real.
- Formato: definido.
- Comercial: explicitamente fora de escopo, sem números inventados.
- Métricas e restrições: definidas.
- Aprovação e fontes: registradas.
