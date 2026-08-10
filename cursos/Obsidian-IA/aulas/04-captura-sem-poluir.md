---
type: lesson
course: obsidian-ia
course_title: Obsidian + IA
lesson_id: captura-sem-poluir
lesson_position: 4
title: "Captura sem poluir o canônico"
status: canonical
canonical_scope: cursos/Obsidian-IA
reading_minutes: 14
tags: [curso/obsidian-ia, segundo-cerebro]
maturity: study
---

# Captura sem poluir o canônico

[← Agent como professor](03-agent-como-professor.md) · [⌂ Curso](../README.md) · [→ MOCs e hubs](05-mocs-e-hubs.md)

## Resultado

Ao final desta aula você consegue **gravar um insight** em espaço pessoal (`notas/…`) ligado a uma aula canônica, sem editar o oficial.

## Quando usar — e quando não usar

**Use** depois de cada bloco de estudo de 25–50 minutos.

**Não** edite pastas canônicas (`aulas/`, `modulos/`, quizzes oficiais) para “ficar do seu jeito”.  
**Não** use captura para reescrever o curso “melhor” — isso é trabalho de maintainer (`skills/teach/`), não de aluno.

## Onde gravar

| Destino | Uso |
|---------|-----|
| `notas/inbox/` | Captura rápida (local, gitignored) |
| `notas/notes/` | Notas destiladas |
| `notas/cards/` | Progressive summary / revisão |
| `notas/retornos/` | Resultado e aprendizado devolvidos depois de uma execução |
| Vault pessoal | Depois de destilar, se quiser PARA/LYT da sua vida |

Skill: `study-capture` no repositório (`skills/study-capture/SKILL.md`). Layout canônico: `notas/README.md`.

## Tipos de nota (quando usar cada uma)

Não invente taxonomia de 20 pastas. Use **tipos** (inspirados em PKM clássico, adaptados a este acervo):

| Tipo | Onde | Quando |
|------|------|--------|
| **Inbox** | `notas/inbox/` | Durante a aula; rascunho sujo |
| **Atômica** | `notas/notes/` ou `notas/cards/` | Uma ideia reutilizável (1 ideia = 1 nota) |
| **Por aula** | `notas/aulas/` (opcional) | Espelho pessoal de uma aula canônica |
| **MOC** | `notas/MOCs/` | ≥5 conexões úteis ou dor recorrente (aula 05) |
| **Retorno** | `notas/retornos/` | Depois de executar no projeto / fechar ciclo |

Anti-padrão: uma “nota dump” eterna sem fonte. Sempre: **fonte → insight → próximo passo**.

## Pastas mínimas (não premature organization)

**Errado:** criar `Trabalho/Projetos/…/IA/Marketing/` com 5 notas.  
**Certo:** `inbox` → destilar → MOC só quando o tema puxar.

O canônico (`cursos/`) já tem a taxonomia do produto. Sua pasta pessoal **espelha captura**, não reorganiza o acervo.

## Template inbox (copie)

```markdown
# {título curto}
- fonte: path da aula canônica
- data: YYYY-MM-DD
- insight: 1–3 frases
- próximo passo: 1 ação
```

## Progressive summary (BASB-light)

1. Highlight — ideia bruta da aula
2. Suas palavras — o que muda no seu trabalho
3. Card — pergunta + resposta para revisar

Depois de operar no projeto, capture também **resultado → decisão → aprendizado reutilizável** em `notas/retornos/`. Esse retorno fecha o loop; log bruto de terminal não é memória.

## Tags e propriedades (leve)

Opcional — não bloqueie a captura por falta de YAML perfeito:

```markdown
---
type: study-note
source: "cursos/…/….md"
created: YYYY-MM-DD
tags: [estudo, aiox]
---
```

| Campo | Para quê |
|-------|----------|
| `source` | Proveniência (path relativo) |
| `type` | Filtrar inbox vs retorno vs card |
| `tags` | Poucos e estáveis (`estudo`, tema); não 30 tags por nota |

Frontmatter rico e plugins de properties ficam para o curso de **produto** Obsidian. Aqui basta **fonte + insight + próximo passo**.

## O que **não** capturar

- Transcrição integral da aula ou de livro
- Secrets, tokens, dumps de terminal
- Paths absolutos de máquina (`/Users/…`)
- “Melhoria” disfarçada do arquivo canônico
- Logs completos do agent (destile decisão + evidência)

## Fluxo pós-sessão (10 minutos)

```text
1. Inbox sujo (durante)
2. Destilar 1 atômica ou card (após)
3. Se ≥5 conexões no tema → MOC (aula 05)
4. Se missão operacional nasceu → rascunho de Context Brief (aula 06)
```

Não pule do inbox direto para “executar no projeto” sem Brief.

## Prática

1. Escolha **uma** aula que você já leu no núcleo comum ou em uma rota de aplicação.
2. Crie uma nota em `notas/inbox/` (ou peça ao agent com `study-capture`).
3. Linke a fonte com path ou wikilink.
4. Escreva um próximo passo que caiba em uma ação (não “estudar tudo”).

## Evidência de conclusão

Existe um arquivo de captura com fonte + insight + próximo passo, **fora** de `cursos/**/aulas/`.

## Navegação
[← Anterior](03-agent-como-professor.md) · [↑ Curso](../README.md) · [Próxima →](05-mocs-e-hubs.md)
