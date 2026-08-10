# DMN Formalization: Redactia

**Data:** 2026-03-23
**Agente:** James Taylor (Tier 2)
**Input:** Decision Models von Halle (7 DMs)
**Padrão:** DMN 1.3 (OMG) com expressões FEEL

---

## Decision Requirements Diagram (DRD) - Visão Geral

```
+------------------------------------------------------------------+
|                    REDACTIA SYSTEM DRD                            |
+------------------------------------------------------------------+

  [Essay PDF/Image]     [User Token]     [Essay Text]
        |                    |                |
        v                    v                v
  +------------+    +--------------+   +-----------+
  | DM-1: OCR  |    | DM-3: Auth   |   | DM-5: LLM |
  | Routing    |    | Gate         |   | Scoring   |
  +-----+------+    +------+-------+   +-----+-----+
        |                  |                  |
        v                  v                  v
  +------------+    +--------------+   +-----------+
  | DM-2: Word |    | DM-4: Essay  |   | DM-6:     |
  | Marking    |    | Access       |   | Analytics |
  +------------+    +--------------+   +-----------+
                                              |
                           +------------------+
                           v
                    +--------------+
                    | DM-7: Role   |
                    | Routing      |
                    +--------------+
```

---

## DM-1: OCR Routing Decision

### DRD

```
                   +--------------------+
                   | OCR Routing        |
                   | Decision           |
                   +--------+-----------+
                            |
            +---------------+---------------+
            |               |               |
   +--------v------+ +-----v-------+ +-----v---------+
   | Linguistic    | | Confidence  | | Uncertain     |
   | Validation    | | Metrics     | | Ratio         |
   +--------+------+ +-----+-------+ +-----+---------+
            |               |               |
   +--------v------+ +-----v-------+ +-----v---------+
   | Dictionary    | | Word        | | Low Conf      |
   | Result        | | Confidences | | Count         |
   +---------------+ +-------------+ +-----------+---+
                                                 |
                                          +------v--------+
                                          | OCR_CONF_     |
                                          | MEDIUM (0.60) |
                                          +---------------+
```

### Decision Table (DMN Hit Policy: F - First)

**Input columns:**

| Input | Type | Domain |
|-------|------|--------|
| linguistic_triggered | boolean | {true, false} |
| global_confidence | number | [0.0, 1.0] |
| uncertain_ratio | number | [0.0, 1.0] |

**Output columns:**

| Output | Type | Domain |
|--------|------|--------|
| routing_decision | string | {"manual_review", "automatic", "automatic_with_warning"} |
| requires_review | boolean | {true, false} |
| initial_status | string | {"pending_review", "processing"} |

**Rules (F - First match wins):**

| # | linguistic_triggered | global_confidence | uncertain_ratio | routing_decision | requires_review | initial_status |
|---|---------------------|-------------------|-----------------|------------------|----------------|----------------|
| 1 | true | - | - | "manual_review" | true | "pending_review" |
| 2 | false | >= 0.80 | <= 0.05 | "automatic" | false | "processing" |
| 3 | false | >= 0.72 | - | "automatic_with_warning" | false | "processing" |
| 4 | false | < 0.72 | - | "manual_review" | true | "pending_review" |

### FEEL Expressions

```feel
// Global confidence calculation
global_confidence = if total_words > 0 then sum(all_confidences) / total_words else 0.0

// Low confidence count
low_confidence_count = count(c in all_confidences where c < 0.60)

// Uncertain ratio
uncertain_ratio = if total_words > 0 then low_confidence_count / total_words else 0.0

// Warning threshold (derived)
warning_threshold = 0.80 * 0.9  // = 0.72

// Routing decision
routing_decision =
  if linguistic_triggered then "manual_review"
  else if global_confidence >= 0.80 and uncertain_ratio <= 0.05 then "automatic"
  else if global_confidence >= 0.72 then "automatic_with_warning"
  else "manual_review"
```

### Sub-Decision: Linguistic Validation (DMN Hit Policy: F)

| # | dictionary_available | word_count | unknown_count | triggered |
|---|---------------------|------------|---------------|-----------|
| 1 | false | - | - | false |
| 2 | true | < 10 | - | false |
| 3 | true | >= 10 | 0 | false |
| 4 | true | >= 10 | >= 1 | true |

### FEEL Expression

```feel
linguistic_triggered =
  if not dictionary_available then false
  else if word_count < 10 then false
  else unknown_count >= 1
```

### Sub-Decision: Word Filtering Before Dictionary Check (DMN Hit Policy: C - Collect)

**Input:** raw_word (string)
**Output:** include_in_check (boolean)

