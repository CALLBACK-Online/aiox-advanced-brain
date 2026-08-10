---
type: provenance
course: aiox-fundamentals
status: canonical
canonical_scope: cursos/AIOX-Fundamentals
---

# Proveniência

## Desenho curricular

O ponto de partida foi o desenho aprovado de **AIOX Fundamentals** fornecido pelo usuário:

- `COURSE-BRIEF.md`;
- `course-outline.md`;
- `curriculum.yaml`;
- `gap-analysis.md`;
- `deviations.yaml`;
- relatório do gate do brief.

Esse desenho definiu três módulos, 12 aulas, três quizzes, um projeto final, duração de 7h45 e a transformação “de pedidos isolados para execução por contexto, story e evidência”.

## Fonte técnica

Todo o conteúdo operacional foi conferido contra o snapshot rastreado do AIOX Core 5.2.9. O manifesto registra commit e SHA-256 dos arquivos usados.

## Transformações editoriais

- O curso legado chamado AIOS não foi copiado nem renomeado mecanicamente.
- Afirmações foram reescritas para o namespace e a arquitetura atuais.
- A grade permaneceu na arquitetura aprovada de três módulos.
- A aula de seleção cobre o básico dos 12 agents presentes no core.
- Ativação foi descrita de modo portátil; nenhuma superfície de IDE foi tratada como universal.
- Avaliações e validator foram adicionados para exigir evidência.

## Fronteiras com outras trilhas

- **Introdução à Arquitetura de Sistemas:** vocabulário universal para entender sistemas.
- **AIOX Fundamentals:** instalação e operação básica do `aiox-core`.
- **AIOX Advanced:** método, contexto, SDC aprofundado, determinismo e brownfield.
- **AIOX Agent Engineering:** agents, workflows, runners, harness e produção.
- **AIOX Design:** contrato e qualidade visual.
- **AIOX Advanced Squads:** escolha e operação dos especialistas empacotados.

O Fundamentals não absorve arquitetura geral, especialização Advanced nem o curso operacional de squads.

## Regra de atualização

Uma atualização do AIOX Core exige:

1. novo commit e versão no manifesto;
2. recálculo dos hashes;
3. revisão de instalação, agents, autoridade e comandos;
4. execução do validator do curso;
5. registro da mudança no catálogo do acervo.
