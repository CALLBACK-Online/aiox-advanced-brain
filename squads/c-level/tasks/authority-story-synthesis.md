# Task: Authority Story Synthesis

task_id: authority-story-synthesis
```yaml
task:
  task_id: authority-story-synthesis
  id: authority-story-synthesis
  name: Síntese de Authority Story
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
- workspace/{spoke}/L0-identity/founder-dna.yaml
- workspace/{spoke}/L0-identity/credentials.yaml
Output:
- workspace/{spoke}/L0-identity/authority-story.yaml
pre_condition:
- Founder DNA e credenciais disponíveis no workspace.
post_condition:
- Narrativa de autoridade sintetizada sem inventar provas ou marcos.
performance:
- Priorizar clareza narrativa e rastreabilidade das provas utilizadas.
Error Handling:
- Bloquear síntese quando faltar founder-dna, credenciais ou evidência mínima rastreável.
Completion Criteria:
- [ ] authority-story.yaml salvo no caminho canônico.
- [ ] Provas referenciadas derivam de founder-dna.yaml e/ou credentials.yaml.

## Descrição

Task sintetizadora da fase final do pipeline de perfil. Converte credenciais e histórico do fundador em uma narrativa curta, rastreável e reutilizável por outros squads.

## Estrutura esperada

```yaml
authority_story:
  headline: ""
  origin_story: ""
  narrative: ""
  proof_points: []
  signature_themes: []
  evidence_sources:
    - founder-dna.yaml
    - credentials.yaml
```

---

*Task do Squad C-Level - COO Orchestrator*
