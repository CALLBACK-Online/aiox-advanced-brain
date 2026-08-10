# Modelo de learning journey

Fonte de verdade: `catalog.json` → `learning_journey`.

## Modelo padrão

```json
{
  "learning_journey": {
    "model": "common-core-plus-application-routes-and-continuity-preview",
    "common_core": ["curso-a", "curso-b"],
    "responsibilities": {
      "curso-a": "frase curta do que o curso forma"
    },
    "core_transitions": [
      {
        "from": "curso-a",
        "to": "curso-b",
        "bridge": "cursos/Curso-A/aulas/99-capstone.md"
      }
    ],
    "application_routes": {
      "route-id": {
        "entry_from": "curso-b",
        "courses": ["curso-especializado"],
        "bridge": "cursos/Curso-B/ponte/trilhas.md"
      }
    },
    "cross_route_transitions": [],
    "continuity_preview": {
      "course": "preview-id",
      "kind": "preview",
      "entry_from": "curso-b",
      "entry_gate": "evidência mínima",
      "bridge": "cursos/Curso-B/ponte/trilhas.md"
    }
  }
}
```

## Regras

1. Todo `bridge` aponta para um **arquivo existente**.
2. Todo id em journey existe em `courses` (ou `supplemental_courses` legado).
3. Cada curso tem **uma** responsabilidade em uma frase.
4. Split curricular: atualizar seeds, anti-escopo no brief, e **não** deixar
   o curso origem com promessa que mudou de dono.
5. Preview ≠ formação: `kind: preview` não promete implementação.

## Operações manage

- **rebalance-journey** — reordenar common_core, mover curso entre routes.
- **register-course** — adicionar id + responsibility + transition/route.
- **retire-course** — remover de arrays; manter path em archive se histórico.

Gate: `dev/courses/validate_learning_journey.py` (quando presente no acervo).
