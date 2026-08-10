# Task: atm_publish_materialization_report

## Metadata

task: atm_publish_materialization_report
atomic_layer: Atom
responsavel_type: Agent
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: materialization_registry
  tipo: YAML
  origem: atm_assemble_registry.saida.materialization_registry
  obrigatorio: true
- campo: registry_sync_status
  tipo: JSON
  origem: atm_sync_upstream_registry.saida.registry_sync_status
  obrigatorio: true
- campo: execution_log
  tipo: JSONL
  origem: atm_emit_execution_log.saida.execution_log
  obrigatorio: true
```

## Saída

```yaml
- campo: materialization_report
  tipo: Markdown
  destino: processo.output.materialization_report
  persistido: true
- campo: followup_actions
  tipo: array[string]
  destino: processo.output.followup_actions
  persistido: true
```

## Pre-conditions

```yaml
- execution_log existe
- Schema do report está definido
```

## Post-conditions

```yaml
conditions:
- materialization_report resume status, gaps e próximos passos
- Se houver degradação, followup_actions não fica vazio
acceptance_criteria:
- Resume status, falhas, gaps e próximos passos em schema consumível.
- Se houver degradação, followup_actions não fica vazio.
- Fallback humano publica versão validada quando o report automático falha.
```

## Performance

```yaml
duration: < 10 min (inferido; síntese Agent)
cost: Variável médio
cacheable: false
error_handling:
  strategy: fallback
  max_retries: 1
  fallback: Mission Lead valida e publica versão humana do report
  alert_on_failure: true
```
