# Workspace Health Checklist

> **Owner:** COO (coo-orchestrator)
> **Squad:** C-Level
> **Frequency:** Weekly or On-Demand
> **Reference:** STRUCTURE.md

---

## 1. Estrutura Básica

### 1.1 Diretórios Obrigatórios (5-Layer Model)
- [ ] `workspace/{spoke}/` existe
- [ ] `workspace/{spoke}/L0-identity/` existe
- [ ] `workspace/{spoke}/L1-strategy/` existe
- [ ] `workspace/{spoke}/L2-tactical/` existe
- [ ] `workspace/{spoke}/L3-product/` existe
- [ ] `workspace/{spoke}/L4-operational/` existe
- [ ] `workspace/_templates/` existe

### 1.2 Arquivos Obrigatórios (Root)
- [ ] `workspace/{spoke}/document-registry.yaml` existe e é válido
- [ ] `.aiox-core/core-config.yaml` existe
- [ ] `.user/user.md` existe
- [ ] `CLAUDE.md` existe

### 1.3 Arquivos Obrigatórios (L0-identity)
- [ ] `L0-identity/company-dna.yaml` existe
- [ ] `L0-identity/founder-dna.yaml` existe
- [ ] `L0-identity/legal-entity.yaml` existe

### 1.4 Arquivos Obrigatórios (L1-strategy)
- [ ] `L1-strategy/icp.yaml` existe
- [ ] `L1-strategy/bmc.yaml` existe
- [ ] `L1-strategy/lean-canvas.yaml` existe
- [ ] `L1-strategy/pricing-strategy.yaml` existe
- [ ] `L1-strategy/offerbook.yaml` existe

### 1.5 Arquivos Obrigatórios (L2-tactical)
- [ ] `L2-tactical/brand/brandbook.yaml` existe
- [ ] `L2-tactical/design/design-system.yaml` existe
- [ ] `L2-tactical/content/content-strategy.yaml` existe

---

## 2. Validação de Camadas (5-Layer)

### 2.1 Consistência document-registry.yaml ↔ Arquivos

Para CADA entrada em `document-registry.yaml`:
- [ ] Arquivo referenciado existe no path correspondente (L0-L4)
- [ ] Campo `state` é válido (PLACEHOLDER|DRAFT|POPULATED|VALIDATED|APPROVED|STALE|ARCHIVED)
- [ ] Campo `owner` referencia squad existente
- [ ] Campo `ttl` respeita a camada (L0: 365d, L1: 90d, L2: 60d, L3: 30d, L4: 7d)

### 2.2 Hierarquia de Camadas

- [ ] Documentos L1 não contradizem L0
- [ ] Documentos L2 não contradizem L1
- [ ] Documentos L3 não contradizem L2
- [ ] Documentos L4 não contradizem L3

### 2.3 Completude por Camada

- [ ] L0-identity tem pelo menos 2 documentos POPULATED+
- [ ] L1-strategy tem pelo menos 3 documentos POPULATED+
- [ ] L2-tactical tem pelo menos 1 documento POPULATED+
- [ ] L3-product tem pelo menos 1 documento POPULATED+

---

## 3. Validação de Integrações

### 3.1 Consistência services/ ↔ Configuração

Para CADA serviço em `services/`:
- [ ] Pasta `services/{service}/` tem `config.yaml` ou `index.ts`
- [ ] Serviço tem documentação mínima (README ou inline)
- [ ] Dependências listadas no `package.json` local (se aplicável)

### 3.2 Segurança de Configuração

- [ ] Nenhuma credencial hardcoded em arquivos de configuração
- [ ] Todas as credenciais usam `${ENV_VAR}` syntax
- [ ] Nenhum arquivo `.env` commitado

---

## 4. Validação de Document Registry

### 4.1 Existência e Integridade
- [ ] `workspace/{spoke}/document-registry.yaml` parseia sem erro
- [ ] Todos os IDs são únicos (sem duplicatas)
- [ ] Todos os paths referenciados existem no filesystem

### 4.2 Consistência Cross-Layer
Para CADA entrada no registry:
- [ ] Documento está na camada correta (L0-L4) conforme seu tipo
- [ ] Dependências upstream/downstream são válidas
- [ ] Owner squad existe em `squads/`

---

## 5. Validação Design System (se aplicável)

### 5.1 Design System Package (packages/ds/)
- [ ] `packages/ds/` existe
- [ ] `packages/ds/package.json` existe e é válido
- [ ] `packages/ds/src/` existe

