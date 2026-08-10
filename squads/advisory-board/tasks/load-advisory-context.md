# Load Advisory Context Task

Task de preload determinístico do `advisory-board` para continuidade de sessão sem depender de memória implícita.

## Metadata

```yaml
task:
  name: Load Advisory Context
  id: load-advisory-context
  version: "1.0.0"
  category: research
  estimated_time: "2-5 min"
  dependencies:
    - .aiox/advisory-board/alan-nicolas-profile.yaml
    - docs/advisory/
    - squads/advisory-board/scripts/resolve-advisory-context.cjs
  outputs:
    - outputs/advisory-board/context/advisory-context-brief.json
```

---

## Objective

Garantir que o board carregue o profile persistente do founder e a ata mais recente antes de aconselhar, sintetizar ou retomar decisões pendentes.

---

## Resolution Order

1. Executar `node squads/advisory-board/scripts/resolve-advisory-context.cjs --format=json`.
2. Se `profile_path` existir:
   - ler `.aiox/advisory-board/alan-nicolas-profile.yaml`
   - extrair hierarquia operacional, padrões de decisão, blind spots, regras de aconselhamento e sessões anteriores
3. Se `latest_session_path` existir:
   - ler a ata mais recente em `docs/advisory/`
   - extrair decisões pendentes, tensões abertas, owners e follow-ups
4. Se um dos artefatos faltar:
   - registrar exatamente o path ausente
   - continuar sem inventar continuidade
   - explicitar se a sessão está em modo `fresh_session_only`

---

## Phase 1: Resolve Local Continuity Sources

1. Rodar o resolvedor.
2. Registrar:
   - `status`
   - `profile_path`
   - `latest_session_path`
   - `missing_paths`
   - `continuity_mode`

---

## Phase 2: Founder Profile Snapshot

Se `profile_path` existir:

1. Carregar o profile persistente.
2. Extrair no mínimo:
   - `identity.track_record`
   - `operating_hierarchy.order`
   - `decision_patterns`
   - `relationship_with_money`
   - `zone_of_genius`
   - `blind_spots`
   - `board_notes.how_to_advise`

Se não existir:

1. Registrar `founder_profile.status: missing`
2. Não inferir traços além do que o usuário disser na sessão atual.

---

## Phase 3: Latest Session Snapshot

Se `latest_session_path` existir:

1. Ler a ata mais recente em `docs/advisory/`.
2. Extrair no mínimo:
   - tema da sessão
   - recomendações centrais
   - decisões pendentes
   - action items
   - follow-up esperado

Se não existir:

1. Registrar `latest_session.status: missing`
2. Operar como sessão nova.

---

## Output Contract

Salvar `outputs/advisory-board/context/advisory-context-brief.json` com:

```json
{
  "advisory_context_brief": {
    "generated_at": "YYYY-MM-DDTHH:mm:ssZ",
    "status": "ready|partial|missing",
    "continuity_mode": "resume_available|fresh_session_only",
    "profile_path": ".aiox/advisory-board/alan-nicolas-profile.yaml",
    "latest_session_path": "docs/advisory/2026-03-10-....md",
    "missing_paths": [],
    "founder_profile": {
      "track_record": "",
      "operating_hierarchy": [],
      "decision_patterns": [],
      "how_to_advise": []
    },
    "latest_session": {
      "open_decisions": [],
      "action_items": [],
      "follow_up": []
    }
  }
}
```

---

## Quality Checklist

- [ ] Rodou o resolvedor determinístico.
- [ ] Leu o profile persistente quando disponível.
- [ ] Leu a ata mais recente quando disponível.
- [ ] Registrou paths ausentes sem inventar contexto.
- [ ] Explicitou `resume_available` vs `fresh_session_only`.

---

## Fallback

Se ambos os artefatos estiverem ausentes:

1. Operar em `fresh_session_only`.
2. Dizer explicitamente que o board está sem memória persistida local.
3. Não fingir continuidade nem inventar decisões anteriores.
