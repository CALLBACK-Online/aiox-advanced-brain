# Task: Create Mission (Materialize)

## Metadata

```yaml
task: create-mission
atomic_layer: Organism
responsavel_type: Agent
agent: clickup-chief (orchestration) + materializer (execution)
command: "*create-mission {mission-clickup-handoff-path}"
recipe: 5  # materialize_mission
prerequisite: "*bootstrap --mission (deve ter sido executado pelo menos 1x)"
architecture: "Clean — Mission=Task, DAG=Subtasks, Gate=Subtask Type Gate"
```

## Description

Materializar uma Mission SINKRA específica no ClickUp a partir do handoff YAML
gerado pelo `@sinkra-chief` na Phase 7 (Mission Launch).

Cria 1 Task (tipo Mission) na List "Missions" + N subtasks (DAG tasks + Gates)
com dependencies nativas entre elas → Gantt automático com critical path.

## Entrada

- `mission_clickup_handoff` — YAML no formato `mission-clickup-handoff-tmpl.yaml`
  - Path típico: `.aiox/handoffs/handoff-sinkra-chief-to-clickup-chief-mission-{date}.yaml`

## Saída

- 1 Task (Task Type: Mission) na List "Missions"
- N Subtasks (Task Type: Task) — DAG tasks com Custom Fields
- M Subtasks (Task Type: Gate) — Gates com checklists
- Dependencies nativas entre subtasks (waiting_on)
- Custom Fields preenchidos
- Relationship field vinculando ao contexto (produto/projeto)
- `clickup-tokenization.yaml` atualizado
- Relatório de materialização (YAML)

## Pre-Conditions

- [ ] Bootstrap executado — List "Missions", Task Types e Custom Fields existem
- [ ] Handoff YAML válido (9 checks abaixo)
- [ ] APIs necessárias implementadas

## Handoff Validation (9 Checks)

```yaml
validation_checklist:
  - check: "mission.id existe e segue padrão MSN-{YYYY}-{NNN}"
    on_fail: BLOCK
  - check: "mission.name não vazio"
    on_fail: BLOCK
  - check: "mission.timebox.deadline é data válida"
    on_fail: WARN
  - check: "dag_tasks[] tem pelo menos 1 task"
    on_fail: BLOCK
  - check: "Cada dag_task tem task_id, name, phase, executor_type"
    on_fail: BLOCK
  - check: "dependencies[] referencia task_ids existentes em dag_tasks[]"
    on_fail: BLOCK
  - check: "gate_tasks[] tem pelo menos 1 gate"
    on_fail: BLOCK
  - check: "Cada gate_task tem gate_id, criteria_checklist[]"
    on_fail: BLOCK
  - check: "Nenhuma dependency circular (DAG válido)"
    on_fail: BLOCK
```

## Steps

### Step 1 — Validar Handoff

```yaml
action: validate_handoff
input: "{mission-clickup-handoff-path}"
checks: 9
on_fail: "BLOCK — devolver para @sinkra-chief com feedback"
on_pass: "Prosseguir"
```

### Step 2 — Resolver List "Missions"

```yaml
action: resolve_list
name: "Missions"
source: "tokenization registry (bootstrap registrou list_id)"
logic: |
  1. Ler list_id do clickup-tokenization.yaml → missions.list_id
  2. GET /list/{list_id} → validar existência
  3. Se não existe → BLOCK (bootstrap não foi executado)
```

### Step 3 — Criar Task Mission (pai)

```yaml
action: create_task
list_id: "{from step 2}"
task_type: "Mission"
fields:
  name: "{mission.name}"
  description: |
    ## Mission: {mission.name}
    **ID:** {mission.id}
    **Ponto A:** {mission.ponto_a}
    **Ponto B:** {mission.ponto_b}
    **Timebox:** {mission.timebox.duration} (due date: {mission.timebox.deadline})

    ---
    ## Journey Log
    <!-- Super agent registra aqui -->
  status: "Shaped"
  custom_fields:
    Mission ID: "{mission.id}"
    Timebox: "{mission.timebox.size}"
    Circuit Breaker: "Active"
    Ponto A: "{mission.ponto_a}"
    Ponto B: "{mission.ponto_b}"
  relationship: "{produto/projeto vinculado, se especificado no handoff}"
logic: |
  1. POST /list/{list_id}/task com task_type "Mission"
  2. SET custom fields via POST /task/{task_id}/field/{field_id}
  3. Registrar mission_task_id
```

### Step 4 — Criar Subtasks DAG (tipo Task)

