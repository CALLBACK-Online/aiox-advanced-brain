# Task: Bootstrap Mission Infrastructure

## Metadata

```yaml
task: bootstrap-mission
atomic_layer: Organism
responsavel_type: Agent
agent: clickup-chief (orchestration) + materializer (execution) + playwright-ops (automations)
command: "*bootstrap --mission"
idempotent: true
architecture: "Clean — List única dentro de Ops Folder"
```

## Description

Setup one-time da infraestrutura ClickUp para suportar Missions SINKRA.
Cria a List "Missions" dentro do Folder de Ops, Task Types (Mission, Gate),
Custom Fields e Automações base.
**Idempotente:** re-executar valida/corrige sem duplicar.

## Entrada

- Nenhum input externo necessário — usa `mission-clickup-spec.yaml` como referência
- `workspace_id` — lookup from tokenization.yaml
- Ops Folder deve existir

## Saída

- List "Missions" criada dentro do Ops Folder (ou validada se já existe)
- Task Types configurados: Mission, Gate
- Custom Fields configurados na List
- Custom Field universal "Task Status" (se não existir)
- Views padrão configuradas
- Automações base ativas
- `clickup-tokenization.yaml` atualizado
- Relatório de bootstrap (YAML)

## Pre-Conditions

- [ ] API client `services/clickup/` operacional
- [ ] Workspace ID configurado (lookup from tokenization.yaml)
- [ ] Ops Folder existe no ClickUp
- [ ] `mission-clickup-spec.yaml` disponível em `squads/clickup-ops-squad/data/`
- [ ] Task Type IDs registrados em `clickup-tokenization.yaml`: Mission (`custom_item_id` do spoke), Gate (`custom_item_id` do spoke). Estes IDs devem existir antes da materialização — `materialize-mission.js` usa o campo `custom_item` da API para atribuir Task Types programaticamente.

## Steps

### Step 1 — Resolver Ops Folder

```yaml
action: resolve_folder
name: "{ops_folder_name}"  # Lookup from spoke tokenization
workspace_id: "{workspace_id}"  # Lookup from tokenization.yaml
logic: |
  1. GET /team/{workspace_id}/space → listar spaces
  2. Para cada space → GET /space/{space_id}/folder → buscar Ops Folder
  3. Se não existe → BLOCK (criar manualmente ou escalar)
  4. Se existe → usar folder_id
```

### Step 2 — Criar List "Missions"

```yaml
action: create_list
folder_id: "{from step 1}"
name: "Missions"
statuses:
  - name: "Shaped"
    color: "#d3d3d3"
  - name: "Approved"
    color: "#4194f6"
  - name: "Active"
    color: "#f9d900"
  - name: "Complete"
    color: "#6bc950"
  - name: "Cancelled"
    color: "#e50000"
logic: |
  1. GET /folder/{folder_id}/list → buscar list com name "Missions"
  2. Se existe → usar list_id existente (idempotente)
  3. Se não existe → POST /folder/{folder_id}/list com name e statuses
  4. Registrar list_id
note: "Statuses da List = lifecycle da Mission (Shaped → Complete | Cancelled)"
```

### Step 3 — Criar Task Types

```yaml
action: create_task_types
list_id: "{from step 2}"
task_types:
  - name: "Mission"
    description: "Entidade pai — representa uma mission completa com DAG de subtasks"
  - name: "Gate"
    description: "Checkpoint go/no-go entre fases do DAG"
logic: |
  1. Verificar Task Types existentes na list
  2. Se "Mission" não existe → criar via API/Playwright
  3. Se "Gate" não existe → criar via API/Playwright
  4. "Task" (default) já existe — não precisa criar
note: "Task Types são feature do ClickUp que permite categorizar tasks visualmente"
implementation: playwright  # Task Types são UI-only no ClickUp
```

### Step 4 — Criar/Validar Custom Fields

