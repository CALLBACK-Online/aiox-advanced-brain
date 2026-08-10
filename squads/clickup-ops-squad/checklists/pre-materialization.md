# Pre-Materialization Checklist

Checklist OBRIGATÓRIA antes de qualquer materialização.
Se qualquer item falhar → **BLOCK**.

## Structural Checks

- [ ] **CHK-001** Composição segue hierarquia SINKRA sem pular níveis
  - Instance → Template → Organism → Molecule → Atom → Token
- [ ] **CHK-002** Sem dependências circulares (grafo DAG)
- [ ] **CHK-003** Todos Tokens têm família SINKRA definida
  - {Time, Capacity, Threshold, Priority, Permission, Taxonomy, Behavior, Accountability}
- [ ] **CHK-004** Accountability Token presente em Atoms com executor não-Human

## ClickUp Checks

- [ ] **CHK-005** Space de destino existe ou domínio é genuinamente novo
  - Lookup: `clickup-tokenization.yaml → templates`
- [ ] **CHK-006** Campos shared NÃO são duplicados
  - Verificar: `clickup-tokenization.yaml → shared_fields`
- [ ] **CHK-007** Naming conventions respeitadas
  - BU: `[BU] {Nome}`, Generic: `{Nome}`, Fields: emoji prefix
- [ ] **CHK-008** APIs necessárias estão implementadas
  - Verificar: `clickup-composition-rules.yaml → api_implementation_gaps`

## Process Checks

- [ ] **CHK-009** CSO aprovou a composição SINKRA (`*enforce` passou)
- [ ] **CHK-010** Owner squad definido e tem squad-io.yaml
