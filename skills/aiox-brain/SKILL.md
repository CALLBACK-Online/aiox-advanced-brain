---
name: aiox-brain
description: >
  Meta-skill do segundo cérebro aiox-advanced-brain: onboarding do vault de estudo,
  escolha entre Obsidian e agent, captura de aprendizado, MOCs e higiene do grafo
  sem poluir o material canônico. Use quando o usuário perguntar como usar este
  repositório como segundo cérebro, como estudar no Obsidian, como organizar notas
  de aula, criar mapas de conteúdo, ou cuidar do vault de curso (não vault pessoal).
---

# AIOX Brain — segundo cérebro do acervo

## Identidade

Este repositório é um **vault educacional + biblioteca de assets**, não o monorepo AIOX nem o vault pessoal do autor.

Você conduz a pessoa a:

1. Estudar o material canônico em `cursos/`.
2. Capturar aprendizado em espaço **pessoal** (não versionado com o pacote).
3. Escolher skill/squad no acervo quando for operar.
4. Copiar assets para o **projeto dela** e exigir evidência.

## Mapa rápido

| Necessidade | Skill / curso | Path |
|-------------|---------------|------|
| Mini-curso vault + agent | curso | `cursos/Obsidian-IA/` |
| Abrir/estudar no Obsidian, buscar aula, trilha | `obsidian-course-vault` | `skills/obsidian-course-vault/` |
| Criar/atualizar MOC ou hub de estudo | `course-moc` | `skills/course-moc/` |
| Capturar insight / nota atômica ligada à aula | `study-capture` | `skills/study-capture/` |
| Escolher/operar squad | `aiox-squads` | `skills/aiox-squads/` + `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md` |
| Inventário e maturidade | — | `catalog.json` · `README.md` |

Detalhe: [references/brain-map.md](references/brain-map.md).

## Algoritmo

1. Classificar o pedido: **estudar** · **organizar vault** · **capturar** · **mapear** · **operar (skill/squad)**.
2. Se for operar AIOX (implementar, research, marca…): sair desta skill e ir para skill/squad adequados.
3. Se for vault de estudo: preferir a skill da tabela acima (menor mecanismo).
4. Nunca gravar notas pessoais em cima de aulas canônicas (`cursos/**/lessons/`, `aulas/`).
5. Destino de captura: `notas/` (local; gitignored) **ou** o vault pessoal da pessoa, se ela indicar.
6. Fechar com próximo passo verificável (ler X, capturar Y, abrir MOC Z, copiar skill W).

## O que este cérebro **não** é

- Vault de vida/livros/premium (ex.: mentelendaria) — não hardcode paths de máquina.
- Runtime AIOX completo.
- Lugar para commits de diário de estudo da turma no repositório público.

## Resposta mínima

```text
Papel: {estudar | organizar | capturar | mapear | rotear operação}
Skill/caminho: {…}
Canônico vs pessoal: {o que não mexer} / {onde capturar}
Próximo passo: {1 ação}
```

## Guardrails

- Paths relativos ao repositório; sem `/Users/…`.
- Não reescrever aulas canônicas para “ficar do jeito da pessoa”.
- Não misturar curadoria de vault pessoal com material da biblioteca sem pedido explícito.
- `npm run validate` após mudanças estruturais no acervo (não após nota pessoal).
