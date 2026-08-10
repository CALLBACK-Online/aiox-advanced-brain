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
  aiox_advanced: 1
  aiox_advanced_squads: 0
  total: 1
  counted_at: '2026-08-10'
---
# Data contract

Contrato de dados entre o solo de dados e quem o consome: explicita o que o app pode ler e escrever sem contornar policy. Ele transforma schema, policies e operações permitidas em uma fronteira consumível pelo Dev e pela aplicação.

## Como é usado

Use **Data contract** quando uma entidade, API ou relação precisar ser consumida por outro componente: registre a forma dos dados junto com as leituras e escritas permitidas, o responsável pelo solo e as policies que sustentam o acesso. O contrato deve ser consumido pela feature; se estiver errado, volte ao data-engineer em vez de usar uma chave privilegiada para contorná-lo.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], a tabela `proposals` tem schema e RLS definidos; o Dev implementa as queries dentro do contrato e o teste com dois usuários prova que A não lê ou escreve o que é de B. A evidência é schema + policy + migration + teste, não apenas um happy path da UI.

**Não confunda:** **Data contract** não é apenas o [[Schema]]: schema diz quais entidades e relações existem; data contract diz como o app pode usá-las. Também não é uma autorização abstrata nem substitui [[RLS]] — o contrato documenta a fronteira, enquanto a policy deve efetivamente liberar ou negar a linha/ação. **Alerta de segurança:** nunca resolva contrato incorreto liberando `select *`, policy permissiva ou [[Service role]] no client.

**Frequência nos cursos:** **1** menção (AIOX Advanced: 1 · AIOX Advanced Squads: 0).

## Aulas

- [[70-supabase-via-data-engineer]]
- [[68-squad-fora-do-claude-code]]

## Ver também

- [[Schema]]
- [[Contrato de API]]
- [[RLS]]
- [[Migration]]
- [[Service role]]
- [[Glossário AIOX Advanced]]
