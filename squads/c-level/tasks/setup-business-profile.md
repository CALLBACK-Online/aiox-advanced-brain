# Task: Setup Business Profile

task_id: setup-business-profile
```yaml
task:
  task_id: setup-business-profile
  id: setup-business-profile
  name: Pipeline Completo de Perfil de Negócio
  agent: coo-orchestrator
  responsavel_type: Agent
  elicit: true
  output_format: yaml
  workflow: business-profile-pipeline
  commands:
  - '*setup-business-profile {slug}'
  accountability_token: TK-CL-008
```
## SINKRA Contract

Domain: Operational
atomic_layer: Atom
Input:
- workspace context do business atual
- squads/c-level/config.yaml
Output:
- business-profile-envelope.yaml
pre_condition:
- Bootstrap executado ou contexto do business carregado.
post_condition:
- Decisão ou artefato registrado com handoff explícito para a próxima etapa.
performance:
- Responder sem inventar dados e escalar bloqueios estruturais imediatamente.
Error Handling:
- Escalar blockers estruturais imediatamente e interromper a execução quando o input canônico estiver inconsistente.
Completion Criteria:
- [ ] Output produzido no caminho esperado.
- [ ] Critérios de completude registrados.

## Descrição

O COO orquestra o pipeline completo de elicitação de perfil de negócio em 7 fases, incluindo o pre-flight obrigatório. Este é o comando master que coordena COO, Vision Chief e CMO para popular os artefatos core do negócio.

## Prerequisites

- Bootstrap executado (`.user/user.md` existe)
- Negócio criado (`workspace/{spoke}/` existe)

## Usage

```
*setup-business-profile {slug}
```

**Exemplo:**
```
*setup-business-profile lendaria
```

## Pipeline: 7 Fases

### FASE 0: Pre-Flight

**Objetivo:** Garantir que a infraestrutura está pronta.

1. Executar preflight workspace-first:
   - `bash squads/c-level/scripts/bootstrap-c-level-workspace.sh`
   - `bash squads/c-level/scripts/validate-c-level-essentials.sh`
2. Executar `*workspace-context {slug}` (`load-workspace-context.md`) para snapshot inicial.
3. Verificar bootstrap (`.user/user.md`).
4. Verificar negócio existe (`workspace/{spoke}/`).
5. Se negócio não existe: executar `*add-business {slug}`.
6. Executar `*scaffold-templates {slug}` para copiar templates.
7. Verificar que 16 arquivos YAML foram scaffolded.
8. Apresentar overview do pipeline ao usuário:

```
Pipeline de Perfil de Negócio: {slug}

7 Fases, ~210 perguntas, 7 YAMLs core + artefatos de validação.

FASE 1: Formulário Básico → company-dna.yaml (parcial)
FASE 2: Deep Dive Fundador → founder-dna.yaml + credentials.yaml
FASE 3: Empresa + Time → company-dna.yaml (completo) + team-structure.yaml
FASE 4: ICP Completo → icp.yaml
FASE 5: Brand + Pricing → brandbook.yaml + pricing-strategy.yaml
FASE 6: Enriquecimento + Validação → cross-references + authority-story + completeness report

Você pode pausar entre fases e retomar depois.
Deseja começar? (sim/não)
```

### FASE 1: Formulário Básico (~15 min)

**Agente:** coo-orchestrator
**Método:** FORMULÁRIO (respostas curtas e diretas)
**Task:** `*elicit-company-profile {slug}` (apenas campos básicos da Fase 1-2)

**Escopo desta fase:**
- company_essence (legal_name, trade_name, year, headquarters, one_liner)
- mission/vision básico
- stage

**Gate:** Seção `company_essence` deve ter status `COMPLETE`.

**Ao concluir:**
```
FASE 1 completa ✅
company-dna.yaml: 35% preenchido
Seção company_essence: COMPLETE

Próxima: FASE 2 — Deep Dive Fundador
Continuar? (sim/pular/pausar)
```

### FASE 2: Deep Dive Fundador (~40 min)

**Agente:** vision-chief
**Método:** ENTREVISTA (conversacional, profunda)
**Tasks:** `*elicit-founder-dna {slug}` + `*elicit-credentials {slug}`

**Sequência:**
1. Handoff para Vision Chief: "Passando para o CEO para deep dive no fundador."
2. Executar `elicit-founder-dna` (7 fases, ~35 perguntas).
3. Executar `elicit-credentials` (9 fases, ~40 perguntas).
4. Retornar ao COO.

**Gate:** `founder-dna.yaml` >= 85% completude.

**Ao concluir:**
```
FASE 2 completa ✅
founder-dna.yaml: 92% preenchido — PASSED
credentials.yaml: 78% preenchido — OK (muitos campos opcionais)

Próxima: FASE 3 — Empresa + Time
Continuar? (sim/pular/pausar)
```

### FASE 3: Empresa + Time (~30 min)

**Agente:** coo-orchestrator
**Método:** ENTREVISTA + FORMULÁRIO
**Tasks:** `*elicit-company-profile {slug}` (fases restantes) + `*elicit-team-structure {slug}`

