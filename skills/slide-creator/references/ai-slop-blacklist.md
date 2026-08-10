# AI Slop Blacklist — Reference

> **SoT:** `squads/slides-creator/data/ai-slop-blacklist-2026.md` (canonical, 2026 edition).
> **Cross-reference:** `.claude/rules/design-absolute-bans.md` (cross-fit consolidation 2026-05-19).
> Este arquivo é um link/synopsis. A blacklist completa vive no squad e é mantida ali. Use isto para entender o que a skill REJEITA antes de chamar o blacklist real.

## Por que existe

LLMs tendem a gerar slides com características AI-fingerprint detectáveis (genéricas, óbvias, estilo "todo deck que vi nas últimas 100 gerações"). A blacklist é o **gate pre-publish** que recusa estes padrões.

Quando `ai_slop_score > 60`, a skill EMITE warning + recomenda rebrief. Quando > 80, hard-block.

## Categorias de pattern rejeitado (sumário)

### 1. Generic names (Jane Doe effect)
- John Doe, Jane Doe, Sarah Chen, Sarah Chan, Jack Su, Test User, Lorem User
- **Substituir por:** nomes reais do briefing OU placeholder `[TODO: nome de {source}]`

### 2. Fake/lazy numbers
- 99.99%, 50%, 100% (números "redondos" suspeitos)
- 1234567 (sequenciais), 555-1234 (placeholder phone)
- $1,000,000 (round), $99.99
- **Substituir por:** valores orgânicos do briefing — `47.2%`, `+1 (312) 847-1928`, `$1,247,892`

### 3. Startup-slop names
- Acme, Acme Corp, Nexus, SmartFlow, FlowSync, DataSync
- ExampleCo, TestCo, StartupCo
- TechFlow, CloudSync, AISync
- **Substituir por:** nome real do cliente OU `[TODO: empresa do briefing]`

### 4. Filler verbs/adjectives (LLM clichés)
- Elevate, Unlock, Unleash, Seamless, Next-Gen, Best-in-class
- Revolutionary, Disruptive, Cutting-edge, State-of-the-art
- Empower, Transform (como filler), Streamline
- Game-changing, Industry-leading, World-class
- **Substituir por:** verbos concretos do domínio do cliente

### 5. Placeholder images
- placeholder.jpg, via.placeholder.com, unsplash.com/random
- SVG "egg" avatars, Lucide user icon como profile pic
- **Substituir por:** `picsum.photos/seed/{stable-string}/800/600` ou branded SVG avatars

### 6. Lorem ipsum
- `Lorem ipsum dolor sit amet, ...`
- **Substituir por:** texto real do briefing OU `[TODO: copy from {source}]`

### 7. AI-writing tells
- Em dashes `—` ou `--` (uso excessivo)
- "It's worth noting that...", "It's important to understand...", "Let's dive into..."
- **Substituir por:** vírgulas, dois-pontos, ponto-vírgulas, parênteses; remova prefácios genéricos

## Como a skill enforce

1. **Phase 8 (deck spec):** Para cada slide content, run check contra cada categoria.
2. **Phase 9 (key-slide gate):** Hard-fail no key-slide se qualquer banned pattern detectado.
3. **Phase 10 (critique):** Computa `ai_slop_score` 0-100. Score > 60 → revisão obrigatória.
4. **QA report (Phase 11):** Inclui `ai_fingerprint_score` no final report.

## Threshold actions

| Score | Action |
|-------|--------|
| 0-20 | pass |
| 21-40 | warn (cosmetic flag) |
| 41-60 | review (manual gate — human ack required) |
| 61-80 | block (rebrief required before re-emission) |
| 81-100 | hard-block (full rebrief, do not deliver) |

## Cross-fit absorption history

- **2026-05-19:** Cross-fit de impeccable.style v3.1.1 (8 absolute bans) + tasteskill.dev v2 (Jane Doe Effect). Resultado: `.claude/rules/design-absolute-bans.md`.
- **2026 edition (squad SoT):** Curated by slide-chief. Inclui patterns observados em runs reais.

## Skill enforcement consumer

- `templates/qa/visual-gates.yaml#jane_doe_gate`
- `templates/qa/visual-gates.yaml#eight_bans_gate`
- `templates/qa/visual-gates.yaml#ai_slop_score_gate`
- `scripts/validate_design_100_runtime.py` (computes composite score)

## Resync

Mudanças canônicas DEVEM ser feitas em `squads/slides-creator/data/ai-slop-blacklist-2026.md` e propagadas para este arquivo + `.claude/rules/design-absolute-bans.md`. Última sync: 2026-05-20.
