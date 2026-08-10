# Task: Use Capability Matrix

## Metadata

```yaml
task: use-capability-matrix
atomic_layer: Atom
responsavel_type: Agent
agent: clickup-chief (routing decision) + any executor
trigger: "Antes de qualquer operação ClickUp — OBRIGATÓRIO"
ref_file: "squads/clickup-ops-squad/data/capability-matrix.yaml"
```

## Description

Antes de executar qualquer operação ClickUp, o agente DEVE consultar a `capability-matrix.yaml`
para determinar qual ferramenta usar: API REST, Playwright via MCP, ou fluxo híbrido (ambos).

A matrix cobre 109 operações organizadas por domínio. Ignorar essa consulta resulta em uso
incorreto de ferramentas — especialmente tentar operações via API que só funcionam via UI.

## Quando Executar

- **SEMPRE** antes de qualquer operação ClickUp de escrita ou estruturação
- Ao planejar um fluxo de materialização com múltiplas operações
- Ao implementar novos scripts Playwright (`load-selectors.js`)
- Ao auditar estruturas (o auditor usa a matrix para saber o que consultar via API vs UI)

---

## Como Ler a Matrix

### Estrutura do Arquivo

```yaml
_meta:
  priority: "api > api+playwright > playwright"  # preferência de ferramenta

operations:
  {dominio}.{operacao}:
    tool: api | playwright | api+playwright
    module: {arquivo em services/clickup/}          # apenas se tool=api
    fn: {nome da função}
    via_index: true | false                          # se exportado por index.js
    skill: {nome do skill}                          # apenas se tool=playwright
    reason: "Por que usa Playwright"                # apenas se tool=playwright
    mandatory: true                                  # se obrigatório por governance
    note: "Observação importante"

hybrid_flows:
  {nome_do_fluxo}:
    steps:
      - tool: api | playwright
        operation: {operacao}
        description: "O que faz"
```

### Campos de Decisão

| Campo | Significado |
|-------|-------------|
| `tool: api` | Usar `services/clickup/{module}.js` |
| `tool: playwright` | Usar MCP Playwright com o skill referenciado |
| `tool: api+playwright` | Fluxo híbrido — ver `hybrid_flows` |
| `via_index: true` | Acessível via `require('services/clickup')` |
| `via_index: false` | Importar o módulo diretamente |
| `mandatory: true` | Obrigatório por governance — não pode ser substituído |

---

## Lógica de Decisão

```
1. Identificar a operação: {dominio}.{acao}
   Exemplos: task.create, field.create, automation.create

2. Lookup na matrix:
   operations["{dominio}.{acao}"].tool

3. Switch por tool:

   tool == "api":
     → Importar services/clickup/{module}.js
     → Chamar fn diretamente
     → Se via_index == true: pode usar require('services/clickup')[fn]

   tool == "playwright":
     → Ativar MCP Playwright
     → Referenciar skill indicado no campo skill
     → Seguir workflow do skill

   tool == "api+playwright":
     → Consultar hybrid_flows para os steps em ordem
     → Executar step API primeiro, depois Playwright

4. Verificar mandatory/governance:
   → Se mandatory: true → NUNCA substituir por outro método
   → Se governance_refs referenciado → ler regra antes de executar
```

---

## Exemplos de Consulta

### Criar uma task

```yaml
operation: task.create
lookup:
  tool: api
  module: tasks.js
  fn: createTask
  via_index: true
decisão: → usar require('services/clickup').createTask(...)
```

### Criar um custom field

```yaml
operation: field.create
lookup:
  tool: playwright
  skill: cu-custom-fields
  reason: "API REST nao cria custom fields, apenas le/seta valores"
decisão: → ativar Playwright MCP, usar skill cu-custom-fields
```

### Criar automação

```yaml
operation: automation.create
lookup:
  tool: playwright
  skill: cu-automations
  reason: "API REST nao cria automacoes"
decisão: → ativar Playwright MCP, usar skill cu-automations
```

