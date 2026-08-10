---
tags: [hub, aiox-brain, home, layer/curso]
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
cp .obsidian/graph.LOCKED.json .obsidian/graph.json
# ou: cp .obsidian/graph.aiox-brain.json .obsidian/graph.json
```

O Graph **esconde** `tasks/`, `agents/`, `workflows/` (milhares de arquivos internos dos squads).
Assim só entra a camada de conhecimento: cursos, READMEs, entradas, skills, notas.


## Entradas

- [[JORNADA-AIOX|Fundamentals, Advanced ou Enterprise?]]
- [[cursos/README|Hub de trilhas]]
- [[cursos/COMO-ESTUDAR|Como estudar · trilhas por caso]]
- [[cursos/MOC-Acervo-AIOX|MOC · Acervo]]
- [[cursos/MOC-Skills|MOC · Skills]]
- [[cursos/MAPA-SKILLS|MAPA-SKILLS · inventário e anti-duplicação]]
- [[cursos/MOC-Squads|MOC · Squads]]
- [[cursos/AIOX Advanced/MOC-Todas-Aulas|MOC · Todas as aulas (método)]]
- [[cursos/entradas/README|entradas skill/squad]]
- [[cursos/Obsidian-IA/README|Mini-curso Obsidian + IA]]
- [[cursos/Introducao-a-Arquitetura-de-Sistemas/README|Introdução à Arquitetura de Sistemas]]
- [[cursos/AIOX-Fundamentals/README|AIOX Fundamentals — Core básico]]
- [[cursos/AIOX Advanced/README|AIOX Advanced (método)]]

### Rotas de aplicação depois do Advanced

- [[cursos/AIOX-Advanced-Squads/README|AIOX Advanced Squads]]
- [[cursos/AIOX-Agent-Engineering/README|AIOX Agent Engineering]]
- [[cursos/AIOX-Design/README|AIOX Design (contrato visual / DS)]]
- [[cursos/AIOX-Productizacao/README|AIOX Productização (oferta / mercado)]]
- [[cursos/MOC-Agent-Engineering-vs-Productizacao|MOC · AE × Productização]]

### Continuidade

- [[cursos/AIOX-Enterprise/README|AIOX Enterprise — Visão Operacional e Prontidão]]

### Apoio do vault

- [[notas/README|notas — anotações dos alunos]]
- [[AGENTS|Contrato dos agents]]
- [[README|README do repositório]]

## Jornada de aprendizagem

1. [[cursos/Obsidian-IA/README|Obsidian + IA]] — estudar o acervo.
2. [[cursos/Introducao-a-Arquitetura-de-Sistemas/README|Introdução à Arquitetura de Sistemas]] — entender sistemas.
3. [[cursos/AIOX-Fundamentals/README|AIOX Fundamentals]] — instalar e operar o Core.
4. [[cursos/AIOX Advanced/README|AIOX Advanced]] — aplicar o método.

Arquitetura e AIOX Fundamentals são etapas diferentes: linguagem técnica universal primeiro; framework AIOX depois.

Depois do Advanced, escolha a rota pelo resultado: [[cursos/AIOX-Advanced-Squads/README|Squads]] para especialistas publicados, [[cursos/AIOX-Agent-Engineering/README|Agent Engineering]] para capacidade própria, [[cursos/AIOX-Design/README|Design]] para sistema visual ou [[cursos/AIOX-Productizacao/README|Productização]] para mercado. As rotas podem ser combinadas; não formam uma fila obrigatória.

Depois do Advanced e de uma operação real, observe se sustentar a base virou o novo gargalo. Use [[cursos/AIOX-Enterprise/README|AIOX Enterprise — Visão Operacional e Prontidão]] para fazer esse diagnóstico.

## Loop

```text
Entrada: recuperar fontes → Captura/MOC → Context Brief → próxima trilha
Operação: Context Brief + asset → projeto real → validação → notas/retornos/
```

## Skills de vault

- [[skills/aiox-brain/SKILL|aiox-brain]]
- [[skills/obsidian-course-vault/SKILL|obsidian-course-vault]]
- [[skills/course-moc/SKILL|course-moc]]
- [[skills/study-capture/SKILL|study-capture]]
- [[skills/aiox-squads/SKILL|aiox-squads]]

## Pontes skill (Graph)

Notas leves em `cursos/entradas/skill-*.md` (tag `#layer/skill`) ligam skill ↔ squad ↔ aula **sem** poluir o `SKILL.md` de runtime.

## Captura

Novas notas do Obsidian → `notas/inbox/`.
Não reescreva aulas em `cursos/`.

## Cores sumiram no Graph?

O Obsidian **apaga os grupos de cor** se você editar o painel ou se a aba Graph sobrescrever o arquivo.

```bash
# 1) Feche a aba Graph no Obsidian
# 2) No terminal, na raiz do repo:
bash .obsidian/RESTORE-GRAPH.sh
# 3) Reabra o Graph
```

Confira em **Grupos**: `path:skills` (verde), `path:squads` (laranja), `path:notas` (âmbar), `path:cursos/...` (azul/roxo), `tag:#hub` (rosa).
