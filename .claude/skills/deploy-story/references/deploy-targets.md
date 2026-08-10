# Deploy Targets — Pointer

> All deploy target configuration lives in `infrastructure/infrastructure-map.json` → `deploy_targets[]`.
> This file is a pointer only. Do NOT add operational data here.

## Where to find deploy target data

- **SOT:** `infrastructure/infrastructure-map.json` → `deploy_targets[]`
- **Schema reference:** `infrastructure/schemas/deploy-targets-schema.md`

## How to add a new deploy target

1. Add a new entry to `deploy_targets[]` in `infrastructure/infrastructure-map.json`
2. Populate: `id`, `type`, `file_patterns[]`, `deploy_commands[]`, `health_endpoint`, `rollback_command`, `env_required[]`
3. Zero skill changes required — `/deploy-story` reads the registry dynamically

## How to modify an existing deploy target

Edit the relevant entry in `infrastructure/infrastructure-map.json`. No skill changes needed.
