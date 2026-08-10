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
  aiox_advanced: 96
  aiox_advanced_squads: 13
  total: 109
  counted_at: '2026-08-10'
---
# Schema

Estrutura formal dos dados: entidades, relações, campos, constraints e limites que dão forma ao modelo persistido. No AIOX, o schema deve seguir as entidades do produto e evoluir por [[Migration|migration]] versionada.

## Como é usado

Use **Schema** para modelar o solo de dados antes da query ou da tela: alinhe entidades e relações ao produto, defina constraints e aplique a mudança de forma reproduzível entre ambientes. Em dados sensíveis, crie o schema e a [[RLS]] no mesmo ciclo; tabela sem policy não está done.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], uma nova organização ou relação passa por schema, RLS e migration sob responsabilidade do data-engineer. Depois, o Dev consome types, views seguras ou RPCs definidos no contrato, sem remodelar o banco a partir da UI.

**Não confunda:** **Schema** descreve a forma das entidades e relações; [[Data contract|data contract]] descreve o que o app pode ler e escrever nessa forma, incluindo a fronteira de acesso. Schema também não é policy: ter colunas de `user_id` ou `org_id` não prova isolamento. **Alerta de segurança:** não publique uma tabela multi-user sem RLS explícita e teste de acesso permitido e negado.

**Frequência nos cursos:** **109** menções (AIOX Advanced: 96 · AIOX Advanced Squads: 13).

## Aulas

- [[24-entidade-como-unidade-de-processo]]
- [[05-ambientes-local-staging-production]]
- [[70-supabase-via-data-engineer]]

## Ver também

- [[Data contract]]
- [[Migration]]
- [[RLS]]
- [[Entidade]]
- [[Supabase]]
- [[Glossário AIOX Advanced]]
