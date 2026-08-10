# Task: atm_ingest_handoff

## Metadata

task: atm_ingest_handoff
atomic_layer: Atom
responsavel_type: Agent
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: mission_clickup_handoff
  tipo: YAML
  origem: artifact:mission-clickup-handoff.yaml
  obrigatorio: true
- campo: contexto_sinkra_squad
  tipo: Contexto
  origem: runtime:sinkra-squad
  obrigatorio: true
```

## Saída

```yaml
- campo: handoff_normalizado
  tipo: YAML
  destino: atm_validate_contract.entrada.handoff_normalizado | atm_build_preflight.entrada.handoff_normalizado
  persistido: true
- campo: receipt_log
  tipo: JSON
  destino: atm_emit_execution_log.entrada.resultados_workflows_anteriores
  persistido: true
```

## Pre-conditions

```yaml
- Arquivo do handoff existe e é legível
- mission.id e mission.name estão presentes no payload bruto
```

## Post-conditions

```yaml
conditions:
- handoff_normalizado preserva versionamento do artefato
- receipt_log contém timestamp e accountable humano
acceptance_criteria:
- Preserva mission.id, mission.name, schema_version e accountable humano no payload
  normalizado.
- Gera receipt_log com timestamp, versão do artefato e origem do handoff.
- Encaminha contexto mínimo suficiente para validação rígida sem ambiguidade estrutural.
```

## Performance

```yaml
duration: < 5 min (inferido; Agent sem baseline factual)
cost: Variável baixo
cacheable: false
error_handling:
  strategy: fallback
  max_retries: 1
  fallback: Escalar para Mission Lead com o artefato bruto e erro de parsing
  alert_on_failure: true
```
