---
name: course-library-ops
description: >-
  Skill operacional de maintainer para fazer engenharia reversa, criar,
  melhorar, modernizar e governar cursos Markdown verificáveis e seus acervos:
  brief, outline, aulas, avaliações, fontes, harness, catálogo e journey. Use
  em bootstrap, criação greenfield, upgrade brownfield, auditoria didática,
  doctor, gestão curricular ou pack de time. Não expor, instalar ou registrar
  como skill de aluno.
---

# Course Library Ops — fábrica e governança de acervos

## Identidade (não negociável)

| É | Não é |
|---|--------|
| Skill de **time/maintainer** | Skill de aluno no catálogo `skills/` |
| Instala em `.claude/skills/` e `.agents/skills/` | Empacotada no npm pack do aluno |
| Cria e opera **acervos** + **cursos** | Duplicação da `teach` canônica |
| Fecha com `npm run validate` | “Já montei o curso” sem harness |

**Proibido:** copiar para `skills/`, registrar em `catalog.json` → skills de
estudo, criar `cursos/entradas/…`, ou orientar o aluno a usá-la.

**Teach correta:** `skills/teach/SKILL.md` do acervo. A skill global homônima de
tutoria HTML não participa destes fluxos. O ops orquestra a rubrica canônica;
usa `checklists/didactic-rubric.md` apenas quando ela não existir no destino.

**SoT versionada:** `dev/ops/course-library-ops/`  
**Runtime:** `scripts/install.sh` → `.claude/` e `.agents/`  
**Pack de time:** `scripts/package.sh` → zip

## Quatro superfícies

| Superfície | Destino | Conteúdo |
|------------|---------|----------|
| Bastidor | `docs/producao-cursos/<id>/` | brief, outline, gaps, deviations, validation-report |
| Aluno | `cursos/<Curso>/` | curso autocontido |
| Prova | `dev/courses/<slug>/` | manifest + checks |
| Integração | `catalog.json`, hubs, AGENTS | journey e descoberta |

## Sete modos

| Modo | Quando | Ferramentas |
|------|--------|-------------|
| **reverse-engineer** | Recuperar o DNA de curso/acervo | `scripts/analyze_courses.py` + `references/course-dna.md` |
| **bootstrap** | Novo repo “como este acervo” | `scripts/bootstrap_library.py` + `references/library-anatomy.md` |
| **create-course** | Curso novo greenfield | `prepare_course.py` → gates humanos → `scaffold_course.py` |
| **upgrade-course** | Modernizar curso existente sem apagar | `plan_upgrade.py` + `checklists/upgrade-course.md` |
| **improve-course** | Melhorar didática do canônico | `audit_didactics.py` + rubrica `teach` |
| **manage** | Doctor, contadores, journey, split | `scripts/doctor.py` + `checklists/manage.md` |
| **pack-install** | Compartilhar / instalar runtime | `scripts/package.sh` + `scripts/install.sh` |

Se ambíguo: curso ausente → create; curso existente → upgrade ou improve.

### Roteamento rápido

| Pedido | Usar | Não usar |
|--------|------|----------|
| DNA / comparar cursos | reverse-engineer | inventar perfil |
| Repo novo de cursos | bootstrap | copiar monorepo Enterprise |
| Curso novo (pasta vazia) | create-course | scaffold com destino existente |
| Modernizar curso existente | upgrade-course | `--force` / apagar aulas |
| Aulas fracas / didática | improve-course + **teach canônica** | teach global HTML |
| Contadores / journey / doctor | manage | editar só README |
| Zip / instalar Claude·Agents | pack-install | commitar `.claude/` |
| Batch com voz MMOS | **fora** → course-creator Enterprise | este pack |

Aprovações humanas: `references/approval-protocol.md` (brief + outline antes de materializar ou modernizar).
Decisões de absorção: `references/source-patterns.md`.

---

## Modo reverse-engineer

1. Executar `python3 scripts/analyze_courses.py` no root do acervo.
2. Comparar o alvo com 1–3 cursos vizinhos da mesma responsabilidade.
3. Ler bastidor, proveniência, checks específicos e histórico Git.
4. Separar invariantes, diferenças intencionais e dívida que não deve ser clonada.
5. Entregar perfil, pipeline provável, gaps e riscos dominantes.