### 5.2 Design Tokens (packages/tokens/)
- [ ] `packages/tokens/` existe
- [ ] `packages/tokens/` contém tokens de cores, radius, spacing, fonts

### 5.3 Tailwind Config (packages/tailwind-config/)
- [ ] `packages/tailwind-config/` existe
- [ ] Configuração compartilhada é consistente com tokens

---

## 6. Validação de Sintaxe

### 6.1 YAML Files
- [ ] Todos os arquivos `.yaml` parseiam sem erro
- [ ] Todos os arquivos `.yml` parseiam sem erro

### 6.2 JSON Files
- [ ] Todos os arquivos `.json` parseiam sem erro
- [ ] JSON tokens seguem W3C Design Tokens spec (se aplicável)

### 6.3 Markdown Files
- [ ] Todos os arquivos `.md` têm frontmatter válido (se usado)
- [ ] Nenhum link quebrado interno

---

## 7. Padrões Proibidos

### 7.1 Nomes de Arquivo
- [ ] Nenhum arquivo `*_backup`
- [ ] Nenhum arquivo `*_old`
- [ ] Nenhum arquivo `*_v2`, `*_v3`
- [ ] Nenhum arquivo `test_*` (fora de /tests)
- [ ] Nenhum arquivo `temp_*`
- [ ] Nenhum arquivo `TODO_*`
- [ ] Nenhum arquivo `*~`

### 7.2 Nomes de Produto
- [ ] Todos os produtos em `L3-product/` usam snake_case
- [ ] Nenhum PascalCase
- [ ] Nenhum kebab-case

---

## 8. Consistência Cross-Reference

### 8.1 Registry → Filesystem
- [ ] Todos os documentos no registry existem no filesystem
- [ ] Nenhum documento órfão (existe no filesystem mas não no registry)

### 8.2 Squad → Workspace
- [ ] `workspace_integration.documents_owned` em cada squad config referencia IDs válidos no registry

### 8.3 Services → Configuração
- [ ] Serviços referenciados em workflows existem em `services/`

---

## 9. Sagas e Compensação

### 9.1 On Failure Strategy
Para workflows com mutations:
- [ ] Tem `on_failure.strategy` definido
- [ ] Strategy é válido: `compensate_executed | continue | manual`

### 9.2 Compensation Actions
Para steps com side-effects:
- [ ] Step tem `compensation` definido
- [ ] Compensation tem `operation` (operação inversa)
- [ ] Compensation tem `params` com referências corretas

---

## 10. Services

### 10.1 IDE Sync Engine
- [ ] `npm run sync:ide -- --dry-run` executa
- [ ] `npm run sync:ide:check` valida o engine atual
- [ ] `.aiox-core/infrastructure/scripts/ide-sync/index.js` permanece como engine canônico de sync

### 10.2 Service Bus
- [ ] `services/bridge/` existe
- [ ] `services/bridge/package.json` documenta o Service Bus compartilhado

---

## 11. Workflow Integrity Gate

### 11.1 Automated Integrity Test
- [ ] `squads/c-level/scripts/workflow-integrity.test.js` existe
- [ ] `npm test -- squads/c-level/scripts/workflow-integrity.test.js` executa com PASS

### 11.2 Runtime Safety Assertions
- [ ] Não há referência órfã a steps em templates (`{{step.output...}}`)
- [ ] Regras críticas não usam template aninhado inválido
- [ ] Workflows críticos parseiam sem erro sintático

---

## Scoring

| Seção | Peso | Score |
|-------|------|-------|
| Estrutura Básica (5-Layer) | 25% | __/100 |
| Camadas (Registry) | 20% | __/100 |
| Integrações (Services) | 15% | __/100 |
| Document Registry | 15% | __/100 |
| Design System | 10% | __/100 |
| Sintaxe | 5% | __/100 |
| Padrões Proibidos | 5% | __/100 |
| Cross-Reference | 3% | __/100 |
| Sagas | 2% | __/100 |

**Total Score:** __/100

**Gate Decision:**
- 90-100: ✅ PASS
- 70-89: ⚠️ CONCERNS
- <70: ❌ FAIL

---

## Issue Severity Guide

| Severidade | Critério | Ação |
|------------|----------|------|
| 🔴 BLOCKER | Quebra validação básica | Fix imediato |
| 🟡 HIGH | Inconsistência funcional | Fix em 24h |
| 🟠 MEDIUM | Falta de completude | Fix em 1 semana |
| 🔵 LOW | Best practice missing | Backlog |

---

*Checklist do Squad C-Level - COO Orchestrator*
*Versão: 2.0.0*
*Última atualização: 2026-03-15*
