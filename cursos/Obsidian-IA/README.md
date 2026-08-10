---
type: course
course: obsidian-ia
title: Obsidian + IA
status: canonical
canonical_scope: cursos/Obsidian-IA
sharing_boundary: cursos
source: skills/aiox-brain + vault de estudo
source_version: 1.2.0
curriculum_modules: 1
lessons: 8
tags: [curso, obsidian, ia, segundo-cerebro, aiox, layer/curso]
---

# Obsidian + IA

> Do vault à próxima decisão: recuperar contexto, estudar com intenção e, quando houver base operacional, executar no projeto AIOX.

Mini-curso **prático** (cerca de **90–120 minutos**) para usar este repositório como segundo cérebro de estudo com **Obsidian** e um **agent** (Claude Code, Codex ou genérico). Ele abre a jornada e volta a ser usado nas etapas seguintes.

## Para quem

- Aluno em qualquer etapa da jornada AIOX que quer estudar no Obsidian de verdade.
- Quem já clona o `aiox-advanced-brain` e se perde entre GitHub, aulas e “onde anoto?”.
- Quem quer combinar **navegação humana** (grafo) com **condução por agent** (professor-especialista).

## Resultado

Ao terminar você consegue:

1. Abrir o vault certo e achar qualquer aula em menos de um minuto.
2. Usar wikilinks, backlinks e Graph sem medo.
3. Pedir ao agent para ensinar, capturar e mapear — sem reescrever aulas oficiais.
4. Transformar conhecimento recuperado em um **Context Brief** verificável.
5. Encaminhar o briefing para a próxima aula/curso ou, quando já houver base operacional, para o projeto AIOX.
6. Devolver resultado, decisão e aprendizado ao segundo cérebro depois de cada ciclo.

## Não é

- Curso completo de plugins premium do Obsidian.
- Substituição de Introdução à Arquitetura de Sistemas, AIOX Fundamentals, AIOX Advanced ou do curso de Squads.
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
Obsidian + IA (este mini) — estudar o acervo
        ↓
Introdução à Arquitetura de Sistemas — entender sistemas
        ↓
AIOX Fundamentals — instalar e operar o Core
        ↓
AIOX Advanced — aplicar o método
        ↓
AIOX Advanced Squads — operar os especialistas
```

Quem já domina Obsidian pode validar o gate de entrada e seguir. Reabra este mini **em paralelo** às outras etapas sempre que captura, MOC, Context Brief ou retorno ao vault virarem gargalo.

## Evidência de conclusão

O primeiro gate, suficiente para seguir a **Introdução à Arquitetura de Sistemas**, exige:

- 1 captura pessoal ligada a uma aula real **ou** 1 MOC quando houver pelo menos 5 conexões úteis;
- 1 Context Brief de estudo com fontes, próxima trilha e critério de compreensão.

Depois de AIOX Fundamentals ou Advanced, volte para o gate operacional:

- 1 Context Brief com fontes, missão, asset e critério de aceite;
- 1 artefato executado no projeto AIOX com evidência de validação;
- 1 nota de retorno com resultado, decisão e aprendizado reutilizável.

Para conferir os conceitos das 8 aulas, feche com o [Quiz final](avaliacoes/Quiz-final.md).

## Validação

```bash
python3 "cursos/Obsidian-IA/_tools/validate_course.py"
```
