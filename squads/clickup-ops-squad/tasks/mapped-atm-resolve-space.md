# Task: atm_resolve_space

## Metadata

task: atm_resolve_space
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: approved_preflight_bundle
  tipo: YAML
  origem: atm_authorize_execution.saida.approved_preflight_bundle
  obrigatorio: true
- campo: workspace_clickup
  tipo: WorkspaceContext
  origem: service:clickup_workspace
  obrigatorio: true
```

## Saída

```yaml
- campo: space_resolution
  tipo: JSON
  destino: atm_create_folder.entrada.space_resolution
  persistido: true
```

## Pre-conditions

```yaml
- execution_decision = GO
- Credenciais do ClickUp válidas e com permissão de escrita
```

## Post-conditions

```yaml
conditions:
- space_resolution.id existe
- space_resolution.created informa se houve criação ou reaproveitamento
acceptance_criteria:
- Retorna um space_id válido.
- Informa explicitamente se houve criação ou reaproveitamento.
- Falhas de credencial ou permissão abrem fallback humano sem silêncio.
```

## Performance

```yaml
duration: < 30 s (inferido; Worker API idempotente)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead com erro de credencial ou local_docs
  alert_on_failure: true
```
