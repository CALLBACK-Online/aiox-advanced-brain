# Checklist — bootstrap de acervo

- [ ] Destino confirmado (repo vazio ou path novo)
- [ ] `bootstrap_library.py --dest …` executado
- [ ] `AGENTS.md`, `CLAUDE.md`, `README.md`, `catalog.json`, `package.json` presentes
- [ ] `cursos/README.md` + `dev/validate.py` + surface check
- [ ] `.gitignore` ignora `/docs/`, `.claude/`, `.agents/`, `notas/**` (exceto README)
- [ ] `docs/producao-cursos/README.md` existe (bastidor local)
- [ ] `npm run validate` ou `python3 dev/validate.py` PASS
- [ ] Ops instalado no runtime se o time for operar daqui: `scripts/install.sh`
- [ ] Próximo passo: create-course do primeiro curso real