**Sequência:**
1. Completar company-dna.yaml (fases 3-8: posicionamento, portfolio, mercado, métricas, voz).
2. Executar elicit-team-structure (5 fases, ~20 perguntas).

**Gate:** `company-dna.yaml` >= 85% completude.

**Ao concluir:**
```
FASE 3 completa ✅
company-dna.yaml: 87% preenchido — PASSED
team-structure.yaml: 90% preenchido — PASSED

Próxima: FASE 4 — ICP Completo
Continuar? (sim/pular/pausar)
```

### FASE 4: ICP Completo (~30 min)

**Agente:** cmo-architect
**Método:** ENTREVISTA
**Task:** `*elicit-icp-yaml {slug}`

**Sequência:**
1. Handoff para CMO: "Passando para o CMO para deep dive no ICP."
2. Diagnosis gate (2 perguntas se necessário).
3. Executar elicit-icp-yaml (7 fases, ~35 perguntas).
4. Retornar ao COO.

**Gate:** `icp.yaml` >= 85% completude.

### FASE 5: Brand + Pricing (~25 min)

**Agente:** cmo-architect
**Método:** ENTREVISTA + FORMULÁRIO
**Tasks:** `*elicit-brand-yaml {slug}` + `*elicit-pricing-strategy {slug}`

**Sequência:**
1. CMO executa elicit-brand-yaml (6 fases, ~25 perguntas).
2. CMO executa elicit-pricing-strategy (6 fases, ~25 perguntas).
3. Retornar ao COO.

**Gate:** `brandbook.yaml` >= 85% completude.

### FASE 6: Enriquecimento e Validação (~10 min, agente)

**Agente:** coo-orchestrator (sintetizado, sem perguntas ao usuário)
**Método:** SINTETIZADO

**Ações automáticas:**
1. Executar `cross-reference-validation`:
   - Verificar alinhamento entre Company, ICP, Brand e Founder DNA.
   - Gerar `L4-operational/evidence/cross-reference-validation.yaml`.
2. Executar `authority-story-synthesis`:
   - Sintetizar `authority-story.yaml` a partir de `founder-dna.yaml` + `credentials.yaml`.
3. Executar `completeness-report`:
   - Consolidar completude final e publicar o relatório.
4. **Cross-reference ICP vs Company Profile:**
   - Verificar que target_market (company) alinha com demographics (ICP).
   - Reportar inconsistências.
5. **Alinhamento Brand vs Founder:**
   - Verificar que personality da marca alinha com archetype do fundador.
   - Reportar tensões.
6. **Calcular completude geral:**
   - Para cada um dos 7 YAMLs core, calcular %.
   - Reportar total.
7. **Produzir relatório de completude:**

```
═══════════════════════════════════════════
RELATÓRIO DE COMPLETUDE — {slug}
═══════════════════════════════════════════

Company:
  founder-dna.yaml:      92% ✅ PASSED
  credentials.yaml:      78% ✅ PASSED (ajustado)
  company-dna.yaml:  87% ✅ PASSED
  brandbook.yaml:            90% ✅ PASSED
  icp.yaml:              85% ✅ PASSED
  diagnosis.yaml:        100% ✅ COMPLETE

Operations:
  team-structure.yaml:   90% ✅ PASSED
  pricing-strategy.yaml: 88% ✅ PASSED

Sintetizados:
  authority-story.yaml:  AUTO-GERADO ✅

Cross-References:
  ICP ↔ Company Profile:  ALINHADO ✅
  Brand ↔ Founder DNA:    ALINHADO ✅ (1 tensão menor)

RESULTADO GERAL: 7/7 YAMLs >= 85% — PIPELINE COMPLETO ✅
═══════════════════════════════════════════

Próximos passos:
1. Revisar YAMLs gerados em workspace/{spoke}/
2. Executar *health-check para validação completa
3. Iniciar pipeline de produto: *add-product {slug} {product}
```

## Pause/Resume

O pipeline suporta pause/resume:
- **Pausar:** Responder "pausar" a qualquer gate. Estado salvo nos YAMLs parciais.
- **Retomar:** Executar `*setup-business-profile {slug}` novamente. Fase 0 detecta YAMLs parciais e oferece retomar de onde parou.

## Outputs

| Fase | Arquivo | Agente |
|------|---------|--------|
| 1 | company-dna.yaml (parcial) | COO |
| 2 | founder-dna.yaml, credentials.yaml | Vision Chief |
| 3 | company-dna.yaml (completo), team-structure.yaml | COO |
| 4 | icp.yaml, diagnosis.yaml | CMO |
| 5 | brandbook.yaml, pricing-strategy.yaml | CMO |
| 6 | cross-reference-validation.yaml, authority-story.yaml, completeness-report.md | COO |

## Validation

- [ ] Fase 0: scaffold completo (16 arquivos)
- [ ] Fase 1-5: cada gate >= 85%
- [ ] Fase 6: cross-references sem inconsistências críticas
- [ ] Fase 6: cross-reference-validation.yaml gerado
- [ ] Fase 6: authority-story.yaml gerado
- [ ] Todos os 7 YAMLs core >= 85% completude

---

*Task do Squad C-Level - COO Orchestrator*
