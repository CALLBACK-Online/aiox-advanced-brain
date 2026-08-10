---
schema_version: "recommendations-by-use-case.v1"
slug: "fixture-tech-research-multi-player-status"
date: "2026-05-19"
comparison_pattern: "multi_player"
candidates_count: 5
use_cases_count: 5
companion_atoms:
  matrix: "matrices.yaml"
  criteria: "criteria.md"
provenance:
  authored_by: "fixture stub — STORY-RA-F.2 AC-4 minimal coverage"
  authored_at: "2026-05-19T17:38:15Z"
  reviewed_by: null
---

# Recomendações por Caso de Uso — fixture-tech-research

> Fixture mínima exercitando AC-4: 5 use cases distintos com primary/secondary/decisive_dimension/gap.

## Use Cases

### Use Case 1 — Documentos privados

```yaml
id: uc_1_private_docs
scenario: |
  Owner precisa rodar pesquisa contra base privada sem expor a APIs públicas.
primary:
  candidate: "openhands"
  rationale: "Self-host nativo + sem telemetria; status tool_runtime ✅ confirmed."
secondary:
  candidate: "cline"
  rationale: "Suporta self-host com setup mais pesado."
decisive_dimension: "tool_runtime"
gap_to_mitigate: "Sem citation Gate built-in — wrap em script de verificação local."
```

### Use Case 2 — SaaS rápido / time-to-value

```yaml
id: uc_2_saas_fast
scenario: |
  Time pequeno, < 5 min para começar, aceita custo por query.
primary:
  candidate: "cursor"
  rationale: "Hosted, no-install, free tier; status ux_control ✅ confirmed."
secondary:
  candidate: "aider"
  rationale: "CLI rápido mas precisa setup local."
decisive_dimension: "ux_control"
gap_to_mitigate: "Quota gratuita acaba rápido — migrar para pago se uso >100/dia."
```

### Use Case 3 — Agent customizado

```yaml
id: uc_3_custom_agent
scenario: |
  Pipeline próprio consumindo via SDK/API com schema estável.
primary:
  candidate: "claude_code"
  rationale: "SDK + JSON schema estável + multi_agent ✅ confirmed."
secondary:
  candidate: "openhands"
  rationale: "Multi-agent partial; aceita orchestration externa."
decisive_dimension: "multi_agent"
gap_to_mitigate: "Sem schema versioning explícito — pin SDK version."
```

### Use Case 4 — Artigos longos / dossiês

```yaml
id: uc_4_long_form
scenario: |
  Dossiê 5k-15k palavras com seções organizadas e citações inline.
primary:
  candidate: "claude_code"
  rationale: "Multi-wave synthesis + markdown output; agentic_planning ✅."
secondary:
  candidate: "cline"
  rationale: "Bom synthesis mas perde estrutura em outputs longos."
decisive_dimension: "agentic_planning"
gap_to_mitigate: "Context window pode quebrar — chunkar por seção."
```

### Use Case 5 — Modelos locais / data sovereignty

```yaml
id: uc_5_local_models
scenario: |
  Ambiente air-gap ou mandato de data sovereignty.
primary:
  candidate: "openhands"
  rationale: "Ollama-compatible + sem chamadas externas; tool_runtime ✅."
secondary:
  candidate: "aider"
  rationale: "Suporta backends locais via configuração explícita."
decisive_dimension: "tool_runtime"
gap_to_mitigate: "Local model quality varia por hardware — mín 16GB VRAM."
```

## Tabela Cruzada — Candidate × Use Case

Marker key: ✅ best fit (primary) | ◐ acceptable secondary | ? evaluate per case | — does not fit

| Use Case | claude_code | aider | cline | openhands | cursor |
|---|:---:|:---:|:---:|:---:|:---:|
| 1 — Documentos privados | — | — | ◐ | ✅ | — |
| 2 — SaaS rápido | — | ◐ | — | — | ✅ |
| 3 — Agent customizado | ✅ | — | — | ◐ | — |
| 4 — Artigos longos | ✅ | — | ◐ | — | — |
| 5 — Modelos locais | — | ◐ | — | ✅ | — |

**Decision log:**

```yaml
use_cases_total: 5
primary_distribution:
  claude_code: 2
  openhands: 2
  cursor: 1
unanimous_winner: false
ties_broken_by: "decisive_dimension column"
```

---

*Fixture `recommendations-by-use-case.md` minimal — RA-F.2 AC-4 smoke test.*
