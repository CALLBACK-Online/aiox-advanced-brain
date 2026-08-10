# Task: atm_create_folder

## Metadata

task: atm_create_folder
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: space_resolution
  tipo: JSON
  origem: atm_resolve_space.saida.space_resolution
  obrigatorio: true
- campo: approved_preflight_bundle
  tipo: YAML
  origem: atm_authorize_execution.saida.approved_preflight_bundle
  obrigatorio: true
```

## Saída

```yaml
- campo: folder_resolution
  tipo: JSON
  destino: atm_provision_lists.entrada.folder_resolution
  persistido: true
```

## Pre-conditions

```yaml
- space_resolution.id existe
- mission.id e mission.name estão normalizados
```

## Post-conditions

```yaml
conditions:
- folder_resolution.id existe
- folder_resolution.name segue o padrão MSN-{YYYY}-{NNN} — Nome
acceptance_criteria:
- Cria ou resolve uma Folder com padrão MSN-{YYYY}-{NNN} — Nome.
- Retorna folder_id e nome final normalizado.
- Bloqueia etapas seguintes quando a Folder não é resolvida.
```

## Performance

```yaml
duration: < 30 s (inferido; Worker API idempotente)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e bloquear steps seguintes
  alert_on_failure: true
```
