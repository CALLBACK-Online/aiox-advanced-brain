# Changelog — AIOX Advanced library

## 0.6.0 — 2026-08-10

- Adiciona **AIOX Fundamentals** como trilha própria entre Introdução à Arquitetura de Sistemas e AIOX Advanced: 3 módulos, 12 aulas, 3 quizzes, projeto final e guia para agents.
- Rastreia o curso no AIOX Core 5.2.9 por commit e hashes; cobre instalação, anatomia, os 12 agents, contexto, story, autoridade, gates e handoff.
- Expande **AIOX Design v2** (`cursos/AIOX-Design/`) para 20 aulas, 6 módulos e 5 quizzes (20 questões balanceadas): repertório, direção visual, Brand Book → tokens, Storybook como fonte da verdade, governança, multi-produto, ciclo visual e capstone executável.
- Adiciona **AIOX Agent Engineering**: 28 aulas, 7 módulos, 6 quizzes, 24 questões e capstone para construir, orquestrar e operar capacidades agentic.
- Adiciona **AIOX Productização**: 6 aulas, 3 módulos, 2 quizzes, 8 questões, templates e Productization Decision Pack para levar uma capacidade comprovada a um experimento de mercado.
- Amarras de **AIOX Productização**
- Productização: FAQ de campo cohort + 3 personas de capstone; SYNTHESIS §3b gap comercial; ponte no FAQ-cohort do Advanced. no hub (trilhas laterais, MOC AE×Productização, ponte de saída do Agent Engineering); brief alinhado ao estado materializado.

### Added

- Curso `cursos/AIOX-Design/`: DESIGN.md, taxonomia atômica, stack, variantes, repertório, marca → tokens, Storybook, governança, portão vs craft e skill vs squad; seeds e processos das lives curados sem importar transcrições integrais.
- Curso `cursos/AIOX-Agent-Engineering/`: taxonomia, entidades, workflows, research, criação de squads, orquestração, runners, harness e produção.
- Curso `cursos/AIOX-Productizacao/`: Service-as-Software, dor/ROI, distribuição, caminhos de produto e estágios de monetização; inclui mapa de decisão, guia para agentes, templates, avaliações e validador próprio.
- Curso `cursos/Introducao-a-Arquitetura-de-Sistemas/`: 24 aulas, 8 módulos, 8 quizzes, 32 questões, glossário, mapa de termos, projeto integrador e guia para agents.
- Cobertura introdutória de componentes, dados, contratos, comunicação assíncrona, workflow/pipeline, concorrência, fan-out/fan-in, escala, confiabilidade, observabilidade, runtime, deploy, segurança e sistemas com agentes.
- Validador próprio do curso e integração ao bootstrap de Claude Code/Codex, hub de trilhas e catálogo.

### Changed

- `dev/` passa a ser bastidor local gitignored, como `docs/`; validadores,
  reports e `course-library-ops` deixam de integrar o clone público.
- `.github/` passa a ser configuração operacional local gitignored e deixa de
  integrar a superfície pública do acervo.
- AIOX Advanced 2.0 reduz a progressão ativa de 75 para **28 aulas** e de 14 para **6 módulos**; suas avaliações passam a somar **48 questões**; 42 aulas migradas, 4 versões legacy e 1 FAQ permanecem preservados fora da contagem ativa.
- Hubs, catálogo, bootstraps e jornada passam a separar método, Agent Engineering, Design, Productização e operação de squads por responsabilidade curricular.
- Fundamentos antes dispersos no AIOX Advanced passam a ter fonte curricular canônica no novo curso; as aulas antigas permanecem como extensões aplicadas ao método AIOX, preservando o grafo existente.
- Mini-curso Obsidian + IA agora fecha o loop **estudo → Context Brief → execução no projeto → retorno ao segundo cérebro**, com template copiável, capstone operacional e validação estrutural do contrato.
- Obsidian + IA passa a **9 aulas** (`source_version` 1.4.0): aula dedicada **Graph do acervo** (cores, filtros, órfãos, restore); wikilinks/backlinks separados; quiz com 9 questões; `graph.json` restaurado com 13 color groups.
- Skills de vault passam a orientar handoff mínimo, evidência e captura pós-execução sem transferir vault, secrets ou logs brutos.
- Hardening 1.2 do mini-curso: Context Brief obrigatório no bridge, captura/MOC por menor mecanismo, bootstrap de `notas/`, template pessoal com `status: draft`, navegação autocontida e validator comportamental sincronizado ao catálogo e aos bootstraps.
- READMEs, Capstones e projetos finais passam a diagnosticar o próximo passo entre Fundamentals, Advanced e Enterprise sem inserir promoção nas aulas técnicas.

## 0.5.1 — 2026-08-10

### Changed

- Curso de arquitetura renomeado de `AIOX-Fundamentos-de-Arquitetura` para **`Introducao-a-Arquitetura-de-Sistemas`** (título: **Introdução à Arquitetura de Sistemas**), sem prefixo AIOX — evita confusão com AIOX Fundamentals e deixa claro que a trilha é sobre arquitetura de sistemas em geral.

### Added

- Mini-curso `cursos/Obsidian-IA/` (8 aulas: vault, wikilinks, agent professor, captura, MOCs, execução).
- Skills de **vault de estudo** (segundo cérebro do acervo): `aiox-brain`, `obsidian-course-vault`, `course-moc`, `study-capture`.
- Pasta local `notas/` (README versionado; captura do aluno gitignored).
- Wiring em `AGENTS.md` / `CLAUDE.md` / README para curadoria de estudo sem poluir o canônico.
- Layout vault: pasta `cursos/` (minúsculo, alinhado a `skills/`/`squads/`), pasta `notas/` para anotações dos alunos, Graph limpo (orphans off).
- **Vault Obsidian personalizado:** tema padrão, `.obsidian/graph.json` com grupos de cores (cursos/skills/squads), snippet CSS próprio, `00-HOME.md` + MOCs de conexão.
- Glossário ampliado (158 termos + 22 conceitos) com frequência A/S; P0–P2 de vocabulário e wikilinks nas aulas-chave.
- Curso principal: **~299** Markdown e **2.742 wikilinks** verificados (`catalog.json`).
- Pontes de Graph `cursos/entradas/` (skill ↔ squad ↔ aula) ligadas aos MOCs; 14 termos de freq 0 ancorados no corpo das aulas.

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