| # | Condition | include_in_check |
|---|-----------|-----------------|
| 1 | string length(raw_word) < 3 | false |
| 2 | raw_word in common_words_set | false |
| 3 | starts with(upper case(substring(raw_word, 1, 1)), substring(raw_word, 1, 1)) | false |
| 4 | upper case(raw_word) = raw_word and string length(raw_word) <= 5 | false |
| 5 | ends with(raw_word, "ção") or ends with(raw_word, "mente") or ends with(raw_word, "dade") | false |
| 6 | string length(raw_word) > 15 | false |
| 7 | (none of above) | true |

---

## DM-2: Word-Level Confidence Marking

### Decision Table (DMN Hit Policy: U - Unique)

| # | word_confidence | markup | tracking_list | llm_instruction |
|---|----------------|--------|---------------|-----------------|
| 1 | >= 0.85 | "" | "all_confidences" | "evaluate_normal" |
| 2 | [0.60..0.85) | "" | "all_confidences" | "evaluate_normal" |
| 3 | [0.40..0.60) | "[{word}?]" | "uncertain_words" | "evaluate_cautious" |
| 4 | < 0.40 | "[RASURA]" | "erasures" | "ignore_completely" |

### Pre-filter Decision Table (DMN Hit Policy: F)

| # | Condition | action |
|---|-----------|--------|
| 1 | is_digit(word) and number(word) in [1..30] | "skip" |
| 2 | lower_case(word) in PRINTED_TEXT_PATTERNS | "skip" |
| 3 | contains(lower_case(word), "www.") or contains(lower_case(word), "http") | "skip" |
| 4 | (none of above) | "process" |

### FEEL Expressions

```feel
// Word markup
markup =
  if word_confidence >= 0.85 then ""
  else if word_confidence >= 0.60 then ""
  else if word_confidence >= 0.40 then "[" + word + "?]"
  else "[RASURA]"

// Pre-filter
should_process =
  not (is_line_number(word) or is_printed_text(word) or is_url(word))
```

---

## DM-3: Profile Authorization Gate

### Decision Table (DMN Hit Policy: F - Sequential gates)

| # | profile_exists | role_valid | project_access | course_access | result |
|---|---------------|------------|----------------|---------------|--------|
| 1 | false | - | - | - | DENY: "Perfil não localizado" |
| 2 | true | false | - | - | DENY: "Perfil com role inválido" |
| 3 | true | true | false | - | DENY: "Sem permissão para Redactia" |
| 4 | true | true | true | false | DENY: "Curso não autorizado" |
| 5 | true | true | true | true | ALLOW |

### FEEL Expressions

```feel
// Role validation
role_valid = role in ["student", "admin", "manager", "teacher"]

// Project access (permissive: empty = allow all)
project_access =
  if allowed_projects = null or count(allowed_projects) = 0 then true
  else list contains(allowed_projects, "redactia")

// Course access (permissive: no config = allow all)
course_access =
  if count(REDACTIA_ALLOWED_COURSES) = 0 then true
  else if course_slug = null or course_slug = "" then true
  else lower case(course_slug) in REDACTIA_ALLOWED_COURSES

// Final gate
auth_result =
  if not profile_exists then "DENY:profile_not_found"
  else if not role_valid then "DENY:invalid_role"
  else if not project_access then "DENY:no_project_access"
  else if not course_access then "DENY:course_not_authorized"
  else "ALLOW"
```

---

## DM-4: Essay Access Control

### Decision Table (DMN Hit Policy: A - Any true = ALLOW)

| # | Condition | result |
|---|-----------|--------|
| 1 | essay.owner_id = user_id | ALLOW |
| 2 | essay.submitted_by = user_id | ALLOW |
| 3 | user is member of essay.organization_id | ALLOW |
| 4 | (none of above) | DENY (403) |

### FEEL Expression

```feel
essay_access =
  if essay.owner_id = user_id then "ALLOW"
  else if essay.submitted_by = user_id then "ALLOW"
  else if org_membership(user_id, essay.organization_id) != null then "ALLOW"
  else "DENY"
```

### RLS Policy Equivalence Matrix

| Context | Supabase RLS | Flask Logic | Match? |
|---------|-------------|-------------|--------|
| B2C owner | owner_id = auth.uid() | essay.owner_id = user_id | YES |
| B2B org | org_users JOIN + role check | org_membership() | YES |
| Service | auth.role() = 'service_role' | N/A (direct DB) | YES |
| Admin | via org_users role='admin' | auth.profile.role == 'admin' (bypass) | DIVERGE: Flask adds admin bypass |

**Nota:** Flask tem bypass explícito para admin que o RLS não tem. O RLS depende de admin estar como org_user.

---

## DM-5: LLM Score Validation & Clamping

### Decision Table: Score Processing (DMN Hit Policy: U)

