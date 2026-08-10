# Task: Validate Selectors

## Metadata

```yaml
task: validate-selectors
atomic_layer: Atom
responsavel_type: Agent
agent: auditor
command: "*validate-selectors [--summary | --report | --workflow <domain>]"
script: "services/clickup/playwright/validate-selectors.js"
frequencia: "Mensal (primeira semana) + antes de operações Playwright críticas"
```

## Description

Valida que os seletores DOM armazenados em `services/clickup/playwright/selectors/`
ainda funcionam contra o local_docs ClickUp real. O ClickUp ocasionalmente altera
a estrutura DOM em updates — seletores quebrados causam falha silenciosa em scripts
de automação, formulários e dashboards.

Este script gera workflows de validação para o MCP Playwright executar,
reportando PASS / FALLBACK / FAIL por seletor.

---

## Quando Executar

| Trigger | Obrigatoriedade |
|---------|----------------|
| Primeira semana de cada mês | OBRIGATÓRIO (manutenção periódica) |
| Antes de operações Playwright críticas | RECOMENDADO |
| Após update do ClickUp (notificado no changelog interno) | OBRIGATÓRIO |
| Após adicionar novos arquivos em `selectors/` | RECOMENDADO |
| Quando script Playwright falha inesperadamente | DIAGNÓSTICO |

---

## Comandos CLI

### 1. Resumo rápido (use primeiro)

```bash
node services/clickup/playwright/validate-selectors.js --summary
```

Output: lista todos os domínios de seletores disponíveis com contagem de seletores por domínio.
Use para saber quais domínios existem antes de validar.

### 2. Relatório completo

```bash
node services/clickup/playwright/validate-selectors.js --report
```

Output: gera `services/clickup/playwright/selector-validation-report.json` com resultado
detalhado de cada seletor (PASS / FALLBACK / FAIL + timestamp).

### 3. Workflow para um domínio específico

```bash
node services/clickup/playwright/validate-selectors.js --workflow <domain>
```

Output: gera sequência de MCP Playwright calls (browser_navigate + browser_snapshot)
para o domínio especificado. Usar quando falha em domínio específico.

Exemplo:
```bash
node services/clickup/playwright/validate-selectors.js --workflow cu-automations
node services/clickup/playwright/validate-selectors.js --workflow cu-nav-core
```

---

## Workflow Completo de Validação

### Step 1 — Listar domínios disponíveis

```bash
node services/clickup/playwright/validate-selectors.js --summary
```

Registrar domínios retornados. Cada domínio corresponde a um arquivo `.json`
em `services/clickup/playwright/selectors/`.

### Step 2 — Gerar workflow MCP para cada domínio

```bash
node services/clickup/playwright/validate-selectors.js --workflow <domain>
```

O script retorna chamadas MCP que o agente deve executar via Playwright:
1. `browser_navigate` — navegar para a página relevante
2. `browser_wait_for` — aguardar carregamento (networkidle)
3. `browser_snapshot` — capturar accessibility tree
4. Comparar seletores no snapshot

### Step 3 — Executar via MCP Playwright

Executar cada chamada gerada no Step 2 usando o MCP Playwright global.
O Playwright MCP está disponível diretamente (não precisa de docker-gateway).

### Step 4 — Interpretar resultados

| Status | Significado | Ação |
|--------|-------------|------|
| `PASS` | Seletor primário encontrado no DOM | Nenhuma ação |
| `FALLBACK` | Primário não encontrado, fallback funcionou | Atualizar primário para o fallback |
| `FAIL` | Nenhum seletor funcionou | Atualizar seletor manualmente (ver Step 5) |

### Step 5 — Corrigir seletores com FAIL

Para cada seletor com FAIL:
1. Executar `map-ui-page.js` na página relevante para capturar snapshot atual (ver `tasks/map-ui-pages.md`)
2. Identificar o novo seletor no snapshot
3. Atualizar o arquivo `selectors/{domain}.json` com o novo seletor
4. Re-executar `--workflow <domain>` para confirmar PASS

### Step 6 — Gerar relatório final

```bash
node services/clickup/playwright/validate-selectors.js --report
```

Salvar o arquivo `selector-validation-report.json` gerado.
Para auditorias mensais, mover para: `docs/audits/selectors-{YYYY-MM}.json`.

---

## Interpretando o Relatório

O arquivo `selector-validation-report.json` contém:

```json
{
  "generated_at": "2026-03-30T14:00:00Z",
  "domains": {
    "cu-automations": {
      "total": 12,
      "pass": 10,
      "fallback": 1,
      "fail": 1,
      "selectors": {
        "toolbar.add_button": {
          "status": "PASS",
          "matched": "[data-test='add-automation']"
        },
        "modal.trigger_dropdown": {
          "status": "FALLBACK",
          "primary": ".cu-automation-trigger",
          "fallback_used": "[aria-label='Choose a Trigger']"
        }
      }
    }
  }
}
```

**Regras de interpretação:**
- `pass >= 90%` do domínio → saudável
- `fallback > 20%` → atualizar primários (virou legacy)
- `fail > 0` → scripts do domínio podem falhar → ação imediata

---

## Pre-Conditions

- [ ] MCP Playwright disponível e autenticado no ClickUp
- [ ] Arquivos `selectors/*.json` existem (verificar com `--summary`)
- [ ] LocalDocs ClickUp acessível

## Post-Conditions

- [ ] Relatório `selector-validation-report.json` gerado
- [ ] Seletores FAIL corrigidos ou documentados como issue
- [ ] Seletores FALLBACK atualizados para usar o selector que funciona como primário
- [ ] Para auditoria mensal: relatório movido para `docs/audits/selectors-{YYYY-MM}.json`

---

## Referências

- Seletores: `services/clickup/playwright/selectors/`
- Loader: `services/clickup/playwright/load-selectors.js`
- Mapeamento de páginas: `tasks/map-ui-pages.md`
- Capability matrix: `squads/clickup-ops-squad/data/capability-matrix.yaml`

---

*Task: Validate Selectors v1.0*
*Epic 75 | clickup-ops-squad | 2026-03-30*
