---
task-id: an-extract-session-heuristics
name: "Extrair Heurísticas de Sessão de Trabalho"
version: 4.1.0-gah-calibrate
execution_type: Agent
model: Opus
haiku_eligible: false
model_rationale: "Requer síntese de padrões implícitos em execução real — Opus para profundidade"
estimated-time: 15 min
complexity: medium
agent: "@oalanicolas"
process_id: "SP-EXTRACT-SESSION-HEURISTICS"
mode: VALIDAR
parent_task: an-extract-heuristics
parent_relationship: "specialization — herda Pareto ao Cubo, SE/ENTÃO format, 3-Layer, Quality Check; adiciona session eligibility, git worker, cross-session triangulation, hook integration"

inputs:
  required:
    - session_context: "Auto-gerado pelo Worker de contexto OU fornecido manualmente"
  optional:
    - epic_id: "Epic ID se houver (ex: Epic 71)"
    - handoff_file: "Path para handoff da sessão (se existir)"
    - existing_heuristics: "Path para heurísticas existentes (default: minds/alan_nicolas/heuristics/)"

outputs:
  primary:
    - heuristics_files: "Arquivos AN_KE_NNN.md no formato padrão"
    - decision_cards: "Entries em decision-cards.yaml (L2)"
    - extraction_report: "Resumo: N candidatas → N formalizadas, classificação Pareto"
  secondary:
    - memory_update: "Atualização do MEMORY.md do projeto com referência"
    - token_updates: "Novos tokens se thresholds/comportamentos emergirem"

hook_integration:
  trigger: "manual (human invokes after session)"
  location: ".claude/hooks/post-session-heuristics.sh"
  auto_extract: false  # NEVER auto-extract. Human gate is non-negotiable.
  behavior: |
    1. Hook checks eligibility (deterministic, $0, <1s):
       - Filters out runner/mechanical commits (aiox-map, outputs, score_cards)
       - Counts only HUMAN decision commits (feat/refactor/fix non-mechanical)
       - Checks duration ≥30min, human decisions ≥2, code files ≥5
       - If runner_ratio >70% → skip (runner session)
    2. If eligible: SUGGESTS to human, shows what was found
    3. Human decides: /extract-session-heuristics OR skip
    4. NEVER extracts without explicit human approval
  rationale: |
    90% das sessões são runners autônomos (aiox-map, mmos, copy) que geram
    50+ commits mecânicos. Auto-extract iria gerar heurísticas de lixo.
    AN_KE_002: "Se entrar cocô, sai cocô."

memory_routing:
  heuristic_file: "minds/{heuristic_owner_slug}/heuristics/AN_KE_NNN.md"
  decision_cards: "minds/{heuristic_owner_slug}/heuristics/decision-cards.yaml"
  project_memory: "~/.claude/projects/{project}/memory/MEMORY.md"
  memory_entry_format: "- [Heuristics AN_KE_NNN-NNN](file.md) — one-line hook"

checklist: "checklists/session-heuristics-extraction.md"
template: "templates/session-heuristic-tmpl.md"
elicit: false
---

<!-- AIOX_TASK_METADATA:START -->
```yaml
framework_task_metadata:
  task_id: an-extract-session-heuristics
  task_name: Extrair Heurísticas de Sessão de Trabalho
  status: pending
  responsible_executor: '@oalanicolas'
  execution_type: Agent
  estimated_time: 15m
  domain: Operational
  input:
  - 'session_context auto-gerado pelo Worker ou fornecido manualmente'
  output:
  - 'heuristics_files arquivos AN_KE_NNN.md no formato padrão'
  - 'decision_cards entries em decision-cards.yaml'
  - 'extraction_report com contagem por zona Pareto'
  action_items:
  - Verificar session eligibility (duração >= 30min, decisões >= 2)
  - Varrer sessão com perguntas-guia (CDM)
  - Filtrar via Pareto ao Cubo
  - Dedup e triangulação cross-session
  - Formalizar em L2 (YAML) e L3 (.md)
  - Persistir em memory e commit
  acceptance_criteria:
  - Sessão elegível (duração >= 30min, decisões >= 2)
  - Heurísticas formalizadas com [SOURCE:] rastreável
  - Decision-cards atualizados
  - Quality check score >= 5/6
  output_persistence: transient_output
  accountable_id: '@oalanicolas'
  accountability_scope: full
  escalation_priority: medium
```
<!-- AIOX_TASK_METADATA:END -->

<!-- AIOX_CONTRACT:START -->
```yaml
aiox_contract:
  Domain: Operational
  atomic_layer: Atom
  executor: Agent
  pre_condition: "session_context disponível (auto-gerado ou manual), sessão elegível (duração >= 30min, decisões >= 2)"
  post_condition: "heurísticas de sessão formalizadas, decision-cards atualizados, extraction_report com contagem por zona Pareto"
  performance: "executar em 15min, registrar erro explicitamente e escalar via handoff sem falha silenciosa."
```
<!-- AIOX_CONTRACT:END -->

# SP-EXTRACT-SESSION-HEURISTICS — Processo de Extração de Heurísticas de Sessão

