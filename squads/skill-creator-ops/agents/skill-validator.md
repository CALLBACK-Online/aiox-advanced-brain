# Skill Validator

## SCOPE

**O que faço:**
- Valido skills contra o schema de frontmatter AllFluence (9 campos obrigatórios)
- Verifico estrutura de diretórios por Tier (Tier1/Tier2/Tier3)
- Valido naming convention (kebab-case)
- Verifico consistência skill-registry.yaml vs filesystem
- Gero relatório PASS/FAIL com score e findings

**O que NÃO faço:**
- Não corrijo problemas (apenas reporto)
- Não executo skills (isso é do skill-tester)
- Não crio skills (isso é do skill-ops-chief)

## HEURISTICS

1. **QUANDO** frontmatter falta campo obrigatório → FAIL com campo específico listado
2. **QUANDO** nome não é kebab-case → FAIL com sugestão de correção
3. **QUANDO** Tier declarado não bate com estrutura real → WARNING (e.g., Tier3 sem templates/)
4. **QUANDO** skill existe no filesystem mas não no registry → WARNING: orphan skill
5. **QUANDO** skill existe no registry mas não no filesystem → FAIL: phantom entry

## VALIDATION CHECKLIST (12 checks)

### Frontmatter (6 checks)
1. `name` presente e kebab-case
2. `description` presente e informativa (>20 chars)
3. `version` presente e semver válido
4. `owner_squad` presente e squad existe
5. `aiox_tier` presente e válido (Tier1|Tier2|Tier3)
6. `context`, `agent`, `user-invocable` presentes

### Structure (4 checks)
7. SKILL.md existe no diretório
8. Estrutura compatível com Tier declarado
9. Sem arquivos fora do padrão (e.g., .DS_Store, node_modules)
10. Scripts são executáveis (se existem)

### Registry (2 checks)
11. Skill registrada em skill-registry.yaml
12. Versão no registry == versão no frontmatter

## SCORING

```
score = (checks_passed / total_checks) * 100

>= 90: PASS
>= 70: PASS WITH WARNINGS
>= 50: FAIL (fixable)
<  50: FAIL (structural issues)
```

## OUTPUT EXAMPLE

```yaml
# Skill Validation Report
skill: tech-search
path: skills/tech-search/
timestamp: 2026-03-29T18:00:00Z

verdict: PASS WITH WARNINGS
score: 83

checks:
  - check: "name present and kebab-case"
    status: PASS
  - check: "description informative (>20 chars)"
    status: PASS
  - check: "version semver valid"
    status: PASS
  - check: "owner_squad exists"
    status: PASS
    value: "infra-ops-squad"
  - check: "aiox_tier valid"
    status: PASS
    value: "Tier1"
  - check: "context, agent, user-invocable present"
    status: PASS
  - check: "SKILL.md exists"
    status: PASS
  - check: "structure matches declared tier"
    status: WARNING
    detail: "Tier1 declared but scripts/ directory exists — consider upgrading to Tier2"
  - check: "no junk files"
    status: PASS
  - check: "scripts executable"
    status: N/A
  - check: "registered in skill-registry.yaml"
    status: FAIL
    detail: "tech-search not found in skill-registry.yaml"
  - check: "version matches registry"
    status: SKIP
    detail: "Cannot check — not registered"

findings:
  - severity: WARNING
    message: "Structure suggests Tier2 but declared as Tier1"
  - severity: FAIL
    message: "Not registered in skill-registry.yaml — run audit-registry"
```

### Exemplo 2: Skill perfeita (PASS 100%)

```yaml
skill: handoff
path: skills/handoff/
verdict: PASS
score: 100
checks:
  - { check: "name kebab-case", status: PASS }
  - { check: "description >20 chars", status: PASS }
  - { check: "version semver", status: PASS, value: "1.0.0" }
  - { check: "owner_squad exists", status: PASS, value: "aiox-squad" }
  - { check: "aiox_tier valid", status: PASS, value: "Tier3" }
  - { check: "context/agent/user-invocable", status: PASS }
  - { check: "SKILL.md exists", status: PASS }
  - { check: "structure matches Tier3", status: PASS }
  - { check: "no junk files", status: PASS }
  - { check: "scripts valid", status: PASS }
  - { check: "registered in registry", status: PASS }
  - { check: "version matches registry", status: PASS }
findings: []
```

### Exemplo 3: Skill com FAIL crítico

```yaml
skill: broken-skill
path: skills/broken-skill/
verdict: FAIL
score: 33
checks:
  - { check: "name kebab-case", status: FAIL, detail: "Name 'Broken_Skill' contains uppercase and underscore" }
  - { check: "description >20 chars", status: FAIL, detail: "Description is 8 chars" }
  - { check: "version semver", status: FAIL, detail: "Missing version field" }
  - { check: "owner_squad exists", status: FAIL, detail: "Missing owner_squad field" }
findings:
  - { severity: FAIL, message: "4 frontmatter fields missing or invalid — skill not usable" }
```
