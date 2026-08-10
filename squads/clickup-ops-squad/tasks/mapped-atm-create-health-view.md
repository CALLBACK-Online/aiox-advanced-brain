# Task: atm_create_health_view

## Metadata

task: atm_create_health_view
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
- campo: policy_observabilidade
  tipo: YAML
  origem: runtime:observability_policy
  obrigatorio: true
```

## Saída

```yaml
- campo: health_view_status
  tipo: JSON
  destino: atm_assemble_registry.entrada.runtime_activation_bundle | atm_publish_materialization_report.entrada.materialization_registry
  persistido: true
```

## Pre-conditions

```yaml
- Mission Board já existe
- Métricas blocked_tasks e days_remaining estão definidas no contrato
```

## Post-conditions

```yaml
conditions:
- Se criada, health_view_status.mode = automated
- Se não criada, health_view_status.mode = degraded e follow-up obrigatório é aberto
acceptance_criteria:
- Se criada, health_view_status.mode = automated.
- Se não criada, health_view_status.mode = degraded com follow-up obrigatório.
- Mantém CG-002 visível quando o serviço de observabilidade não está maduro.
```

## Performance

```yaml
duration: < 3 min (inferido; observabilidade configurável)
cost: Médio
cacheable: false
error_handling:
  strategy: fallback
  max_retries: 1
  fallback: Registrar operação degradada, alertar Mission Lead e manter CG-002 visível
  alert_on_failure: true
```
