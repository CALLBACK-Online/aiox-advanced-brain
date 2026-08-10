# Task: Visual Extraction

## Metadata

```yaml
task: visual-extraction
atomic_layer: Molecule
responsavel_type: Agent
agent: auditor
prompt_template: "squads/clickup-ops-squad/templates/visual-extraction-prompt.md"
output_schema: "squads/clickup-ops-squad/data/visual-output-schema.json"
output_dir: "squads/clickup-ops-squad/output/visual-extractions/"
```

## Description

Extrai estrutura de local_docs ClickUp a partir de **vídeos de demonstração** ou **screenshots**
usando o mega-prompt de extração visual+verbal. O output alimenta o pipeline de análise
como evidência técnica classificada em 4 níveis de verdade.

Uso principal: reverse engineering de workspaces de clientes durante onboarding,
auditoria de estrutura existente não documentada, ou identificação de padrões
em workspaces ClickUp sem acesso direto à API.

---

## Quando Usar

| Cenário | Usar Visual Extraction? |
|---------|------------------------|
| Onboarding de cliente com docs/project existente não documentado | SIM — reverter estrutura sem acesso API |
| LocalDocs sem credenciais de API disponíveis | SIM — única forma de extrair |
| Vídeo de demonstração/treinamento com estrutura visível | SIM — capturar evidências |
| Análise competitiva de workspaces ClickUp públicos | SIM |
| LocalDocs com acesso API disponível | NÃO — usar `audit-structure` via API diretamente |
| Screenshot parcial de uma única tela | OPCIONAL — limitado, use para seletores |

---

## Inputs

| Input | Obrigatoriedade | Descrição |
|-------|----------------|-----------|
| Vídeo ou screenshot de docs/project | OBRIGATÓRIO | Fonte de extração |
| `visual-extraction-prompt.md` | OBRIGATÓRIO | Mega-prompt de instruções de captura |
| `visual-output-schema.json` | OBRIGATÓRIO | Schema de validação do output |

---

## Workflow Completo

### Step 1 — Preparar o Mega-Prompt

Ler o mega-prompt completo:
```
squads/clickup-ops-squad/templates/visual-extraction-prompt.md
```

O prompt define 7 categorias de captura:
- **A** — Estrutura de docs/project (Spaces, Folders, Lists, hierarquia)
- **B** — Custom Fields (nome, tipo, opções, UUIDs)
- **C** — Status Workflows (nomes, cores, grupos, ordem)
- **D** — Views (tipo, configuração, filtros, agrupamentos)
- **E** — Task Content (campos preenchidos, relacionamentos, checklists)
- **E.2** — View Layout Blueprint (colunas, frozen, scroll, campos ocultos)
- **F** — Automações e Integrações
- **G** — Configurações de LocalDocs (ClickApps, permissões, settings)

### Step 2 — Executar Extração

Para vídeos: usar o mega-prompt com o vídeo como contexto.
Para screenshots: usar o mega-prompt com cada imagem.

**Princípio central (TELA + FALA = TRUTH):**
- Quando elemento aparece na tela E no áudio simultaneamente → `confidence: TRUTH`
- Apenas na tela → `confidence: CODE_ONLY`
- Apenas no áudio → `confidence: CALLS_ONLY`
- Ambos mas contraditórios → registrar como `DIVERGENCIA`

**Regras obrigatórias durante extração:**
- Timestamp `[MM:SS]` em cada observação
- Verbatim primeiro (texto exato como aparece)
- Distinguir `[TELA]`, `[FALA]`, `[ACAO]` na origem
- Nunca interpretar ou resumir — registrar

### Step 3 — Estruturar Output no Schema

Validar o output contra `squads/clickup-ops-squad/data/visual-output-schema.json`.

O schema define:
```json
{
  "source": {
    "type": "video_visual",
    "title": "Título do vídeo",
    "url": "https://...",
    "duration": "MM:SS",
    "speaker": "Nome do apresentador",
    "extraction_date": "YYYY-MM-DD"
  },
  "segments": [...],
  "relationships_discovered": [...],
  "heuristics_captured": [...],
  "summary": {
    "total_segments": N,
    "truth_count": N,
    "both_count": N,
    "code_only_count": N,
    "calls_only_count": N
  }
}
```

### Step 4 — Salvar Output

Salvar em:
```
squads/clickup-ops-squad/output/visual-extractions/extraction-{source-name}-{YYYY-MM-DD}.json
```

### Step 5 — Usar Output

O output extraído pode ser usado para:

| Uso | Como |
|-----|------|
| Criar tokenization de local_docs cliente | Alimentar `clickup-tokenization.yaml` com IDs descobertos |
| Mapear estrutura para materialização | Input para `materialize-process` |
| Identificar gaps vs AIOX | Input para `audit-structure` |
| Identificar seletores DOM faltantes | Extrair seletores de screenshots para `selectors/*.json` |

---

## Pre-Conditions

- [ ] Vídeo ou screenshots disponíveis
- [ ] `visual-extraction-prompt.md` lido antes de iniciar
- [ ] `visual-output-schema.json` disponível para validação

## Post-Conditions

- [ ] Output JSON salvo em `output/visual-extractions/`
- [ ] Output validado contra `visual-output-schema.json`
- [ ] Segmentos com `confidence: TRUTH` destacados no summary
- [ ] Divergências documentadas e sinalizadas para review humano

---

## Referências

- Mega-prompt: `squads/clickup-ops-squad/templates/visual-extraction-prompt.md`
- Schema: `squads/clickup-ops-squad/data/visual-output-schema.json`
- Validação de estrutura via API: `tasks/audit-structure.md` (quando acesso API disponível)
- Mapeamento de seletores DOM: `tasks/map-ui-pages.md`

---

*Task: Visual Extraction v1.0*
*Epic 75 | clickup-ops-squad | 2026-03-30*
