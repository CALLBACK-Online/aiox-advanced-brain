# Task: atm_build_preflight

## Metadata

task: atm_build_preflight
atomic_layer: Atom
responsavel_type: Agent
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: handoff_normalizado
  tipo: YAML
  origem: atm_ingest_handoff.saida.handoff_normalizado
  obrigatorio: true
- campo: contract_validation_result
  tipo: JSON
  origem: atm_validate_contract.saida.contract_validation_result
  obrigatorio: true
- campo: capability_gaps
  tipo: YAML
  origem: artifact:capability_gaps.yaml
  obrigatorio: true
```

## Saída

```yaml
- campo: materialization_preflight
  tipo: YAML
  destino: atm_authorize_execution.entrada.materialization_preflight
  persistido: true
- campo: risk_summary
  tipo: YAML
  destino: atm_authorize_execution.entrada.risk_summary
  persistido: true
```

## Pre-conditions

```yaml
- contract_validation_result.status = PASS
- Todos os atoms do TO-BE estão resolvidos no executor_matrix
```

## Post-conditions

```yaml
conditions:
- materialization_preflight enumera space, folder, listas, views, gates e sync
- risk_summary classifica pelo menos risco estrutural, risco de automação e risco
  de sync
acceptance_criteria:
- Enumera Space, Folder, listas, fields, grafo, gates, automações, views e sync esperados.
- Classifica riscos estrutural, automação e sync com racional explícito.
- Expõe gaps CG-001, CG-002, CG-003 e CG-005 quando aplicáveis ao runtime.
```

## Performance

```yaml
duration: < 10 min (inferido; Agent de síntese estruturada)
cost: Variável médio
cacheable: false
error_handling:
  strategy: fallback
  max_retries: 1
  fallback: Mission Lead revisa o preflight manualmente
  alert_on_failure: true
```
