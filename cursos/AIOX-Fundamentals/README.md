---
tags: [curso, aiox, fundamentals, aiox-core, layer/curso]
aliases: [AIOX Fundamentals, Fundamentals]
status: canonical
canonical_scope: cursos/AIOX-Fundamentals
source_commit: a68bd88f45e560f606e9bdc8a0f663570bdcef88
---

# AIOX Fundamentals

Base mental e operacional para entender o framework AIOX, reconhecer o contexto de uma tarefa, escolher o caminho de execução e validar a entrega com evidência.

## Resultado do curso

Ao concluir o curso, o aluno consegue:

- explicar AIOX como framework de orquestração, não como uma coleção de prompts;
- instalar o core e obter o primeiro resultado útil em uma IDE compatível;
- distinguir agent, task, skill, workflow e squad sem delegar o problema errado;
- conduzir uma mudança pelo ciclo de story, implementação, QA e fechamento;
- validar o resultado com gates, autoridade correta e evidência reproduzível.

## Estrutura

1. **Fundamentos** — o que é AIOX, CLI First, arquitetura e first-value.
2. **Sinais e contexto** — leitura do repositório, seleção de agentes, granularidade e rotas greenfield/brownfield.
3. **Validação básica** — quality gates, permissões, ciclo da story e handoff baseado em evidência.

O curso contém 12 aulas, três quizzes e um projeto final. A duração estimada é de 7h45, incluindo avaliações.

## Trilha completa

### Módulo 1 — Fundamentos

1. [O que é AIOX](lessons/01-fundamentos/1.1-o-que-e-aiox.md)
2. [CLI First e as duas fases](lessons/01-fundamentos/1.2-cli-first-e-duas-fases.md)
3. [Anatomia do framework](lessons/01-fundamentos/1.3-anatomia-do-framework.md)
4. [Instalação e primeiro valor](lessons/01-fundamentos/1.4-instalacao-e-primeiro-valor.md)

### Módulo 2 — Sinais e contexto

1. [Ler o contexto antes de agir](lessons/02-sinais-e-contexto/2.1-ler-o-contexto-antes-de-agir.md)
2. [Escolher o agent certo](lessons/02-sinais-e-contexto/2.2-escolher-o-agente-certo.md)
3. [Task, skill, workflow ou squad](lessons/02-sinais-e-contexto/2.3-task-skill-workflow-ou-squad.md)
4. [Greenfield, brownfield e story](lessons/02-sinais-e-contexto/2.4-greenfield-brownfield-e-story.md)

### Módulo 3 — Validação básica

1. [Qualidade em três camadas](lessons/03-validacao-basica/3.1-qualidade-em-tres-camadas.md)
2. [Autoridade e permissões](lessons/03-validacao-basica/3.2-autoridade-e-permissoes.md)
3. [Ciclo da story na prática](lessons/03-validacao-basica/3.3-ciclo-da-story-na-pratica.md)
4. [Evidência, doctor e handoff](lessons/03-validacao-basica/3.4-evidencia-doctor-e-handoff.md)

### Avaliações

- [Quiz do Módulo 1](assessments/quiz-module-1.yaml)
- [Quiz do Módulo 2](assessments/quiz-module-2.yaml)
- [Quiz do Módulo 3](assessments/quiz-module-3.yaml)
- [Projeto final — Primeiro ciclo AIOX com evidência](assessments/final-project.md)
- [Rubrica do projeto](assessments/final-project-rubric.md)

## Fonte canônica

O conteúdo técnico foi reconstruído a partir do checkout rastreado do repositório `SynkraAI/aiox-core`, commit `a68bd88f45e560f606e9bdc8a0f663570bdcef88`, pacote `@aiox-squads/core` versão `5.2.9`.

A seleção exata de arquivos e seus hashes está em [sources/SOURCE-MANIFEST.yaml](sources/SOURCE-MANIFEST.yaml). O acervo não duplica o checkout completo: [FONTES.md](FONTES.md) explica como auditar cada afirmação no snapshot.

## Como estudar

Cada aula segue Goal → Position → Steps, inclui um exercício executável e fecha com prática de recuperação sem assistência de IA. Faça as aulas em ordem; o Módulo 2 assume o vocabulário do Módulo 1 e o Módulo 3 usa os artefatos criados nos dois primeiros.

## Arquivos principais

- `COURSE-BRIEF.md` — público, transformação, limites e aprovação curricular.
- `curriculum.yaml` — identidade estável das aulas, objetivos de Bloom e paths.
- `lessons/` — conteúdo didático.
- `assessments/` — quizzes e projeto final.
- `validation-report.md` — resultado consolidado dos gates.
- `deviations.yaml` — decisões conscientes tomadas durante o upgrade.
- `FONTES.md` e `PROVENIENCIA.md` — rastreabilidade sem importar paths de máquina.

## Escopo

Este curso ensina fundamentos do framework open source. Não substitui a trilha AIOX Advanced, não promete domínio de uma IDE específica e não inclui recursos comerciais do AIOX Pro.

Também não substitui **Fundamentos de Arquitetura**. Arquitetura ensina a ler sistemas em geral; este curso ensina a instalar e operar o `aiox-core`.

## Posição no acervo

`Obsidian + IA → Fundamentos de Arquitetura → AIOX Fundamentals → AIOX Advanced → AIOX Advanced Squads`
