# Task: atm_sync_upstream_registry

## Metadata

task: atm_sync_upstream_registry
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: materialization_registry
  tipo: YAML
  origem: atm_assemble_registry.saida.materialization_registry
  obrigatorio: true
- campo: store_upstream
  tipo: ServiceEndpoint
  origem: service:registry_store_upstream
  obrigatorio: true
```

## Saída

```yaml
- campo: registry_sync_status
  tipo: JSON
  destino: atm_emit_execution_log.entrada.resultados_workflows_anteriores | atm_publish_materialization_report.entrada.registry_sync_status
  persistido: true
```

## Pre-conditions

```yaml
- materialization_registry válido
- Store upstream configurada e autenticada
```

## Post-conditions

```yaml
conditions:
- registry_sync_status.state = synced ou degraded
- Toda falha registra tentativa, erro e destino não atualizado
acceptance_criteria:
- Retorna state synced ou degraded sem estado opaco.
- Qualquer falha registra tentativa, erro e destino não atualizado.
- Mantém CG-003 explícito quando o serviço upstream não está formalizado.
```

## Performance

```yaml
duration: < 2 min (inferido; writeback versionado)
cost: Médio
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e manter CG-003 aberto no report
  alert_on_failure: true
```
