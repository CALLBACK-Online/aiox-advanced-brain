# Task: atm_create_checklists

## Metadata

task: atm_create_checklists
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: task_id_map
  tipo: JSON
  origem: atm_create_dag_tasks.saida.task_id_map
  obrigatorio: true
- campo: checklists_declarados
  tipo: array[ChecklistSpec]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: checklist_status
  tipo: JSON
  destino: atm_bind_dependencies.entrada.checklist_status | atm_create_gate_tasks.entrada.execution_graph_bundle
  persistido: true
```

## Pre-conditions

```yaml
- task_id_map existe
- O runtime conhece o checklist associado a cada dag_task
```

## Post-conditions

```yaml
conditions:
- Tasks com tokens receberam checklist Tokens
- Falhas parciais foram logadas com task_id e item afetado
acceptance_criteria:
- Cada task com tokens declarados recebe checklist Tokens correspondente.
- Falhas parciais ficam logadas com task_id e item afetado.
- Não ocorre falha silenciosa quando um checklist não é criado.
```

## Performance

```yaml
duration: < 2 min (inferido; expansão de checklist)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 1
  fallback: Continuar com warning estruturado e abrir follow-up no report
  alert_on_failure: true
```
