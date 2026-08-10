# Task: Extract Expert Gold (Knowledge Enrichment Pipeline)

**Task ID:** extract-expert-gold
**Execution Type:** Hybrid (automated extraction + human validation)
**Purpose:** Extract actionable frameworks, insights, and mental models from expert content (transcriptions, podcasts, talks) and enrich squad reference files
**Orchestrator:** @squad-chief
**Model:** `Sonnet` (multi-lense analysis requires contextual reasoning)
**Haiku Eligible:** NO -- expert framework extraction requires deep domain comprehension

**Philosophy:**
```
"Raw content is noise. Extracted frameworks are signal.
 The pipeline turns 3 hours of audio into operational knowledge
 that agents can use to produce better outputs."
```

---

## Overview

This task transforms raw expert content (transcriptions, podcasts, lectures, interviews) into structured reference data that squad agents can consume. It follows a 5-phase pipeline:

```
INPUT (transcription)
    |
[PHASE 0: CONTEXT LOAD]
    -> Load existing references for this expert
    -> Identify what we ALREADY know
    |
[PHASE 1: MULTI-LENSE EXTRACTION]
    -> Run N analyst agents in parallel
    -> Each extracts through their framework lens
    |
[PHASE 2: GOLD FILTER]
    -> Diff against existing references
    -> Classify: NEW vs KNOWN vs CONTRADICTS
    -> Rank by impact: GAME-CHANGER / TACTICAL / CONTEXTUAL
    |
[PHASE 3: ENRICHMENT]
    -> Merge NEW insights into existing reference files
    -> Create new reference files if needed
    -> Preserve confidence markers ([DOC]/[REP]/[INF])
    |
[PHASE 4: VALIDATION]
    -> Verify no data was lost from existing references
    -> Confirm squad-agnosticism (zero business-specific data)
    -> Generate extraction summary with stats
    |
OUTPUT: Enriched reference files + extraction report
```

---

