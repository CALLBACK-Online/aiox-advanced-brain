# Post-Materialization Checklist

Validação OBRIGATÓRIA após materialização.
Se qualquer item falhar → **WARN** (fix cycle).

## Structure Verification

- [ ] Folder existe com nome correto no Space correto
- [ ] Todas Lists existem dentro da Folder
- [ ] Custom Fields existem nas Lists (verificar via API GET)
- [ ] Shared fields reutilizados (não duplicados)

## Configuration Verification

- [ ] Views padrão configuradas (Board, Table, Calendar conforme tokens)
- [ ] Automações criadas e ativas (verificar via Playwright screenshot)
- [ ] Status workflow configurado conforme Organism state_machine

## Registry Update

- [ ] `clickup-tokenization.yaml` atualizado com todos novos IDs
- [ ] Novos Organisms registrados com IDs
- [ ] Novas Molecules registradas com IDs
- [ ] Novos Tokens registrados com IDs
- [ ] Statistics atualizadas
- [ ] Changelog entry adicionada

## Documentation

- [ ] Relatório de materialização gerado (YAML)
- [ ] Screenshots de automações criadas (se Playwright usado)
