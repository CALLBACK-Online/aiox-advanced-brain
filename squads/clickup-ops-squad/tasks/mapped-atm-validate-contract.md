# Task: atm_validate_contract

## Metadata

task: atm_validate_contract
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: handoff_normalizado
  tipo: YAML
  origem: atm_ingest_handoff.saida.handoff_normalizado
  obrigatorio: true
- campo: schema_contrato_mission
  tipo: YAML Schema
  origem: runtime:schema_contrato_mission
  obrigatorio: true
```

## Saída

```yaml
- campo: contract_validation_result
  tipo: JSON
  destino: atm_build_preflight.entrada.contract_validation_result
  persistido: true
- campo: contract_errors
  tipo: array[string]
  destino: atm_publish_materialization_report.entrada.contract_errors_context
  persistido: true
```

## Pre-conditions

```yaml
- handoff_normalizado foi produzido no step_01
- Schema do contrato está disponível no runtime
```

## Post-conditions

```yaml
conditions:
- contract_validation_result.status é PASS ou FAIL
- Se FAIL, contract_errors contém lista não vazia de violações
acceptance_criteria:
- Retorna status PASS ou FAIL sem terceiro estado.
- Se FAIL, contract_errors lista todas as violações obrigatórias do contrato.
- Bloqueia qualquer chamada de API quando o contrato falha.
```

## Performance

```yaml
duration: < 30 s (inferido; Worker de validação)
cost: Baixo
cacheable: false
error_handling:
  strategy: abort
  max_retries: 0
  fallback: Bloquear o workflow e notificar Mission Lead
  alert_on_failure: true
```
