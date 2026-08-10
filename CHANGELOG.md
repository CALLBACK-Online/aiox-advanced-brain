# Changelog — AIOX Advanced library

## 0.5.1 — 2026-08-10

### Added

- Mini-curso `cursos/Obsidian-IA/` (8 aulas: vault, wikilinks, agent professor, captura, MOCs, execução).
- Skills de **vault de estudo** (segundo cérebro do acervo): `aiox-brain`, `obsidian-course-vault`, `course-moc`, `study-capture`.
- Pasta local `notas/` (README versionado; captura do aluno gitignored).
- Wiring em `AGENTS.md` / `CLAUDE.md` / README para curadoria de estudo sem poluir o canônico.
- Layout vault: pasta `cursos/` (minúsculo, alinhado a `skills/`/`squads/`), pasta `notas/` para anotações dos alunos, Graph limpo (orphans off).
- **Vault Obsidian personalizado:** tema padrão, `.obsidian/graph.json` com grupos de cores (cursos/skills/squads), snippet CSS próprio, `00-HOME.md` + MOCs de conexão.
- Glossário ampliado para 235 arquivos Markdown e **2.004 wikilinks** verificados no curso principal.

## 0.5.0 — 2026-08-10

### Added

- Skill `aiox-squads`, wrappers de entrada dos squads e roteamento em linguagem natural sem depender de arquivos locais da IDE.
- `AGENT-GUIDE.md`, manifesto de roteamento por runtime e suíte de avaliações comportamentais dentro do curso de squads.
- Validação de paridade entre curso, skill, catálogo, agentes de entrada e casos de roteamento.

### Fixed

- Metadados de maturidade e contagens das 24 aulas sincronizados com `catalog.json`.
- Regra de links alinhada ao escopo autocontido do curso de squads.
- Catálogo reconciliado em **62 skills**: 43 skills-base, 18 entradas dedicadas de squad e 1 roteador.
- Guias públicos `AGENTS.md` e `CLAUDE.md` versionados como contrato pedagógico do segundo cérebro; `docs/` e `scripts/` permanecem fora da distribuição.

## 0.4.1 — layout de distribuição

### Changed

- Skills canônicas movidas de `.claude/skills/` para **`skills/`** na raiz (paralelo a `squads/`).
- Este repositório é biblioteca de distribuição: copiar `skills/` e `squads/` para o projeto do aluno (ex.: `.claude/skills/` na IDE).
- `.claude/`, `.codex/`, `.agents/` no `.gitignore` (não são layout público).

## 0.4.0 — 2026-08-10

### Removed (enterprise project-context subsystem)

- Contratos e paths multi-tenant (camadas L0–L4, `docs/project/`, readiness/bootstrap de local_docs corporativo) em squads e skills.
- Scripts e tasks operacionais de integração multi-tenant (quando ainda presentes).
- Acoplamento residual a readiness enterprise / COO handoff de contexto.

### Added

- `npm run gate:enterprise` e enforce em `npm run validate`.
- `scripts/sync-from-source.mjs --write` copia com filtro + gate antes de manter o asset.
- Curso `cursos/AIOX-Advanced-Squads/`: 24 aulas práticas, 6 módulos, 6 quizzes, mapa de decisão, projeto integrador e validador próprio.

### Preserved

- “local_docs” genérico de diretório temporário (`/tmp`, `staging_dir`, `TemporaryDirectory`).
- ClickUp/Google Workspace como produtos de terceiros.
- Checklists de readiness de domínio (AI, copy, etc.), sem contrato multi-tenant.

## 0.3.1 — 2026-08-10

### Removed

- Squad executivo reservado à oferta AIOX Enterprise.
- Contratos, estados, scripts de readiness e integrações corporativas multi-tenant.

### Changed

- Catálogo e README atualizados para **49 skills** e **24 squads**.
- Sincronização limitada a inventário (`dry-run`); importações agora exigem curadoria manual.
- Validador reforçado para impedir a reintrodução de componentes corporativos reservados.

## 0.3.0 — 2026-08-10

### Changed

- Paths internos normalizados para referências portáteis.
- Integrações corporativas substituídas por contexto local de projeto onde aplicável.
- README e docs de runtime atualizados.

## 0.2.0 — 2026-08-10

### Fixed

- Removidos artefatos de importação: `*.bak` e estados locais de hardening.
- Paths absolutos de máquina (`/Users/...`) normalizados para placeholders portáteis.
- Aulas do curso alinhadas ao acervo real:
  - exemplo canônico de anatomia: `squads/squad-creator/` (não `course-creator`);
  - notas de sucessor para Spy/Bench → `research`, tech-research, code-anatomist.
- Contagem da skill `brand` (16 agentes).

### Added

- Skill wrappers de entrada: `research`, `copy`, `sales`, `advisory-board`, `claude-code-mastery`, `conteudo`.
- `catalog.json` schema v2: `library_version`, `counts`, `skill_meta`, `squad_meta`, `maturity_labels`, aliases e sucessores.
- `docs/course-asset-map.md` — ponte curso ↔ skills/squads.
- Maturidade e matriz em `docs/runtime-dependencies.md`.
- Validador reforçado (`scripts/validate-library.mjs`): paths absolutos, `*.bak`, refs skill→squad, paridade README.
- `scripts/sync-from-source.mjs` — inventário seletivo da fonte em modo `dry-run`.
- CI GitHub Actions: `.github/workflows/validate.yml`.
- `NOTICE.md` de distribuição educacional.
- Este `CHANGELOG.md`.

### Source

- Monorepo canônico de materiais: `../upstream-monorepo`.
- Commit pin documentado em `catalog.json` → `source.commit` (atualize após sync).
