# Brand Squad — Production Examples

Outputs do squad `brand` são artefatos canônicos de marca que vivem no workspace, não no filesystem do squad.

## Onde os outputs reais vivem

| Tipo | Localização canônica |
|---|---|
| Brand platform (naming, positioning, tagline) | `workspace/businesses/{biz}/L2-tactical/brand/` |
| Brand assets (logos, identidade visual) | `workspace/businesses/{biz}/L2-tactical/brand/assets/` |
| Campaign briefs que usam brand | `workspace/businesses/{biz}/L4-operational/campaigns/{slug}/brand/` |

## Evidência de uso

O squad foi executado para múltiplas BUs (aiox, casting, your-business) — artefatos de marca estão commitados nos diretórios canônicos do workspace. Ver `workspace/businesses/*/L2-tactical/brand/` para evidência atual.

## Templates canônicos

- `squads/brand/templates/` — templates usados em cada execução
- `docs/schemas/campaign-brief-schema.yaml` — schema ADR-012 para cross-squad brand briefs

## Provenance

Outputs são artefatos canônicos sob governança do Document Registry, lifecycle PLACEHOLDER → POPULATED → VALIDATED → APPROVED. Não copiados aqui porque são específicos de cada BU e vivem no workspace.
