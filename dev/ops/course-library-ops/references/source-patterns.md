# Padrões absorvidos e fronteiras

Este pack combina três fontes sem copiá-las como um runtime único.

## Cursos canônicos deste acervo

Absorvido:

- curso autocontido em `cursos/`, prova separada em `dev/courses/` e memória
  editorial em `docs/producao-cursos/`;
- perfis pedagógicos diferentes em vez de um template universal;
- fontes, avaliação, catálogo e jornada como parte do curso, não acabamento;
- validação específica para o risco dominante de cada trilha.

## Squad course-creator (referência operacional)

Absorvido em versão slim:

- separar greenfield de brownfield;
- inventariar e analisar gaps antes de modernizar;
- gates humanos antes de materialização;
- plano e ledger antes de editar; mudanças em lotes verificáveis;
- preservação explícita de legado útil e decisão humana para arquivamento.

Não importado:

- `outputs/courses/`, workers, banco, MMOS, agentes especializados ou comandos
  do runtime Enterprise;
- scorer 0–100 e thresholds não calibrados neste acervo;
- organização/movimentação automática de materiais brownfield.

Estado e retomada:

- **estado derivado** via `doctor.py --course <id>` (e `--states` no acervo);
  não há `course-state.json` — evita dessincronia.
- Aprovações humanas continuam no frontmatter + `deviations.yaml`.

Retrospectiva:

- template `assets/course-templates/retrospective.md` → bastidor
  `docs/producao-cursos/<id>/retrospective.md` no fechamento de create/upgrade/improve;
- alimenta DNA/arquétipos sob decisão humana, sem auto-merge no pack.

## Skill `teach` canônica

Absorvido:

- ciclo `baseline → auditoria → priorização → lote pequeno → validação → evidência`;
- seis dimensões: objetivo, ancoragem, exercício, navegação, ponte e terminologia;
- ledger por aula/dimensão com `PASS|FAIL|PENDING` e contagem de falhas;
- `npm run validate` como fechamento obrigatório.

O modo `improve-course` orquestra esse contrato; não duplica a `teach`. Em outro
acervo sem `skills/teach/SKILL.md`, usa somente a cópia enxuta da rubrica em
`checklists/didactic-rubric.md`. A skill global homônima de tutoria HTML fica fora.
