---
type: course
course: obsidian-ia
title: Obsidian + IA
status: canonical
canonical_scope: cursos/Obsidian-IA
sharing_boundary: cursos
source: skills/aiox-brain + vault de estudo
source_version: 1.1.0
curriculum_modules: 1
lessons: 8
tags: [curso, obsidian, ia, segundo-cerebro, aiox, layer/curso]
---

# Obsidian + IA

> Do vault à execução: recuperar contexto, operar no projeto AIOX e devolver aprendizado ao segundo cérebro.

Mini-curso **prático** (cerca de **90–120 minutos**, mais o tempo da missão real) para integrar este repositório ao trabalho com AIOX como segundo cérebro de estudo usando **Obsidian** e um **agent** (Claude Code, Codex ou genérico).

## Para quem

- Aluno do AIOX Advanced que quer estudar no Obsidian de verdade.
- Quem já clona o `aiox-advanced-brain` e se perde entre GitHub, aulas e “onde anoto?”.
- Quem quer combinar **navegação humana** (grafo) com **condução por agent** (professor-especialista).

## Resultado

Ao terminar você consegue:

1. Abrir o vault certo e achar qualquer aula em menos de um minuto.
2. Usar wikilinks, backlinks e Graph sem medo.
3. Pedir ao agent para ensinar, capturar e mapear — sem reescrever aulas oficiais.
4. Transformar conhecimento recuperado em um **Context Brief** verificável.
5. Levar o briefing e o menor asset necessário ao projeto AIOX e executar uma missão real.
6. Devolver resultado, decisão e aprendizado ao segundo cérebro.

## Não é

- Curso completo de plugins premium do Obsidian.
- Substituição do AIOX Advanced (método) ou do curso de Squads (operação).
- Tutorial do vault pessoal mentelendaria (paths de máquina / vida / livros).
- Sincronização automática entre vault e projeto: a ponte ensinada é manual, mínima e reproduzível.

## Como estudar

1. Abra a **raiz do repositório** como vault para acessar cursos, notas, skills e squads no mesmo Graph.
2. Siga as aulas em ordem (00 → 07).
3. Faça os exercícios curtos; use as skills de vault quando o agent estiver no repo.

| Skill de apoio | Path |
|----------------|------|
| Meta do cérebro | `skills/aiox-brain/SKILL.md` (no repo, fora desta pasta) |
| Vault Obsidian | `skills/obsidian-course-vault/SKILL.md` |
| MOCs | `skills/course-moc/SKILL.md` |
| Captura | `skills/study-capture/SKILL.md` |

Entre cursos, os paths monoespaçados apontam para o hub: `cursos/README.md`.

## Aulas

0. [Por que Obsidian + IA neste acervo](aulas/00-por-que-obsidian-ia.md)
1. [Abrir o vault e o mapa](aulas/01-abrir-o-vault.md)
2. [Wikilinks, backlinks e Graph](aulas/02-wikilinks-e-grafo.md)
3. [O agent como professor-especialista](aulas/03-agent-como-professor.md)
4. [Captura sem poluir o canônico](aulas/04-captura-sem-poluir.md)
5. [MOCs e hubs de estudo](aulas/05-mocs-e-hubs.md)
6. [Context Brief: do estudo à execução](aulas/06-do-estudo-a-execucao.md)
7. [Prática integrada: estudo → execução → memória](aulas/07-pratica-integrada.md)

## Ordem com as outras trilhas

```text
Obsidian + IA (este mini)     ← pode vir primeiro se o vault for o gargalo
        ↓
AIOX Advanced (método)
        ↓
AIOX Advanced Squads (operação)
```

Ou encaixe este mini **em paralelo** à Rota Essencial do Advanced, quando o aluno reclamar de “não sei estudar isso no Obsidian”.

## Evidência de conclusão

Você “passou” no mini-curso se entregar:

- 1 captura pessoal ligada a uma aula real;
- 1 MOC com pelo menos 5 links úteis;
- 1 Context Brief com fontes, missão, asset e critério de aceite;
- 1 artefato executado no projeto AIOX com evidência de validação;
- 1 nota de retorno com resultado, decisão e aprendizado reutilizável.

## Validação

```bash
python3 "cursos/Obsidian-IA/_tools/validate_course.py"
```
