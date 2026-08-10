# Task: Delete Squad Artifact Surface

## Task Anatomy

| Field | Value |
|-------|-------|
| **Task ID** | `delete-squad` |
| **Version** | `1.0.0` |
| **Status** | `active` |
| **Responsible Executor** | `squad-chief` |
| **Execution Type** | `Hybrid` |

## Metadata

```yaml
id: delete-squad
name: "Delete Squad Artifact Surface"
category: maintenance
agent: squad-chief
elicit: true
autonomous: false
description: "Executa a retirada controlada de um squad do ecossistema, com backup, trilha auditavel e atualizacao de registries."
accountability:
  human: squad-operator
  scope: full
domain: Tactical

```


<!-- SINKRA_CONTRACT -->
Domain: `Tactical`
atomic_layer: Atom
Input: request::delete_squad
Output: artifact::delete_squad
pre_condition: squad_name fornecido AND squad existe AND confirmação do usuário para scope (artifacts/runtime/full)
post_condition: squad retirado do ecossistema com backup, registries atualizados e trilha auditável persistida
performance: < 15 min (Hybrid — backup + delete + registry update + user confirmation), reversível via backup
Completion Criteria: backup criado AND artifacts removidos per scope AND registries atualizados AND audit trail persistido
error_handling: fail-loud, persist error context, escalate to squad-chief
## Purpose

Oferecer um delete contextual para lifecycle do pack sem remocao cega. A task garante que qualquer retirada seja reversivel, auditavel e deliberada. Existe para cumprir o contrato de lifecycle do validator (structural completeness check).

## Command Contract

```text
*delete-squad {squad_name} [--scope artifacts|runtime|full] [--dry-run]
```

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `squad_name` | string | Yes | Nome do squad a remover |
| `scope` | enum | No | `artifacts` (apenas arquivos), `runtime` (apenas estado), `full` (ambos). Default: `full` |
| `dry_run` | boolean | No | Preview do blast radius sem executar |

## Workflow

### Step 1: Pre-flight Validation

1. Confirmar que `squads/{squad_name}/` existe
2. Verificar se o squad tem consumidores ativos no `ecosystem-registry.yaml`
3. Se consumidores ativos > 0 e `--force` nao fornecido, BLOCK com lista de dependentes

### Step 2: Backup

1. Criar backup comprimido: `backups/squads/pre-delete-{timestamp}/{squad_name}.tar.gz`
2. Validar integridade do backup (listar conteudo e comparar com fonte)
3. Registrar backup path no output

### Step 3: Elicitation — Confirmar Escopo

Apresentar ao operador:
- Blast radius: arquivos, registries, runtime state, IDE mirrors afetados
- Scope selecionado: `artifacts`, `runtime`, ou `full`
- Listar cada item a ser removido

**Aguardar confirmacao explicita antes de prosseguir.**

### Step 4: Execute Removal

Baseado no `scope`:

**artifacts:**
- Remover `squads/{squad_name}/`
- Remover IDE skill mirrors em `.claude/skills/` (se existirem)

**runtime:**
- Remover `.aiox/squad-runtime/{squad_name}/`
- Remover `.aiox/squad-runtime/create-squad/{squad_name}/`

**full:**
- Executar ambos `artifacts` + `runtime`

### Step 5: Registry Update

1. Remover entrada de `squads/sinkra-squad/data/ecosystem-registry.yaml`
2. Remover entrada de `squads/infra-ops-squad/data/service-catalog.yaml` (se existir)
3. Atualizar `.aiox-core/core/ecosystem/ecosystem-sync-config.yaml` (se referenciado)

### Step 6: Report

Gerar relatorio com:
- Squad removido
- Scope executado
- Backup path
- Registries atualizados
- Warnings (refs residuais, se houver)

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Backup | `backups/squads/pre-delete-{timestamp}/{squad_name}.tar.gz` | Backup completo do squad |
| Report | `runtime_context` | Relatorio da remocao |

## Veto Conditions

- Squad nao existe -> bloquear
- Backup falhou -> bloquear
- Confirmacao do operador nao obtida -> bloquear
- Squad e `squad-creator` (self-delete) -> bloquear

## Acceptance Criteria

- [ ] Backup criado e validado antes de qualquer remocao
- [ ] Escopo da remocao confirmado explicitamente pelo operador
- [ ] Registries atualizados (ecosystem-registry, service-catalog)
- [ ] Nenhum artefato ativo orfao permanece apos a remocao
- [ ] Report gerado com blast radius e resultado

## Related Documents

- `tasks/rename-squad.md`
- `tasks/upgrade-squad.md`
- `tasks/refresh-registry.md`

---

_Task Version: 1.0.0_
_Last Updated: 2026-04-12_
