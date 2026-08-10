# Task: atm_emit_execution_log

## Metadata

task: atm_emit_execution_log
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: resultados_workflows_anteriores
  tipo: JSON
  origem: atm_ingest_handoff.saida.receipt_log | atm_create_dag_tasks.saida.task_creation_summary
    | atm_bind_dependencies.saida.dependency_status | atm_activate_automations.saida.automation_activation_status
    | atm_activate_circuit_breaker.saida.circuit_breaker_status | atm_sync_upstream_registry.saida.registry_sync_status
  obrigatorio: true
```

## Saída

```yaml
- campo: execution_log
  tipo: JSONL
  destino: atm_publish_materialization_report.entrada.execution_log
  persistido: true
```

## Pre-conditions

```yaml
- Workflow mantém steps e timestamps disponíveis
- Schema de observabilidade definido
```

## Post-conditions

```yaml
conditions:
- execution_log contém duração, falhas, warnings e estado final por etapa
- Nenhuma falha operacional fica só em texto solto
acceptance_criteria:
- Inclui duração, falhas, warnings e estado final por etapa.
- Nenhuma falha operacional permanece apenas em texto livre.
- Se o schema não fechar, emite log degradado e mantém CG-005 visível.
```

## Performance

```yaml
duration: < 60 s (inferido; telemetria estruturada)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 1
  fallback: Gerar log degradado local e marcar CG-005
  alert_on_failure: true
```
