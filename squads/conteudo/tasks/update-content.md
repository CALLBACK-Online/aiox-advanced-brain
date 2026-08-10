# Update Content Squad

**Task ID:** `update-content`
**Pattern:** HO-TP-001 (Task Anatomy Standard)
**Version:** 1.0.0
**Last Updated:** 2026-03-16

---

## Task Anatomy

| Field | Value |
|-------|-------|
| **task_name** | Update Content Squad |
| **status** | `pending` |
| **responsible_executor** | @squad-chief ou @content-chief |
| **execution_type** | `Hybrid` |
| **input** | Mudancas desejadas (novos agents, tasks, workflows, data) |
| **output** | Squad atualizado + CHANGELOG bumped + validate-squad PASS |
| **action_items** | 6 steps |
| **acceptance_criteria** | 4 criteria |

---

## Overview

Task de brownfield update para o squad conteudo. Permite adicionar novos agents, tasks, workflows, data files ou atualizar os existentes mantendo compatibilidade retroativa.

---

## Input

- **change_request** (text) — Descricao das mudancas desejadas
  - Required: Yes
- **new_sources** (files, optional) — Novos materiais de referencia
  - Required: No
- **existing_squad** (path) — `squads/_conteudo/`
  - Required: Yes (auto-detected)

## Output

- **updated_files** — Arquivos modificados ou criados
- **changelog_entry** — Nova entrada no CHANGELOG.md
- **validation_report** — Resultado do validate-squad

---

## Action Items

### Step 1: Auditar Estado Atual

- Ler config.yaml para entender versao e estrutura atual
- Ler CHANGELOG.md para historico
- Identificar o que sera afetado pela mudanca

### Step 2: Planejar Mudancas

- Mapear arquivos a criar/editar
- Verificar se mudanca nao quebra workflows existentes
- Definir nova versao (semver: patch/minor/major)

### Step 3: Executar Mudancas

- Criar/editar arquivos conforme plano
- Se novo agent: seguir agent-tmpl.md do squad-creator
- Se nova task: seguir task-tmpl.md do squad-creator
- Se novo workflow: seguir workflow-tmpl.yaml

### Step 4: Atualizar Metadados

- Bumpar version no config.yaml
- Adicionar entrada no CHANGELOG.md
- Atualizar README.md se necessario (tabela de agents/tasks)

### Step 5: Atualizar config.yaml

- Adicionar novos agents/tasks/workflows/checklists a lista no config.yaml

### Step 6: Validar

- Executar `*validate-squad _conteudo`
- Garantir score PASS
- Se FAIL: corrigir issues e re-validar

---

## Acceptance Criteria

- [ ] **AC-1:** Todos os arquivos novos/editados existem no filesystem
- [ ] **AC-2:** config.yaml reflete a nova versao e lista todos os components
- [ ] **AC-3:** CHANGELOG.md tem entrada para esta versao
- [ ] **AC-4:** validate-squad retorna PASS

---

## Veto Conditions

- Editar agents existentes sem ler o original primeiro
- Criar arquivo sem usar template do squad-creator
- Bumpar versao sem entrada no CHANGELOG
- Declarar update completo sem rodar validate-squad

---

## Handoff

| Attribute | Value |
|-----------|-------|
| **Next Task** | `validate-content` (se conteudo foi criado) |
| **Trigger** | Update completo |
| **Executor** | @content-validator |

---

_Task Version: 1.0.0_
_Pattern: HO-TP-001 (Task Anatomy Standard)_
_Last Updated: 2026-03-16_
