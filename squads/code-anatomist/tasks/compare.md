# Task: Compare Extractions

> Molecule M2-Analyze — Diff estrutural entre 2 extrações code-anatomist

**Task ID:** compare
**Version:** 1.0.0
**Execution Type:** Agent
**Model:** Sonnet
**Purpose:** Comparar 2 extrações do code-anatomist (mesmo formato 9-phase) e gerar delta-report com gaps, padrões divergentes e insights acionáveis
**Orchestrator:** @decoder-chief
**Primary Agent:** @rick-kazman (architecture comparison) + @gail-murphy (conformance diff)
**Phase:** Post-extraction (M2)
**Tier:** 2

---

## Inputs

```yaml
required:
  - name: "slug_a"
    description: "Slug do projeto A (baseline — geralmente 'allfluence')"
    example: "allfluence"
  - name: "slug_b"
    description: "Slug do projeto B (referência — projeto externo)"
    example: "n8n"
optional:
  - name: "phase_focus"
    description: "Fase específica para comparar (default: all)"
    example: "2"
    valid_values: ["0", "1", "2", "3", "5", "6", "all"]
  - name: "dimension"
    description: "Dimensão de comparação (default: all)"
    example: "architecture"
    valid_values: ["architecture", "dependencies", "data", "domain", "api", "infra", "all"]
```

---

## Elicitation (elicit: true)

Before comparing, gather from the user:

1. **Qual projeto é o baseline?** (default: allfluence — o espelho do próprio projeto)
2. **Qual projeto é a referência?** (ex: n8n, twenty, context-mode)
3. **Foco em qual dimensão?** (architecture, dependencies, data, domain, api, infra, ou all)
4. **Objetivo da comparação?** (feature inspiration, refactor guidance, architecture benchmark, pattern adoption)
5. **Escopo?** (módulo específico ou projeto inteiro)

---

## Steps

### Step 1: Validate Extractions Exist

```bash
ls outputs/decoded/{slug_a}/phase-0-scoping/
ls outputs/decoded/{slug_b}/phase-0-scoping/
```

**VETO:** Se alguma extração não existe ou está incompleta (< 5 phases), HALT.

### Step 2: Load Phase Outputs

Para cada phase_focus (ou all phases):
1. Ler outputs de slug_a e slug_b para a mesma fase
2. Normalizar: extrair entidades comparáveis (modules, endpoints, tables, dependencies)

### Step 3: Compare por Dimensão

| Dimensão | Arquivo A | Arquivo B | Comparação |
|----------|-----------|-----------|------------|
| Architecture | phase-1-context/c4-context.md | phase-1-context/c4-context.md | Containers, external systems, boundaries |
| Dependencies | phase-2-extraction/dependency-graph.md | dependency-graph.md | Module coupling, circular deps, shared libs |
| Data | phase-2-extraction/er-diagram.md | er-diagram.md | Tables, relationships, constraints, RLS |
| Domain | phase-5-domain/domain-map.yaml | domain-map.yaml | Bounded contexts, entities, rules |
| API | phase-2-extraction/api-surface.yaml | api-surface.yaml | Endpoints, auth patterns, error handling |
| Infra | stack-detection.yaml | stack-detection.yaml | Stack, deploy targets, CI/CD |

### Step 4: Classify Deltas

Para cada diferença encontrada:
- **PATTERN_IN_B_NOT_A:** Padrão que B tem e A não → candidato a adoção
- **PATTERN_IN_A_NOT_B:** Padrão que A tem e B não → vantagem competitiva ou over-engineering
- **PATTERN_DIFFERENT:** Mesmo concern, abordagem diferente → trade-off analysis
- **PATTERN_SAME:** Mesmo padrão → confirmação de boa prática

### Step 5: Rank by Impact

Classificar deltas por:
- **Severity:** CRITICAL > HIGH > MEDIUM > LOW
- **Effort:** dias estimados para adotar
- **Value:** impacto no projeto A se adotado

### Step 6: Generate Delta Report

Escrever `outputs/decoded/{slug_a}/comparisons/{slug_b}/delta-report.yaml` usando template.

---

## Output

```yaml
output:
  file: "outputs/decoded/{slug_a}/comparisons/{slug_b}/delta-report.yaml"
  template: "templates/delta-report-tmpl.yaml"
  artifact_contract: "delta-report"
  lifecycle_state: draft
```

---

## Veto Conditions

1. **Extração incompleta:** Se slug_a ou slug_b tem < 5 phases completadas → HALT
2. **Schema mismatch:** Se extrações usam versões diferentes do pipeline (v1 vs v2) → WARN + limitar comparação a phases comuns
3. **Comparabilidade baixa:** Se stacks são completamente diferentes (ex: Rust CLI vs Python API) → WARN com `comparability_score` < 0.3
4. **Baseline stale:** Se allfluence/ extraction é > 90 dias → WARN, recomendar re-extração

---

## Completion Criteria

- [ ] Delta report gerado com todas dimensões solicitadas
- [ ] Cada delta classificado (PATTERN_IN_B_NOT_A, DIFFERENT, SAME)
- [ ] Deltas rankeados por severity + effort + value
- [ ] Comparability score calculado
- [ ] Report salvo em `outputs/decoded/{slug_a}/comparisons/{slug_b}/`

---

## Handoff

| Para | Quando | Artifact |
|------|--------|----------|
| @decoder-chief | Comparação completa | delta-report.yaml |
| *adopt task | Usuário quer adotar padrão identificado | delta com PATTERN_IN_B_NOT_A |
| @architect | Review de trade-offs arquiteturais | delta com PATTERN_DIFFERENT |
