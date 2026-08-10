# Task: atm_create_gate_tasks

## Metadata

task: atm_create_gate_tasks
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
- campo: gate_tasks
  tipo: array[GateTaskSpec]
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: gate_task_bundle
  tipo: JSON
  destino: atm_attach_gate_criteria.entrada.gate_task_bundle
  persistido: true
```

## Pre-conditions

```yaml
- gates_list_id existe
- gate_tasks não está vazio
```

## Post-conditions

```yaml
conditions:
- gate_task_bundle.created_count = quantidade de gates declarados
- Cada gate recebeu status inicial compatível com a policy
acceptance_criteria:
- Cria uma gate task por gate declarado.
- Cada gate recebe status inicial compatível com a policy do processo.
- Bloqueia transição de fase quando algum gate obrigatório não é criado.
```

## Performance

```yaml
duration: < 2 min (inferido; materialização de gates)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e bloquear transição de fase
  alert_on_failure: true
```
