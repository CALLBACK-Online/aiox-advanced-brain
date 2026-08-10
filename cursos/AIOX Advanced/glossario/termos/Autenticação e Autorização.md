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
  aiox_advanced: 15
  aiox_advanced_squads: 7
  total: 22
  counted_at: '2026-08-10'
---
# Autenticação e Autorização

Duas decisões diferentes de acesso: **autenticação** verifica quem é a pessoa ou sistema; **autorização** decide o que essa identidade pode fazer, em qual tenant e sob qual role. No AIOX, as duas entram no contrato da API e nas policies de dados.

## Como é usado

Use **Autenticação e Autorização** em sequência: identifique o chamador e depois aplique permissão explícita por usuário, tenant, role e operação. No Supabase, `auth.uid()` e claims de tenant sustentam policies RLS; valide com usuários distintos e registre a diferença entre acesso permitido e negado.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], o usuário A autenticado pode ler suas propostas conforme a policy, enquanto o usuário B não pode ler as linhas de A. Na aula [[68-squad-fora-do-claude-code]], o contrato do job registra quem pode disparar a execução por tenant e role, além do schema, estados e erros.

**Não confunda:** **autenticado** não significa **autorizado**: login não libera qualquer linha, job ou ação. Autorização também não é esconder botão na UI; a regra precisa valer na fronteira de dados, com [[RLS]] e teste dos dois usuários. **Alerta de segurança:** não use [[Service role]] no browser como atalho para fazer um fluxo autenticado funcionar; a chave privilegiada é server-only.

**Frequência nos cursos:** **22** menções (AIOX Advanced: 15 · AIOX Advanced Squads: 7).

## Aulas

- [[13-pensamento-estruturado-antes-do-terminal]]
- [[68-squad-fora-do-claude-code]]
- [[70-supabase-via-data-engineer]]
- [[73-prontidao-de-producao]]

## Ver também

- [[RLS]]
- [[Tenant isolation]]
- [[Service role]]
- [[Contrato de API]]
- [[Supabase]]
- [[Glossário AIOX Advanced]]
