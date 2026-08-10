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
  aiox_advanced: 3
  aiox_advanced_squads: 0
  total: 3
  counted_at: '2026-08-10'
---
# Tenant isolation

Isolamento entre tenants: fronteira que impede um cliente, organização ou tenant de ler ou escrever dados e estado pertencentes a outro. No AIOX, tenant é a unidade de isolamento acima do usuário quando há operação multi-org.

## Como é usado

Use **Tenant isolation** desde o primeiro desenho de um produto multi-tenant: modele a unidade de isolamento, carregue essa fronteira no contrato e faça as policies RLS filtrarem por usuário ou tenant. Valide com dois usuários e dois tenants antes de chamar a feature de pronta.

**Exemplo prático:** na aula [[70-supabase-via-data-engineer]], a tabela `proposals` começa com `user_id` e evolui para isolamento por `org_id` quando há multi-org; a policy usa a identidade e claims disponíveis, e o teste prova que A não lê a linha de B. Na aula [[68-squad-fora-do-claude-code]], usar o mesmo store, vector store ou banco para clientes diferentes sem isolamento aparece como bloqueio de extração.

**Não confunda:** **Tenant isolation** não é apenas ter login, separar ambientes local/staging/production ou chamar o produto de [[SaaS]]. Também não é um filtro aplicado só na tela: precisa existir no acesso aos dados e no estado do job. **Alerta de segurança:** sem RLS ou com policy permissiva demais, a API pública vira canal de vazamento; interrompa o ship até haver policy e evidência dos dois usuários/tenants.

**Frequência nos cursos:** **3** menções (AIOX Advanced: 3 · AIOX Advanced Squads: 0).

## Aulas

- [[68-squad-fora-do-claude-code]]
- [[69-escada-progressiva-script-a-saas]]
- [[70-supabase-via-data-engineer]]
- [[73-prontidao-de-producao]]

## Ver também

- [[RLS]]
- [[Autenticação e Autorização]]
- [[Service role]]
- [[Data contract]]
- [[Supabase]]
- [[SaaS]]
- [[Glossário AIOX Advanced]]
