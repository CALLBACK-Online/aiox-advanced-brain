# Configuração Obsidian — aiox-advanced-brain

Personalização versionada do vault na raiz do repositório.

| Arquivo | Função |
|---------|--------|
| `appearance.json` | Tema padrão do Obsidian + snippet de pastas |
| `graph.json` | Color groups ativos no Graph |
| `graph.aiox-brain.json` | **Cópia canônica** do Graph — restaure se o Obsidian sobrescrever |
| `snippets/aiox-brain-folders.css` | Cores no explorador de pastas |
| `app.json` | Notas novas → `_notas-pessoais/inbox` |

O arquivo de estado local da interface do Obsidian **não** é versionado.

## Restaurar cores do Graph

Se o Graph voltar cinza:

```bash
cp .obsidian/graph.aiox-brain.json .obsidian/graph.json
```

Feche e reabra o Graph no Obsidian (ou recarregue o app).

## Vault root

Abra a **raiz do repositório** como vault para ver cursos + skills + squads no mesmo grafo.
