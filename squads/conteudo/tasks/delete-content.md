# Delete Content Component

**Task ID:** `delete-content`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-03-16

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Delete Content Component |
| **status** | `pending` |
| **responsible_executor** | @squad-chief ou @content-chief |
| **execution_type** | `Hybrid` |
| **input** | Component a remover (agent, task, workflow, data) |
| **output** | Squad limpo + config atualizado + CHANGELOG bumped |
| **action_items** | 5 steps |
| **acceptance_criteria** | 4 criteria |

---

## Overview

Task de cleanup para remover components obsoletos do squad conteudo. Remove arquivos, atualiza config.yaml, atualiza README e registra no CHANGELOG.

---

## Input

- **component_type** (enum) — Tipo: agent | task | workflow | checklist | data
  - Required: Yes
- **component_name** (text) — Nome do component a remover
  - Required: Yes
- **reason** (text) — Justificativa da remocao
  - Required: Yes

## Output

- **deleted_files** — Lista de arquivos removidos
- **updated_config** — config.yaml atualizado (sem o component)
- **changelog_entry** — Entrada de remocao no CHANGELOG.md

---

## Action Items

### Step 1: Verificar Dependencias

- Buscar referencias ao component em outros agents, tasks, workflows
- Se referenciado: ALERTAR e listar dependentes
- Se nao referenciado: prosseguir com remocao

### Step 2: Confirmar Remocao

- Apresentar ao usuario: component, dependencias encontradas, impacto
- Aguardar confirmacao explicita
- VETO: nunca remover sem confirmacao do usuario

### Step 3: Executar Remocao

- Deletar arquivo do component
- Se agent: remover entrada de agents[] no config.yaml
- Se task: remover entrada de tasks[] no config.yaml
- Se workflow: remover entrada de workflows[] no config.yaml
- Se checklist: remover entrada de checklists[] no config.yaml
- Se data: remover da lista data[] no config.yaml

### Step 4: Atualizar Documentacao

- Atualizar README.md (remover da tabela de components)
- Adicionar entrada no CHANGELOG.md com `### Removed`
- Bumpar version (patch se component menor, minor se significativo)

### Step 5: Validar

- Executar `*validate-squad _conteudo`
- Garantir que cross-references nao estao quebradas
- Score PASS obrigatorio

---

## Acceptance Criteria

- [ ] **AC-1:** Arquivo do component deletado do filesystem
- [ ] **AC-2:** config.yaml nao lista mais o component
- [ ] **AC-3:** CHANGELOG.md registra a remocao com justificativa
- [ ] **AC-4:** validate-squad retorna PASS (zero cross-ref quebradas)

---

## Veto Conditions

- Remover component sem verificar dependencias
- Remover sem confirmacao explicita do usuario
- Remover entry_agent (content-chief) — BLOQUEADO
- Declarar remocao completa sem rodar validate-squad

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-03-16_
