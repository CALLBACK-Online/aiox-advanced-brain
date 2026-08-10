# Decision Models: Question Engine (von Halle)

**Data:** 2026-03-23
**Input:** 27 regras extraídas

---

## 4 Decision Models

| # | Decision Model | Complexidade |
|---|---------------|-------------|
| DM-Q1 | Stock Management & Replenishment | ALTA |
| DM-Q2 | Batch Job Lifecycle | MEDIA |
| DM-Q3 | Generation Worker Job Processing | MEDIA |
| DM-Q4 | Audit Verdict (Creator vs Auditor) | MEDIA |

---

## DM-Q1: Stock Management

### Decision Table: Stock Mode (Hit Policy: U)

| # | MGQ_RELATIVE_STOCK_MONITOR | Mode | Query |
|---|---------------------------|------|-------|
| 1 | "on" | Relative | view_ai_stock_deficits (per student/topic) |
| 2 | "off" | Legacy | COUNT questions WHERE created_by_ai per topic |

### Decision Table: Stock Replenishment (Hit Policy: F)

| # | effective_count | Action |
|---|----------------|--------|
| 1 | >= 50 (threshold) | No action |
| 2 | < 50 | Trigger generation job |

---

## DM-Q2: Batch Job Lifecycle

### Decision Table: Vertex AI State -> Action (Hit Policy: U)

| # | Vertex State | Batch Status | Action |
|---|-------------|-------------|--------|
| 1 | PENDING/QUEUED/RUNNING | processing | Continue polling |
| 2 | SUCCEEDED | - | Ingest outputs |
| 3 | CANCELLED/FAILED/CANCELLING/PAUSED/EXPIRED | failed | Mark failed, stop |

### Decision Table: Batch Status Transitions (Hit Policy: U)

| From | To | Trigger |
|------|----|---------|
| draft | pending_upload | Upload started |
| pending_upload | submitted | Vertex job created |
| submitted | processing | Vertex job running |
| processing | succeeded | All outputs ingested |
| processing | failed | Vertex error or ingest error |

---

## DM-Q3: Generation Worker

### Decision Table: Job Claiming (Hit Policy: U)

| # | Condition | Action |
|---|-----------|--------|
| 1 | queued job exists | FOR UPDATE SKIP LOCKED, status->processing |
| 2 | no queued job | Sleep GENERATION_WORKER_SLEEP_SECONDS (5s) |

### Decision Table: LLM Parameters (Hit Policy: U)

| Role | Model | Temperature | Max Tokens |
|------|-------|-------------|------------|
| Creator | Gemini 2.5 Flash | 0.7 (configurable) | 32000 |
| Auditor | Gemini 2.5 Pro | 0.0 (fixed) | 65000 |

### Decision Table: Retry Logic (Hit Policy: U)

| Context | Max Retries | Backoff |
|---------|------------|---------|
| LLM calls | 6 | Exponential, max 8s |
| DB calls | 6 | Exponential, max 3s |
| Worker (Tenacity) | 3 | Exponential 2-10s |

---

## DM-Q4: Audit Verdict

### Decision Table: Question Acceptance (Hit Policy: U)

| # | Audit Status | Action | Job Status |
|---|-------------|--------|------------|
| 1 | "APROVADO" | Insert question, append to generated_ids | completed |
| 2 | Any other | Raise AuditRejected | audit_rejected |

### Decision Table: Question Validation (Hit Policy: A - ALL must pass)

| # | Field | Validation |
|---|-------|-----------|
| 1 | question_style | IN {ME5, ME4, CE} |
| 2 | statement | >= 12 chars |
| 3 | correct_option | IN {A, B, C, D, E} |
| 4 | alternatives | Count matches style (4 for ME4, 5 for ME5) |
| 5 | difficulty_level | IN [1, 5] |
| 6 | detail_main + detail_funny | Non-empty |
