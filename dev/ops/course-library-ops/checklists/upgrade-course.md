# Checklist — upgrade-course

- [ ] Curso, harness e catálogo inventariados; baseline registrado.
- [ ] Bastidor preservado ou preparado com `prepare_course.py --mode upgrade` (ou `--mode brownfield`).
- [ ] Brief/outline novos descrevem o delta, não apagam a história.
- [ ] `creation_mode: upgrade` no `course-spec.json`.
- [ ] `plan_upgrade.py --write` gerou inventário e ledger sem mutar o curso.
- [ ] Paths e `lesson_id` válidos marcados para preservação.
- [ ] `archive-candidate` recebeu decisão humana e destino recuperável.
- [ ] Brief e outline re-aprovados com identidade, data, artefato e escopo.
- [ ] `check_approvals.py` PASS.
- [ ] Plano regenerado com `--require-approved` antes da primeira edição.
- [ ] Apply assistido (explícito; **nunca** `rm`):
  - `apply_upgrade.py --add <lesson-id>` — stub novo
  - `apply_upgrade.py --archive <lesson-id>` — move para `archive/upgraded/<date>/`
- [ ] Edição em lote pequeno; cada linha registra gate, evidência e ação corretiva.
- [ ] `doctor.py --course <id>` (estado derivado).
- [ ] Harness, catálogo, módulos, navegação e contadores sincronizados.
- [ ] Validador do curso e `npm run validate` verdes.
