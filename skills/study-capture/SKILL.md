---
name: study-capture
description: >
  Captura aprendizado do curso AIOX em notas pessoais ligadas às aulas canônicas
  (insight, pergunta, card, próximo passo) sem editar o material oficial. Use quando
  o usuário quiser anotar o que aprendeu, fazer resumo progressivo, zettel de uma
  aula, diary de estudo, ou “salvar isso no meu segundo cérebro” a partir do acervo.
---

# Study Capture — captura sem poluir o canônico

## Regra de ouro

**Aulas e módulos em `Cursos/` são canônicos.**
Captura da pessoa vai para espaço pessoal:

| Preferência | Path |
|-------------|------|
| Neste clone (local) | `Cursos/_notas-pessoais/` |
| Vault pessoal | path que a pessoa indicar (nunca inventar iCloud/Users) |

Estrutura sugerida (local):

```text
Cursos/_notas-pessoais/
  README.md                 # explicação (versionado)
  inbox/                    # captura rápida
  notes/                    # notas destiladas
  MOCs/                     # hubs pessoais (ver course-moc)
  cards/                    # flashcards / progressive summary
```

## Quando usar

- “Anota o que acabei de aprender”
- “Resume esta aula em camadas”
- “Cria uma nota ligada à aula X”
- “Quero levar isso pro meu Obsidian”

## Quando **não** usar

- Reescrever a aula oficial → PR/curso, não capture.
- Escolher squad → `aiox-squads`.
- Só navegar o grafo → `obsidian-course-vault`.

## Formatos de captura

### 1. Inbox (30–60s)

```markdown
# {título curto}
- fonte: [[nome-da-aula]] ou `path/relativo.md`
- data: {YYYY-MM-DD}
- insight: {1–3 frases}
- próximo passo: {1 ação}
```

### 2. Nota atômica (Zettel-like)

Uma ideia = uma nota. Título declarativo. Links para:

- aula canônica
- 1–2 notas irmãs
- eventual skill/squad (`skills/…`, `squads/…`)

### 3. Progressive summary (BASB-light)

Camadas na mesma nota ou em `cards/`:

1. **Highlight** — citação/ideia bruta da aula
2. **Próprias palavras** — o que isso muda no meu trabalho
3. **Card** — pergunta + resposta curta (revisão)

### 4. Bridge para operação

Se o insight pede execução:

```text
Captura: {nota}
Operação sugerida: skill `{x}` ou squad `{y}`
Maturidade: consultar catalog.json
Copiar para o projeto: só quando for executar
```

## Algoritmo

1. Identificar a **fonte canônica** (path real).
2. Extrair **uma** transformação desejada (não resumo de 10 páginas sem pedido).
3. Escolher formato (inbox / atômica / progressive / bridge).
4. Gravar **somente** no espaço pessoal acordado.
5. Ligar com wikilink ou path de volta à aula.
6. Oferecer 1 próximo passo (releitura, exercício da aula, MOC, skill).

## Template de nota atômica

```markdown
---
type: study-note
source: "Cursos/…/….md"
created: YYYY-MM-DD
tags: [estudo, aiox]
---

# {Afirmação em uma linha}

{Desenvolvimento curto.}

## Fonte
- Aula: [[…]] — `path/relativo.md`

## Implicação prática
- …

## Próximo passo
- [ ] …
```

## Guardrails

- Não commitar dumps pessoais no repositório público.
- Não usar paths absolutos de máquina.
- Não copiar livros/transcrições integrais.
- Não “melhorar” o canônico disfarçado de nota.
- Português (ou idioma da pessoa); tom de estudo, não de marketing.

## Handoffs

| Depois da captura… | Skill |
|--------------------|-------|
| Organizar vários insights em hub | `course-moc` |
| Voltar a navegar o curso | `obsidian-course-vault` |
| Executar no projeto | skill/squad do domínio · `aiox-squads` |
| Visão geral do cérebro | `aiox-brain` |
