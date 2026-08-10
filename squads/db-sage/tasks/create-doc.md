# Create Document from Template (YAML Driven)

| Field | Value |
|-------|-------|
| **responsavel_type** | `Agent` |
| **atomic_layer** | `Atom` |
| **domain** | `Operational` |
| **pattern** | EXEC-A-001 |
| **rationale** | Criação de documento requer elicitação interativa e interpretação |

## Inputs

- `template_path` (string): Path to the YAML template file in `squads/db-sage/templates/`, or user-provided path
- `output_path` (string, optional): Destination file path for the generated document; defaults to agent-suggested location

## Outputs

- **generated document**: file materialized at `output_path` with all template sections populated or marked `[RESTRICTED — requires {owner} agent]`
- **elicitation log**: every `elicit: true` section records the user-selected option (1-9) or a YOLO override marker inline in the output
- **section ownership notes**: owner/editor metadata preserved as inline notes within the generated document
- **status flag**: success if all required sections rendered without permission failures; failure if output path was not writable or template could not be parsed


## Pre-conditions

- Database connection established (validated by db-env-check)

## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

When this task is invoked:

1. **DISABLE ALL EFFICIENCY OPTIMIZATIONS** - This workflow requires full user interaction
2. **MANDATORY STEP-BY-STEP EXECUTION** - Each section must be processed sequentially with user feedback
3. **ELICITATION IS REQUIRED** - When `elicit: true`, you MUST use the 1-9 format and wait for user response
4. **NO SHORTCUTS ALLOWED** - Complete documents cannot be created without following this workflow

**VIOLATION INDICATOR:** If you create a complete document without user interaction, you have violated this workflow.

## Critical: Template Discovery

If a YAML Template has not been provided, list all templates from squads/db-sage/templates/ or ask the user to provide another.

## CRITICAL: Mandatory Elicitation Format

**When `elicit: true`, this is a HARD STOP requiring user interaction:**

**YOU MUST:**

1. Present section content
2. Provide detailed rationale (explain trade-offs, assumptions, decisions made)
3. **STOP and present numbered options 1-9:**
   - **Option 1:** Always "Proceed to next section"
   - **Options 2-9:** Select 8 methods from `.aiox-core/product/data/elicitation-methods.md`
   - End with: "Select 1-9 or just type your question/feedback:"
4. **WAIT FOR USER RESPONSE** - Do not proceed until user selects option or provides feedback

**WORKFLOW VIOLATION:** Creating content for elicit=true sections without user interaction violates this task.

## Error Handling

| Condition | Action |
|-----------|--------|
| Template file not found at given path | List all templates in `squads/db-sage/templates/` and ask user to select one |
| Template YAML is malformed or unparseable | Report parse error with line number and halt until user provides a valid template |
| Section has `elicit: true` but no elicitation methods available in `.aiox-core/product/data/elicitation-methods.md` | Warn user, fall back to open-ended question for that section |
| Agent permission check fails (current agent not in `editors` list) | Display a warning noting the restricted section, skip population, and mark it as `[RESTRICTED — requires {owner} agent]` |
| Output file path is not writable | Prompt user for an alternative output path before proceeding |

**NEVER ask yes/no questions or use any other format.**

## Post-conditions

After successful execution:
- Document materialized at `output_path` with all template sections populated or marked `[RESTRICTED — requires {owner} agent]`
- All `elicit: true` sections received explicit user input via 1-9 format (or YOLO override recorded in document)
- Section ownership (owner/editors) preserved in generated document as inline notes

Acceptance Criteria:
- [ ] Output file exists at the agreed `output_path` and parses as valid Markdown/YAML for its template type
- [ ] Every `elicit: true` section either captured user choice or carries an explicit YOLO marker
- [ ] Sections restricted by editor permissions are flagged in the output (no silent population)

## Processing Flow

1. **Parse YAML template** - Load template metadata and sections
2. **Set preferences** - Show current mode (Interactive), confirm output file
3. **Process each section:**
   - Skip if condition unmet
   - Check agent permissions (owner/editors) - note if section is restricted to specific agents
   - Draft content using section instruction
   - Present content + detailed rationale
   - **IF elicit: true** → MANDATORY 1-9 options format
   - Save to file if possible
4. **Continue until complete**

## Detailed Rationale Requirements

When presenting section content, ALWAYS include rationale that explains:

- Trade-offs and choices made (what was chosen over alternatives and why)
- Key assumptions made during drafting
- Interesting or questionable decisions that need user attention
- Areas that might need validation

## Elicitation Results Flow

After user selects elicitation method (2-9):

1. Execute method from `.aiox-core/product/data/elicitation-methods.md`
2. Present results with insights
3. Offer options:
   - **1. Apply changes and update section**
   - **2. Return to elicitation menu**
   - **3. Ask any questions or engage further with this elicitation**

## Agent Permissions

When processing sections with agent permission fields:

- **owner**: Note which agent role initially creates/populates the section
- **editors**: List agent roles allowed to modify the section
- **readonly**: Mark sections that cannot be modified after creation

**For sections with restricted access:**

- Include a note in the generated document indicating the responsible agent
- Example: "_(This section is owned by dev-agent and can only be modified by dev-agent)_"

## YOLO Mode

User can type `#yolo` to toggle to YOLO mode (process all sections at once).

## CRITICAL REMINDERS

**❌ NEVER:**

- Ask yes/no questions for elicitation
- Use any format other than 1-9 numbered options
- Create new elicitation methods

**✅ ALWAYS:**

- Use exact 1-9 format when elicit: true
- Select options 2-9 from `.aiox-core/product/data/elicitation-methods.md` only
- Provide detailed rationale explaining decisions
- End with "Select 1-9 or just type your question/feedback:"