```yaml
action: create_subtasks
parent_task_id: "{from step 3}"
task_type: "Task"  # default
source: "handoff.dag_tasks[]"
logic: |
  Para cada dag_task:
  1. POST /list/{list_id}/task com:
     - name: dag_task.name
     - parent: mission_task_id
     - description: |
         {dag_task.description}

         ---
         ## Journey Log
         <!-- Super agent registra aqui -->
     - assignees: [executor_id] se executor_type == Human (resolvido via person-resolver.js)
     - tags: [source_squad] se executor_type != Human
     - start_date: dag_task.start_date (epoch ms)
     - due_date: dag_task.due_date (epoch ms)
     - time_estimate: dag_task.estimated_duration (ms)
     - custom_item: Task Type ID (lookup from tokenization.yaml)
  2. SET custom fields:
     - Task Status: "To Do"
     - Phase: dag_task.phase
     - Executor Type: dag_task.executor_type
     - Source Squad: dag_task.source_squad
  3. CREATE checklist "Tokens" com dag_task.checklist[] items (se houver)
  4. Registrar mapping: dag_task.task_id → clickup_task_id
```

### Step 5 — Criar Subtasks Gate (tipo Gate)

```yaml
action: create_gate_subtasks
parent_task_id: "{from step 3}"
task_type: "Gate"
source: "handoff.gate_tasks[]"
logic: |
  Para cada gate_task:
  1. POST /list/{list_id}/task com:
     - name: gate_task.name (ex: "Gate: Phase 1 → Phase 2")
     - parent: mission_task_id
     - task_type: "Gate"
     - assignee: Mission Lead
     - description: "Gate entre Phase {X} e Phase {Y}. Critérios abaixo."
  2. SET custom fields:
     - Task Status: "To Do"
     - Phase: gate_task.between_phases[1]  # fase de destino
     - Gate Score: gate_task.min_score
  3. CREATE checklist "Critérios Go/No-Go" com gate_task.criteria_checklist[] items
  4. Registrar mapping: gate_task.gate_id → clickup_task_id
```

### Step 6 — Criar Dependencies

```yaml
action: create_dependencies
source: "handoff.dependencies[]"
logic: |
  Para cada dependency:
  1. Resolver task_id → clickup_task_id via mapping dos Steps 4+5
  2. POST /task/{task_id}/dependency
     - depends_on: clickup_task_id da task que precisa completar primeiro
     - type: "waiting_on"

  Também criar dependencies dos Gates:
  - Gate "Phase X → Phase Y" waiting_on todas tasks de Phase X

  CRITICAL: Dependencies geram o Gantt com critical path automático.
```

### Step 7 — Atualizar Tokenization

```yaml
action: update_registry
file: "squads/sinkra-squad/data/clickup-tokenization.yaml"
section: "missions.instances"
register:
  mission_id: "{MSN-YYYY-NNN}"
  task_id: "{clickup mission task id}"
  task_url: "https://app.clickup.com/t/{task_id}"
  subtask_mapping: "{dag_task_id → clickup_task_id}"
  gate_mapping: "{gate_id → clickup_task_id}"
  materialized_at: "{YYYY-MM-DD}"
  materialized_by: "@clickup-chief"
```

### Step 8 — Gerar Relatório

```yaml
action: generate_report
output: "squads/clickup-ops-squad/output/materialization-report-{mission-id}.yaml"
content:
  mission_id: "{MSN-YYYY-NNN}"
  mission_name: "{name}"
  mission_task_id: "{id}"
  mission_task_url: "https://app.clickup.com/t/{task_id}"
  subtasks_created: "{count}"
  gates_created: "{count}"
  dependencies_created: "{count}"
  status: "COMPLETE"
  errors: []
  warnings: []
```

## Post-Conditions

- [ ] Task Mission existe na List "Missions" com Task Type Mission
- [ ] Todas subtasks DAG criadas com Custom Fields preenchidos
- [ ] Todas subtasks Gate criadas com checklists de critérios
- [ ] Dependencies configuradas (Gantt mostra critical path)
- [ ] Tokenization atualizado com todos IDs
- [ ] Relatório de materialização gerado

## Performance

- SLA: 15 minutos (API)
- Escalação: Se API falhar 3x → escalar para @devops
- Rollback: Não automático — relatório documenta o que foi criado para cleanup manual

## Assignee Resolution

`materialize-mission.js` usa `person-resolver.js` para resolver assignees automaticamente:

1. Cada `dag_task.assignee` no handoff é resolvido via `resolvePersonId(name)` contra `people-registry.yaml`
2. Se o nome não é encontrado no registry, a task é criada **sem assignee** com WARN no relatório
3. Gates usam `resolveByRole('mission-lead')` para atribuir o Mission Lead
4. O resolver mantém cache em memória — use `clearPersonCache()` se o registry for atualizado mid-session

**Campos adicionais suportados por `materialize-mission.js`:**
- `start_date` / `start_date_time` — data de início individual por subtask
- `time_estimate` — duração estimada em milissegundos
- `custom_item` — Task Type ID (lookup from tokenization.yaml)

**Política WARN para assignees não resolvidos:**
- Task é criada normalmente, sem assignee
- Warning registrado no relatório de materialização
- Não bloqueia a materialização (WARN, não BLOCK)

## CLI Usage

```bash
# Via services/clickup module
node services/clickup materialize-mission {handoff-path}

# Dry-run (validação sem criação)
node services/clickup materialize-mission {handoff-path} --dry-run
```