### Atualizar description de task (OBRIGATÓRIO)

```yaml
operation: task.update_description_safe
lookup:
  tool: api
  module: tasks.js
  fn: updateTaskDescriptionSafe
  mandatory: true
  note: "OBRIGATÓRIO para qualquer update de description — preserva Journey Log"
decisão: → SEMPRE usar updateTaskDescriptionSafe. NUNCA usar PUT direto.
```

### Materializar Mission (fluxo híbrido)

```yaml
operation: mission.bootstrap
lookup:
  tool: api+playwright
  module: bootstrap.js
  fn: run
decisão: → consultar hybrid_flows.mission_bootstrap
         → Step 1: API (createList + createCustomField)
         → Step 2: Playwright (Task Types creation — não suportado por API REST)
```

---

## Domínios Disponíveis na Matrix

| Domínio | Ops | Tool padrão |
|---------|-----|-------------|
| `task.*` | 12 ops | api (exceto move_cross_space, bulk_operations) |
| `status.*` | 4 ops | api (exceto workflow_create) |
| `field.*` | 6 ops | api para read/set, playwright para create |
| `comment.*` | 3 ops | api (exceto threads) |
| `attachment.*` | 6 ops | api (exceto upload) |
| `doc.*` | 7 ops | api (exceto edit_rich) |
| `workspace.*` | 4 ops | api |
| `sprint.*` | 6 ops | api |
| `sync.*` | 3 ops | api |
| `data.*` | 4 ops | api |
| `automation.*` | 3 ops | playwright |
| `form.*` | 2 ops | playwright |
| `dashboard.*` | 3 ops | playwright |
| `view.*` | 9 ops | playwright |
| `template.*` | 2 ops | playwright |
| `goal.*` | 2 ops | playwright |
| `space.*` | 2 ops | playwright |
| `folder.*` | 1 op | playwright |
| `list.*` | 1 op | playwright |
| `mission.*` | 4 ops | api ou api+playwright |
| `settings.*` | 6 ops | playwright |
| `superagent.*` | 1 op | playwright |
| `audit.*` | 1 op | api |

---

## Novos Scripts Playwright — Usar load-selectors.js

Para **novos scripts Playwright** criados em `services/clickup/playwright/`,
SEMPRE usar `load-selectors.js` para carregar seletores DOM:

```javascript
const { loadSelectors, getSelector } = require('./load-selectors');

// Carregar todos os seletores de um domínio
const selectors = loadSelectors('cu-automations');  // carrega selectors/cu-automations.json

// Acessar seletor específico via path
const btnSelector = getSelector('cu-automations', 'toolbar.add_button');
```

**Domínios de seletores disponíveis:**
```bash
node services/clickup/playwright/validate-selectors.js --summary
```

Os scripts legados (`create-automation.js`, `create-dashboard.js`, `create-form.js`)
funcionam independentemente e NÃO precisam ser migrados para `load-selectors.js`.
A integração de seletores acontece apenas em novos scripts.

---

## Governance Refs

Antes de executar operações de escrita, verificar:

| Operação | Regra obrigatória |
|----------|-------------------|
| Qualquer escrita em description | usar helpers Zone-safe (updateTaskDescriptionSafe / appendJournalEntry) |
| Criar Space/Folder/List | checklist H1-H11 — ver `squads/clickup-ops-squad/rules/clickup.md` |
| Pre-materialização | `squads/clickup-ops-squad/checklists/pre-materialization.md` |

---

## Post-Conditions

- [ ] tool correto identificado (api / playwright / hybrid)
- [ ] módulo ou skill referenciado está disponível
- [ ] governance obrigatória verificada (description, organization)
- [ ] mandatory fields respeitados sem substituição

---

*Task: Use Capability Matrix v1.0*
*Epic 75 | clickup-ops-squad | 2026-03-30*
