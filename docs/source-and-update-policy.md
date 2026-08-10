# Proveniência e política de atualização

## Fonte

- Repositório: `sinkra-hub`
- Branch no momento da importação: `oalanicolas`
- Commit: `c2cd70b92cb68f49a6cb5256da2d5b7985b02c85`
- Data da importação: 10/08/2026
- Estado das pastas importadas: limpo no Git; mudanças existentes em outras áreas do `sinkra-hub` não foram copiadas.

## Regras da cópia

- Skills vieram de `.claude/skills/{nome}`.
- Squads vieram de `squads/{nome}`.
- A estrutura relativa foi preservada para manter o máximo possível de referências internas.
- Nenhum arquivo do `sinkra-hub` foi alterado.

## Exclusões deliberadas

- `_archive`: versões históricas e duplicadas.
- `outputs`, `artifacts`, `.state`: estado de execução e evidências temporárias.
- `node_modules`: dependências reinstaláveis.
- `__pycache__`, `*.pyc` e `.synapse`: caches e sessões locais.
- `.env` e variantes: credenciais/configuração local.
- `*.local.yaml`: configuração de infraestrutura local; exemplos `.example.yaml` permanecem.
- `source-text`: fontes integrais de livros e transcrições, potencialmente protegidas por direitos autorais.

## Atualizações futuras

Ao atualizar um asset:

1. confirmar o novo commit-fonte;
2. verificar se a pasta-fonte está limpa no Git;
3. reaplicar as exclusões;
4. atualizar `catalog.json` e `docs/search-results.md`;
5. executar `npm run validate`;
6. revisar o diff antes de qualquer commit.
