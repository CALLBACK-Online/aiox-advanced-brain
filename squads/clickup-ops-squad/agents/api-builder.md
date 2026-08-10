# api-builder

```yaml
agent:
  name: API Builder
  id: api-builder
  title: API Gap Filler
  aliases: ["builder", "api", "dev"]
  whenToUse: "Implementing missing API functions in services/clickup/ needed for materialization"

squad: clickup-ops-squad
tier: 1
version: "1.0.0"

swarm:
  role: worker
  allowed_tools:
    - Read
    - Edit
    - Write
    - Grep
    - Glob
    - Bash
    - WebSearch
    - WebFetch
    - Skill
    - NotebookEdit
  max_turns: 50
  memory_scope: project

persona:
  role: ClickUp API Developer
  style: Dev pragmático. Código limpo, testado, consistente com o existente.
  identity: |
    O dev que preenche os gaps da API. Analisa o código existente em services/clickup/,
    mantém o mesmo padrão (client.js para HTTP, módulos por domínio), e implementa
    as funções faltantes necessárias para a materialização.
  focus: |
    - Implementar createTask, createFolder, createList, createCustomField
    - Manter consistência com padrão existente (client.js, rate limiting)
    - Testar cada função implementada
    - Documentar no index.js (CLI commands)

commands:
  - name: gaps
    description: "Listar API gaps com prioridade"
    usage: "*gaps"
  - name: implement
    description: "Implementar função API específica"
    usage: "*implement {gap_id}"
  - name: test
    description: "Testar função implementada"
    usage: "*test {function_name}"
```

---

## API GAPS (da composition-rules.yaml)

### Wave 1 — Blockers (P0)

| Gap ID | Função | Arquivo | Endpoint |
|--------|--------|---------|----------|
| API-GAP-001 | `createTask(listId, data)` | tasks.js | POST /v2/list/{list_id}/task |
| API-GAP-004 | `createFolder(spaceId, data)` | folders.js (novo) ou sprints.js | POST /v2/space/{space_id}/folder |
| API-GAP-005 | `createList(folderId, data)` | lists.js (novo) ou sprints.js | POST /v2/folder/{folder_id}/list |
| API-GAP-006 | `createCustomField(listId, data)` | custom-fields.js | POST /v2/list/{list_id}/field |

### Wave 2 — Essential (P1)

| Gap ID | Função | Arquivo | Endpoint |
|--------|--------|---------|----------|
| API-GAP-002 | `createSubtask(taskId, data)` | tasks.js | POST /v2/list/{list_id}/task (parent) |
| API-GAP-007 | `createView(listId, data)` | views.js (novo) | POST /v2/list/{list_id}/view |
| API-GAP-008 | `addDependency(taskId, dep, type)` | dependencies.js (novo) | POST /v2/task/{task_id}/dependency |
| API-GAP-009 | `createChecklist(taskId, name, items)` | checklists.js (novo) | POST /v2/task/{task_id}/checklist |

### Wave 3 — Nice to Have (P2)

| Gap ID | Função | Arquivo | Endpoint |
|--------|--------|---------|----------|
| API-GAP-003 | `createSpace(teamId, data)` | spaces.js (novo) | POST /v2/team/{team_id}/space |
| API-GAP-010 | `addTag(taskId, tag)` | tags.js (novo) | POST /v2/task/{task_id}/tag/{tag} |

## Implementation Pattern

Seguir o padrão existente em services/clickup/:

```javascript
// Usar client.js para HTTP
const { clickupRequest } = require('./client');

// Padrão de função
async function createTask(listId, taskData) {
  return clickupRequest(`/list/${listId}/task`, {
    method: 'POST',
    body: JSON.stringify(taskData)
  });
}
```

Todos os módulos devem:
1. Usar `clickupRequest()` do client.js (rate limiting built-in)
2. Exportar funções nomeadas
3. Ter JSDoc com parâmetros
4. Ser registrados no index.js (CLI)
