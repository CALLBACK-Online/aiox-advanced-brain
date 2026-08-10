# Task: atm_bind_dependencies

## Metadata

task: atm_bind_dependencies
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
- campo: dependencies
  tipo: array[DependencySpec]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: dependency_status
  tipo: JSON
  destino: atm_create_gate_tasks.entrada.execution_graph_bundle | atm_emit_execution_log.entrada.resultados_workflows_anteriores
  persistido: true
- campo: critical_path_trace
  tipo: array[string]
  destino: atm_create_execution_views.entrada.execution_graph_bundle | atm_publish_materialization_report.entrada.materialization_registry
  persistido: true
```

## Pre-conditions

```yaml
- task_id_map expected_count = created_count
- Todas as referências do DAG foram aprovadas no step_02
```

## Post-conditions

```yaml
conditions:
- dependency_status.created_count cobre todas as dependências válidas
- critical_path_trace foi registrado para observabilidade
acceptance_criteria:
- Cria todas as dependências válidas declaradas no DAG.
- Registra o critical_path_trace para observabilidade downstream.
- Impede runtime_governance quando há binding estrutural incompleto.
```

## Performance

```yaml
duration: < 2 min (inferido; binding nativo)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e impedir runtime_governance
  alert_on_failure: true
```
