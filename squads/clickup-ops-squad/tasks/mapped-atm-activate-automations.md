# Task: atm_activate_automations

## Metadata

task: atm_activate_automations
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
- campo: receita_automacoes
  tipo: YAML
  origem: runtime:automation_recipe
  obrigatorio: true
```

## Saída

```yaml
- campo: automation_activation_status
  tipo: JSON
  destino: atm_activate_circuit_breaker.entrada.automation_activation_status | atm_emit_execution_log.entrada.resultados_workflows_anteriores
  persistido: true
```

## Pre-conditions

```yaml
- gate_criteria_status = PASS
- Receita de automações declarativa disponível
```

## Post-conditions

```yaml
conditions:
- Automações phase_complete_notification, appetite_deadline_alert e mission_complete
  foram tentadas
- Toda falha produziu log estruturado e rota de fallback explícita
acceptance_criteria:
- Tenta phase_complete_notification, appetite_deadline_alert e mission_complete.
- Toda falha produz log estruturado e fallback explícito.
- Se o runner dedicado não estiver disponível, registra execução assistida e CG-001.
```

## Performance

```yaml
duration: < 5 min (inferido; runner com fallback)
cost: Médio
cacheable: false
error_handling:
  strategy: retry
  max_retries: 1
  fallback: Acionar runner assistido por humano e abrir follow-up crítico
  alert_on_failure: true
```