| # | Input | parse_ok | Clamping | Output |
|---|-------|----------|----------|--------|
| 1 | competency_score (any) | float(value) succeeds | max(0, min(200, value)) | score: [0, 200] |
| 2 | competency_score (any) | float(value) fails | 0 (default) | score: 0 |
| 3 | overall_score | sum(C1..C5) | max(0, min(1000, sum)) | score: [0, 1000] |

### Sub-Decision: Placeholder Detection -> Retry (DMN Hit Policy: A)

| # | field_value | is_placeholder | action |
|---|------------|---------------|--------|
| 1 | "" (empty) | true | retry_with_reinforced_prompt |
| 2 | contains "<<<" | true | retry_with_reinforced_prompt |
| 3 | contains "não fornecido" | true | retry_with_reinforced_prompt |
| 4 | (retry also placeholder) | true | use_fallback_text |
| 5 | (valid content) | false | accept |

### FEEL Expressions

```feel
// Competency score clamping
clamped_score = max(0, min(200, number(raw_score)))

// Overall score
overall_score = max(0, min(1000, sum(clamped_scores)))

// Placeholder detection
is_placeholder =
  raw_value = "" or
  contains(raw_value, "<<<") or
  contains(raw_value, "não fornecido")

// Fallback texts
fallback_summary = "Resumo indisponível. Reenvie o arquivo..."
fallback_overall_comment = "Comentário geral indisponível..."
fallback_strengths = ["Não foi possível extrair pontos fortes..."]
fallback_improvements = ["Reenvie o arquivo certificando-se..."]
```

### Cross-Layer Conflict: Score Step

| Layer | Constraint | FEEL |
|-------|-----------|------|
| Frontend | step = 40 | score in [0, 40, 80, 120, 160, 200] |
| Backend | continuous | score in [0..200] |
| Database | CHECK >= 0 AND <= 200 | score in [0..200] |

```feel
// PROPOSTA de enforcement: (não implementado atualmente)
is_valid_enem_step = decimal(score / 20, 0) * 20 = score
// Valores aceitos: 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200
```

---

## DM-6: Competency Analytics

### Decision Table: Performance Level (DMN Hit Policy: F)

| # | score | level | label |
|---|-------|-------|-------|
| 1 | null | "none" | "--" |
| 2 | >= 180 | "excellent" | "Excelente" |
| 3 | >= 140 | "good" | "Bom" |
| 4 | >= 100 | "regular" | "Regular" |
| 5 | >= 60 | "below" | "Abaixo" |
| 6 | < 60 | "critical" | "Critico" |

### FEEL Expression

```feel
performance_level =
  if score = null then "none"
  else if score >= 180 then "excellent"
  else if score >= 140 then "good"
  else if score >= 100 then "regular"
  else if score >= 60 then "below"
  else "critical"
```

### Decision Table: Competency Criticality (DMN Hit Policy: F)

| # | reinforcement_pct | status |
|---|-------------------|--------|
| 1 | > 30 | "critical" |
| 2 | > 15 | "warning" |
| 3 | <= 15 | "normal" |
| 4 | null | "normal" |

### FEEL Expression

```feel
competency_status =
  if reinforcement_pct = null then "normal"
  else if reinforcement_pct > 30 then "critical"
  else if reinforcement_pct > 15 then "warning"
  else "normal"
```

### Decision Table: Student At-Risk (DMN Hit Policy: U)

| # | reinforcement_count | status |
|---|-------------------|--------|
| 1 | >= 3 | "needs_attention" |
| 2 | < 3 | "normal" |

### FEEL Expression

```feel
// Reinforcement flag per competency
needs_reinforcement_cx = cx_avg < threshold  // threshold default = 100

// Reinforcement count
reinforcement_count =
  (if needs_reinforcement_c1 then 1 else 0) +
  (if needs_reinforcement_c2 then 1 else 0) +
  (if needs_reinforcement_c3 then 1 else 0) +
  (if needs_reinforcement_c4 then 1 else 0) +
  (if needs_reinforcement_c5 then 1 else 0)

// At-risk flag
student_at_risk = reinforcement_count >= 3
```

---

## DM-7: Role-Based Routing

### Decision Table: Default Path (DMN Hit Policy: U)

| # | role | default_path |
|---|------|-------------|
| 1 | "admin" | "/redactia/admin" |
| 2 | "manager" | "/redactia/manager" |
| 3 | "student" | "/redactia/student" |
| 4 | "teacher" | "/redactia/teacher" |
| 5 | (other/null) | "/redactia/teacher" |

### Decision Table: Permissions Matrix (DMN Hit Policy: U)

| # | role | view_essays | edit_feedback | view_analytics | view_audit | org_bypass |
|---|------|------------|---------------|---------------|------------|------------|
| 1 | "admin" | "all" | true | true | true | true |
| 2 | "manager" | "org" | true | true | true | false |
| 3 | "teacher" | "org" | true | true | true | false |
| 4 | "student" | "own" | false | false | false | false |

