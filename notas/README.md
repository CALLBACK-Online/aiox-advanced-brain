---
tags: [hub, notas, estudo, layer/nota]
aliases: [Notas, Anotações dos alunos]
---

> Vault: [[00-HOME]] · [[cursos/MOC-Acervo-AIOX]] · [[cursos/entradas/README|entradas]]


# notas — anotações dos alunos

Pasta **pessoal** para o que você escreve sobre as aulas (insights, dúvidas, resumos, cards).
**Não edite** o material canônico em `cursos/`.

## Layout

```text
notas/
  inbox/     # captura rápida (durante a aula)
  notes/     # notas destiladas
  aulas/     # uma nota por aula (opcional)
  MOCs/      # seus mapas de conteúdo
  cards/     # progressive summary / revisão
  retornos/  # resultado + decisão + aprendizado de execuções
```

## Como usar

1. Estude em `cursos/…`
2. Capture aqui com a skill `study-capture` ou à mão
3. Linke sempre a fonte, ex.: `cursos/AIOX Advanced/lessons/…` ou wikilink da aula
4. Organize com `course-moc` se o tema crescer
5. Para operar, gere um Context Brief a partir de `cursos/Obsidian-IA/templates/context-brief.md`
6. Depois da execução no projeto, registre em `notas/retornos/` resultado, evidência, decisão e aprendizado reutilizável

## Primeiro uso

As pastas pessoais são gitignored e, por isso, não existem em um clone limpo. Crie-as pelo Explorer do Obsidian ou, na raiz do repositório, execute:

```bash
mkdir -p notas/inbox notas/notes notas/MOCs notas/cards notas/retornos notas/attachments
```

Depois disso, `.obsidian/app.json` direciona novas notas para `notas/inbox/` e anexos para `notas/attachments/`.

## Config do vault

Novas notas do Obsidian apontam para `notas/inbox` (ver `.obsidian/app.json`).

## Git

Só este `README.md` é versionado. Seu conteúdo pessoal fica no clone (ver `.gitignore` na raiz).
