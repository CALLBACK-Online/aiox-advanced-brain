---
type: validation-report
course: aiox-fundamentals
status: pass
canonical_scope: cursos/AIOX-Fundamentals
validated_at: 2026-08-10
---

# Relatório de validação — AIOX Fundamentals

## Veredito

**PASS**

## Escopo validado

- 3 módulos;
- 12 aulas;
- 3 quizzes;
- 15 questões com gabarito e rationale;
- projeto final e rubrica;
- mapa dos 12 agents do AIOX Core;
- 32 fontes com SHA-256;
- links internos e fronteira autocontida;
- ausência de paths absolutos específicos de máquina.

## Fonte técnica

- repositório: `SynkraAI/aiox-core`;
- commit: `a68bd88f45e560f606e9bdc8a0f663570bdcef88`;
- pacote: `@aiox-squads/core@5.2.9`.

## Evidência

Comando executado na raiz do acervo:

    npm run validate

Resultado consolidado:

    AIOX Advanced: PASS
    Introdução à Arquitetura de Sistemas: 24 aulas, 8 módulos, 8 quizzes, 0 erros
    AIOX Fundamentals: 12 aulas, 3 módulos, 3 quizzes, 15 questões, 32 fontes, 0 erros
    AIOX Advanced Squads: 24/24 squads, 0 erros
    Obsidian + IA: 8 aulas, 0 erros
    Agent routing: 24/24 rotas, 0 erros

## Limites

O gate valida estrutura, metadados, contagens, cobertura curricular, links, fontes e regras editoriais. Ele não instala o AIOX no computador do aluno nem garante paridade entre IDEs; a aula de instalação exige evidência no projeto de prática.
