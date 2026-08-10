# Task: atm_assemble_registry

## Metadata

task: atm_assemble_registry
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: runtime_activation_bundle
  tipo: YAML
  origem: org_runtime_governance.output.runtime_activation_bundle
  obrigatorio: true
- campo: ids_gerados_execucao
  tipo: JSON
  origem: atm_create_dag_tasks.saida.task_id_map | atm_create_execution_views.saida.execution_views_status
  obrigatorio: true
```

## Saída

```yaml
- campo: materialization_registry
  tipo: YAML
  destino: atm_sync_upstream_registry.entrada.materialization_registry | atm_publish_materialization_report.entrada.materialization_registry
  persistido: true
```

## Pre-conditions

```yaml
- space_id, folder_id, list_ids e task_id_map existem
- runtime_activation_bundle foi finalizado
```

## Post-conditions

```yaml
conditions:
- materialization_registry contém ids, contagens e views
- Registry está serializável para writeback
acceptance_criteria:
- Consolida ids, contagens, gates e views em estrutura serializável.
- Materialization_registry fica pronto para writeback versionado.
- Sem registry válido, o sync upstream não inicia.
```

## Performance

```yaml
duration: < 2 min (inferido; assembly determinístico)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e impedir sync upstream
  alert_on_failure: true
```
