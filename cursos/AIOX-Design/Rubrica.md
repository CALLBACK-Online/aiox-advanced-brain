---
type: rubric
course: aiox-design
status: canonical
canonical_scope: cursos/AIOX-Design
---

# Rubrica — Capstone AIOX Design (v2 executável)

| Critério | Peso | Nota máxima se… |
|----------|-----:|-----------------|
| DESIGN.md utilizável | 20 | Agente saberia ler tokens, proibições e componentes |
| Taxonomia e REUSE | 10 | Átomo/molécula na camada certa; REUSE/ADAPT/CREATE explícito |
| **Storybook rodando** | 25 | Local com stories das variantes mínimas (evidência: URL/print/log) |
| Matriz de variantes em stories | 15 | Estados + tema ou breakpoint + nota a11y materializados |
| Ciclo visual | 10 | Screenshot→comparação→patch documentado |
| Governança / rota operacional | 10 | Quem mexe no DS; skill/squad + anti-escopo |
| Clareza e honestidade | 10 | Limitações explícitas; sem inventar runtime |

**Aprovação:** ≥ 80 e **nenhuma falha crítica**.

## Falhas críticas

- Ausência de DESIGN.md.
- **Storybook não rodando** sem bloqueio de ambiente documentado **e** sem caminho de remediação — bloqueio de ambiente **não** conta como aprovação.
- “Passou no papel” como substituto de materialização.

## Opcional (não bloqueia)

- Chromatic / regressão visual em CI.
- Biblioteca completa de organismos.

[Projeto](Projeto-Integrador.md) · [Aula 20](aulas/20-capstone-ds-storybook-executavel.md) · [⌂ Curso](README.md)
