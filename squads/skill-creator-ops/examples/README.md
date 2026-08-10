# Skill-Creator-Ops Squad — Production Examples

Outputs do squad `skill-creator-ops` são skills instaladas em `skills/` — governam lifecycle completo de skills.

## Onde os outputs reais vivem

| Tipo | Localização |
|---|---|
| Skills instaladas | `skills/` |
| Skill registry | `skills/skill-registry.yaml` |
| Validation reports (pontuais) | Gerados sob demanda |
| Golden input/output tests | `skills/{skill}/tests/` quando aplicável |

## Evidência de uso

- 80+ skills instaladas e ativas em `skills/`
- Skill lifecycle (init → develop → validate → test → package) executado em produção
- Registry governance check integrado em pre-push
- Phase 5 AIOX Skills Compliance Roadmap implementado

## Tasks canônicas

- Skill creation (via `skill-creator`)
- Skill validation (`validate-skill`)
- Skill testing (golden inputs/outputs pattern)
- Skill packaging e distribution

## Provenance

Outputs vivem em `skills/` (skills ativas) e `skills/skill-registry.yaml` (registry canônico). Todas as skills listadas no registry foram processadas por este squad.
