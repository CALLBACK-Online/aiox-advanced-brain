# Checklist — improve-course

- [ ] Baseline verde antes da melhoria.
- [ ] Preferir `skills/teach/SKILL.md`; usar `didactic-rubric.md` apenas como fallback.
- [ ] Gerar `didactic-audit.md` com `audit_didactics.py --write`.
- [ ] Resolver `PENDING` por revisão humana; registrar evidência concreta.
- [ ] Priorizar falhas sistemáticas por impacto × esforço.
- [ ] Editar 3–4 aulas ou um módulo por lote.
- [ ] Não mover/renomear sem atualizar harness, catálogo, navegação e contadores.
- [ ] Validar o curso entre lotes.
- [ ] `audit_didactics.py --check ...` sem `FAIL`/`PENDING`.
- [ ] `npm run validate` EXIT 0 e evidência no ledger.
- [ ] `retrospective.md` no bastidor se a rodada mudou padrões reutilizáveis.
