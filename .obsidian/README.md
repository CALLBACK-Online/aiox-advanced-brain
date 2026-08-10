# Configuração Obsidian — aiox-advanced-brain

Pastas do vault (minúsculas): `cursos/` · `skills/` · `squads/` · `notas/`.

| Arquivo | Função |
|---------|--------|
| `appearance.json` | Tema padrão + snippet próprio de pastas |
| `graph.json` | Graph **limpo** (orphans off + cores) |
| `graph.aiox-brain.json` | Backup do Graph limpo |
| `graph.aiox-brain.audit.json` | Graph com orphans on (auditoria) |
| `snippets/aiox-brain-folders.css` | Cores no explorador |
| `app.json` | Novas notas → `notas/inbox` |

## Restaurar Graph limpo

```bash
cp .obsidian/graph.aiox-brain.json .obsidian/graph.json
```

## Auditoria (anel de órfãos)

```bash
cp .obsidian/graph.aiox-brain.audit.json .obsidian/graph.json
```

Abra a **raiz do repositório** como vault.
