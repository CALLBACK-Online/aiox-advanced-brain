---
tags: [hub, aiox-brain, home]
aliases: [Home, Início, AIOX Brain Home]
---

# AIOX Advanced Brain — Home

> Dashboard do vault. Pastas no padrão minúsculo: `cursos/` · `skills/` · `squads/` · `notas/`.

## Pastas

| Pasta | Cor no Graph | Conteúdo |
|-------|--------------|----------|
| `cursos/` | azul / roxo / ciano | Material canônico das trilhas |
| `skills/` | verde | Skills portáveis |
| `squads/` | laranja | Pacotes multi-agente |
| `notas/` | âmbar | **Suas** anotações sobre as aulas |
| `#hub` | rosa | Este Home + MOCs |

## Como ler o Graph

1. **Orphans off** (padrão neste vault) → some o anel de pontos soltos; sobra o miolo conectado.
2. Filtro de busca já exclui `.obsidian`, `scripts`, `docs`, yaml/json/css…
3. Auditoria (ver tudo): copie `.obsidian/graph.aiox-brain.audit.json` → `graph.json`.

**Tema:** padrão do Obsidian, com o snippet próprio `aiox-brain-folders` para destacar as pastas.

Se o Graph voltar cinza:

```bash
cp .obsidian/graph.aiox-brain.json .obsidian/graph.json
```

## Entradas

- [[cursos/README|Hub de trilhas]]
- [[cursos/MOC-Acervo-AIOX|MOC · Acervo]]
- [[cursos/MOC-Skills|MOC · Skills]]
- [[cursos/MOC-Squads|MOC · Squads]]
- [[cursos/Obsidian-IA/README|Mini-curso Obsidian + IA]]
- [[cursos/AIOX Advanced/README|AIOX Advanced (método)]]
- [[cursos/AIOX-Advanced-Squads/README|AIOX Advanced Squads]]
- [[notas/README|notas — anotações dos alunos]]
- [[AGENTS|Contrato dos agents]]
- [[README|README do repositório]]

## Loop

```text
Estudar (cursos/) → Anotar (notas/) → Skill/Squad → Projeto real → Evidência
```

## Skills de vault

- [[skills/aiox-brain/SKILL|aiox-brain]]
- [[skills/obsidian-course-vault/SKILL|obsidian-course-vault]]
- [[skills/course-moc/SKILL|course-moc]]
- [[skills/study-capture/SKILL|study-capture]]
- [[skills/aiox-squads/SKILL|aiox-squads]]

## Captura

Novas notas do Obsidian → `notas/inbox/`.
Não reescreva aulas em `cursos/`.
