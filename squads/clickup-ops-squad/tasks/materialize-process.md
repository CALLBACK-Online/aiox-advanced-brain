# Task: Materialize Process

## Metadata

```yaml
task: materialize-process
atomic_layer: Organism
responsavel_type: Agent
agent: clickup-chief (orchestration) + materializer (execution)
accountable: "{spoke-owner}"
```

## Description

Materializar um processo completo mapeado pelo AIOX no ClickUp.
Segue Receita 1 de `clickup-composition-rules.yaml` (11 steps).

## Entrada

- `aiox_composition` — YAML com hierarquia completa (Instance→Token)
- `domain` — Domínio de negócio
- `owner_squad` — Squad responsável

## Saída

- Folder criada no Space correto
- Lists criadas dentro da Folder
- Custom Fields configurados nas Lists
- Views padrão configuradas
- Automações criadas (se especificadas)
- `clickup-tokenization.yaml` atualizado
- Relatório de materialização (YAML)

## Pre-Conditions

- [ ] Composição AIOX validada (pre-materialization checklist)
- [ ] APIs necessárias implementadas (Wave 1 gaps resolvidos)
- [ ] CSO enforcement passou

## Post-Conditions

- [ ] Todas entidades existem no ClickUp (verificado via API)
- [ ] Tokenization atualizado com novos IDs
- [ ] Post-materialization checklist passou

## Performance

- SLA: 30 minutos para processo simples, 2 horas com Playwright
- Escalação: Se API falhar 3x → escalar para @devops
- Erro: Rollback não automático — documentar o que foi criado para cleanup manual
