# Changelog — Squad Conteudo

Todas as mudancas notaveis deste squad sao documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/).

---

## [2.2.0] - 2026-03-16

### Added
- `entry_agent: content-chief` no config.yaml (compliance SC_STRUCT_001)
- `tested: true` no config.yaml
- `CHANGELOG.md` (este arquivo)
- `ARCHITECTURE.md` (diagrama de pipeline e tiers)
- `tasks/update-content.md` (lifecycle task — brownfield update)
- `tasks/delete-content.md` (lifecycle task — cleanup)
- `activation-instructions` YAML block no content-chief.md (compliance agent-tmpl.md)

### Fixed
- Version mismatch entre config.yaml (2.1.0) e README (v2.2) — alinhado para 2.2.0

## [2.1.0] - 2026-03-10

### Added
- Workflow `wf-multiplicar` — 1 conteudo longo para 30+ micro-pecas
- Task `ingest-pillar` — ingestao de conteudo longo (YouTube, texto, arquivo)
- Task `create-impact-phrases` — frases de impacto para quote cards
- Heuristica H9 no content-chief (*multiplicar)

## [2.0.0] - 2026-03-09

### Added
- Modulo de pesquisa de concorrentes (competitor-analyst, 3 tasks, 1 workflow, 1 checklist)
- Agent `competitor-analyst` (Tier 1)
- Workflow `wf-competitor-intel`
- Workflow `wf-atomization`
- Task `atomize-content`

## [1.0.0] - 2026-03-08

### Added
- Squad inicial com 8 agents, 20 tasks, 7 workflows, 8 checklists
- Baseado em AGENTE IMPERADOR + AGENTE BLAZE + BRANDCONTENT
- Content-chief como orchestrador Tier 0
- Oraculo unificado (posts + reels)
