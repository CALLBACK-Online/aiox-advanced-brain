# Checklist — improve-course

- [ ] Baseline verde antes da melhoria.
- [ ] Preferir `skills/teach/SKILL.md`; usar `didactic-rubric.md` apenas como fallback.
- [ ] **Lente Obsidian (links):** `python3 scripts/audit_vault_links.py --course <id> --write`
      → `docs/producao-cursos/<id>/vault-links.md` (wikilinks por stem, md quebrados, órfãos).
      Skill de leitura: `skills/obsidian-course-vault/SKILL.md` (vault root = repo ou pasta do curso).
- [ ] Gerar `didactic-audit.md` com `audit_didactics.py --write`.
- [ ] Resolver `PENDING` por revisão humana; registrar evidência concreta.
- [ ] Priorizar falhas sistemáticas por impacto × esforço (incl. wikilinks vermelhos no Graph).
- [ ] Editar 3–4 aulas ou um módulo por lote.
- [ ] Não mover/renomear sem atualizar harness, catálogo, navegação e contadores.
- [ ] Validar o curso entre lotes.
- [ ] `audit_didactics.py --check ...` sem `FAIL`/`PENDING`.
- [ ] Re-rodar `audit_vault_links.py --course <id>` se a rodada tocou links/nav.
- [ ] `npm run validate` EXIT 0 e evidência no ledger.
- [ ] `retrospective.md` no bastidor se a rodada mudou padrões reutilizáveis.