```yaml
action: create_custom_fields
list_id: "{from step 2}"
fields:
  # Universal (verificar se já existe no workspace)
  - name: "Task Status"
    type: dropdown
    options: ["To Do", "In Progress", "Review", "Done", "Blocked"]
    scope: universal
    note: "Se já existe em outro lugar do workspace, reutilizar"

  # Mission-level
  - name: "Mission ID"
    type: short_text
    required: true

  - name: "Timebox"
    type: dropdown
    options: ["2 semanas", "6 semanas"]
    note: "Renomeado de 'Appetite' para 'Timebox'"

  # DEPRECATED: "Appetite Deadline" removido — substituído por due date nativo do ClickUp

  - name: "Circuit Breaker"
    type: dropdown
    options: ["Active", "Extended", "Triggered"]

  - name: "Ponto A"
    type: text

  - name: "Ponto B"
    type: text

  # Subtask-level
  - name: "Phase"
    type: number
    required: true

  - name: "Executor Type"
    type: dropdown
    options: ["Human", "Agent", "Worker", "Clone"]

  - name: "Source Squad"
    type: short_text

  # Gate-level
  - name: "Gate Score"
    type: number

  # Relationship
  - name: "Relacionado a"
    type: relationship
    note: "Para vincular mission a projeto/produto/cliente"

logic: |
  Para cada field:
  1. GET /list/{list_id}/field → buscar fields existentes
  2. Se field com mesmo nome existe → skip (idempotente)
  3. Se não existe → POST /list/{list_id}/field
  4. Registrar field_id em tokenization
```

### Step 5 — Configurar Views

```yaml
action: create_views
list_id: "{from step 2}"
views:
  - name: "Gantt"
    type: Gantt
    group_by: "parent task (Mission)"
    show_dependencies: true
    show_subtasks: true

  - name: "Board"
    type: Board
    group_by: "Status"

  - name: "Missions por Status"
    type: List
    filter: "Task Type = Mission"
    group_by: "Status"

implementation: playwright  # Views são UI-only
```

### Step 6 — Configurar Automações

```yaml
action: create_automations
list_id: "{from step 2}"
automations:
  # DEPRECATED: "Appetite Deadline Alert" removido — substituído por notificação nativa de due date overdue do ClickUp.

  - name: "Circuit Breaker Extension"
    trigger: "Circuit Breaker mudou para Extended"
    action: "Due date += 50%"

  - name: "All Subtasks Done"
    trigger: "Todas subtasks Done + todos Gates com checklist completo"
    action: "Mover Mission para Complete"

implementation: playwright
```

### Step 7 — Atualizar Tokenization

```yaml
action: update_registry
file: "squads/sinkra-squad/data/clickup-tokenization.yaml"
section: "missions"
register:
  folder_id: "{Ops folder_id}"
  list_id: "{Missions list_id}"
  task_types: ["Mission", "Gate"]
  custom_field_ids: "{map de field_name → field_id}"
  automations: "{list de automation names}"
  bootstrap_date: "{YYYY-MM-DD}"
  bootstrap_status: "COMPLETE"
```

### Step 8 — Gerar Relatório

```yaml
action: generate_report
output: "squads/clickup-ops-squad/output/bootstrap-mission-report.yaml"
content:
  list_created_or_found: "{list_id}"
  task_types_created: ["Mission", "Gate"]
  custom_fields_created: "{count}"
  views_created: "{count}"
  automations_created: "{count}"
  tokenization_updated: true
  status: "COMPLETE"
  next_step: "Executar *create-mission {handoff-path}"
```

## Post-Conditions

- [ ] List "Missions" existe dentro do Ops Folder (verificado via API)
- [ ] Task Types Mission e Gate configurados
- [ ] Custom Fields existem na List (verificado via API)
- [ ] Custom Field "Task Status" universal existe
- [ ] Tokenization atualizado com todos IDs
- [ ] Relatório de bootstrap gerado

## Performance

- SLA: 10 minutos (API) + 20 minutos (Playwright: Task Types, Views, Automações)
- Escalação: Se Ops Folder não existe → escalar para humano
- Re-execução: Segura — idempotente por design
