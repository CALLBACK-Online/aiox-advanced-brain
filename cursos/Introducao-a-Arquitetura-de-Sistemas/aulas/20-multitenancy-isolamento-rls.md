---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: multitenancy-isolamento-rls
lesson_position: 20
module: M7
sequence: M7.2
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [supabase-rls]
---

# Multi-tenancy, isolamento e RLS

## Resultado

Você identifica a fronteira de cada cliente e projeta defesa contra leitura ou alteração cruzada de dados.

## Mapa visual

```text
Plataforma compartilhada
├── tenant A → usuários, projetos e dados A
└── tenant B → usuários, projetos e dados B

Request + identidade + tenant
          ↓
backend autoriza
          ↓
RLS reforça filtro por linha no banco
```

## Modelo mental

**Tenant** é uma organização ou cliente com fronteira de dados, configuração e operação. **Multi-tenancy** compartilha parte da plataforma entre tenants, exigindo isolamento explícito.

O isolamento pode ocorrer por linha, schema, banco, projeto ou infraestrutura separada. Quanto maior o isolamento, maior tende a ser o custo operacional; quanto mais compartilhamento, mais rigor exige cada consulta, cache, fila, storage e log.

**RLS** aplica políticas no banco que filtram linhas conforme identidade e regra. É defesa em profundidade: não substitui modelagem de autorização, mas reduz o dano de uma consulta esquecida.

## Quando usar — e quando não usar

Defina tenant desde a primeira entidade se o produto atende organizações distintas. Propague contexto do tenant por request e job. Teste negação cruzada. Use RLS em schemas expostos e políticas mínimas.

Não aceite `tenant_id` enviado pelo cliente sem validar associação. Não use cache sem tenant na chave. Não processe jobs sem identidade do tenant. E não presuma que RLS protege credencial administrativa que a ignora.

## Caso rápido

`GET /projetos` recebe token do usuário. O backend resolve memberships; o banco aplica policy ligando `auth.uid()` à organização. Um teste tenta acessar ID conhecido de outro tenant e precisa falhar, mesmo que a interface nunca mostre esse ID.

Anti-padrão: filtro `WHERE tenant_id = ?` em 99 endpoints. O centésimo vazará; crie camadas de defesa e testes.

## Prática

Desenhe a fronteira de tenant em banco, cache, fila, storage e observabilidade. Crie três testes negativos: leitura, alteração e job cruzado.

## Pergunte ao seu agente

```text
Revise isolamento multi-tenant ponta a ponta. Procure tenant ausente em tabela, cache key, evento, job, path de storage e log. Proponha testes negativos e política RLS sem usar service role no cliente.
```

## Evidência de conclusão

Mapa de propagação do tenant e testes que provam negação cruzada em todas as superfícies de estado.

Fonte: [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security).

[Anterior](19-autenticacao-autorizacao-secrets.md) · [Próxima: estilos arquiteturais](21-monolito-modulos-microsservicos.md)
