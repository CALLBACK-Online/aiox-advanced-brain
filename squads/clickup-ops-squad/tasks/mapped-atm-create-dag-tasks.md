# Task: atm_create_dag_tasks

## Metadata

task: atm_create_dag_tasks
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: topology_bundle
  tipo: YAML
  origem: org_topology_provisioning.output.topology_bundle
  obrigatorio: true
- campo: dag_tasks
  tipo: array[DagTaskSpec]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: task_id_map
  tipo: JSON
  destino: atm_enrich_task_metadata.entrada.task_id_map | atm_create_checklists.entrada.task_id_map
    | atm_bind_dependencies.entrada.task_id_map | atm_assemble_registry.entrada.ids_gerados_execucao
  persistido: true
- campo: task_creation_summary
  tipo: JSON
  destino: atm_bind_dependencies.pre_conditions.task_creation_summary | atm_emit_execution_log.entrada.resultados_workflows_anteriores
  persistido: true
```

## Pre-conditions

```yaml
- field_map disponível e validado
- dag_tasks não está vazio
```

## Post-conditions

```yaml
conditions:
- task_id_map contém uma entrada por dag_task criada
- task_creation_summary.expected_count = task_creation_summary.created_count
acceptance_criteria:
- Cria exatamente uma task ClickUp por node do DAG recebido.
- task_id_map cobre 100% das dag_tasks criadas.
- Mismatch entre expected_count e created_count bloqueia binding downstream.
```

## Performance

```yaml
duration: < 3 min (inferido; materialização do board)
cost: Médio
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e impedir binding de dependências
  alert_on_failure: true
```
