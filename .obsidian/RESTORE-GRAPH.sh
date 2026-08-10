#!/bin/bash
# Restaura cores + grafo limpo.
# IMPORTANTE: feche a aba "Visualização em gráfico" no Obsidian ANTES de rodar.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cp "$ROOT/.obsidian/graph.LOCKED.json" "$ROOT/.obsidian/graph.json"
cp "$ROOT/.obsidian/graph.LOCKED.json" "$ROOT/.obsidian/graph.aiox-brain.json"
echo "OK: cores restauradas ($(python3 -c "import json;print(len(json.load(open('$ROOT/.obsidian/graph.json'))['colorGroups']))") grupos)."
echo "1) Feche o Graph no Obsidian (se estiver aberto)"
echo "2) Rode este script"
echo "3) Reabra o Graph"
echo "4) Em Filtros: Órfãos = OFF | Etiquetas = ON"
echo "5) Em Grupos: deve listar path:skills, path:squads, tag:#hub, etc."
