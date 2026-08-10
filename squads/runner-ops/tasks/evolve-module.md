# Task: evolve-module

> Process: RP-EVOLVE-MODULE | Mode: CONFIGURAR | Version: 1.0.0
> Owner: runner-architect | Executor: Agent

## Purpose

Adicionar, modificar ou deprecar um módulo no runner-lib framework.
Mantém retrocompatibilidade e atualiza documentação automaticamente.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `action` | ✅ | `add`, `modify`, `deprecate` |
| `module_name` | ✅ | Nome do módulo (ex: `retry-logic`, `cost-tracking`) |
| `rationale` | ✅ | Por que essa mudança é necessária (ADR justification) |
| `breaking_change` | ✅ | `true` / `false` — afeta runners existentes? |

## Veto Conditions

- **BLOCKER:** `breaking_change: true` sem migration guide → STOP
- **BLOCKER:** Modificar módulo sem rodar validate-runner em todos os runners que o usam → STOP
- **BLOCKER:** Deprecar módulo sem replacement documentado → STOP
- **WARN:** Novo módulo duplica funcionalidade existente → justificar ou recusar

## Execution by Action

### ADD new module

```bash
# 1. Criar módulo em runner-lib
cp infrastructure/scripts/runner-lib/templates/module-template.sh \
   infrastructure/scripts/runner-lib/{module_name}.sh

# 2. Exportar função principal
# 3. Adicionar ao pipeline-bootstrap.sh (source list)
# 4. Adicionar ao module-index.yaml
# 5. Criar teste básico em runner-lib/tests/
# 6. Atualizar runner-lib/README.md
```

### MODIFY existing module

```bash
# 1. Criar ADR: docs/adr/ADR-{N}-{module_name}-evolution.md
# 2. Implementar mudança com backward compat (se possível)
# 3. Se breaking: criar migration guide
# 4. Rodar validate-runner em todos runners afetados
# 5. Bump version em module-index.yaml
```

### DEPRECATE module

```bash
# 1. Marcar como deprecated em module-index.yaml
# 2. Adicionar deprecation warning na função
# 3. Documentar replacement
# 4. Definir sunset date (mínimo 30 dias)
# 5. Criar migration task para runners afetados
```

## ADR Template (required for all evolutions)

```markdown
# ADR-{N}: {Module Name} Evolution

## Status: Proposed | Accepted | Deprecated

## Context
{Por que essa mudança é necessária}

## Decision
{O que foi decidido}

## Consequences
- Positive: {benefícios}
- Negative: {tradeoffs}
- Runners affected: {lista}
```

## Completion Criteria

- [ ] Módulo criado/modificado/deprecado em `infrastructure/scripts/runner-lib/`
- [ ] ADR criado em `docs/adr/`
- [ ] `module-index.yaml` atualizado
- [ ] `pipeline-bootstrap.sh` atualizado (se necessário)
- [ ] Teste básico passando
- [ ] Migration guide criado (se breaking change)
- [ ] README.md atualizado

## Handoff

- **ADD/MODIFY →** runner-validator para validar impacto nos runners existentes
- **DEPRECATE →** runner-integrator para criar plano de migração dos runners afetados
- **Sempre →** runner-chief com ADR aprovado
