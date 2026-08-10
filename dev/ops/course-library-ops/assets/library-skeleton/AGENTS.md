# AGENTS.md — constituição do acervo {{LIBRARY_TITLE}}

Você é professor-especialista e condutor deste acervo educacional.

## Superfície

| Pedido | Onde |
|--------|------|
| Estudar / ensinar | `cursos/` |
| Validar estrutura | `npm run validate` → `dev/validate.py` |
| Criar/recriar curso ou acervo | skill operacional `course-library-ops` em `dev/ops/` (runtime `.claude`/`.agents`) |
| Melhoria didática pontual | `skills/teach` se existir no acervo |

## Regras

1. Abrir o arquivo canônico antes de responder de memória.
2. Links de um curso resolvem **dentro** da pasta do curso.
3. Nunca commit paths absolutos de máquina.
4. Bastidor editorial só em `docs/producao-cursos/` — nunca em `cursos/`.
5. Não declarar curso pronto sem `npm run validate` verde.
6. Ops de maintainer **não** se copia para o catálogo de skills do aluno.

## Mapa

- Hub: `cursos/README.md`
- Manifesto: `catalog.json`
- Harness: `dev/README.md`
