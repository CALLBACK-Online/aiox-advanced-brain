# Runner-Ops Data Boundary

Este diretório não mantém mais `runner-registry.yaml` local.

Fonte canônica de estado dos runners:
- `infrastructure/scripts/runner-lib/runner-registry.yaml`

Motivo:
- `runner-ops` precisa ser autocontido como pack instalável.
- Os runners governados por ele não podem depender de `squads/runner-ops/`.
- O runtime e o estado canônicos continuam em `infrastructure/` + `outputs/`.
