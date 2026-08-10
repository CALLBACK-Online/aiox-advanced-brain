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
  aiox_advanced: 100
  aiox_advanced_squads: 2
  total: 102
  counted_at: '2026-08-10'
---
# Memória

Camada 4 da anatomia do agente: fatos, padrões e contexto que atravessam turnos ou handoffs. Ela evita que o agente recomece do zero, mas precisa de uma fonte confiável e atualização.

## Como é usado

Use **Memória** para persistir decisões, restrições e contexto que o próximo turno ou agente precisa recuperar sem repetir toda a investigação.

**Exemplo prático:** na aula [[14-anatomia-do-agente]], depois de decidir a estratégia de migração, registre a decisão, as restrições e as pendências no artefato de handoff; o próximo agente lê esse contexto antes de continuar.

**Não confunda:** **Memória** não é a janela inteira de contexto nem substitui a fonte de verdade; informação antiga ou não registrada pode induzir o próximo turno ao erro. Quando o agente não faz o esperado, o diagnóstico da aula é abrir o arquivo e conferir as 4 camadas — memória desatualizada é causa tão comum quanto persona genérica ou autoridade faltando.

**Frequência nos cursos:** **102** menções (AIOX Advanced: 100 · AIOX Advanced Squads: 2).

## Aulas

- [[14-anatomia-do-agente]]

## Ver também

- [[Anatomia do Agente]]
- [[Persona]]
- [[Autoridade]]
- [[Squad]]
- [[Glossário AIOX Advanced]]
