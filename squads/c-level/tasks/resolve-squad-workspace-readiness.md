# Task: Resolve Squad Workspace Readiness

task_id: resolve-squad-workspace-readiness
```yaml
task:
  task_id: resolve-squad-workspace-readiness
  id: resolve-squad-workspace-readiness
  name: Resolver Readiness de Workspace por Squad
  agent: coo-orchestrator
  responsavel_type: Agent
  trigger: manual
  elicit: false
  commands:
  - '*resolve-readiness {squad}'
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- workspace-readiness-report.yaml
pre_condition:
- Bootstrap executado ou contexto do business carregado.
post_condition:
- Decisão ou artefato registrado com handoff explícito para a próxima etapa.
performance:
- Responder sem inventar dados e escalar bloqueios estruturais imediatamente.
Error Handling:
- Escalar blockers estruturais imediatamente e interromper a execução quando o input canônico estiver inconsistente.
Completion Criteria:
- [ ] Output produzido no caminho esperado.
- [ ] Critérios de completude registrados.

## Descrição

Task canônica do `COO` para decidir se um squad consumidor pode operar com contexto suficiente de `workspace/`.

## Objetivo

1. Resolver readiness por `squad`.
2. Normalizar o resultado para um contrato único.
3. Bloquear, permitir draft ou liberar output final conforme as fontes canônicas disponíveis.

## Inputs

- `squad_slug`
- `business_slug`
- `product_slug`
- `app_id`
- `context_type`

## Contrato

Executar:

```bash
node squads/c-level/scripts/resolve-squad-workspace-readiness.cjs --squad={slug} [--business={slug}] [--product={slug}] [--app={id}] [--context-type={type}]
```

Status válidos:

- `ready`
- `draft`
- `blocked`
- `read_only`
- `not_applicable`

Saída mínima:

```yaml
owner: coo-orchestrator
squad_slug: string
context_type: string
status: ready|draft|blocked|read_only|not_applicable
reason: string
required_sources_loaded: []
missing_required_sources: []
allowed_write_paths: []
canonical_config_paths: []
```

## Regras

1. `design` usa contexto `design_system`.
2. `brand` usa contexto `brand`.
3. `copy` e `hormozi` usam contexto `product`.
4. `gerador-pop` usa contexto `operations`.
5. O registry canônico de squads, contexts e product consumers vive em `squads/c-level/config.yaml`.
6. O resolver do COO delega aos resolvers canônicos já existentes; não duplica regras locais.
7. `draft` permite exploração, mas não output final/canônico.
8. `blocked` interrompe a execução até corrigir as fontes faltantes.
9. `not_applicable` proíbe tratar ausência de setup como erro.

## Validação

- [ ] Resolver executa sem inventar pré-requisitos.
- [ ] Saída inclui `status`, `reason` e fontes faltantes.
- [ ] O squad consumidor consegue bloquear ou degradar para draft com base na saída.

---

*Task do Squad C-Level - COO Orchestrator*
