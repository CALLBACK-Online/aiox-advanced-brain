# Task: atm_attach_gate_criteria

## Metadata

task: atm_attach_gate_criteria
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: gate_task_bundle
  tipo: JSON
  origem: atm_create_gate_tasks.saida.gate_task_bundle
  obrigatorio: true
- campo: criteria_checklist
  tipo: array[string]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
- campo: policy_pack_gates
  tipo: YAML
  origem: runtime:gate_policy_pack
  obrigatorio: true
```

## Saída

```yaml
- campo: gate_criteria_status
  tipo: JSON
  destino: atm_activate_automations.entrada.gate_criteria_status
  persistido: true
```

## Pre-conditions

```yaml
- gate_task_bundle existe
- Cada gate possui criteria_checklist definido
```

## Post-conditions

```yaml
conditions:
- Todos os gates receberam checklist Critérios
- min_score e transição de fase foram registrados
acceptance_criteria:
- Todos os gates recebem checklist Critérios.
- min_score e transição entre fases ficam registrados no runtime.
- Sem PASS nesta task, automações não são ativadas.
```

## Performance

```yaml
duration: < 2 min (inferido; binding declarativo)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e impedir ativação de runtime
  alert_on_failure: true
```
