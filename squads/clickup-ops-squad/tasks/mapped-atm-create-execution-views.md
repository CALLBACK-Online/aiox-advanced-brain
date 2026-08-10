# Task: atm_create_execution_views

## Metadata

task: atm_create_execution_views
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: execution_graph_bundle
  tipo: YAML
  origem: org_execution_graph.output.execution_graph_bundle
  obrigatorio: true
- campo: mission_board_id
  tipo: string
  origem: atm_provision_lists.saida.list_bundle
  obrigatorio: true
```

## Saída

```yaml
- campo: execution_views_status
  tipo: JSON
  destino: atm_create_health_view.entrada.execution_graph_bundle | atm_assemble_registry.entrada.ids_gerados_execucao
  persistido: true
```

## Pre-conditions

```yaml
- mission_board_id existe
- Tipos de view gantt e board estão suportados
```

## Post-conditions

```yaml
conditions:
- DAG View e Board foram criadas ou registradas como reaproveitadas
- execution_views_status.created_count >= 2
acceptance_criteria:
- Cria ou reaproveita DAG View e Board View.
- execution_views_status.created_count é pelo menos 2 quando não há reaproveitamento
  total.
- Warnings ficam explícitos quando a criação não ocorre integralmente.
```

## Performance

```yaml
duration: < 2 min (inferido; configuração de views)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Continuar com warning estruturado e notificar Mission Lead
  alert_on_failure: true
```
