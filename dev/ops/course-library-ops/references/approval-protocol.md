# Protocolo de aprovação humana

Dois gates bloqueiam materialização ou modernização:

1. `COURSE-BRIEF.md` aprovado antes de fechar outline/spec.
2. `course-outline.md` aprovado antes de criar stubs ou editar aulas existentes.

Cada artefato registra no frontmatter:

```yaml
status: approved
approved_by: "identidade do humano autorizado"
approval_date: "YYYY-MM-DD"
approved_artifact: "docs/producao-cursos/<id>/<arquivo>"
approval_scope: "decisões cobertas pela aprovação"
```

O `course-spec.json` referencia os dois paths em `approval_artifacts`; ele não
duplica os dados. `approved_artifact` deve repetir exatamente o path canônico
do próprio artefato. `check_approvals.py` verifica existência, localização, campos e
rejeita brief, outline ou spec que ainda conservem marcadores inequívocos de scaffold
como `_DRAFT_`, `REPLACE_ME`, `YYYY-MM-DD` e tokens estruturais `<...>`.

O agente nunca inventa identidade ou aprovação. Se o usuário não aprovou, manter
`status: draft` e parar antes do scaffold/edição. Mudança material posterior
invalida o gate: voltar a `draft`, registrar o delta e pedir nova aprovação.
