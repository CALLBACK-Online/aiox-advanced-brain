# Task: atm_activate_circuit_breaker

## Metadata

task: atm_activate_circuit_breaker
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: automation_activation_status
  tipo: JSON
  origem: atm_activate_automations.saida.automation_activation_status
  obrigatorio: true
- campo: policy_pack_circuit_breaker
  tipo: YAML
  origem: runtime:circuit_breaker_policy
  obrigatorio: true
```

## Saída

```yaml
- campo: circuit_breaker_status
  tipo: JSON
  destino: atm_create_execution_views.entrada.execution_graph_bundle | atm_emit_execution_log.entrada.resultados_workflows_anteriores
  persistido: true
```

## Pre-conditions

```yaml
- Receita de circuit breaker está definida
- Mission possui appetite.deadline válido
```

## Post-conditions

```yaml
conditions:
- Monitoramento e notificação foram tentados com trilha auditável
- Se não ativado, circuit_breaker_status registra fallback humano obrigatório
acceptance_criteria:
- Tenta ativar monitoramento e notificação parametrizados.
- Se não ativado, registra fallback humano obrigatório e mantém CG-001 explícito.
- Nunca fecha a etapa sem trilha auditável do resultado.
```

## Performance

```yaml
duration: < 3 min (inferido; policy bootstrap)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 1
  fallback: Acionar operação assistida e sinalizar CG-001
  alert_on_failure: true
```
