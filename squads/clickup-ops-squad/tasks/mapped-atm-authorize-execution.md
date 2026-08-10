# Task: atm_authorize_execution

## Metadata

task: atm_authorize_execution
atomic_layer: Atom
responsavel_type: Human
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: materialization_preflight
  tipo: YAML
  origem: atm_build_preflight.saida.materialization_preflight
  obrigatorio: true
- campo: risk_summary
  tipo: YAML
  origem: atm_build_preflight.saida.risk_summary
  obrigatorio: true
```

## Saída

```yaml
- campo: execution_decision
  tipo: enum[GO,NO_GO]
  destino: atm_resolve_space.pre_conditions.execution_decision
  persistido: true
- campo: approved_preflight_bundle
  tipo: YAML
  destino: atm_resolve_space.entrada.approved_preflight_bundle
  persistido: true
```

## Pre-conditions

```yaml
- materialization_preflight existe
- Mission Lead identificado no handoff
```

## Post-conditions

```yaml
conditions:
- execution_decision é GO ou NO_GO
- Se GO, approved_preflight_bundle contém referência do accountable e timestamp
acceptance_criteria:
- Registra decisão GO ou NO_GO com accountable humano explícito.
- Se GO, approved_preflight_bundle contém timestamp, Mission Lead e referência do
  preflight aprovado.
- Se NO_GO, o processo permanece bloqueado com trilha auditável.
```

## Performance

```yaml
duration: < 1 dia útil (inferido; gate humano por Mission)
cost: Alto humano
cacheable: false
error_handling:
  strategy: abort
  max_retries: 0
  fallback: Sem fallback automatizado; ausência de decisão mantém bloqueio
  alert_on_failure: true
```
