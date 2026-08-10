# Task: Map UI Pages

## Metadata

```yaml
task: map-ui-pages
atomic_layer: Atom
responsavel_type: Agent
agent: auditor (primary) | playwright-ops (Playwright execution)
command: "*map-ui [--list | --index | --steps <name>]"
script: "services/clickup/playwright/map-ui-page.js"
output_dir: "services/clickup/playwright/ui-snapshots/"
```

## Description

Captura snapshots de acessibilidade (accessibility tree) e screenshots de páginas
ClickUp para manutenção de seletores DOM. Usado quando seletores falham na validação
(`validate-selectors.js`) ou quando novas páginas precisam ser mapeadas.

O script gera os passos MCP exatos que o agente deve executar via Playwright —
ele não chama o Playwright diretamente.

---

## Quando Executar

| Trigger | Obrigatoriedade |
|---------|----------------|
| Seletor com status FAIL após `validate-selectors.js` | OBRIGATÓRIO |
| Nova área do ClickUp a ser automatizada | OBRIGATÓRIO (antes de criar seletores) |
| ClickUp lança nova feature/página | RECOMENDADO |
| Manutenção trimestral de seletores base | RECOMENDADO |

---

## Comandos CLI

### 1. Listar páginas disponíveis

```bash
node services/clickup/playwright/map-ui-page.js --list
```

Output: lista todas as páginas configuradas no script com nome, URL e descrição.
Use para identificar o nome correto antes de mapear.

### 2. Gerar índice de todas as páginas com URLs

```bash
node services/clickup/playwright/map-ui-page.js --index
```

Output: JSON com nome, URL completa e descrição de cada página.
Útil para referência cruzada com seletores.

### 3. Gerar passos MCP para uma página específica

```bash
node services/clickup/playwright/map-ui-page.js --steps <name>
```

Output: array de 4 MCP tool calls para executar via Playwright.

Exemplos:
```bash
node services/clickup/playwright/map-ui-page.js --steps automations
node services/clickup/playwright/map-ui-page.js --steps settings-task-types
node services/clickup/playwright/map-ui-page.js --steps ai-brain
```

---

## Workflow Completo de Mapeamento

### Step 1 — Identificar a página a mapear

```bash
node services/clickup/playwright/map-ui-page.js --list
```

Identificar o `name` da página relevante.

### Step 2 — Gerar passos MCP

```bash
node services/clickup/playwright/map-ui-page.js --steps <name>
```

O script retorna 4 passos:
```json
[
  {
    "step": 1,
    "tool": "mcp__playwright__browser_navigate",
    "params": { "url": "https://app.clickup.com/{WORKSPACE_ID}/..." }
  },
  {
    "step": 2,
    "tool": "mcp__playwright__browser_wait_for",
    "params": { "time": 3000 }
  },
  {
    "step": 3,
    "tool": "mcp__playwright__browser_snapshot",
    "params": {},
    "postAction": "Save output to: services/clickup/playwright/ui-snapshots/<name>-snapshot.md"
  },
  {
    "step": 4,
    "tool": "mcp__playwright__browser_take_screenshot",
    "params": {}
  }
]
```

**Nota:** O `{WORKSPACE_ID}` é resolvido em runtime a partir de `clickup-tokenization.yaml` do spoke ativo.

### Step 3 — Executar via MCP Playwright

Executar cada passo em sequência usando o MCP Playwright global.

O MCP Playwright está disponível diretamente (sem docker-gateway):
- `mcp__playwright__browser_navigate`
- `mcp__playwright__browser_wait_for`
- `mcp__playwright__browser_snapshot`
- `mcp__playwright__browser_take_screenshot`

### Step 4 — Salvar outputs

Após Step 3, salvar:
- Snapshot (accessibility tree) → `services/clickup/playwright/ui-snapshots/<name>-snapshot.md`
- Screenshot → `services/clickup/playwright/ui-snapshots/<name>.png`

O diretório `ui-snapshots/` é criado automaticamente se não existir.

### Step 5 — Extrair seletores do snapshot

Do snapshot de acessibilidade:
1. Identificar o elemento DOM relevante (role, aria-label, data-test, etc.)
2. Formular o seletor CSS ou XPath
3. Adicionar ao arquivo `selectors/{domain}.json`

Formato de um seletor no JSON:
```json
{
  "metadata": {
    "skill": "cu-automations",
    "description": "Automation management page",
    "last_validated": "2026-03-30"
  },
  "selectors": {
    "toolbar": {
      "add_button": {
        "primary": "[data-test='add-automation']",
        "fallback": ["[aria-label='Add Automation']", ".automation-add-btn"]
      }
    }
  }
}
```

### Step 6 — Validar novo seletor

Após adicionar ao JSON, executar:
```bash
node services/clickup/playwright/validate-selectors.js --workflow <domain>
```

Confirmar status PASS antes de usar o seletor em scripts.

---

## Mapear Páginas Não Listadas

Para páginas com IDs específicos não incluídas na lista padrão, usar os overrides de CLI:

```bash
node services/clickup/playwright/map-ui-page.js --steps list-missions \
  --list-id {LIST_ID}

# Com Space diferente
node services/clickup/playwright/map-ui-page.js --steps space-delivery \
  --space1 {SPACE_ID}
```

Flags disponíveis: `--space1`, `--space2`, `--folder`, `--list-id`

---

## Pre-Conditions

- [ ] MCP Playwright disponível e autenticado no ClickUp
- [ ] Diretório `services/clickup/playwright/ui-snapshots/` existe (criado automaticamente)

## Post-Conditions

- [ ] Snapshot `.md` salvo em `ui-snapshots/`
- [ ] Screenshot `.png` salvo em `ui-snapshots/`
- [ ] Se novo seletor: adicionado a `selectors/{domain}.json`
- [ ] Se correção: seletor validado com `validate-selectors.js --workflow <domain>`

---

## Referências

- Script: `services/clickup/playwright/map-ui-page.js`
- Seletores: `services/clickup/playwright/selectors/`
- Validação: `tasks/validate-selectors.md`
- Loader: `services/clickup/playwright/load-selectors.js`

---

*Task: Map UI Pages v1.0*
*Epic 75 | clickup-ops-squad | 2026-03-30*
