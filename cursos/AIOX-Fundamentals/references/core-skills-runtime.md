---
type: reference
course: aiox-fundamentals
status: canonical
canonical_scope: cursos/AIOX-Fundamentals
tags: [skills, core, runtime-aiox, sdc, orbitais]
---

# Skills core do AIOX (runtime) — mapa detalhado

> Complemento obrigatório das aulas 2.2, 2.3 e 3.3.  
> Paths de skill no acervo: `skills/<id>/SKILL.md` (copiar para o runtime do **projeto**, não “rodar” só no vault de estudo).

Maturidade catalog: **`runtime-aiox`** (e orbitais de persona).  
Mapa geral do acervo (fora desta pasta de curso, path monoespaçado): `cursos/MAPA-SKILLS.md`.

---

## 1. Agents orbitais × skills de persona

No core, o trabalho se encaminha por **autoridade**. As skills `aiox-*` no acervo espelham essas personas para runtimes que usam skills em vez de (ou além de) `@agent`.

| Agent (core) | Skill no acervo | Use quando | Não use para | Evidência típica |
|--------------|-----------------|------------|--------------|------------------|
| `@aiox-master` / Orion | `aiox-master` | Governança do framework, rota sem especialista claro | Fazer o trabalho do especialista | Rota / decisão de framework |
| `@analyst` | `aiox-analyst` | Pesquisa, discovery, brief | PRD final ou código | Fontes + síntese |
| `@pm` | `aiox-pm` | PRD, epic, estratégia de produto | Story pronta ou implementação | PRD/epic |
| `@architect` | `aiox-architect` | Arquitetura, stack, ADRs | Pesquisa de mercado | Decisão arquitetural |
| `@ux-design-expert` | `aiox-ux-designer` | UX, fluxos, UI de build | Backend geral | Fluxo / spec UI |
| `@data-engineer` | `aiox-data-engineer` | Schema, RLS, migrações | Arquitetura inteira do app | Schema/migração |
| `@sm` | `aiox-sm` | Story draft, critérios, branch local | PRD ou push | Story validável |
| `@po` | `aiox-po` | Prioridade, validar draft, fechar | Implementar | Veredito / transição |
| `@dev` | `aiox-dev` | Implementar, depurar, testar | Criar story ou deploy remoto | Código + testes |
| `@qa` | `aiox-qa` | Gate de qualidade, NFR, riscos | Implementar a correção | Findings + veredito |
| `@devops` | `aiox-devops` | Push, PR, release, CI remoto | Feature de produto | Gate pré-push / operação |
| (squad factory) | `squad-creator` / skill `aiox-sop` em domínio SOP | Criar/validar squad ou SOP | Dor coberta por squad publicado | Blueprint / pack |

**Superfície de ativação** muda ( `@dev` vs `$aiox-dev` vs prompt genérico). A **autoridade** não muda: dev não fecha Done; QA não implementa; devops não inventa regra de negócio.

Aula: [2.2 Escolher o agent certo](../aulas/02-sinais-e-contexto/2.2-escolher-o-agente-certo.md).

---

## 2. Skills do ciclo de story (SDC)

Ordem canônica de **uma** mudança:

```text
validate-story-draft
    → develop-story
    → review-story  (+ apply-qa-fixes em loop se necessário)
    → [deploy-story → verify-deploy]   se o projeto tem deploy
    → close-story                     # única que coloca Done
```

| Skill | Fase | Responsabilidade | Falha se… |
|-------|------|------------------|-----------|
| `validate-story-draft` | Draft → Ready | Critérios, clareza, anti-self-validation | Story vaga ou sem AC |
| `develop-story` | Ready → In progress | Código + testes locais; commits locais | “Pronto” sem teste |
| `review-story` | Review | Achados de qualidade (não self-approve eterno) | Ignorar CRITICAL |
| `apply-qa-fixes` | Review loop | Aplicar findings e devolver ao gate | Fechar sem re-review |
| `deploy-story` | Deploy | Publicar versão se configurado | Deploy sem autorização |
| `verify-deploy` | Verify | Provar valor no alvo (não só “subiu”) | Só health check vazio |
| `close-story` | Done | Gates de fechamento + log | Marcar Done sem evidência |
| `full-sdc` | Orquestração | Corre a cadeia de **uma** story com budget | Usar para 10 stories sem wave |

### Skills de apoio no mesmo arco

| Skill | Papel |
|-------|--------|
| `handoff` | Compactar estado para outro agent/sessão |
| `enhance-workflow` | Melhorar workflow já existente |
| `roundtable` | Várias lentes de revisão (não substitui QA gate) |
| `three-brain` | Motor diferente para review (no-self-review) |

Aula: [3.3 Ciclo da story na prática](../aulas/03-validacao-basica/3.3-ciclo-da-story-na-pratica.md).

---

## 3. Skills de roteamento e meta do acervo

| Skill | Papel no Fundamentals |
|-------|------------------------|
| `aiox-squads` | Escolher entre os 24 squads **depois** de saber que precisa de pacote multi-agente |
| `aiox-brain` | Estudar o acervo (não executar produto do cliente) |

Task vs skill vs workflow vs squad: [2.3](../aulas/02-sinais-e-contexto/2.3-task-skill-workflow-ou-squad.md).

---

## 4. O que **não** é “core Fundamentals”

| Família | Onde estudar |
|---------|----------------|
| 24 squads de domínio | `cursos/AIOX-Advanced-Squads/` |
| Design system / DESIGN.md | `cursos/AIOX-Design/` |
| Oferta / monetização | `cursos/AIOX-Productizacao/` |
| Vault Obsidian | `cursos/Obsidian-IA/` |
| Research profundo / runner / creator avançado | `cursos/AIOX-Agent-Engineering/` |

---

## 5. Como ativar (sem inventar runtime)

1. Confirme se a skill existe em `skills/<id>/SKILL.md` neste acervo.  
2. Copie para o harness do **projeto** (ex. `.claude/skills/` ou o path que o runtime usa).  
3. Só use `$nome` / `/comando` se o runtime **registrar** a superfície.  
4. Senão: abra o `SKILL.md` e execute o procedimento como prompt/checklist.  
5. Consulte `catalog.json` → `skill_meta.<id>.maturity`.

---

## 6. Exercício de síntese (Fundamentals)

Pegue uma missão real e preencha:

```text
Missão:
Agent/skill de persona:
Skills de SDC na ordem:
Precisa de squad? (sim/não + id):
Evidência de Done:
```

Sem squad se skill + agent bastarem. Sem `full-sdc` se a story ainda está Draft.

[Voltar ao README do curso](../README.md) · inventário do acervo: `cursos/MAPA-SKILLS.md`
