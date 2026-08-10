# Checklist Validation Task

| Field | Value |
|-------|-------|
| **responsavel_type** | `Agent` |
| **atomic_layer** | `Atom` |
| **domain** | `Operational` |
| **pattern** | EXEC-A-001 |
| **rationale** | Validação de checklist requer interpretação de cada item |

## Inputs

- `checklist_name` (string, optional): Name or fuzzy match of the checklist to run (e.g. `architect-checklist`); if omitted, agent lists available checklists
- `mode` (enum): Execution mode — `interactive` (section by section) or `yolo` (all at once); defaults to `yolo`
- `artifacts` (list, optional): Paths to documents or artifacts required by the checklist; agent will prompt if missing

This task provides instructions for validating documentation against checklists. The agent MUST follow these instructions to ensure thorough and systematic validation of documents.

## Outputs

- **resolved checklist**: name of the loaded checklist from `squads/db-sage/checklists/` (or fuzzy-match result)
- **per-item verdicts**: `✅ PASS` / `❌ FAIL` / `⚠️ PARTIAL` / `N/A` classification for every checklist item
- **section pass rates**: per-section pass percentage and themes for failed items
- **final report**: overall completion status, list of failed items with context, and improvement recommendations
- **user decisions log**: rationale captured for `N/A` items or skipped sections (interactive mode)


## Pre-conditions

- Database connection established (validated by db-env-check)

## Available Checklists

If the user asks or does not specify a specific checklist, list the checklists available to the agent persona. If the task is being run not with a specific agent, tell the user to check the squads/db-sage/checklists/ folder to select the appropriate one to run.

## Instructions

1. **Initial Assessment**

   - If user or the task being run provides a checklist name:
     - Try fuzzy matching (e.g. "architecture checklist" -> "architect-checklist")
     - If multiple matches found, ask user to clarify
     - Load the appropriate checklist from squads/db-sage/checklists/
   - If no checklist specified:
     - Ask the user which checklist they want to use
     - Present the available options from the files in the checklists folder
   - Confirm if they want to work through the checklist:
     - Section by section (interactive mode - very time consuming)
     - All at once (YOLO mode - recommended for checklists, there will be a summary of sections at the end to discuss)

2. **Document and Artifact Gathering**

   - Each checklist will specify its required documents/artifacts at the beginning
   - Follow the checklist's specific instructions for what to gather, generally a file can be resolved in the docs folder, if not or unsure, halt and ask or confirm with the user.

3. **Checklist Processing**

   If in interactive mode:

   - Work through each section of the checklist one at a time
   - For each section:
     - Review all items in the section following instructions for that section embedded in the checklist
     - Check each item against the relevant documentation or artifacts as appropriate
     - Present summary of findings for that section, highlighting warnings, errors and non applicable items (rationale for non-applicability).
     - Get user confirmation before proceeding to next section or if any thing major do we need to halt and take corrective action

   If in YOLO mode:

   - Process all sections at once
   - Create a comprehensive report of all findings
   - Present the complete analysis to the user

4. **Validation Approach**

   For each checklist item:

   - Read and understand the requirement
   - Look for evidence in the documentation that satisfies the requirement
   - Consider both explicit mentions and implicit coverage
   - Aside from this, follow all checklist llm instructions
   - Mark items as:
     - ✅ PASS: Requirement clearly met
     - ❌ FAIL: Requirement not met or insufficient coverage
     - ⚠️ PARTIAL: Some aspects covered but needs improvement
     - N/A: Not applicable to this case

5. **Section Analysis**

   For each section:

   - think step by step to calculate pass rate
   - Identify common themes in failed items
   - Provide specific recommendations for improvement
   - In interactive mode, discuss findings with user
   - Document any user decisions or explanations

6. **Final Report**

   Prepare a summary that includes:

   - Overall checklist completion status
   - Pass rates by section
   - List of failed items with context
   - Specific recommendations for improvement
   - Any sections or items marked as N/A with justification

## Checklist Execution Methodology

Each checklist now contains embedded LLM prompts and instructions that will:

1. **Guide thorough thinking** - Prompts ensure deep analysis of each section
2. **Request specific artifacts** - Clear instructions on what documents/access is needed
3. **Provide contextual guidance** - Section-specific prompts for better validation
4. **Generate comprehensive reports** - Final summary with detailed findings

The LLM will:

- Execute the complete checklist validation
- Present a final report with pass/fail rates and key findings
- Offer to provide detailed analysis of any section, especially those with warnings or failures

## Error Handling

| Condition | Action |
|-----------|--------|
| Checklist name provided but no match found in `squads/db-sage/checklists/` | List available checklists and ask user to clarify |
| Multiple fuzzy matches for checklist name | Present all candidates and ask user to select one |
| Required artifact/document not found at expected path | Halt and ask user to provide the correct path or confirm the artifact is unavailable (mark dependent items as N/A) |
| Checklist file is malformed YAML | Report parse error and halt until file is corrected |
| Section item references an external resource that is inaccessible | Mark item as N/A with rationale noting the inaccessible resource |

## Post-conditions

After successful execution:
- Every checklist item categorized as PASS / FAIL / PARTIAL / N/A with rationale
- Section pass rates calculated and surfaced in the final report
- Recommendations for failed/partial items captured for downstream remediation

Acceptance Criteria:
- [ ] Final report covers 100% of checklist items (no silent omissions)
- [ ] Each FAIL/PARTIAL item has a specific recommendation tied to the artifact under review
- [ ] Items marked N/A include explicit rationale for non-applicability
