# Task: atm_provision_fields

## Metadata

task: atm_provision_fields
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: list_bundle
  tipo: JSON
  origem: atm_provision_lists.saida.list_bundle
  obrigatorio: true
- campo: catalogo_custom_fields
  tipo: YAML
  origem: runtime:custom_fields_catalog
  obrigatorio: true
```

## Saída

```yaml
- campo: field_map
  tipo: JSON
  destino: atm_create_dag_tasks.entrada.field_map | atm_enrich_task_metadata.entrada.field_map
  persistido: true
- campo: critical_field_status
  tipo: enum[PASS,FAIL]
  destino: atm_create_dag_tasks.pre_conditions.critical_field_status
  persistido: true
```

## Pre-conditions

```yaml
- list_bundle.mission_board_id existe
- Catálogo de campos inclui Mission ID, Phase, Ponto A e Ponto B
```

## Post-conditions

```yaml
conditions:
- field_map contém pelo menos os campos críticos do runtime
- critical_field_status = PASS quando todos os campos críticos foram resolvidos
acceptance_criteria:
- Resolve Mission ID, Phase, Ponto A e Ponto B no field_map.
- Critical_field_status só é PASS quando todos os campos críticos estão disponíveis.
- Se algum campo crítico falhar, a materialização do DAG não inicia.
```

## Performance

```yaml
duration: < 2 min (inferido; bootstrap de schema)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead; bloquear wf_graph_materialization se campo
    crítico faltar
  alert_on_failure: true
```
