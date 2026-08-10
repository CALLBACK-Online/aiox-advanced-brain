# Task: atm_enrich_task_metadata

## Metadata

task: atm_enrich_task_metadata
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
- campo: field_map
  tipo: JSON
  origem: atm_provision_fields.saida.field_map
  obrigatorio: true
- campo: dag_tasks
  tipo: array[DagTaskSpec]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: metadata_enrichment_status
  tipo: JSON
  destino: atm_create_gate_tasks.entrada.execution_graph_bundle
  persistido: true
```

## Pre-conditions

```yaml
- task_id_map existe
- Campos Mission ID, Phase, Ponto A e Ponto B estão resolvidos
```

## Post-conditions

```yaml
conditions:
- Todas as tasks criadas receberam Mission ID
- Tasks com phase, ponto_a e ponto_b no handoff receberam os bindings correspondentes
acceptance_criteria:
- Todas as tasks criadas recebem Mission ID.
- Bindings de phase, ponto_a e ponto_b são aplicados quando declarados no handoff.
- Qualquer falha crítica bloqueia a governança runtime.
```

## Performance

```yaml
duration: < 2 min (inferido; enriquecimento determinístico)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Registrar erro crítico e bloquear governança runtime
  alert_on_failure: true
```
