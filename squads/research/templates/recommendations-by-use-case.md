---
schema_version: "recommendations-by-use-case.v1"
slug: "{YYYY-MM-DD}-{slug}"
date: "{YYYY-MM-DD}"
comparison_pattern: "multi_player"
candidates_count: {N}
use_cases_count: {M}                   # MUST be >= 5 per STORY-RA-F.2 AC-4
companion_atoms:
  matrix: "matrices.yaml | comparison-matrix.json"
  report: "02-research-report.md | executive-report.md"
  criteria: "criteria.md"              # paired atom from STORY-RA-F.1
provenance:
  authored_by: "{agent_id}"            # e.g. "tech-research synthesizer" | "research-bench analyst"
  authored_at: "{ISO-8601}"
  reviewed_by: "{operator_handle_or_null}"
---

# Recomendações por Caso de Uso — {ANCHOR_OR_DOMAIN}

> **Emitido por:** `/tech-research` Phase M7/P5 OR `/research-bench` Phase de síntese, quando `comparison_pattern: multi_player` AND `candidates_count >= 3`.
> **Origem:** STORY-RA-F.2 AC-4 (lição L23 das 2 sessões Manus). Precedente: `deep_research_lacunas_recomendacoes_por_caso_de_uso.md` (sessão 2 Manus, 7 cenários).
> **Status code referenced:** ✅ confirmed (2.0) | ◐ partial (1.0) | ? uncertain (0.5) | — not_present (0.0). ASCII fallback: `[X]/[~]/[?]/[ ]` quando `RESEARCH_OUTPUT_ASCII=true`.

Este atomo é **prescritivo** — traduz o ranking geral em decisão **por contexto**. NÃO é sumário do `02-research-report.md`; é a resposta à pergunta "no MEU caso, qual escolho?" para CADA caso identificado.

---

## Como ler

Cada use case responde a 5 perguntas operacionais:

1. **Cenário** — quem é o usuário, que problema enfrenta, qual a constraint dominante?
2. **Primary** — escolha de primeira ordem + por que vence neste contexto
3. **Secondary** — fallback / alternativa quando primary não couber
4. **Justificativa** — qual dimension/feature da matriz decide o ranking aqui
5. **Lacuna** — o que primary NÃO entrega, e como mitigar

A tabela final (no fim do atomo) cruza `candidate × use_case` com marker `best_fit`.

---

## Use Cases

Mínimo de 5 use cases distintos. Os 7 abaixo são o template canônico derivado da sessão Manus 2 (deep research tools); substitua/ajuste pelos use cases reais do seu domínio.

### Use Case 1 — Documentos privados / KB interna

```yaml
id: uc_1_private_docs
scenario: |
  Usuário precisa rodar pesquisa contra base de conhecimento privada (PDFs internos,
  Notion exportado, transcrições proprietárias) sem expor o conteúdo a APIs públicas
  de LLM ou search engines. Constraint dominante: privacy/compliance.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {dimensão decisiva — ex: "suporte nativo a private RAG via local embeddings + sem
     telemetria por default. Score `tool_runtime_integration` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"
  rationale: |
    {fallback — ex: "self-host disponível mas requer setup mais pesado. Use quando
     {candidate_x} não couber por outro motivo."}

decisive_dimension: "{group_id ou microdim_id que diferencia neste contexto}"
gap_to_mitigate: |
  {o que primary NÃO entrega aqui — ex: "Não tem citation Gate built-in; mitigação:
   wrap output em script de verificação local."}
```

### Use Case 2 — SaaS sem fricção / time-to-first-result

```yaml
id: uc_2_saas_fast
scenario: |
  Time pequeno sem ops, precisa começar a pesquisar em < 5 minutos, aceita SaaS,
  aceita custo por query. Constraint dominante: time-to-value.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "Hosted, no-install, free tier suficiente para primeiros 50 queries/mês.
     Score `ux_operator_control` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Quota gratuita acaba rápido — migrar para plano pago ou self-host se uso > 100/dia."}
```

### Use Case 3 — Agent customizado / pipeline próprio

```yaml
id: uc_3_custom_agent
scenario: |
  Owner quer construir agent customizado consumindo a pesquisa via API/SDK,
  integrando em pipeline próprio (Sinkra/AIOX/N8N/Zapier). Constraint dominante:
  programmability + estabilidade de contrato.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "SDK Python + JSON schema estável + webhook callbacks. Score
     `multi_agent_orchestration` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Sem schema versioning explícito — pin SDK version em requirements."}
```

### Use Case 4 — Artigos longos / dossiês profundos

```yaml
id: uc_4_long_form
scenario: |
  Pesquisador precisa gerar dossiê de 5k-15k palavras com seções organizadas,
  citações inline, tabelas comparativas. Constraint dominante: depth + structure.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "Multi-wave search + synthesis pipeline + native markdown output.
     Score `research_depth_synthesis` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Output longo pode quebrar context window — chunkar por seção."}
```

