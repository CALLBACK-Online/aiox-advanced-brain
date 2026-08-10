---
tags: [hub, layer/skill, mapa]
aliases: [Mapa Skills, inventário skills, skills sem squad]
---

# MAPA-SKILLS — inventário de uso (67 skills + 24 squads)

> Não é runtime. É o mapa para **não se perder** e **não duplicar**.

- Squads 1:1 com aula: [[cursos/AIOX-Advanced-Squads/README|AIOX Advanced Squads]]
- Core AIOX (orbitais + SDC) em detalhe: [[cursos/AIOX-Fundamentals/README|Fundamentals]] · [[cursos/AIOX-Fundamentals/references/core-skills-runtime|core-skills-runtime]]
- Pontes Graph: [[cursos/entradas/README|entradas]]
- MOCs: [[cursos/MOC-Skills]] · [[cursos/MOC-Squads]]
- Maturidade: `catalog.json` → `skill_meta` / `squad_meta`

## Regra de ouro

| Precisa de… | Vá para… |
|-------------|----------|
| Pacote multi-agente (vários agents/tasks) | **Squad** + aula em Advanced Squads |
| Procedimento estreito / um ritual | **Skill** (`skills/<id>/SKILL.md`) |
| Escolher entre 24 squads | skill `aiox-squads` + `agent-router.json` |
| Agent orbital ou ciclo de story do **core** | **Fundamentals** (mapa de agents + skills SDC) |

---

## 1. Skills de entrada de squad (24) — cobertas por aula

Cada uma: skill + squad + **aula 01–24** + entrada Graph.

Ver lista 1:1 em [[cursos/MOC-Squads]].

Maturidade típica: `study` — estudar anatomia; copiar para o projeto; não prometer run autônomo sem evidência.

---

## 2. Skills **core runtime-aiox** (23) — detalhadas no Fundamentals

Estas vêm do núcleo AIOX (ciclo de entrega e agents). **Não** têm aula 1:1 no curso de Squads; o mapa completo está em:

`cursos/AIOX-Fundamentals/references/core-skills-runtime.md`

### Orbitais (persona / autoridade)

`aiox-master` · `aiox-analyst` · `aiox-pm` · `aiox-architect` · `aiox-ux-designer` · `aiox-data-engineer` · `aiox-sm` · `aiox-po` · `aiox-dev` · `aiox-qa` · `aiox-devops`  
(+ superfícies `@analyst`… no core)

Aula âncora: Fundamentals `2.2-escolher-o-agente-certo`.

### Ciclo de story / SDC

| Skill | Papel |
|-------|--------|
| `validate-story-draft` | Draft → Ready |
| `develop-story` | Implementar na branch |
| `review-story` / `apply-qa-fixes` | Revisão e remediação |
| `deploy-story` / `verify-deploy` | Deploy + verificação (se houver target) |
| `close-story` | Única que fecha Done |
| `full-sdc` | Orquestra o ciclo completo de **uma** story |
| `enhance-workflow` | Melhorar workflow existente |
| `roundtable` | Revisão multi-perspectiva |
| `three-brain` | Roteamento de motor / no-self-review |
| `telegram` | Canal/notificação (quando configurado) |

Aula âncora: Fundamentals `3.3-ciclo-da-story-na-pratica` + referência core-skills.

---

## 3. Skills portable / vault / util (17)

| Skill | Quando usar |
|-------|-------------|
| `aiox-brain` | Segundo cérebro do acervo |
| `aiox-squads` | Router universal dos 24 squads |
| `obsidian-course-vault` | Abrir vault / achar aula |
| `course-moc` | Hubs e mapas |
| `study-capture` | Nota pessoal sem editar canônico |
| `teach` | Melhorar aulas canônicas (exceção) |
| `design-md` | Lint/contrato DESIGN.md |
| `skill-creator` | Criar skill (lifecycle) |
| `slide-creator` | Deck **standalone** (sem squad) |
| `tech-search` / `tech-research` | Pesquisa tech (search = skill leve; research = pipeline mais fundo) |
| `handoff` | Compactar contexto para outro agent |
| `impeccable` | Craft visual **pós**-gate |
| `doc-rot` | Documentação apodrecida |
| `extract-session-heuristics` | Heurísticas de sessão |
| `deep-strategic-planning` | Planejamento estratégico longo |
| `survey-intel` | Inteligência de survey |

Cursos de apoio: Obsidian-IA (vault), Design (`design-md`), Productização (não substitui copy/sales squads).

---

## 4. Skills study “chief” / meta (sem squad próprio)

| Skill | Papel | Não confundir com |
|-------|--------|-------------------|
| `design-chief` | Orquestra camada design | `design-system` / `design-ops` (squads) |
| `decoder-chief` | Orquestra decoder | `domain-decoder` / `code-anatomist` |
| `squad-chief` | Entry de criação/validação de squad | `squad-creator` / `squad-creator-pro` |

---

## 5. Anti-duplicação explícita

| Par | Como escolher |
|-----|----------------|
| **`slide-creator` vs `slides-creator`** | `slide-creator` = portable, deck sozinho. `slides-creator` = skill **+ squad + aula 17**. |
| **`tech-search` vs `tech-research`** | `tech-search` = pesquisa tech self-contained. `tech-research` = portable mais profunda / multi-fonte (alinhar à missão; se for squad research, use aula 02). |
| **`skill-creator` vs `skill-creator-ops`** | Creator = lifecycle da skill. Ops = squad/aula 22 de operação de criação. |
| **Skill de squad vs aula** | Aula ensina **julgamento**; SKILL.md é **porta de entrada** no runtime. |

### Entradas Graph com “skill-skill-” no nome

Ids como `skill-creator` geram arquivo `skill-skill-creator.md` (prefixo `skill-` + id). **Não** são dois produtos — é convenção de path.

---

## 6. Skills sem squad (43) — checklist

Todas têm `SKILL.md`. Explicação didática:

- **Core runtime** → Fundamentals + `references/core-skills-runtime.md`
- **Vault** → Obsidian-IA + skills vault
- **Chiefs / util** → este mapa + SKILL.md
- **Nunca** exigir aula de Squads para skill que não tem squad

Lista completa no disco: pasta `skills/` (67 pastas com `SKILL.md`).

---

## 7. Squads (24) — nada de fora

Cada squad: pacote + skill de entrada + aula + router + entrada Graph.  
Curso: [[cursos/AIOX-Advanced-Squads/README|AIOX Advanced Squads]].

---

## Manutenção

Ao adicionar skill/squad no acervo:

1. `catalog.json`  
2. `skills/<id>/SKILL.md` (com **Quando usar** se for entrada de squad)  
3. `cursos/entradas/skill-<id>.md` (e squad se houver)  
4. Se squad: aula em Advanced Squads + rota no router  
5. Atualizar este MAPA se for core ou anti-duplicação nova  

[⌂ Hub cursos](README.md) · [00-HOME](../00-HOME.md)
