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
  aiox_advanced: 24
  aiox_advanced_squads: 0
  total: 24
  counted_at: '2026-08-10'
---
# Service role

Chave administrativa privilegiada do Supabase, destinada a uso exclusivo em servidor confiável. No AIOX, serve para jobs e operações administrativas no server — nunca é uma chave para distribuir ao client.

## Como é usado

Use **Service role** somente no lado servidor e mantenha-a fora do bundle do browser, do mobile client e de variáveis públicas como `NEXT_PUBLIC_`. Para o fluxo de usuário, use as identidades e policies adequadas; para jobs ou admin, registre o dono, o ambiente e a evidência do acesso.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], o anti-padrão é o Dev colocar a service role no client, testar o happy path e marcar done; depois de dois tenants pode haver vazamento. A rota segura é mover a operação para o server, manter RLS no mesmo ciclo do schema e testar dois usuários. A aula [[71-vercel-deploy]] reforça que service role e outras chaves privadas são server only.

**Não confunda:** **Service role** não é `anon`, não é o usuário `authenticated` e não é uma solução para policy faltante. “Funciona no client” não significa “está seguro”. **Alerta de segurança:** service role no browser é veto; se a chave apareceu em bundle, `NEXT_PUBLIC_` ou fluxo mobile, pare o ship e redesenhe a fronteira antes de continuar.

**Frequência nos cursos:** **24** menções (AIOX Advanced: 24 · AIOX Advanced Squads: 0).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[71-vercel-deploy]]
- [[73-prontidao-de-producao]]

## Ver também

- [[Supabase]]
- [[RLS]]
- [[Autenticação e Autorização]]
- [[Tenant isolation]]
- [[Data contract]]
- [[Migration]]
- [[Glossário AIOX Advanced]]
