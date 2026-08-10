---
name: teach
description: >
  Conduz rodadas de melhoria didática dos cursos canônicos deste acervo:
  auditoria pedagógica por rubrica, priorização por impacto, edição segura e
  validação estrutural. Use quando o usuário pedir para melhorar um curso ou
  aula, revisar a didática, criar exercícios ou quizzes, padronizar navegação
  entre aulas, reforçar pontes método ↔ operação, ou disser "/teach",
  "melhorar os cursos", "elevar a qualidade das aulas".
---

# Teach — melhoria didática do canônico

## Princípio

No vault de estudo, `study-capture` e `course-moc` existem para **não** tocar o
material oficial. `teach` é a exceção deliberada: ela **edita aulas canônicas**,
e por isso nunca improvisa. Toda rodada segue o ciclo completo:

**baseline → auditoria → priorização → edição em lote pequeno → validação → evidência**

Sem `npm run validate` verde no fim, a rodada não terminou.

## Quando usar (e quando não)

| Pedido | Skill |
|--------|-------|
| “Melhorar/revisar as aulas”, “curso mais didático”, “/teach” | **teach** |
| “Anotar o que aprendi” sem editar o oficial | `study-capture` |
| “Como X se conecta com Y” (hub/mapa) | `course-moc` |
| “Por onde estudo / abrir o vault” | `obsidian-course-vault` |

## Rubrica didática (auditar cada aula contra isto)

1. **Objetivo verificável** — a aula declara o que a pessoa saberá fazer ao final
   (não “falaremos sobre…”, e sim “ao final você consegue…”).
2. **Ancoragem no acervo** — exemplos citam assets **presentes neste repo**
   (`skills/…`, `squads/…`, aulas irmãs); nada inventado.
3. **Exercício ou checkpoint** — pelo menos uma prática curta ou pergunta de
   autoavaliação; exercício vale mais que resumo longo.
4. **Navegação** — links de módulo, aula anterior/próxima e retorno ao README do
   curso resolvem **dentro da pasta do próprio curso**.
5. **Ponte método ↔ operação** — conceito do AIOX Advanced aponta a aula de squad
   correspondente (e vice-versa) via pastas `ponte/` e matriz de `cursos/README.md`.
6. **Terminologia consistente** — termos técnicos batem com o glossário do curso;
   um termo novo entra no glossário, não solto na aula.

## Algoritmo da rodada

1. **Baseline** — rodar `npm run validate`; se já houver erro, corrigir antes de
   melhorar (nunca empilhar melhoria sobre estrutura quebrada).
2. **Auditar** — amostrar aulas de cada curso contra a rubrica acima; registrar
   achados com path concreto (aula + item da rubrica que falha).
3. **Priorizar** — ordenar por impacto didático × esforço; preferir correções
   sistemáticas (um padrão aplicado a N aulas) a retoques isolados.
4. **Aplicar em lote pequeno** — editar poucas aulas por vez, preservando
   frontmatter, tags e convenções de navegação do curso; validar entre lotes.
5. **Validar** — `npm run validate` cobre wikilinks, metadados, navegação,
   quizzes e roteamento; um curso alterado sem validação não está pronto.
6. **Evidenciar** — fechar com: o que mudou (paths), qual item da rubrica cada
   mudança atende e a saída do validador.

## Guardrails (herdam as regras de biblioteca do `AGENTS.md`)

- Cursos são **autocontidos**: links de um curso resolvem dentro da própria pasta.
- **Não mover nem renomear** aulas canônicas sem atualizar os validadores em
  `dev/courses/` — os contadores de aulas/módulos são verificados.
- Quizzes têm gabarito **balanceado por posição** (o validador confere); ao criar
  questões, distribuir as respostas corretas entre A/B/C/D.
- Sem paths absolutos de máquina; exemplos usam paths relativos deste repo.
- Captura pessoal continua em `notas/` — melhorar o canônico não é despejar
  anotações de estudo nele.
- Nada de push/publicação sem pedido explícito do usuário.

## Fontes canônicas da rodada

- Regras de biblioteca: `AGENTS.md`
- Hub de trilhas e matriz método ↔ squads: `cursos/README.md`
- Validadores: `dev/validate.py` + `dev/courses/<slug>/{manifest.yaml,checks.py}` via `npm run validate`
- Existência e maturidade de assets citados: `catalog.json`
- Pontes: `cursos/AIOX Advanced/ponte/` · `cursos/AIOX-Advanced-Squads/ponte/`
