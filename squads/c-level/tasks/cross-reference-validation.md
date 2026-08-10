# Task: Cross-Reference Validation

task_id: cross-reference-validation
```yaml
task:
  task_id: cross-reference-validation
  id: cross-reference-validation
  name: Validação de Cross-References do Perfil
  agent: coo-orchestrator
  responsavel_type: Agent
  trigger: workflow
  elicit: false
  output_format: yaml
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace/{spoke}/L0-identity/company-dna.yaml
- workspace/{spoke}/L0-identity/founder-dna.yaml
- workspace/{spoke}/L1-strategy/icp.yaml
- workspace/{spoke}/L2-tactical/brand/brandbook.yaml
Output:
- workspace/{spoke}/L4-operational/evidence/cross-reference-validation.yaml
pre_condition:
- Artefatos base do pipeline populados antes da fase final.
post_condition:
- Tensões, lacunas e alinhamentos registrados com decisão explícita.
performance:
- Consolidar inconsistências sem inventar correções e sem sobrescrever artefatos fonte.
Error Handling:
- Interromper a fase final quando algum artefato obrigatório estiver ausente ou ilegível.
Completion Criteria:
- [ ] Arquivo de cross-reference salvo no caminho canônico.
- [ ] Alinhamento entre company, founder, ICP e brand explicitado.

## Descrição

Task de fechamento do `business-profile-pipeline`. O COO compara os artefatos centrais já produzidos, aponta conflitos semânticos e registra se o pipeline pode seguir para síntese final.

## Checks mínimos

1. `company-dna.yaml` vs `icp.yaml`
   - target market, estágio e linguagem de mercado não podem se contradizer.
2. `founder-dna.yaml` vs `brandbook.yaml`
   - personalidade, archetype e voice DNA devem ser compatíveis.
3. `company-dna.yaml` vs `brandbook.yaml`
   - positioning e differentiators devem refletir a proposta da empresa.

## Output mínimo

```yaml
cross_reference_validation:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  verdict: PASS|REVIEW|FAIL
  checks:
    company_vs_icp: aligned|review|fail
    founder_vs_brand: aligned|review|fail
    company_vs_brand: aligned|review|fail
  blockers: []
  warnings: []
  next_actions: []
```

---

*Task do Squad C-Level - COO Orchestrator*
