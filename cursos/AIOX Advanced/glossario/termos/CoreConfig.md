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
  aiox_advanced: 130
  aiox_advanced_squads: 0
  total: 130
  counted_at: '2026-08-10'
---
# CoreConfig

Arquivo de configuração social do projeto, normalmente `core-config.yaml`, que liga ou desliga extensões e composições do framework e registra quais capacidades estão ativas.

## Como é usado

Use **CoreConfig** para declarar uma capacidade do framework e sua ativação no projeto. Antes de adicionar uma regra, separe a jurisdição: CoreConfig configura extensões; [[Constitution]] governa comportamento; [[CLAUDE md]] descreve a física, a stack e o contexto do projeto.

**Exemplo prático:** na aula [[06-code-rabbit-boost]], abra `.aiox-core/core-config.yaml` e confirme `coderabbit_integration.enable: true`; se estiver `false`, o reviewer foi instalado, mas o gate não está ativo no pipeline.

**Não confunda:** **CoreConfig** não é [[CLAUDE md]] nem [[Constitution]]. Ele não substitui as leis da física do projeto nem os artigos de comportamento; seu papel é configurar quais extensões e integrações participam do sistema.

**Frequência nos cursos:** **130** menções (AIOX Advanced: 130 · AIOX Advanced Squads: 0).

## Aulas

- [[25-core-config-leis-sociais]]
- [[03-claude-md-leis-da-fisica]]
- [[06-code-rabbit-boost]]

## Ver também

- [[CLAUDE md]]
- [[Constitution]]
- [[Gate]]
- [[Composição]]
- [[Glossário AIOX Advanced]]
