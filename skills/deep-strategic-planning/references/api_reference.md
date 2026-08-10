# Deep Strategic Planning — Integration Notes

> Reescrito 2026-07-06 (doc-rot): a versão anterior referenciava `squads/multi-lens-framework/`
> e comandos `/lens *...` que NÃO existem neste repo — executores obedientes à rule
> `skill-execution.md` tentavam invocar um squad fantasma.

## Dependências reais

**Nenhuma dependência externa.** A skill é autocontida:

- Lentes: `{SKILL_DIR}/references/lens-catalog.md` (as 12 definições completas)
- Scoring: `{SKILL_DIR}/references/scoring-methodology.md` (bases, ajustes, caps, tie-break)
- Pipeline: `{SKILL_DIR}/SKILL.md` (fases 0-6, vetos, protocolo de resiliência)

## Integrações opcionais (existentes no repo)

| Integração | Quando | Como |
|---|---|---|
| `--multi-vendor` (Phase 3) | Decisões de alto valor | Clusters por vendor via `cli-handoff`/`cli-router` |
| `/roundtable --mode decision` | Validar o dossiê ANTES de executar o plano | O 04-synthesis + 05-action-plan são o input |
| `/schedule` | Agendar a Phase 6 (re-bench) no `review_at` | Lembrete com o path do predictions.yaml |
| policy/ (EPIC-186) | Heurísticas embutidas como mecanismo | Ver tabela "Heurísticas Embutidas" no SKILL.md |

## Limitações

1. **Intensivo em tokens** — análise completa (12 lentes × 10 futuros) é extensa; use `--tier quick` para decisões médias.
2. **Requer contexto** — decisões sem contexto suficiente geram cenários genéricos.
3. **Não substitui julgamento** — scores são opinião estruturada, não medição; o output é suporte à decisão humana.
4. **Viés de disponibilidade** — cenários limitados pela criatividade do momento; o Red Team (Phase 1) mitiga, não elimina.

## Quando NÃO usar

- Decisões triviais ou facilmente reversíveis (just do it)
- Urgência extrema (sem tempo para o pipeline; anote a decisão e o racional em 5 linhas)
- Informação insuficiente (primeiro coletar dados — a matriz não conserta input vazio)
- Decisão já tomada em dossiê anterior (Phase 0 prior-art detecta — aponte o dossiê)
