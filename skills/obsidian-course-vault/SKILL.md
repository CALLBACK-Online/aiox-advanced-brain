---
name: obsidian-course-vault
description: >
  Opera os cursos deste repositório como vault Obsidian: escolher raiz do vault,
  navegar wikilinks, localizar aulas/módulos, orientar Graph/backlinks e trilha de
  estudo. Use quando o usuário falar em Obsidian, vault, wikilinks, Graph view,
  “por onde estudo”, “abrir o curso”, ou precisar achar uma aula no grafo pedagógico.
---

# Obsidian Course Vault

## Escopo

Vault de **estudo AIOX** neste repositório. Não assume plugins pagos. Não configura o vault pessoal da pessoa salvo pedido explícito.

## Escolher a raiz do vault

| Raiz | Quando |
|------|--------|
| `cursos/Obsidian-IA/` | Aprender o vault e preparar Context Brief |
| `cursos/Introducao-a-Arquitetura-de-Sistemas/` | Entender sistemas e vocabulário técnico |
| `cursos/AIOX-Fundamentals/` | Instalar e operar o Core |
| `cursos/AIOX Advanced/` | Foco no método (grafo com milhares de links) |
| `cursos/AIOX-Advanced-Squads/` | Rota de aplicação: squads publicados 1:1 |
| `cursos/AIOX-Agent-Engineering/` | Rota de aplicação: capacidades agentic |
| `cursos/AIOX-Design/` | Rota de aplicação: contrato visual |
| `cursos/AIOX-Productizacao/` | Rota de aplicação: oferta e mercado |
| `cursos/AIOX-Enterprise/` | Vitrine de continuidade: prontidão operacional |
| `cursos/` | Ver a jornada completa (hub) |
| Raiz do repo | Estudo + `skills/` + `squads/` (índice mais pesado) |

Instruções humanas: `README.md` (seção Obsidian) e `cursos/README.md`.

## Onboarding (primeiros minutos)

1. Confirmar que a pessoa tem o material clonado/extraído.
2. Indicar **Open folder as vault** na raiz escolhida.
3. Abrir o `README.md` do curso.
4. Sugerir a entrada da etapa atual; no método, a sequência ativa de 29 aulas; em Squads, aula `00-como-usar-este-curso`.
5. Explicar: agent ensina/roteia; Obsidian navega o grafo.

## Localizar material

Sempre paths relativos ao repo:

```text
cursos/AIOX Advanced/aulas/
cursos/AIOX Advanced/modulos/
cursos/Introducao-a-Arquitetura-de-Sistemas/aulas/
cursos/AIOX-Fundamentals/aulas/
cursos/AIOX-Agent-Engineering/aulas/
cursos/AIOX-Design/aulas/
cursos/AIOX-Productizacao/aulas/
cursos/AIOX-Advanced-Squads/aulas/
cursos/AIOX-Advanced-Squads/modulos/
cursos/AIOX-Enterprise/aulas/
cursos/README.md
```

Busca: pelo nome da aula no frontmatter/`title`, tags `curso/…`, ou palavra da missão.

Para **qual squad** a partir de linguagem natural: não inventar — usar `skills/aiox-squads` / `agent-router.json`.

## Wikilinks

- No Obsidian, `[[Nome da nota]]` resolve pelo basename dentro do vault.
- Fora do Obsidian, traduza para path relativo quando orientar o agent.
- Links de cada curso devem permanecer **dentro da pasta daquele curso** (contrato do validador).

## Papel do agent neste vault

| Fazer | Evitar |
|-------|--------|
| Guiar trilha e citar aulas | Reescrever lições canônicas |
| Sugerir próxima aula | Dump de 75 títulos sem prioridade |
| Ligar conceito ↔ squad | Assumir que o vault pessoal está aberto |
| Lembrar maturidade antes de executar | Prometer runtime AIOX completo aqui |

## Saída esperada

- Raiz de vault recomendada + por quê.
- Arquivo de entrada (README ou aula).
- 1–3 próximos passos de estudo.
- Se a missão for operacional: handoff para `aiox-brain` montar o Context Brief e depois para a skill/squad com path.

## Templates de resposta

**Onboarding**

```text
Vault root: {path}
Abra: {README ou aula 00}
Trilha: {Essencial | módulo | missão}
Depois: {study-capture | course-moc | aiox-brain → Context Brief → skill/squad}
```

**“Onde está X?”**

```text
Arquivo: {path relativo}
Curso: {Obsidian + IA | Introdução à Arquitetura | Fundamentals | Advanced | Squads | Agent Engineering | Design | Productização | Enterprise}
Ligue com: {1–2 vizinhos úteis}
```