O relatório do script é a verdade dinâmica; `references/course-dna.md` registra
o baseline que originou esta skill.

---

## Modo bootstrap

1. Confirmar destino.
2. `python3 scripts/bootstrap_library.py --dest <path> --title "…" --slug <lib-slug>`
3. `cd <path> && python3 dev/validate.py` → PASS.
4. `bash dev/ops/course-library-ops/scripts/install.sh --target both`
5. Entregar paths + próximo passo (create-course).

Checklist: `checklists/bootstrap.md`. Skeleton: `assets/library-skeleton/`.

---

## Modo create-course

Pipeline: `references/production-pipeline.md`.  
Anatomia: `references/course-anatomy.md`.  
Arquétipos: `references/archetypes.md`.  
Templates: `assets/course-templates/`.

Fail-closed:

1. Prior art (slug, pasta, journey, anti-duplicação).
2. Preparar bastidor sem tocar o aluno:
   `python3 scripts/prepare_course.py --course-id <id> --title "…" --path cursos/<Curso> --profile <perfil>`.
3. Aprovação humana do brief e outline pelo contrato
   `references/approval-protocol.md`; o agente nunca se autoaprova.
4. Fonte/proveniência (+ SOURCE-MANIFEST se técnico).
5. Aulas pelo arquétipo (lote pequeno).
6. Avaliação coerente com o perfil: quiz/capstone/rubrica ou diagnóstico.
7. README e somente os artefatos condicionais úteis (AGENT-GUIDE, pontes, glossário, mapas, templates).
8. `dev/courses/<slug>/{manifest.yaml,checks.py}`.
9. catalog + hub + maps se rota nova.
10. `npm run validate` EXIT 0 + validation-report no bastidor.

Preencher o `course-spec.json` preparado, validar os gates e criar o scaffold:

```bash
python3 scripts/check_approvals.py \
  --spec docs/producao-cursos/<id>/course-spec.json
python3 scripts/scaffold_course.py \
  --spec docs/producao-cursos/<id>/course-spec.json \
  --repo-root /caminho/do/acervo
```

Perfis de spec: `fundacional`, `tecnico-operacional`, `decisorio-aplicado`,
`catalogo-roteamento`, `preview-protegido`, `migracao-profunda`.
O scaffold nunca sobrescreve destino existente e permanece `draft` até remover
placeholders, integrar catálogo/journey e validar. Bastidor pré-existente é
aceito somente com brief e outline aprovados; curso ou harness existentes
continuam bloqueando o create.

Checklist: `checklists/create-course.md`.

---

## Modo upgrade-course

Não usar `--force` no scaffold. Abrir `checklists/upgrade-course.md`.

1. Baseline do curso existente e inventário de course/harness/catalog.
2. Preparar ou preservar brief, outline e spec com `creation_mode: upgrade`.
3. Gerar plano sem mutação:

```bash
python3 scripts/plan_upgrade.py --course <id> \
  --spec docs/producao-cursos/<id>/course-spec.json --write
```

4. Revisar `upgrade-plan.json` e `upgrade-ledger.md`; preservar paths/IDs válidos.
5. Reaprovar brief/outline e repetir com `--require-approved --refresh`.
6. Humano marca `status: approved` somente nas ações autorizadas do plano.
7. Apply **assistido e explícito** (nunca apaga; nunca bulk):

```bash
python3 scripts/apply_upgrade.py --course <id> --add <lesson-id>
python3 scripts/apply_upgrade.py --course <id> --archive <lesson-id>
# archive → docs/producao-cursos/<id>/archive/upgraded/YYYY-MM-DD/
```

8. Editar lotes pequenos. `review-preserve-path` = edição humana do conteúdo.
9. Estado derivado (sem JSON extra): `python3 scripts/doctor.py --course <id>`.
10. Fechar cada lote com o validador do curso; fechar o fluxo com `npm run validate`.

`creation_mode` canônico: **`create` | `upgrade`** (aliases `greenfield`→create,
`brownfield`→upgrade).

---

## Modo improve-course

Abrir a `skills/teach/SKILL.md` canônica e `checklists/improve-course.md`.

```bash
npm run validate
python3 scripts/audit_didactics.py --course <id> --write
# revisar/corrigir o ledger em lotes de 3–4 aulas ou um módulo
python3 scripts/audit_didactics.py \
  --check docs/producao-cursos/<id>/didactic-audit.md
python3 dev/validate.py --course <id>
```