> **Processo AIOX mapeado.** Não é uma task solta — é um pipeline de 5 fases
> com tokens, checkpoints e composição formal.
>
> **Parent task:** `an-extract-heuristics` (SP-EXTRACT-HEURISTICS) — framework base para extração de experts.
> Esta é uma **especialização** que extrai de sessões de execução (o que aprendemos fazendo).
> Herda: Pareto ao Cubo, SE/ENTÃO/NUNCA format, 3-Layer (L1/L2/L3), Quality Check pattern.
> Adiciona: Session Eligibility, git worker, cross-session triangulation, hook integration.
>
> **Princípio:** "Curadoria > Volume. Se entrar cocô, sai cocô."

---

## Process Tokens

```yaml
tokens:
  - token_id: "TKN-ESH-THR-001"
    family: Threshold
    name: min_source_traceability
    value: 100
    unit: "%"
    description: "Todas as heurísticas DEVEM ter [SOURCE:]. Zero tolerância."
    consumed_by: ["phase_4_formalize", "quality_check"]

  - token_id: "TKN-ESH-THR-002"
    family: Threshold
    name: min_candidatas_brutas
    value: 5
    description: "Mínimo de candidatas brutas antes de filtrar. Se < 5, sessão não teve profundidade suficiente."
    consumed_by: ["phase_1_identify"]

  - token_id: "TKN-ESH-THR-003"
    family: Threshold
    name: max_generico_ratio
    value: 30
    unit: "%"
    description: "Se > 30% das candidatas são genéricas (💩), a varredura está rasa. Aprofundar."
    consumed_by: ["phase_2_filter"]

  - token_id: "TKN-ESH-THR-004"
    family: Threshold
    name: min_quality_check_score
    value: 5
    unit: "de 6"
    description: "Score mínimo no quality check para aprovar extração."
    consumed_by: ["quality_check"]

  - token_id: "TKN-ESH-BEH-001"
    family: Behavior
    name: overlap_action
    value: "update_existing"
    description: "SE heurística duplica existente COM nova evidência → ATUALIZAR, não criar nova."
    consumed_by: ["phase_3_overlap"]

  - token_id: "TKN-ESH-BEH-002"
    family: Behavior
    name: triangulation_promotion
    value: "3_sessions_promote"
    description: "SE 3+ sessões confirmam mesma heurística → ELEVAR zona (20% → 4%, 4% → 0,8%)."
    consumed_by: ["phase_3_overlap"]

  - token_id: "TKN-ESH-TAX-001"
    family: Taxonomy
    name: heuristic_types
    value: ["Decision Heuristic", "Veto Heuristic", "Architecture Heuristic", "Observability Heuristic", "State Management Heuristic"]
    description: "Tipos válidos de heurística. Toda nova deve encaixar em um desses."
    consumed_by: ["phase_4_formalize"]

  - token_id: "TKN-ESH-TAX-002"
    family: Taxonomy
    name: pareto_zones
    value:
      genialidade: "0.8% — muda paradigma"
      excelencia: "4% — guardrail que previne retrabalho"
      impacto: "20% — boa prática que acelera"
      merda: "80% — genérico, sem evidência, descartar"
    description: "Classificação obrigatória via Pareto ao Cubo."
    consumed_by: ["phase_2_filter"]

  - token_id: "TKN-ESH-ACC-001"
    family: Accountability
    name: extractor
    value: "@oalanicolas"
    description: "Knowledge Architect é accountable pela qualidade da extração."
    consumed_by: ["all_phases"]

  # ── Gap #3: Session Eligibility ──
  - token_id: "TKN-ESH-THR-005"
    family: Threshold
    name: session_min_duration_minutes
    value: 30
    description: "Sessão < 30min não merece extração. Typo fixes não geram heurísticas."
    consumed_by: ["hook_integration", "phase_0_eligibility"]

  - token_id: "TKN-ESH-THR-006"
    family: Threshold
    name: session_min_decisions
    value: 2
    description: "Sessão precisa de ≥2 decisões de arquitetura/pivot pra justificar extração."
    consumed_by: ["hook_integration", "phase_0_eligibility"]

  - token_id: "TKN-ESH-THR-007"
    family: Threshold
    name: session_min_files_changed
    value: 5
    description: "Sessão com <5 arquivos modificados provavelmente não tem profundidade."
    consumed_by: ["hook_integration"]

  # ── Gap #6: Evidence Append ──
  - token_id: "TKN-ESH-BEH-003"
    family: Behavior
    name: evidence_append_format
    value: "\"[SOURCE: sessão {id}, {project}] '{evidência concreta verbal}'\""
    description: "Formato padronizado para append de evidence em heurísticas existentes."
    consumed_by: ["phase_3_overlap"]

  - token_id: "TKN-ESH-THR-008"
    family: Threshold
    name: max_evidence_entries
    value: 10
    description: "Máximo de evidence entries por heurística. Acima disso, consolidar."
    consumed_by: ["phase_3_overlap"]
```

---

## Session Eligibility (Phase 0 — Gate)

Antes de iniciar a extração, verificar se a sessão merece:

```yaml
session_eligibility:
  min_duration: 30  # TKN-ESH-THR-005
  min_decisions: 2   # TKN-ESH-THR-006
  min_files_changed: 5  # TKN-ESH-THR-007
  skip_if:
    - "only docs/ changes (no code)"
    - "only outputs/ changes (artifacts, not decisions)"
    - "only typo/formatting fixes"
    - "session < 30 minutes"
```

