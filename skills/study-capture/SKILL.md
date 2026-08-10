---
name: study-capture
description: >
  Captura aprendizado do curso e retorno de execuções AIOX em notas pessoais ligadas
  às fontes canônicas (insight, pergunta, card, resultado, decisão, evidência e próximo
  passo) sem editar o material oficial. Use para resumo progressivo, zettel de aula,
  diary de estudo, “salvar isso no meu segundo cérebro” ou fechar o loop após operar.
---

# Study Capture — captura sem poluir o canônico

## Regra de ouro



**Aulas e módulos em `cursos/` são canônicos.**
Captura da pessoa vai para espaço pessoal:

| Preferência | Path |
|-------------|------|
| Neste clone (local) | `notas/` |
| Vault pessoal | path que a pessoa indicar (nunca inventar iCloud/Users) |

Estrutura sugerida (local):

```text
notas/
  README.md                 # explicação (versionado)
  inbox/                    # captura rápida
  notes/                    # notas destiladas
  MOCs/                     # hubs pessoais (ver course-moc)
  cards/                    # flashcards / progressive summary
  retornos/                 # resultado + decisão + aprendizado de execuções
```

## Quando usar

- “Anota o que acabei de aprender”
- “Resume esta aula em camadas”
- “Cria uma nota ligada à aula X”
- “Quero levar isso pro meu Obsidian”
- “Registra o que esta execução ensinou”

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
Fontes sintetizadas: {1–3 paths + por que importam}
Context Brief: {cópia preenchida de cursos/Obsidian-IA/templates/context-brief.md}
Operação sugerida: skill `{x}` ou squad `{y}`
Maturidade: consultar catalog.json
Handoff: Context Brief + menor asset necessário
Retorno planejado: {resultado + decisão + evidência + aprendizado}
```

Não pule da captura direto para a execução. Passe por `aiox-brain`, complete o Context Brief e só então entregue o briefing à skill/squad do projeto.

### 5. Retorno de execução

Use depois de uma missão executada e validada no projeto:

```markdown
# Retorno — {missão}
- data: YYYY-MM-DD
- Context Brief: {nome ou link}
- projeto: {identificador não sensível}
- resultado: {o que mudou}
- evidência: {artefato + validação}
- decisão: {mantida, alterada ou descartada}
- aprendizado reutilizável: {1–3 frases}
- próximo passo: {1 ação}
```

Destile o resultado. Não copie logs completos, secrets, dados privados ou transcrições do agent.

## Algoritmo

1. Identificar a **fonte canônica** ou o Context Brief (path real).
2. Extrair **uma** transformação ou aprendizado desejado (não resumo de 10 páginas sem pedido).
3. Escolher formato (inbox / atômica / progressive / bridge / retorno).
4. Gravar **somente** no espaço pessoal acordado.
5. Ligar com wikilink ou path de volta à aula.
6. Se for retorno, ligar também o artefato e a evidência da execução sem expor conteúdo privado.
7. Oferecer 1 próximo passo (releitura, exercício, MOC, skill ou nova missão).

## Template de nota atômica

```markdown
---
type: study-note
source: "cursos/…/….md"
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
- Não copiar secrets, dumps de terminal ou dados privados do projeto.
- Não “melhorar” o canônico disfarçado de nota.
- Português (ou idioma da pessoa); tom de estudo, não de marketing.

## Handoffs

| Depois da captura… | Skill |
|--------------------|-------|
| Organizar vários insights em hub | `course-moc` |
| Voltar a navegar o curso | `obsidian-course-vault` |
| Preparar execução no projeto | `aiox-brain` → Context Brief → skill/squad do domínio |
| Registrar uma execução concluída | `study-capture` no formato Retorno de execução |
| Visão geral do cérebro | `aiox-brain` |