O ledger usa seis dimensões e estados `PASS|FAIL|PENDING`; não usa score
Enterprise não calibrado. Sinais automáticos nunca aprovam semântica. Resolver
todo `PENDING`, corrigir todo `FAIL` e registrar evidência final.

---

## Modo manage

| Operação | Ação |
|----------|------|
| doctor | `doctor.py` · `--course <id>` · `--states` (resumo derivado do acervo) |
| validate | `npm run validate` / `python3 dev/validate.py --course <slug>` |
| sync-counters | README ↔ checks ↔ catalog |
| rebalance-journey | `catalog.json` + bridges reais (`references/journey-model.md`) |
| split / retire | brief de fronteira + archive + journey limpa |
| surface-check | zero bastidor em `cursos/` |
| ops-sync | SoT editado → `install.sh --target both` → doctor sem DERIVA |

Checklist: `checklists/manage.md` — **abrir a matriz de toques antes de
executar**: cada operação lista as superfícies acopladas (README ↔ checks ↔
catalog ↔ hub ↔ MOCs ↔ pontes bidirecionais ↔ mapas) e o gate que a fecha.

---

## Modo pack-install

```bash
# instalar no acervo atual
bash scripts/install.sh --target both          # claude + agents
bash scripts/install.sh --target claude
bash scripts/install.sh --target agents

# empacotar para o time
bash scripts/package.sh
# → dist/course-library-ops-<version>.zip
```

Colega: descompacta no acervo (ou usa zip) →
`bash scripts/install.sh --target both --repo /path/to/acervo`.

Contrato anti-deriva (o que torna 3 cópias sustentáveis):

- **Só o SoT é editável** (`dev/ops/course-library-ops/`); `.claude/` e
  `.agents/` são projeções regeneráveis — nunca editar a cópia instalada.
- Após editar o SoT: `install.sh --target both` (operação `ops-sync`).
- `doctor.py` compara SoT ↔ projeções arquivo a arquivo e **falha com ERR**
  em qualquer divergência.
- `package.sh` só gera zip após selftest funcional (bootstrap num tmp +
  `dev/validate.py` PASS) — nunca distribuir o que não prova nascer verde.
- Versão: fonte única em `package.json` (SemVer validada no empacote).

---

## Guardrails

- Superfície limpa (gate `check_course_surface.py`).
- Links de um curso resolvem **dentro** da pasta do curso.
- Sem paths absolutos de máquina.
- Contadores sincronizados: README = harness = catalog.
- Harness **não** exige `docs/`.
- Aprovação humana não pode ser inferida ou fabricada pelo agente.
- `create-course` nunca toca destino existente; `upgrade-course` nunca apaga.
- Sem invenção de assets/comandos.
- Sem push sem pedido explícito.

## Evidência de conclusão

| Modo | Pronto quando |
|------|----------------|
| reverse-engineer | invariantes + variações + gaps + perfil respaldados por paths |
| bootstrap | validate PASS + skeleton + ops SoT em `dev/ops/` |
| create-course | brief/outline aprovados + superfície + harness + catalog + validate PASS (+ retro opcional) |
| upgrade-course | plano aprovado + paths/IDs preservados + ledger + apply + validate PASS (+ retro) |
| improve-course | ledger sem FAIL/PENDING + lotes evidenciados + validate PASS (+ retro se DNA mudou) |
| manage | operação + doctor/validate |
| pack-install | selftest PASS + zip gerado e/ou projeções instaladas + doctor sem DERIVA |

## Mapa do pack

```text
SKILL.md
scripts/install.sh | package.sh | bootstrap_library.py | prepare_course.py
         scaffold_course.py | plan_upgrade.py | apply_upgrade.py
         audit_didactics.py | check_approvals.py | course_common.py
         doctor.py | analyze_courses.py | selftest.py
references/library-anatomy | production-pipeline | course-anatomy | course-dna
           archetypes | surface-vs-bastidor | journey-model | approval-protocol
           source-patterns
checklists/bootstrap | create-course | upgrade-course | improve-course | manage
assets/course-templates/ (… | retrospective.md) | assets/library-skeleton/
agents/openai.yaml
```
