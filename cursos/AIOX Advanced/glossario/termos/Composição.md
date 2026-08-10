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
  aiox_advanced: 20
  aiox_advanced_squads: 1
  total: 21
  counted_at: '2026-08-10'
---
# Composição

Direção em que as peças do AIOX se combinam em camadas: cada nível usa os elementos de baixo e entrega uma capacidade para o nível de cima, sem inverter responsabilidades nem inflar o primitivo escolhido.

## Como é usado

Use **Composição** para desenhar ou diagnosticar a hierarquia de uma capacidade. Na escala da aula, uma Skill agrupa Tasks, um Agente usa Skills, um Workflow orquestra Agentes e um Runner materializa o Workflow de forma determinística.

**Exemplo prático:** na aula [[28-taxonomia-task-skill-agent-workflow-runner]], validar um Story pode ser uma Task agrupada numa Skill, aplicada pelo agente `@qa` e encadeada no workflow `full-sdc`; criar um agente inteiro para uma única transformação seria composição inflada.

**Não confunda:** **Composição** é a relação entre camadas e responsabilidades; não é simplesmente decomposição de um problema nem uma lista de componentes. O sentido importa: o Workflow orquestra Agentes, enquanto o Runner executa o caminho já provado.

**Frequência nos cursos:** **21** menções (AIOX Advanced: 20 · AIOX Advanced Squads: 1).

## Aulas

- [[28-taxonomia-task-skill-agent-workflow-runner]]
- [[33-anatomia-de-um-squad]]
- [[29-sub-agents-vs-swarm-agents]]

## Ver também

- [[Task]]
- [[Skill]]
- [[Workflow]]
- [[Runner]]
- [[CoreConfig]]
- [[Glossário AIOX Advanced]]