**Worker de contexto automático (Gap #3):**

```bash
# Gerar contexto da sessão automaticamente ($0, <2s)
SESSION_COMMITS=$(git log --since="3 hours ago" --oneline 2>/dev/null | head -20)
SESSION_FILES=$(git diff --stat HEAD~10 2>/dev/null | tail -5)
SESSION_DURATION_ESTIMATE=$(git log --since="3 hours ago" --format="%ar" 2>/dev/null | tail -1)
FILES_CHANGED=$(git diff --stat HEAD~10 2>/dev/null | tail -1 | grep -oE '[0-9]+ file' | grep -oE '[0-9]+')

# Eligibility check
if [[ "${FILES_CHANGED:-0}" -lt 5 ]]; then
  echo "SKIP: <5 files changed"
  exit 0
fi

# Gerar contexto compacto
cat <<EOF
Session Context (auto-generated):
- Commits: $(echo "$SESSION_COMMITS" | wc -l | tr -d ' ')
- Files changed: ${FILES_CHANGED:-0}
- Duration estimate: ${SESSION_DURATION_ESTIMATE:-unknown}
- Recent commits:
$SESSION_COMMITS
- Files summary:
$SESSION_FILES
EOF
```

---

## Veto Conditions

| ID | Condition | Token | Action |
|----|-----------|-------|--------|
| VETO-ESH-001 | Heurística sem [SOURCE:] | TKN-ESH-THR-001 | BLOCK — adicionar evidência ou descartar |
| VETO-ESH-002 | Heurística inferida sem evidência empírica | TKN-ESH-THR-001 | BLOCK — precisa de caso real, não teoria |
| VETO-ESH-003 | Heurística duplica existente sem nova evidência | TKN-ESH-BEH-001 | BLOCK — atualizar existente em vez de criar nova |
| VETO-ESH-004 | < 5 candidatas brutas (sessão rasa) | TKN-ESH-THR-002 | BLOCK — aprofundar varredura antes de filtrar |
| VETO-ESH-005 | > 30% candidatas genéricas | TKN-ESH-THR-003 | WARN — varredura rasa, re-analisar com perguntas-guia |

---

## Phase 1: IDENTIFY — Varredura de Candidatas (5 min)

**Executor:** @oalanicolas
**Input:** session_context (conversa, handoff, commits, bugs)
**Output:** Lista de 5-15 candidatas brutas

### Fontes de Heurísticas (5 categorias)

| Categoria | O que procurar | Exemplo |
|-----------|---------------|---------|
| **Decisões pivot** | Momentos que mudaram o rumo | "Comparamos validate-skill vs validate-squad → gap analysis gerou roadmap" |
| **Bugs/Incidentes** | Erros que revelaram regras | "Bug ${} quoting → 'testar módulo isolado, não pipeline'" |
| **Anti-patterns evitados** | O que quase deu errado | "Quase removemos post-process.sh → 'audit gate antes de cleanup'" |
| **Patterns validados** | O que funcionou e por quê | "Batch fix mecânico 19% → 94% → 'mecânico primeiro, hardening depois'" |
| **Research insights** | Confirmação/refutação externa | "Anthropic paper confirma composable > frameworks" |

### Perguntas-guia (Critical Decision Method)

```
1. "O que deu certo que NÃO ERA ÓBVIO antes desta sessão?"
2. "O que quase deu errado? Em que PONTO EXATO evitamos?"
3. "O que faríamos DIFERENTE na próxima vez?"
4. "Que regra SE/ENTÃO emergiu que não tínhamos antes?"
5. "Que suposição foi INVALIDADA por dados empíricos?"
6. "Que padrão se REPETIU 2+ vezes durante a sessão?"
```

### Checkpoint Phase 1

```yaml
gate: "candidatas >= TKN-ESH-THR-002 (5)"
pass: "Prosseguir para Phase 1.5 (GAH)"
fail: "VETO-ESH-004 — sessão insuficiente, precisa de mais contexto"
```

---

## Phase 1.5: GAH — Gate de Admissibilidade Heurística (5 min)

**Executor:** @oalanicolas
**Input:** Lista de candidatas brutas de Phase 1
**Output:** 1 audit YAML por candidata em `outputs/minds/gah-audits/{owner_slug}/{candidate-slug}-{YYYYMMDD}.yaml`
**Mode:** FLAG (calcula verdict, não bloqueia persistência — operador revisa)
**Template:** `squads/squad-creator-pro/templates/gah-audit-tmpl.yaml`

### Por que existe

Sintomas observados em sessões anteriores (alimentaram o desenho deste gate):

1. **OVERLAP raso (Phase 3 era performativo)** — agente ignorou cards existentes que cobriam o princípio (ex: AN_KE_201 era subset puro de AN_KE_007).
2. **Inflação de cards específicos** — agente aprovou cards stack-locked (ex: AN_KE_204 GENIALIDADE com vocabulário CSS-only).
3. **Tautologias disfarçadas de heurísticas** — cards sem tensão sistêmica real (ex: AN_KE_208 "use spread re-export" — técnica JS-específica, não decisão).

GAH força 4 testes semânticos estruturados que filtram cada um desses eixos antes da candidata chegar em Phase 2 (FILTER).

### Princípio operacional

**Cada candidata bruta passa por 4 testes IN ORDER. Cada teste produz output ESTRUTURADO obrigatório.** LLM não pode escapar com "depende, talvez". Se não consegue produzir o output estruturado → já é sinal de que a candidata não é heurística.

### Test 1 — Vocabulary Strip (semântico estruturado)

**Goal:** heurística sobrevive sem vocabulário stack-específico?

```yaml
llm_task:
  step_1_extract_specific_vocab:
    instruction: |
      Liste TODOS os termos stack/tool/format-específicos no `rule:` da candidata.
      Categorias a varrer:
        - Tools: node_modules, npm, playwright, eslint, ts, tsx, react, tailwind, css, html, dom, etc
        - Paths: src/, app/, .claude/, squads/, lib/, etc
        - Formats: yaml, json, jsonl, ndjson, tsx, cjs, esm, etc
        - Stack-keywords: :root, .btn, max-w-, text-[, pb-, AWS, Postgres, etc
    output:
      stack_specific_terms: [lista]

  step_2_rewrite_with_placeholders:
    instruction: |
      Reescreva o `rule:` substituindo cada termo de step_1 por [PLACEHOLDER-GENÉRICO].
      Exemplos de mapping:
        node_modules → [DEPENDENCY-REGISTRY]
        src/ → [SOURCE-DIR]
        :root → [SCHEMA-DECLARATION]
        .btn → [COMPONENT-SELECTOR]
    output:
      rewritten_rule: "..."
      placeholder_mapping: { ... }

  step_3_evaluate:
    instruction: |
      Compare original vs reescrito. Responda:
        - O reescrito ainda é uma INSTRUÇÃO COERENTE? (yes/no)
        - O reescrito ainda CARREGA INFORMAÇÃO ACIONÁVEL ou virou platitude? (yes/low/no)
        - Algum termo de step_1 era ESSENCIAL pro princípio (não pode virar placeholder)? (yes/no)
    output:
      coherent_after_rewrite: yes|no
      information_preserved: yes|low|no
      stack_locked: yes|no

verdict_logic:
  PASS: "(coherent_after_rewrite=yes AND information_preserved=yes) AND stack_locked=no"
  FAIL_paths:
    stack_locked=yes:
      → "REJECT como heurística → ARCHIVE ou virar TASK"
    coherent=no:
      → "REJECT — rule é só sequência mecânica → vira TASK"
    information_preserved=low:
      → "REJECT — rule é trivialmente verdadeira/subset de existing → pipeline_instance ou ARCHIVE"
```

**Exemplo aplicado — AN_KE_201 (FAIL):**

```yaml
original: "SE prestes a propor stack/dependência → ENTÃO ANTES de sugerir, inventariar `node_modules` (e equivalentes)."
stack_specific_terms: ["node_modules", "npm ls", "find -maxdepth", "playwright", "axios"]
rewritten_rule: "SE prestes a propor [TOOL-CATEGORY] → ENTÃO inventariar [DEPENDENCY-REGISTRY] (e equivalentes)."
coherent_after_rewrite: yes
information_preserved: low  ← reescrita vira "verifique se já existe antes de propor novo" = AN_KE_007
stack_locked: no
verdict: FAIL → REJECT → pipeline_instance em AN_KE_007
```

**Exemplo aplicado — AN_KE_211 (PASS):**

```yaml
original: "SE consumer reporta erro em location X AND erro tem padrão grep-able → ENTÃO extrair signature, sweep escopo, batch-fix todas instâncias."
stack_specific_terms: []  ← rule já é agnóstica
rewritten_rule: <same>
coherent_after_rewrite: yes
information_preserved: yes
stack_locked: no
verdict: PASS
```

### Test 2 — Cross-Domain Instances (semântico estruturado)

**Goal:** rule aplica em ≥3 domínios sem reescrita?

```yaml
llm_task:
  step_1_propose_instances:
    instruction: |
      Para cada um dos 8 domínios abaixo, gere UMA instância concreta onde o rule se aplica:
        UI, API, DB, Security, DevOps, Content/Copy, Process/Workflow, Negotiation/Communication

      Para cada instância, output:
        - domain: <nome>
        - instance: <descrição concreta de 1 frase OU "N/A" se não aplica>
        - applies_literally: yes|no  ← rule funciona SEM reescrita?
        - needs_rewrite: <se applies_literally=no, qual reescrita seria necessária>
    output:
      instances: [...]

  step_2_count_literal_matches:
    instruction: "Contar instâncias com applies_literally=yes E needs_rewrite vazio"
    output:
      literal_matches: <int>

verdict_logic:
  PASS: "literal_matches >= 3"
  FLAG: "literal_matches == 2 → REVIEW (heurística borderline cross-domain)"
  FAIL: "literal_matches < 2 → REJECT como heurística → vira TASK ou pipeline_instance"
```

**Exemplo aplicado — AN_KE_212 (PASS):**

```yaml
instances:
  - { domain: UI, instance: "container width singleton per page", applies_literally: yes }
  - { domain: API, instance: "base URL env config singleton", applies_literally: yes }
  - { domain: DB, instance: "connection string single source", applies_literally: yes }
  - { domain: Security, instance: "auth token TTL config singleton", applies_literally: yes }
  - { domain: DevOps, instance: "retry policy in HTTP wrapper", applies_literally: yes }
  - { domain: Content, instance: "N/A", applies_literally: no }
  - { domain: Process, instance: "single workflow definition referenced by N stages", applies_literally: yes }
  - { domain: Negotiation, instance: "N/A", applies_literally: no }
literal_matches: 6
verdict: PASS
```

**Exemplo aplicado — AN_KE_208 (FAIL):**

```yaml
instances:
  - { domain: UI, instance: "N/A — rule fala de module.exports", applies_literally: no }
  - { domain: API, instance: "N/A", applies_literally: no }
  - { domain: DB, instance: "N/A", applies_literally: no }
  - { domain: Security, instance: "N/A", applies_literally: no }
  - { domain: DevOps, instance: "Maybe — package versioning?", applies_literally: no, needs_rewrite: "muito" }
  - { domain: Content, instance: "N/A", applies_literally: no }
  - { domain: Process, instance: "N/A", applies_literally: no }
  - { domain: Negotiation, instance: "N/A", applies_literally: no }
literal_matches: 0
verdict: FAIL → REJECT → archive (técnica JS-específica)
```

### Test 3 — Other-Human Test (semântico com critic externo simulado)

**Goal:** outro humano em outro projeto encontra valor sem o contexto desta sessão?

```yaml
llm_task:
  step_1_strip_context:
    instruction: |
      Reescreva a card REMOVENDO toda referência ao contexto original:
        - [SOURCE: ...] → [SOURCE: <generic example>]
        - Empresa/produto específico → [PRODUCT-X]
        - Arquivos específicos → [FILE-Y]
        - Pessoa específica → [PERSON]
    output:
      stripped_version_rule: "..."
      stripped_version_evidence: "..."

  step_2_simulate_outside_reader:
    instruction: |
      ROLE-PLAY como dev/PM/designer em projeto que NUNCA viu.
      Você lê só a versão stripped da card (não tem contexto desta sessão).
      Output:
        - first_impression: <1-frase reação ao ler>
        - utility_score: 1-10 (1=trivial/óbvio, 10=mind-blowing/transformativo)
        - applicable_to_my_work: yes|no
        - if_yes_example: <exemplo concreto de aplicação no projeto hipotético>
        - if_no_why_not: <justificativa>

  step_3_self_critic:
    instruction: |
      O exemplo gerado em step_2.if_yes_example é COERENTE com o rule original
      OU forçado/genérico? (coherent / forced)
    output:
      example_coherence: coherent|forced|n/a

verdict_logic:
  PASS: "utility_score >= 6 AND applicable_to_my_work=yes AND example_coherence=coherent"
  FLAG: "utility_score == 5 OR example_coherence=forced → REVIEW"
  FAIL: "utility_score < 5 OR applicable_to_my_work=no → REJECT como heurística"
```

**Exemplo aplicado — AN_KE_204 pré-rewrite (FAIL):**

```yaml
stripped_version: "Per-Selector CSS Beats :root Token Inference"
first_impression: "Hmm, isso é só sobre CSS. Não trabalho com CSS."
utility_score: 4
applicable_to_my_work: no
verdict: FAIL → REWRITE OBRIGATÓRIO antes de admitir como GENIALIDADE
```

**Exemplo aplicado — AN_KE_204 pós-rewrite (PASS):**

```yaml
stripped_version: "Per-Instance Usage Beats Schema Declaration"
first_impression: "Interessante. Schema declarado vs uso real — vejo isso em OpenAPI specs."
utility_score: 8
applicable_to_my_work: yes
example: "Nosso OpenAPI declara default=0 num campo, mas 80% dos requests reais mandam 5. Documentação diverge da realidade."
example_coherence: coherent
verdict: PASS
```

### Test 4 — Anti-Test (semântico de tensão sistêmica)

**Goal:** existe contexto onde fazer o oposto é certo? (= heurística tem tensão real, não é tautologia)

```yaml
llm_task:
  step_1_generate_anti_rule:
    instruction: "Gere o anti-rule: SE <trigger original> → ENTÃO NÃO <ação original>"
    output:
      anti_rule: "..."

  step_2_search_legitimate_anti_context:
    instruction: |
      Existe contexto REAL onde anti-rule é a escolha CORRETA?
      Cuidado: NÃO é "mau uso do rule original".
      É contexto onde o oposto é genuinamente certo.
    output:
      anti_context_exists: yes|no
      anti_context_description: "..."
      anti_context_evidence: "..."

  step_3_classify_tension:
    instruction: "Se anti_context_exists=yes, nomeie a TENSÃO sistêmica entre rule e anti-rule"
    output:
      tension_axis: "ex: 'speed vs thoroughness', 'autonomy vs coordination'"
      resolution_principle: "quando rule wins vs quando anti-rule wins"

verdict_logic:
  PASS: "anti_context_exists=yes AND tension_axis named AND resolution_principle articulable"
  FLAG: "anti_context_exists=yes mas tension_axis vago → REVIEW"
  FAIL: "anti_context_exists=no → REJECT — rule é tautologia/convenção universal → vira RULE ou nada"
```

**Exemplo aplicado — AN_KE_211 (PASS):**

```yaml
anti_rule: "SE consumer reporta erro com pattern grep-able → ENTÃO NÃO sweep, fix só local"
anti_context_exists: yes
anti_context_description: "Erro genuinamente local — single text node, intentional divergence, scoped change"
tension_axis: "minimal blast radius vs systemic-fix economy"
resolution_principle: "sweep quando padrão repetível; fix local quando intentional divergence"
verdict: PASS
```

**Exemplo hipotético — "Sempre commit antes de end-of-day" (FAIL):**

```yaml
anti_rule: "SE end-of-day → ENTÃO NÃO commit"
anti_context_exists: no  ← exceto bugs WIP que quebram tudo, raríssimo
verdict: FAIL → não é heurística, é convenção universal → vira rule (.claude/rules/) ou nada
```

### Aggregate verdict (decisão matrix)

```yaml
| pass | flag | fail | final_verdict              | next_step |
|-----:|-----:|-----:|----------------------------|-----------|
|    4 |    0 |    0 | ADMIT                      | Procede para Phase 2 |
|    3 |    1 |    0 | ADMIT_WITH_REWRITE_LIGHT   | Reescrever campo FLAG, depois Phase 2 |
|    2 |  1-2 |  0-1 | REWRITE_REQUIRED           | Não procede sem reescrita do(s) campo(s) FAIL |
|  0-2 |    * |  2-4 | REJECT                     | Reclassificar destination |

destination_if_reject:
  - pipeline_instance — subset of existing heuristic
  - task — mechanical sequence
  - checklist — point-by-point validation gate
  - rule — repo convention
  - archive — none of the above
```

### Mode v1: FLAG only

Audit é gerado para cada candidata. Verdict é calculado. Mas:

- **TODAS** candidatas (incluindo REJECT) seguem para Phase 2 (FILTER)
- Operador revisa audit YAML em `outputs/minds/gah-audits/{owner_slug}/` ANTES de Phase 5 (PERSIST)
- Operador pode override: aceitar verdict, rejeitar verdict, requisitar mais info

**Quando promover para BLOCK mode:** após 3 sessões consecutivas onde GAH verdict bate com decisão final do operador (calibração).

### Output

```
outputs/minds/gah-audits/{heuristic_owner_slug}/
├── {candidate-1-slug}-{YYYYMMDD}.yaml
├── {candidate-2-slug}-{YYYYMMDD}.yaml
├── ...
└── summary-{YYYYMMDD}.md   (opcional — agregação por sessão)
```

### Gate

```yaml
gate: "Para cada candidata bruta de Phase 1, gerar 1 audit YAML completo (4 testes preenchidos + aggregate verdict)"
pass: "Todos audits gerados → prosseguir para Phase 2 com candidatas + verdicts"
fail: "Audit incompleto (algum teste sem output estruturado) → flag VETO-ESH-007 (GAH incompleto) + escalonar"
```

---

## Phase 2: FILTER — Pareto ao Cubo (3 min)

**Executor:** @oalanicolas
**Input:** Lista de candidatas brutas
**Output:** Lista filtrada com classificação por zona

### Classificação

| Zona | Critério | Ação | Emoji |
|------|----------|------|-------|
| **0,8% Genialidade** | Muda paradigma. Sem isso, o trabalho seria fundamentalmente diferente. | FORMALIZAR primeiro | 🧠 |
| **4% Excelência** | Guardrail que previne retrabalho significativo | FORMALIZAR | 💎 |
| **20% Impacto** | Boa prática que acelera | FORMALIZAR se tiver [SOURCE:] forte | 🔥 |
| **80% Merda** | Óbvio, genérico, sem evidência específica | DESCARTAR | 💩 |

### Teste de Genericidade (anti-💩)

```
SE a heurística funciona pra QUALQUER projeto sem contexto específico
→ Provavelmente genérica demais (💩)

SE a heurística só faz sentido DENTRO DO CONTEXTO desta sessão
→ Provavelmente valiosa (🔥💎🚀)

Boas heurísticas = contexto específico + evidência empírica + dados
```

### Checkpoint Phase 2

```yaml
gate: "generico_ratio <= TKN-ESH-THR-003 (30%)"
pass: "Prosseguir para Phase 3"
warn: "VETO-ESH-005 — re-analisar candidatas com perguntas-guia mais profundas"
```

---

## Phase 3: OVERLAP — Dedup + Triangulação (3 min)

**Executor:** @oalanicolas
**Input:** Lista filtrada
**Output:** Lista deduplicada (novas vs updates)

### Procedimento

```bash
# 1. Listar existentes
ls minds/{heuristic_owner_slug}/heuristics/ | sort

# 2. Para cada candidata:
#    a. Grep pela regra SE/ENTÃO nas existentes
#    b. Se match → verificar se sessão traz NOVA evidência
#    c. Se nova evidência → ATUALIZAR existente (adicionar evidence block)
#    d. Se sem match → CRIAR nova
```

### Triangulação (TKN-ESH-BEH-002)

```
SE 3+ sessões diferentes confirmam a mesma heurística
→ ELEVAR zona: 20% Impacto → 4% Excelência (ou 4% → 0,8%)
→ Adicionar nota: "Confirmada por N sessões independentes"
```

### Evidence Append Format (Gap #6 — TKN-ESH-BEH-003)

Quando atualizando heurística existente com nova evidência:

```markdown
## Evidence

    - "[SOURCE: sessão 8b1f20d, mmos] 'Batch fix 29 frontmatters: 19% → 94% PASS em 5min'"
    - "[SOURCE: sessão 9c3ca5e, mmos] 'yaml-repair.py desbloqueou Opus (0% → 67%)'"
```

**Regras:**
- Adicionar no final do bloco `evidence` do YAML na seção `## Configuration`
- Formato: `- "[SOURCE: sessão {id}, {projeto}] '{citação ou fato verbatim}'"`
- Máximo TKN-ESH-THR-008 (10) entries. Acima disso, consolidar as mais antigas.
- Se evidence contradiz a heurística → REAVALIAR a regra, não apenas appendar.

### Output

```yaml
dedup_result:
  new_heuristics: N      # criar AN_KE_NNN.md
  updated_existing: N    # adicionar evidence a AN_KE existente
  promoted: N            # zona elevada por triangulação
  discarded: N           # duplicata sem nova evidência
```

---

## Phase 4: FORMALIZE — 3 Camadas (4 min)

**Executor:** @oalanicolas
**Input:** Lista deduplicada
**Output:** L2 decision card (YAML) + L3 arquivo .md

### 3-Layer Format

| Camada | Formato | Propósito | Quando consultar |
|--------|---------|-----------|-----------------|
| **L1** | 3 campos inline no agente | Decisão rápida em runtime | Sempre — carregado com o agente |
| **L2** | ~8 campos em `decision-cards.yaml` | Decisão informada com evidence | Quando L1 não basta |
| **L3** | 40-80 linhas em AN_KE_NNN.md | Documentação completa, onboarding | Nunca em runtime — só referência |

**OBRIGATÓRIO:** Criar L2 (decision card) E L3 (.md). L1 é atualizado quando o agente é re-synced.

### Step 4a: Adicionar Decision Card (L2)

Em `minds/{heuristic_owner_slug}/heuristics/decision-cards.yaml`, adicionar:

```yaml
- id: AN_KE_NNN
  name: "Nome"
  rule: "SE {condição} → ENTÃO {ação}"
  zone: "{genialidade|excelencia|impacto}"
  trigger: "{quando se aplica}"
  anti_pattern: "{o que acontece quando ignora}"
  evidence: "{dado empírico com números [SOURCE:]}"
```

### Step 4b: Criar Arquivo .md (L3)

### Template

```markdown
# AN_KE_NNN - Nome da Heurística

**Type:** {TKN-ESH-TAX-001 — um dos tipos válidos}
**Zone:** {TKN-ESH-TAX-002 — 🧠|💎|🔥}
**Agent:** @oalanicolas
**Source:** [SOURCE: sessão {id}, {project} — descrição/contexto da sessão]

## Purpose

{Parágrafo substancial explicando o PROBLEMA que resolve, QUANDO se aplica, e POR QUE é específico (não genérico). Incluir exemplos contextuais da sessão onde ocorreu.}

## Configuration

\```yaml
AN_KE_NNN:
  name: "Nome da Heurística"
  zone: "{genialidade|excelencia|impacto}"
  trigger: "Quando esta heurística se aplica (condições exatas)"

  rule: |
    SE {condição observável no trabalho/código/planning}
    ENTÃO {ação específica de mitigação/decisão}
    NUNCA {anti-pattern ou abordagem ingênua correspondente}

  veto_condition:
    trigger: "O que caracteriza a quebra flagrante da regra"
    action: "VETO — Pesar: {Ação de emergência para bloquear e corrigir}"

  evidence:
    - "[SOURCE: sessão {id}, {project}] '{citação verbatim 1}'"
    - "[SOURCE: sessão {id}, {project}] '{citação verbatim 2}'"
\```

## Decision Tree

\```javascript
IF ({condição_principal})
  STEP_1: {ação inicial — ex: STOP, ANALYZE}
  STEP_2: {avaliação de subcondições}
    IF ({subcondição_tipo_a}) → {ação_especializada_a}
    ELSE IF ({subcondição_tipo_b}) → {ação_especializada_b}
    ELSE → {ação_padrão_fallback}
\```

## Failure Modes

### {Nome Criativo do Incidente (ex: O Schema que Conflitou)}
- **Trigger:** {condição prática que causou a falha no histórico}
- **Manifestation:** {como a falha se manifestou em log, erro ou UI}
- **Detection:** {como farejar este problema o mais cedo possível}
- **Prevention:** {a mudança exata de paradigma para nunca mais repetir}
\```
```

### Numeração (com proteção de race condition — Gap #4)

```bash
# Pegar último ID
last=$(ls minds/{heuristic_owner_slug}/heuristics/AN_KE_*.md 2>/dev/null | sort | tail -1 | grep -oE '[0-9]+')
last=${last:-0}
next=$((last + 1))
target="minds/{heuristic_owner_slug}/heuristics/AN_KE_$(printf '%03d' $next).md"

# SAFETY: verificar se arquivo já existe (race condition protection)
while [[ -f "$target" ]]; do
  next=$((next + 1))
  target="minds/{heuristic_owner_slug}/heuristics/AN_KE_$(printf '%03d' $next).md"
done

echo "Próximo ID: AN_KE_$(printf '%03d' $next)"
```

**Anti-pattern:** NUNCA sobrescrever heurística existente. Se ID conflita, incrementar até achar slot vazio.

### Localização

```
minds/{heuristic_owner_slug}/heuristics/AN_KE_NNN.md
```

---

## Phase 5: PERSIST — Memory + Commit (2 min)

**Executor:** @oalanicolas
**Input:** Arquivos criados + decision cards atualizados
**Output:** Memory atualizado, commit pushed

### Step 5a: Memory Routing (Gap #2)

Atualizar o MEMORY.md do **projeto** (cross-session recall):

```bash
# Path: ~/.claude/projects/{project-slug}/memory/MEMORY.md
# Formato: uma linha por batch de heurísticas
echo "- [Heuristics AN_KE_NNN-NNN](file.md) — one-line description" >> MEMORY.md
```

**Regras de routing:**
- **SEMPRE** atualizar project memory (`~/.claude/projects/.../memory/MEMORY.md`)
- **SE** heurística existente em memory → atualizar entrada, não duplicar
- **NÃO** criar entries separadas por heurística — agrupar por sessão

### Step 5b: Commit + Push

```
feat(minds): add AN_KE_NNN-NNN {descrição} heuristics to @oalanicolas
```

### Step 5c: Token Update (se aplicável)

Se uma heurística define um novo threshold ou comportamento que pode virar token:

```yaml
- token_id: "TKN-NEW-THR-001"
  family: Threshold
  name: min_consumers_for_extraction
  value: 3
  description: "Extraído de AN_KE_013"
```

---

## Quality Check

| # | Check | Token | Weight |
|---|-------|-------|--------|
| 1 | Todas heurísticas têm [SOURCE:] rastreável | TKN-ESH-THR-001 | BLOCKER |
| 2 | Zero heurísticas genéricas (sem evidência específica) | TKN-ESH-THR-003 | BLOCKER |
| 3 | Zero duplicatas (overlap = atualizar, não criar) | TKN-ESH-BEH-001 | HIGH |
| 4 | Classificação Pareto ao Cubo aplicada | TKN-ESH-TAX-002 | HIGH |
| 5 | Formato padrão seguido (YAML + decision tree + evidence) | — | MEDIUM |
| 6 | Numeração contínua (sem gaps, sem sobreposição) | — | LOW |

**Score mínimo:** TKN-ESH-THR-004 = 5/6 (BLOCKER + HIGH devem passar)

---

## Composition Map

```yaml
process:
  id: "SP-EXTRACT-SESSION-HEURISTICS"
  mode: VALIDAR
  executor: "@oalanicolas"
  trigger: "*extract-session-heuristics"

  phases:
    - phase: 1
      name: "IDENTIFY"
      executor: "@oalanicolas"
      input: [session_context, handoff_file]
      output: [candidatas_brutas]
      checkpoint: "candidatas >= 5"
      duration: "5 min"

    - phase: 2
      name: "FILTER"
      executor: "@oalanicolas"
      input: [candidatas_brutas]
      output: [candidatas_filtradas, classification_pareto]
      checkpoint: "generico_ratio <= 30%"
      duration: "3 min"

    - phase: 3
      name: "OVERLAP"
      executor: "@oalanicolas"
      input: [candidatas_filtradas, existing_heuristics]
      output: [dedup_result, new_list, update_list]
      checkpoint: null
      duration: "3 min"

    - phase: 4
      name: "FORMALIZE"
      executor: "@oalanicolas"
      input: [new_list, update_list]
      output: [heuristics_files]
      checkpoint: "all have [SOURCE:]"
      duration: "4 min"

    - phase: 5
      name: "PERSIST"
      executor: "@oalanicolas"
      input: [heuristics_files]
      output: [memory_update, commit]
      checkpoint: "quality_check >= 5/6"
      duration: "2 min"

  tokens_produced:
    - "Novos tokens se thresholds/comportamentos emergirem das heurísticas"

  tokens_consumed:
    - TKN-ESH-THR-001 (source traceability)
    - TKN-ESH-THR-002 (min candidatas)
    - TKN-ESH-THR-003 (max genérico ratio)
    - TKN-ESH-THR-004 (quality check score)
    - TKN-ESH-BEH-001 (overlap action)
    - TKN-ESH-BEH-002 (triangulation promotion)
    - TKN-ESH-TAX-001 (heuristic types)
    - TKN-ESH-TAX-002 (pareto zones)
    - TKN-ESH-ACC-001 (accountability)
```

---

## Activation

Mission router do agente @oalanicolas:

```yaml
"*extract-session-heuristics":
  task: "tasks/an-extract-session-heuristics.md"
  data: null
```

**Invocação:** `*extract-session-heuristics`

---

*"Curadoria > Volume. Heurísticas de sessão são ouro — extraídas de execução real, não de livro."* 🧠
