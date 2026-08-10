---
name: aiox-brain
description: >
  Meta-skill do segundo cérebro aiox-advanced-brain: onboarding do vault de estudo,
  escolha entre Obsidian e agent, captura, MOCs, Context Brief, handoff ao projeto
  e retorno de aprendizado sem poluir o material canônico. Use quando o usuário
  perguntar como usar este repositório como segundo cérebro, estudar no Obsidian,
  organizar notas, preparar contexto para uma missão AIOX ou fechar o loop depois
  da execução (não para curadoria completa de vault pessoal).
---

# AIOX Brain — segundo cérebro do acervo

## Identidade

Este repositório é um **vault educacional + biblioteca de assets**, não o monorepo AIOX nem o vault pessoal do autor.

Você conduz a pessoa a:

1. Estudar o material canônico em `cursos/`.
2. Capturar aprendizado em espaço **pessoal** (não versionado com o pacote).
3. Escolher skill/squad no acervo quando for operar.
4. Transformar o contexto recuperado em um **Context Brief**.
5. Copiar o menor asset necessário para o **projeto dela** e exigir evidência.
6. Devolver resultado, decisão e aprendizado ao espaço pessoal.

## Mapa rápido

| Necessidade | Skill / curso | Path |
|-------------|---------------|------|
| Mini-curso vault + Context Brief + execução + retorno | curso | `cursos/Obsidian-IA/` |
| Entender sistemas | curso | `cursos/Introducao-a-Arquitetura-de-Sistemas/` |
| Instalar e operar o Core | curso | `cursos/AIOX-Fundamentals/` |
| Aplicar o método | curso | `cursos/AIOX Advanced/` |
| Operar especialistas publicados | rota de aplicação | `cursos/AIOX-Advanced-Squads/` |
| Construir capacidade agentic própria | rota de aplicação | `cursos/AIOX-Agent-Engineering/` |
| Estabelecer contrato visual | rota de aplicação | `cursos/AIOX-Design/` |
| Transformar capacidade em oferta | rota de aplicação | `cursos/AIOX-Productizacao/` |
| Diagnosticar prontidão para operação mantida | vitrine de continuidade | `cursos/AIOX-Enterprise/` |
| Abrir/estudar no Obsidian, buscar aula, trilha | `obsidian-course-vault` | `skills/obsidian-course-vault/` |
| Criar/atualizar MOC ou hub de estudo | `course-moc` | `skills/course-moc/` |
| Capturar insight / nota atômica ligada à aula | `study-capture` | `skills/study-capture/` |
| Preparar handoff cérebro → projeto | `aiox-brain` + aula 07 | `cursos/Obsidian-IA/templates/context-brief.md` |
| Escolher/operar squad | `aiox-squads` | `skills/aiox-squads/` + `cursos/AIOX-Advanced-Squads/AGENT-GUIDE.md` |
| Inventário e maturidade | — | `catalog.json` · `README.md` |

Detalhe: [references/brain-map.md](references/brain-map.md).

## Algoritmo

1. Classificar o pedido: etapa do núcleo comum, rota de aplicação (**Squads**, **Agent Engineering**, **Design**, **Productização**) ou vitrine de continuidade (**Enterprise**).
2. Se for vault de estudo: preferir a skill da tabela acima (menor mecanismo).
3. Se for operar AIOX: recuperar 1–3 fontes, montar o Context Brief e confirmar asset + maturidade.
4. Fazer handoff do briefing e do menor asset necessário; a execução pertence à skill/squad do domínio no projeto.
5. Depois da execução, voltar a `study-capture` para registrar resultado, decisão, evidência e aprendizado reutilizável.
6. Nunca gravar notas pessoais em cima de aulas canônicas (`cursos/**/aulas/`, `aulas/`).
7. Destino de captura: `notas/` (local; gitignored) **ou** o vault pessoal da pessoa, se ela indicar.
8. Fechar com próximo passo verificável em qualquer fase do loop.

## Contrato de integração operacional

```text
Segundo cérebro → Context Brief + asset → projeto AIOX
Segundo cérebro ← resultado + decisão + evidência ← projeto AIOX
```

O Context Brief é a fronteira. Ele contém missão, fontes sintetizadas, restrições, mecanismo, aceite, evidência e retorno planejado. Não transfira o vault inteiro, notas privadas, secrets ou logs brutos ao projeto.

Template: `cursos/Obsidian-IA/templates/context-brief.md`.

## O que este cérebro **não** é

- Vault de vida/livros/premium (ex.: mentelendaria) — não hardcode paths de máquina.
- Runtime AIOX completo.
- Lugar para commits de diário de estudo da turma no repositório público.

## Resposta mínima

```text
Papel: {estudar | organizar | capturar | mapear | rotear operação}
Skill/caminho: {…}
Canônico vs pessoal: {o que não mexer} / {onde capturar}
Fase do loop: {recuperar | preparar Context Brief | executar no projeto | retornar}
Próximo passo: {1 ação}
```

## Guardrails

- Paths relativos ao repositório; sem `/Users/…`.
- Não reescrever aulas canônicas para “ficar do jeito da pessoa”.
- Não misturar curadoria de vault pessoal com material da biblioteca sem pedido explícito.
- Não executar uma missão do projeto dentro deste repositório de distribuição.
- Não declarar o loop concluído sem artefato validado e nota de retorno.
- Com o bastidor local `dev/` instalado, `npm run validate` após mudanças
  estruturais no acervo; sem o harness, não declarar a mudança pronta.
