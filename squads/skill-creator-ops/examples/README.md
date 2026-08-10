# Skill-Creator-Ops Squad — Production Examples

Outputs do squad `skill-creator-ops` são skills instaladas em `.claude/skills/` — governam lifecycle completo de skills.

## Onde os outputs reais vivem

| Tipo | Localização |
|---|---|
| Skills instaladas | `.claude/skills/` |
| Skill registry | `.claude/skills/skill-registry.yaml` |
| Validation reports (pontuais) | Gerados sob demanda |
| Golden input/output tests | `.claude/skills/{skill}/tests/` quando aplicável |

## Evidência de uso

- 80+ skills instaladas e ativas em `.claude/skills/`
- Skill lifecycle (init → develop → validate → test → package) executado em produção
- Registry governance check integrado em pre-push
- Phase 5 SINKRA Skills Compliance Roadmap implementado

## Tasks canônicas

- Skill creation (via `skill-creator`)
- Skill validation (`validate-skill`)
- Skill testing (golden inputs/outputs pattern)
- Skill packaging e distribution

## Provenance

Outputs vivem em `.claude/skills/` (skills ativas) e `.claude/skills/skill-registry.yaml` (registry canônico). Todas as skills listadas no registry foram processadas por este squad.