## Inputs

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_file` | path | Yes | Path to transcription file (`.md` or `.txt`, preferably diarized) |
| `expert_slug` | string | Yes | Expert identifier (e.g., `thiagoroas`, `russellbrunson`) |
| `expert_name` | string | Yes | Human-readable name (e.g., "Thiago Roas") |
| `target_squads` | list | Yes | Squads to enrich (e.g., `[copy, traffic-masters]`) |
| `analyst_agents` | list | No | Override default analyst selection per squad |
| `source_context` | string | No | Description of source (e.g., "Podcast Segredos da Escala #122, 3h01m") |

---

## PHASE 0: Context Load

**Purpose:** Understand what we already know about this expert before extracting.

### Step 0.1: Scan Existing References

```yaml
search_paths:
  - squads/{squad}/data/references/{expert_slug}-*.yaml
  - squads/{squad}/data/references/{expert_slug}-*.md
  - squads/{squad}/data/sops/*{expert_slug}*
  - docs/research/{expert_slug}-*.md

for each file found:
  - Record: path, line_count, last_modified
  - Extract: section headers, key topics covered
  - Count: existing insights/frameworks
```

### Step 0.2: Build Knowledge Baseline

```yaml
output:
  existing_knowledge:
    files: [{path, lines, topics}]
    total_insights: N
    frameworks_documented: []
    gaps_known: []
  new_source:
    file: "{source_file}"
    format: "diarized_md | raw_txt | json"
    estimated_duration: "Xh Ym"
    word_count: N
```

### Step 0.3: Select Analyst Agents

If `analyst_agents` not provided, select based on `target_squads`:

```yaml
default_analysts:
  copy:
    - eugene-schwartz    # Awareness levels, sophistication
    - jon-benson         # VSL structure, format, production
    - dan-kennedy        # Monetization, metrics, direct response
    - todd-brown         # Unique mechanisms, big ideas
  traffic-masters:
    - depesh-mandalia    # Strategic Meta Ads, brand + DR
    - ralph-burns        # Scaling, creative testing
    - kasim-aslam        # Google Ads, Performance Max
    - pedro-sobral       # Brazil market, operational execution
  hormozi:
    - hormozi-offers     # Offer architecture, value equation
    - hormozi-models     # Money models, unit economics
    - hormozi-leads      # Lead generation, core four
  storytelling:
    - joseph-campbell    # Narrative structure, archetypes
    - kindra-hall        # Business storytelling
    - park-howell        # ABT framework, brand narrative
```

**Checkpoint 0:** Confirm analyst selection with user before proceeding.

---

## PHASE 1: Multi-Lense Extraction

**Purpose:** Each analyst reads the FULL transcription through their specific framework lens.

### Step 1.1: Parallel Agent Dispatch

```yaml
for each analyst in selected_analysts:
  dispatch:
    agent: "{analyst}"
    input: "{source_file}"
    instruction: |
      Read the full transcription. Extract ONLY what is relevant to your
      specific framework and expertise. For each insight extracted:

      1. Quote the exact words when possible (with timestamp if available)
      2. Assign confidence marker:
         - [DOC] = Direct explicit statement from expert
         - [REP] = Repeated/corroborated across multiple points
         - [INF] = Inferred from context or partial evidence
      3. Categorize: framework | tactic | metric | case_study | philosophy
      4. Note the timestamp or section reference

    output_format: yaml
    output_path: ".aiox/squad-runtime/etl/{batch_id}/{analyst}-extraction.yaml"
```

### Step 1.2: Collect Results

Wait for all agents to complete. Merge into unified extraction.

```yaml
merged_extraction:
  total_insights: N  # sum across all analysts
  by_analyst:
    - agent: "{name}"
      insights_found: N
      categories: {framework: N, tactic: N, metric: N, case_study: N, philosophy: N}
  by_confidence:
    DOC: N
    REP: N
    INF: N
```

---

## PHASE 2: Gold Filter

**Purpose:** Separate genuinely NEW knowledge from what we already have.

### Step 2.1: Diff Against Baseline

```yaml
for each insight in merged_extraction:
  compare_against: existing_knowledge.files

  classify:
    NEW:
      criteria: "Insight not present in any existing reference file"
      action: "Include in enrichment"
    KNOWN:
      criteria: "Insight already documented (same or equivalent)"
      action: "Skip (optionally note as corroboration)"
    CONTRADICTS:
      criteria: "Insight conflicts with existing documented data"
      action: "Flag for human review, include both versions"
    ENRICHES:
      criteria: "Adds depth/detail to existing insight"
      action: "Include as enrichment to existing section"
```

### Step 2.2: Impact Classification

```yaml
for each NEW or ENRICHES insight:
  classify_impact:
    GAME_CHANGER:
      criteria: |
        - Changes fundamental approach or mental model
        - Backed by data/case study with measurable results
        - Applicable immediately to current workflows
      examples:
        - "Custo de checkout > ROAS como metrica soberana"
        - "Formato muda conversao 2X com mesma copy"

    TACTICAL:
      criteria: |
        - Specific technique or process improvement
        - Clear execution steps
        - Incremental improvement, not paradigm shift
      examples:
        - "Cost cap deve ser proximo ao ticket medio do funil"
        - "Trial 7 dias no upsell com one-click"

    CONTEXTUAL:
      criteria: |
        - Background information, philosophy, or market context
        - Useful for understanding but not directly actionable
        - Supports other insights
      examples:
        - "Digital como falha na Matrix"
        - "Historia do expert no perpetuo"
```

### Step 2.3: Gold Summary

```yaml
output:
  gold_summary:
    total_new: N
    total_known: N
    total_contradicts: N
    total_enriches: N
    by_impact:
      game_changer: N
      tactical: N
      contextual: N
    top_insights:  # max 15, ranked by impact
      - insight: "{description}"
        impact: "GAME_CHANGER"
        confidence: "[DOC]"
        timestamp: "HH:MM:SS"
        analyst: "{who found it}"
```

**Checkpoint 2:** Present gold summary to user. Confirm before enriching reference files.

---

## PHASE 3: Enrichment

**Purpose:** Write new insights into the correct squad reference files.

### Step 3.1: Route to Target Files

```yaml
routing_rules:
  # Each insight goes to the squad reference file that matches its domain
  - if insight.category in [framework, tactic, philosophy] AND squad == "copy":
      target: "squads/copy/data/references/{expert_slug}-copy-analysis.yaml"
  - if insight.category in [metric, tactic] AND squad == "traffic-masters":
      target: "squads/traffic-masters/data/references/{expert_slug}-*.yaml"
  - if insight relates to offer/pricing/funnel architecture:
      target: "squads/hormozi/data/references/{expert_slug}-*.yaml"  # if hormozi in target_squads

  # Create new file if no existing reference matches
  - if no matching file exists:
      create: "squads/{squad}/data/references/{expert_slug}-{topic}-analysis.yaml"
```

### Step 3.2: Merge Strategy

```yaml
merge_rules:
  # NEVER overwrite existing data
  strategy: "append_and_enrich"

  for NEW insights:
    - Add as new section or append to matching section
    - Include source attribution: "Source: {source_context}, {timestamp}"
    - Include confidence marker

  for ENRICHES insights:
    - Add detail under existing section
    - Mark as "Enrichment from: {source_context}"
    - Preserve original data intact

  for CONTRADICTS insights:
    - Add both versions with clear labels
    - Mark: "CONFLICT — requires human resolution"
    - Include timestamps and confidence for both

  formatting:
    - Follow existing file structure (YAML or Markdown)
    - Maintain alphabetical/logical section ordering
    - Keep line count manageable (warn if file > 1000 lines)
```

### Step 3.3: Squad Agnosticism Check

```yaml
before_writing:
  scan_for_violations:
    - Business names (company, product, brand names)
    - Specific pricing (real prices of specific products)
    - Client/customer names
    - Internal project references

  if violation found:
    - Generalize: "R$297 product" -> "low-ticket front (R$197-497 range)"
    - Remove: specific client names -> "case study in {niche}"
    - Flag: anything that cannot be generalized
```

---

## PHASE 4: Validation

**Purpose:** Ensure enrichment was clean and complete.

### Step 4.1: Data Integrity Check

```yaml
checks:
  - id: "EEG-VAL-001"
    check: "No existing data was deleted or overwritten"
    method: "Diff original vs new file, verify all original lines present"

  - id: "EEG-VAL-002"
    check: "All NEW insights were written"
    method: "Count insights routed vs insights in files"

  - id: "EEG-VAL-003"
    check: "Confidence markers present on all new entries"
    method: "Grep for lines without [DOC]/[REP]/[INF] in new sections"

  - id: "EEG-VAL-004"
    check: "Squad agnosticism maintained"
    method: "Scan for business-specific terms"

  - id: "EEG-VAL-005"
    check: "Source attribution on all new entries"
    method: "Grep for 'Source:' in new sections"
```

### Step 4.2: Generate Extraction Report

```yaml
report:
  path: ".aiox/squad-runtime/etl/{batch_id}/extraction-report.md"
  sections:
    - summary: "Expert, source, duration, date"
    - baseline: "What we knew before"
    - extraction: "What each analyst found"
    - gold: "New insights ranked by impact"
    - enrichment: "Files modified with line counts"
    - conflicts: "Any contradictions found"
    - gaps: "What we still don't know"
    - next_steps: "Suggested follow-up (more sources, SOPs to create, etc.)"
```

---

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Enriched reference files | `squads/{squad}/data/references/` | Updated with new insights |
| Per-analyst extractions | `.aiox/squad-runtime/etl/{batch_id}/` | Raw extraction per analyst |
| Extraction report | `.aiox/squad-runtime/etl/{batch_id}/extraction-report.md` | Full summary with stats |
| Gold summary | `.aiox/squad-runtime/etl/{batch_id}/gold-summary.yaml` | Top insights ranked |

---

## Elicitation Points

| # | When | Question | Default |
|---|------|----------|---------|
| 1 | Phase 0.3 | "These are the analysts I'll use. Confirm or override?" | Use defaults per squad |
| 2 | Phase 2.3 | "Here's the gold summary. Proceed with enrichment?" | Yes |
| 3 | Phase 3 (if conflicts) | "Found contradictions. Which version to keep?" | Flag both |

---

## Example Usage

```bash
# Basic: enrich copy squad from Thiago Roas podcast
*extract-expert-gold \
  source_file=".aiox/squad-runtime/etl/etl-20260311-qj04/qj04cUeaRAw-diarized.md" \
  expert_slug="thiagoroas" \
  expert_name="Thiago Roas" \
  target_squads="[copy, traffic-masters]" \
  source_context="Podcast Segredos da Escala #122, 3h01m"

# With custom analysts
*extract-expert-gold \
  source_file=".aiox/squad-runtime/etl/etl-20260315-abc/transcript.md" \
  expert_slug="russellbrunson" \
  expert_name="Russell Brunson" \
  target_squads="[copy, hormozi]" \
  analyst_agents="[russell-brunson, todd-brown, hormozi-offers]"
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Extract without checking existing refs | Produces duplicates, misses what's truly new | ALWAYS run Phase 0 first |
| Single analyst extraction | Misses insights outside one framework | Minimum 3 analysts per squad |
| Skip gold filter (Phase 2) | Floods reference files with noise | Phase 2 is mandatory |
| Write business-specific data to squad | Violates squad agnosticism | Generalize or route to workspace/ |
| Overwrite existing reference sections | Loses previously extracted knowledge | Append-only merge strategy |
| Skip confidence markers | Agents can't assess reliability of data | Every insight needs [DOC]/[REP]/[INF] |

---

## Related Tasks

| Task | Relationship |
|------|-------------|
| `deep-research-pre-agent.md` | Research BEFORE agent creation (complementary) |
| `etl-ops/tasks/process.md` | ETL processing (upstream — produces the transcription) |
| `gerador-pop/tasks/extract-sop.md` | SOP extraction (downstream — uses enriched refs to create SOPs) |
| `squad-creator/tasks/create-agent.md` | Agent creation (downstream — agents consume reference data) |

---

## Quality Gate

```yaml
gate_id: SC_EEG_001
gate_name: "Expert Gold Extraction Quality"
checks:
  - "Phase 0 baseline documented"
  - "Minimum 3 analysts ran"
  - "Gold filter produced summary with impact classification"
  - "All enriched files pass squad-agnosticism scan"
  - "Extraction report generated with all sections"
  - "No existing data deleted from reference files"
passing_threshold: "All checks pass"
```

---

_Task Version: 1.0.0_
_Created: 2026-03-11_
_Philosophy: "Raw content is noise. Extracted frameworks are signal."_
