# Task: atm_provision_lists

## Metadata

task: atm_provision_lists
atomic_layer: Atom
responsavel_type: Worker
domínio: Operacional
accountability: Mission Lead

## Entrada

```yaml
- campo: folder_resolution
  tipo: JSON
  origem: atm_create_folder.saida.folder_resolution
  obrigatorio: true
- campo: template_statuses
  tipo: YAML
  origem: runtime:template_statuses
  obrigatorio: true
```

## Saída

```yaml
- campo: list_bundle
  tipo: JSON
  destino: atm_provision_fields.entrada.list_bundle
  persistido: true
```

## Pre-conditions

```yaml
- folder_resolution.id existe
- Template de statuses do board e gates está disponível
```

## Post-conditions

```yaml
conditions:
- list_bundle.mission_board_id existe
- list_bundle.gates_list_id existe
acceptance_criteria:
- Provisiona Mission Board e Gates com IDs distintos.
- Statuses seguem o template padronizado do board e dos gates.
- Registra created_count compatível com o bootstrap esperado.
```

## Performance

```yaml
duration: < 2 min (inferido; bootstrap estrutural)
cost: Baixo
cacheable: false
error_handling:
  strategy: retry
  max_retries: 2
  fallback: Escalar para Mission Lead e abortar bootstrap
  alert_on_failure: true
```
