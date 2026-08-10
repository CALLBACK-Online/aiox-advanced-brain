# AIOX Advanced — Skills e Squads

Biblioteca local criada a partir das skills e squads citados nos grupos AIOX Advanced e encontrados no `sinkra-hub`.

## Conteúdo

- **43 skills** em `.claude/skills/`.
- **25 squads** em `squads/`.
- Inventário das conversas em `docs/whatsapp-inventory.md`.
- Resultado do cruzamento em `docs/search-results.md`.
- Proveniência e regras de atualização em `docs/source-and-update-policy.md`.

## Estrutura

```text
.
├── .claude/skills/       # Skills canônicas
├── squads/               # Squads canônicos e sucessores atuais
├── docs/                 # Inventário, cruzamento e limitações
├── scripts/              # Validação local
├── catalog.json          # Manifesto legível por máquina
└── package.json
```

## Escopo da seleção

A seleção contém:

1. correspondências exatas entre os nomes mencionados e o `sinkra-hub`;
2. sucessores documentados, como `research`, que absorveu `spy`, `deep-research` e `tech-research`;
3. renomes atuais `aios-*` → `aiox-*`;
4. pacotes relacionados de alta confiança, como `sales` para `sales-squad` e `clickup-ops-squad` para `project-management-clickup`.

Arquivos em `_archive`, `outputs`, `artifacts`, `.state`, `.synapse`, `__pycache__`, `node_modules`, `.env`, configurações `*.local.yaml` e diretórios `source-text` foram excluídos. Isso evita distribuir lixo de runtime, infraestrutura local, credenciais e fontes integrais potencialmente protegidas por direitos autorais.

## Uso

Esta é uma biblioteca-fonte. Algumas skills e squads esperam o runtime completo AIOX/SINKRA e podem referenciar `.aiox-core`, `workspace`, apps ou scripts que não pertencem a este recorte. Consulte `docs/runtime-dependencies.md` antes de tentar executá-los isoladamente.

Validação:

```bash
npm run validate
```

## Estado Git

O repositório é local e privado por padrão. Nenhum remoto é configurado automaticamente e nenhuma licença de redistribuição é presumida.
