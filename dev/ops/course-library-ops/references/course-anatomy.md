# Anatomia de curso

Os cursos compartilham contratos, não uma árvore rígida.

## Núcleo

| Artefato | Função | Gate |
|---|---|---|
| `README.md` | promessa, entrada, sequência e saída | escopo e próximo passo inequívocos |
| `aulas/` | progressão de competências | mudança observável e evidência/diagnóstico |
| fonte/proveniência | rastreabilidade | claims importantes têm origem e limite |
| `dev/courses/<id>/manifest.yaml` | descoberta | id/path corretos |
| `dev/courses/<id>/checks.py` | prova específica | falha nos invariantes relevantes |

`FONTES.md` e `PROVENIENCIA.md` são o padrão para cursos formativos, mas podem
ser combinados ou substituídos por equivalente explícito em mini-curso/preview.

## Artefatos condicionais

| Artefato | Criar quando |
|---|---|
| `modulos/` | há progressão e evidência intermediária |
| `avaliacoes/` + `Assessments.md` | retenção/transferência precisam ser medidas |
| `Projeto-Integrador.md` + `Rubrica.md` | existe performance terminal executável |
| `AGENT-GUIDE.md` | agentes precisam rotear ou ensinar |
| mapa de decisão/termos | entrada acontece por intenção ou vocabulário |
| `Glossario.md` | vocabulário próprio pode derivar |
| `templates/` | aluno produz artefatos repetíveis |
| `ponte/` | existe transição curricular real |
| `curriculum.yaml` | ordem/duração/identidade precisam de SoT machine-readable |
| `sources/SOURCE-MANIFEST.yaml` | fonte técnica versionável exige auditoria |
| FAQ/casos/personas | evidência de campo muda decisões |

Não criar arquivo cerimonial vazio.

## Frontmatter de aula

```yaml
---
type: lesson
course: <id>
lesson_id: <slug-estável>
lesson_position: 1
title: "<Título>"
module: M0
status: canonical
canonical_scope: cursos/<Curso>
reading_minutes: 10
---
```

Adicionar apenas campos consumidos:

- `sequence`, `difficulty` para progressão;
- `maturity`, `squad`, `agents`, `tasks`, `workflows` para catálogo;
- `source_refs` ou `source_commit` para rastreabilidade;
- `source_lesson_id`, `source_path`, `source_version`, `curriculum_role` para
  migração.

## Brief

O `COURSE-BRIEF.md` fecha identidade, público, antes/depois, performance
terminal, objetivos, voz, formato, avaliação, anti-escopo, restrições, fontes,
aprovação e fronteira de publicação. Brief e outline registram os campos do
`references/approval-protocol.md`; o `course-spec.json` apenas referencia os
artefatos aprovados. Preview enfatiza IP; brownfield inclui gap e decisões de
migração.

## Outline e rastreabilidade

Para cada aula:

```text
id → módulo → competência → fonte → prática/evidência → avaliação → capstone
```

O outline nomeia o entregável de cada módulo antes da redação. Rejeitar aula que
não move evidência ou pré-requisito real.

## Quiz

- Cenários e decisões, não definição decorada.
- `### N.` e A–D quando usar `dev/lib/quizzes.py`.
- `<details>` com rationale e `## Transferência`.
- Posição correta balanceada com diferença máxima de 1.
- Quiz não substitui evidência prática.

## Capstone e rubrica

Escrever a rubrica antes das aulas. Incluir critérios, pesos/níveis, falhas
críticas e evidência aceitável. Bloqueio de ambiente é estado honesto, não
aprovação. O capstone reutiliza artefatos dos módulos.

## AGENT-GUIDE

Incluir sinais, anti-sinais, intenção → aula, profundidade por nível, prática,
evidência, fronteira com vizinhos e prompt genérico quando runtime não estiver
confirmado.

## Harness

Usar `dev/lib/frontmatter.py`, `links.py`, `quizzes.py` e regras declarativas do
manifesto. O `checks.py` protege o específico: sequência, perfil, fonte, IP,
capstone, maturidade ou cobertura. Não duplicar contagens do catálogo quando ele
já for SoT. Nunca depender de `docs/`.

## Regras transversais

- Links internos resolvem na pasta do curso, salvo contrato legado explícito.
- Sem paths absolutos de máquina.
- Contagens filesystem ↔ catálogo ↔ curriculum/README ↔ checks.
- Nada de brief, relatório ou executável em `cursos/`.
