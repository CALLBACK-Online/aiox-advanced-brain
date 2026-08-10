# Task: Completeness Report

task_id: completeness-report
```yaml
task:
  task_id: completeness-report
  id: completeness-report
  name: Relatório de Completude do Perfil
  agent: coo-orchestrator
  responsavel_type: Agent
  trigger: workflow
  elicit: false
  output_format: markdown
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace/{spoke}/L0-identity/
- workspace/{spoke}/L1-strategy/
- workspace/{spoke}/L2-tactical/brand/
- workspace/{spoke}/L4-operational/evidence/cross-reference-validation.yaml
Output:
- workspace/{spoke}/L4-operational/evidence/completeness-report.md
pre_condition:
- Fases anteriores do business-profile-pipeline concluídas.
post_condition:
- Completude final consolidada com status por artefato e próximos passos.
performance:
- Reportar completude real do workspace sem inflar score nem ocultar gaps.
Error Handling:
- Marcar REVIEW quando algum artefato central estiver ausente ou abaixo do threshold.
Completion Criteria:
- [ ] Relatório salvo no caminho canônico.
- [ ] Todos os artefatos core avaliados individualmente.

## Descrição

Task final do pipeline de perfil. Consolida o estado dos artefatos produzidos, o resultado da validação cruzada e a recomendação operacional para o próximo handoff.

## Seções mínimas

1. Resumo executivo com `PASS | REVIEW | FAIL`
2. Tabela de completude por artefato core
3. Blockers e warnings
4. Próximos passos canônicos

---

*Task do Squad C-Level - COO Orchestrator*
