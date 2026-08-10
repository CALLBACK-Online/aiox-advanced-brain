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
  aiox_advanced: 55
  aiox_advanced_squads: 5
  total: 60
  counted_at: '2026-08-10'
---
# RLS

Row Level Security no Postgres/Supabase: política de quem lê/escreve cada linha. Gate de segurança de dados — não é opcional em production.

## Como é usado

Use **RLS** sempre que uma tabela contiver dados de mais de um usuário ou tenant: habilite Row Level Security e escreva políticas explícitas de leitura e escrita por linha — em produção, tabela exposta sem política é incidente, não detalhe.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], a tabela `orders` recebe a política `user_id = auth.uid()` via migration versionada; a verificação em staging loga com dois usuários distintos e confere que cada um enxerga apenas as próprias linhas — política e contagem ficam registradas como evidência.

**Não confunda:** não confunda **RLS** com filtro na aplicação: o `WHERE` no código some no primeiro endpoint esquecido; a política no banco vale para todo acesso — e precisa entrar por migration reproduzível, não por ajuste manual no painel.

**Frequência nos cursos:** **60** menções (AIOX Advanced: 55 · AIOX Advanced Squads: 5).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[73-prontidao-de-producao]]

## Ver também

- [[Supabase]]
- [[Migration]]
- [[Gate]]
- [[Glossário AIOX Advanced]]
