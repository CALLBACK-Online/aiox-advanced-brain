# Task: Fill API Gaps

## Metadata

```yaml
task: fill-api-gaps
atomic_layer: Molecule
responsavel_type: Agent
agent: api-builder
```

## Description

Implementar funções API faltantes em `services/clickup/` necessárias para materialização.

## Entrada

- `clickup-composition-rules.yaml → api_implementation_gaps`
- `services/clickup/` — código existente como referência de padrão

## Saída

- Funções implementadas em services/clickup/
- Testes básicos passando
- CLI commands registrados em index.js

## Implementation Order

### Wave 1 — Blockers (P0)

1. **createTask** em `tasks.js`
   - Endpoint: POST /v2/list/{list_id}/task
   - Payload: name, description, assignees, status, priority, due_date, tags, custom_fields, points

2. **createFolder** — generalizar `createSprintFolder` de `sprints.js`
   - Extrair para módulo próprio ou generalizar
   - Endpoint: POST /v2/space/{space_id}/folder

3. **createList** — generalizar `createList` de `sprints.js`
   - Adicionar suporte a status workflow no payload
   - Endpoint: POST /v2/folder/{folder_id}/list

4. **createCustomField** em `custom-fields.js`
   - Endpoint: POST /v2/list/{list_id}/field
   - Suportar todos os tipos: dropdown, number, text, date, currency, checkbox, users, labels

### Wave 2 — Essential (P1)

5. **createSubtask** em `tasks.js` (task com parent)
6. **createView** em novo `views.js`
7. **addDependency** em novo `dependencies.js`
8. **createChecklist** em novo `checklists.js`

## Pre-Conditions

- [ ] Acesso ao CLICKUP_API_KEY configurado
- [ ] Entendimento do padrão client.js (rate limiting, retry)

## Post-Conditions

- [ ] Funções Wave 1 implementadas e testadas
- [ ] CLI commands funcionando (`node services/clickup create-task ...`)