### Use Case 5 — SOTA / fronteira científica

```yaml
id: uc_5_sota_scientific
scenario: |
  Owner pesquisando state-of-the-art em domínio acadêmico (paper review, lit
  survey). Constraint dominante: cobertura de arXiv/PubMed/Semantic Scholar +
  citation accuracy.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "Native scholarly adapters (arXiv/PubMed/Semantic Scholar) +
     citation Gate. Score `evidence_fidelity_evaluation` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Cobertura de preprints depende do adapter — confirmar update frequency."}
```

### Use Case 6 — Controle de fontes / curadoria explícita

```yaml
id: uc_6_source_control
scenario: |
  Owner quer restringir busca a domínios pré-aprovados (whitelist) e rejeitar
  fontes não-autoritativas (blacklist). Constraint dominante: source curation
  policy.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "Suporta `allowed_domains` + `blocked_domains` flags + per-query override.
     Score `ux_operator_control` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Não verifica overlap entre domain whitelist e SERP cap — review manual."}
```

### Use Case 7 — Modelos locais / offline / data sovereignty

```yaml
id: uc_7_local_models
scenario: |
  Owner em ambiente sem internet ou com mandato de data sovereignty (defesa,
  saúde, jurídico). Constraint dominante: tudo on-prem + reproducibilidade.

primary:
  candidate: "{candidate_x}"
  rationale: |
    {ex: "Ollama-compatible + local embeddings + sem chamadas externas.
     Score `tool_runtime_integration` ✅ confirmed."}

secondary:
  candidate: "{candidate_y}"

decisive_dimension: "{...}"
gap_to_mitigate: |
  {ex: "Local model quality varia por hardware — recomendar mínimo 16GB VRAM."}
```

---

## Tabela Cruzada — Candidate × Use Case

Marker key: ✅ best fit (primary) | ◐ acceptable secondary | ? evaluate per case | — does not fit

> Substitua os candidatos abaixo pelos players reais do seu run. A tabela DEVE incluir TODOS os candidates avaliados (mesmo aqueles que perdem em todos os use cases — transparência).

| Use Case | {candidate_1} | {candidate_2} | {candidate_3} | {candidate_4} | {candidate_5} |
|---|:---:|:---:|:---:|:---:|:---:|
| 1 — Documentos privados | ✅ | ◐ | — | ? | — |
| 2 — SaaS rápido | — | ✅ | ◐ | — | ? |
| 3 — Agent customizado | ◐ | — | ✅ | ? | — |
| 4 — Artigos longos | ✅ | ◐ | — | ? | — |
| 5 — SOTA científico | — | ? | ◐ | ✅ | — |
| 6 — Controle de fontes | ◐ | — | ✅ | — | ? |
| 7 — Modelos locais | — | — | — | — | ✅ |

**Leitura por candidate (TL;DR):**

- `{candidate_1}` — primary em [1, 4]; secondary em [3, 6].
- `{candidate_2}` — primary em [2]; secondary em [1, 4].
- `{candidate_3}` — primary em [3, 6]; secondary em [2, 5].
- `{candidate_4}` — primary em [5]; uncertain em vários (avaliar caso a caso).
- `{candidate_5}` — primary em [7]; raramente competitivo fora deste use case.

---

## Anti-Patterns Evitados

- ❌ Tratar este atomo como sumário do report (`02-research-report.md`/`executive-report.md`) — este é **prescritivo**, não descritivo.
- ❌ Recomendar o mesmo candidate em todos os use cases (ranking-disfarçado-de-recomendação).
- ❌ Omitir candidates que perdem em todos os use cases — transparência exige listar.
- ❌ Usar < 5 use cases — quebra a granularidade prescritiva (STORY-RA-F.2 AC-4 mínimo).
- ❌ Pular `decisive_dimension` em algum use case — sem ele a recomendação vira opinião.
- ❌ Pular `gap_to_mitigate` em algum use case — primary sem lacuna é hype, não análise.

---

## Decision Trail

```yaml
decision_log:
  use_cases_total: {M}
  primary_distribution:                 # quantas vezes cada candidate ganhou como primary
    {candidate_1}: {N1}
    {candidate_2}: {N2}
    # ...
  unanimous_winner: false                # se TRUE → use case framing está sub-segmentando; revise
  ties_broken_by: "{microdim_id ou critério usado para desempates}"
  references:
    - "matrices.yaml | comparison-matrix.json"
    - "criteria.md"
    - "02-research-report.md | executive-report.md"
```

---

*Template `recommendations-by-use-case.md` v1.0 — STORY-RA-F.2 AC-4 | Aligned to `.claude/rules/research-bench-gold.md` (companion to criteria.md from STORY-RA-F.1) | Status code 4-níveis from `squads/research/scripts/tech-research/coverage_matrix_helper.py`.*
