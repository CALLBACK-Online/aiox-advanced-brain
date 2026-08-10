# Checklist — manage

Escolher a operação mínima. Toda operação termina com o gate da última coluna
verde; operação sem gate citável não está concluída.

## Matriz de toques (superfícies acopladas)

Uma mudança editorial raramente toca um arquivo só. Antes de executar, abrir a
linha da operação e tocar **todas** as superfícies listadas — os validadores
conferem a coerência entre elas.

| Operação | Superfícies a tocar | Gate |
|----------|--------------------|------|
| **add/remove-lesson** | `aulas/NN-*.md` (numeração) · frontmatter README (`lessons`) · `EXPECTED` + `MODULE_OF` em `dev/courses/<slug>/checks.py` · `catalog.json` → `courses.<id>.lessons` · módulo dono em `modulos/` · navegação das aulas vizinhas | `python3 dev/validate.py --course <slug>` |
| **add/edit-quiz** | `avaliacoes/Quiz-M*.md` (gabarito balanceado A/B/C/D) · frontmatter README (`quizzes`, `questions`) · checks + catalog | idem |
| **sync-counters** | frontmatter README = arquivos reais = checks = `catalog.json` | `doctor.py` sem DIVERGE |
| **register-course** | `catalog.json` → `courses.<id>` + `learning_journey` · hub `cursos/README.md` · MOCs/`entradas/` (wikilinks) · mapas `AGENTS.md`/`CLAUDE.md` se cria rota nova · `dev/courses/<slug>/` | `npm run validate` |
| **rebalance-journey** | `catalog.json` → `learning_journey` (core, rotas, transições) · pontes `ponte/*.md` **bidirecionais** (o vizinho também) · responsibilities | `validate_learning_journey` PASS |
| **split-course** | brief de fronteira no bastidor · curso novo (pipeline completo) · origem: aulas movidas para `archive/` + `source_*` no destino · journey + catalog dos dois lados | validate PASS nos dois cursos |
| **retire-course** | `archive/` do material · remoção em catalog/journey/hub/MOCs/mapas · pontes dos vizinhos apontando para substituto | `npm run validate` + doctor sem órfãos |
| **surface-check** | mover bastidor vazado de `cursos/` para `docs/producao-cursos/<id>/` | `check_course_surface.py` limpo |
| **ops-sync** | após editar o SoT (`dev/ops/course-library-ops/`): reinstalar projeções | `doctor.py` sem DERIVA |
| **improve-course** | baseline validate · `audit_didactics.py --write` · ledger `didactic-audit.md` · lotes (rubrica teach) · `audit --check` | audit sem FAIL/PENDING + `dev/validate.py --course` |
| **upgrade-course** | bastidor/spec delta · `plan_upgrade.py --write` · ledger · re-aprovação · lotes (sem apagar) · contadores | plano + `npm run validate` |

## improve-course

- [ ] Abrir `checklists/improve-course.md` e `skills/teach/SKILL.md` (fallback: `didactic-rubric.md`)
- [ ] Baseline: `npm run validate` (ou corrigir estrutura antes de polish)
- [ ] `python3 scripts/audit_didactics.py --course <id> --write`
- [ ] Priorizar FAIL sistemáticos; resolver PENDING com evidência humana
- [ ] Lotes 3–4 aulas; validar entre lotes
- [ ] `audit_didactics.py --check docs/producao-cursos/<id>/didactic-audit.md` + validate curso

## upgrade-course

- [ ] Abrir `checklists/upgrade-course.md` (nunca `scaffold` em destino existente)
- [ ] `prepare_course.py --mode upgrade` se bastidor ausente
- [ ] `plan_upgrade.py --write` → inventário + ledger (sem mutar aulas)
- [ ] `archive-candidate` só com decisão humana e destino recuperável
- [ ] Reaprovar brief/outline; `plan_upgrade.py --require-approved --refresh`
- [ ] Editar por linha do ledger; sync counters; validate

## doctor

- [ ] `python3 dev/ops/course-library-ops/scripts/doctor.py` (root do acervo)
- [ ] Revisar: contadores divergentes, journey órfã, bridges ausentes,
      **deriva SoT ↔ `.claude`/`.agents`**
- [ ] Cada ERR vira uma linha da matriz acima; WARN vira backlog declarado

## reverse-engineer

- [ ] `python3 scripts/analyze_courses.py --course cursos/<Curso>`
- [ ] Comparar com 1–3 vizinhos
- [ ] Separar invariantes, variações intencionais e dívida

## validate

- [ ] `npm run validate` ou `python3 dev/validate.py --course <slug>`
- [ ] Corrigir erros antes de nova feature editorial (nunca empilhar sobre
      estrutura quebrada)

## Princípios

- Preferir correção sistemática (padrão aplicado a N aulas) a retoque isolado.
- Lote pequeno; validar entre lotes.
- Desvio de processo (gate pulado) → `deviations.yaml` no bastidor, nunca
  silêncio.