### FEEL Expressions

```feel
default_path =
  if role = "admin" then "/redactia/admin"
  else if role = "manager" then "/redactia/manager"
  else if role = "student" then "/redactia/student"
  else "/redactia/teacher"

can_edit_feedback = role in ["admin", "manager", "teacher"]
can_view_analytics = role in ["admin", "manager", "teacher"]
requires_org_check = role != "admin"
```

---

## Essay Status State Machine (DMN-compatible)

### Decision Table: Status Transitions (DMN Hit Policy: U)

| # | current_status | trigger | next_status |
|---|---------------|---------|-------------|
| 1 | "draft" | "submit" | "submitted" |
| 2 | "submitted" | "ocr_requires_review" | "pending_review" |
| 3 | "submitted" | "ocr_auto" | "processing" |
| 4 | "pending_review" | "teacher_approves" | "processing" |
| 5 | "processing" | "llm_success" | "completed" |
| 6 | "processing" | "llm_error" | "failed" |

### FEEL Expression

```feel
next_status =
  if current = "draft" and trigger = "submit" then "submitted"
  else if current = "submitted" and requires_review then "pending_review"
  else if current = "submitted" and not requires_review then "processing"
  else if current = "pending_review" and trigger = "approve" then "processing"
  else if current = "processing" and llm_success then "completed"
  else if current = "processing" and llm_error then "failed"
  else current  // no transition
```

---

## Configuration Parameters (Knowledge Source)

| Parameter | Default | FEEL Type | Source |
|-----------|---------|-----------|--------|
| OCR_CONF_HIGH | 0.85 | number | env var |
| OCR_CONF_MEDIUM | 0.60 | number | env var |
| OCR_CONF_LOW | 0.40 | number | env var |
| OCR_GLOBAL_CONF_AUTO | 0.80 | number | env var |
| OCR_RATIO_UNCERTAIN_MAX | 0.05 | number | env var |
| OCR_UNKNOWN_WORDS_MAX | 1 | number | env var |
| OCR_MIN_WORDS_FOR_DICT_CHECK | 10 | number | env var |
| OCR_HEADER_REGION_PERCENT | 0.10 | number | env var |
| OCR_FOOTER_REGION_PERCENT | 0.92 | number | env var |
| OCR_PARAGRAPH_GAP_MULTIPLIER | 1.8 | number | env var |
| OCR_LEFT_MARGIN_PERCENT | 0.08 | number | env var |
| OCR_RIGHT_MARGIN_PERCENT | 0.92 | number | env var |
| OCR_V2_ENABLED | true | boolean | env var |
| REDACTIA_ALLOWED_COURSES | {"enem"} | list<string> | env var |
| LLM_TEMPERATURE | 0.0 | number | hardcoded |
| LLM_MAX_COMPLETION_TOKENS | 900 | number | hardcoded |
| THREAD_POOL_MAX_WORKERS | 5 | number | hardcoded |
| SIGNED_URL_EXPIRY_DAYS | 7 | number | hardcoded |
| MIN_TEXT_AFTER_REVIEW | 50 | number | hardcoded |
| PDF_DOWNLOAD_TIMEOUT_SEC | 30 | number | hardcoded |
| QUERY_LIMIT_MAX | 200 | number | hardcoded |
| AUDIT_RETENTION_DAYS | 90 | number | hardcoded |
| REINFORCEMENT_THRESHOLD | 100 | number | param (default) |
| CRITICAL_COMPETENCY_PCT | 30 | number | hardcoded |
| WARNING_COMPETENCY_PCT | 15 | number | hardcoded |
| STUDENT_AT_RISK_COUNT | 3 | number | hardcoded |

---

## Completeness Check

| DM | Decision Tables | Cells vazias | Regras default | Status |
|----|----------------|--------------|----------------|--------|
| DM-1 | 2 (routing + linguistic) | 0 | Sim (row 4 = fallback) | COMPLETO |
| DM-2 | 2 (marking + pre-filter) | 0 | Sim (row 4 = process) | COMPLETO |
| DM-3 | 1 (4 gates) | 0 | Sim (row 5 = ALLOW) | COMPLETO |
| DM-4 | 1 (OR logic) | 0 | Sim (row 4 = DENY) | COMPLETO |
| DM-5 | 2 (scoring + placeholder) | 0 | Sim (row 2 = default 0) | COMPLETO |
| DM-6 | 3 (perf + crit + risk) | 0 | Sim (null handlers) | COMPLETO |
| DM-7 | 2 (path + permissions) | 0 | Sim (row 5 = teacher) | COMPLETO |

**Gate de Formalização: COMPLETO**
