# Pipeline de produção

## Gate 0 — Baseline, modo e autorização

1. Ler instruções, hub e catálogo.
2. Rodar o validador antes de editar; registrar falhas preexistentes.
3. Classificar `greenfield`, `brownfield`, `migration` ou `preview`.
4. Confirmar prior art, responsabilidade na jornada e vizinhos.
5. Confirmar autoridade para fontes restritas, publicação e efeitos externos.

Saída: id, pasta, modo, responsabilidade, baseline e limites.

## Gate 1 — Engenharia reversa

Executar `scripts/analyze_courses.py` no alvo e em 1–3 vizinhos. Inspecionar
bastidor, proveniência, checks e histórico Git. Registrar:

1. invariantes que precisam sobreviver;
2. diferenças intencionais;
3. dívida/gaps que não devem ser clonados.

Saída: diagnóstico, perfil sugerido e riscos dominantes.

## Gate 2 — Fonte e fronteira epistemológica

Montar ledger:

```text
claim/competência | fonte primária | versão/commit | uso permitido | destino
```

- fonte primária para comandos, APIs e comportamento técnico;
- commit/versão/hash quando a exatidão depende de snapshot;
- seed → aula em migração;
- síntese de lives/transcrições sem dump integral;
- fato, hipótese, desconhecido e material não publicável separados;
- lacuna de fonte não é preenchida por memória.

Saída: fontes, proveniência e, quando necessário, SOURCE-MANIFEST.

## Gate 3 — Brief, gap e aprovação

Criar no bastidor `COURSE-BRIEF.md`, `gap-analysis.md` para brownfield/migration
e `deviations.yaml` para gate pulado/herdado. Registrar aprovação humana pelo
contrato `references/approval-protocol.md`; o agente não inventa `approved_by`.
Ambiguidade material bloqueia outline e aulas.

Saída: brief aprovado ou bloqueio explícito.

## Gate 4 — Backward design

1. Escrever capstone e rubrica em rascunho quando o perfil os exigir.
2. Decompor a performance terminal em evidências por módulo.
3. Decompor cada evidência em competências atômicas.
4. Ordenar dependências cognitivas.
5. Criar outline com ids, fonte, evidência e avaliação.
6. Escolher arquétipo e árvore de artefatos.
7. Registrar aprovação humana do `course-outline.md` antes do scaffold ou da
   primeira edição brownfield.

Teste: remover uma aula deve enfraquecer evidência ou pré-condição. Se não,
ela é decorativa. Se exige duas performances independentes, dividir.

Saída: fonte → objetivo → aula → evidência → avaliação → capstone, com outline aprovado.

## Gate 5 — Materialização em lotes

Produzir navegação mínima, um módulo e seu checkpoint. Para cada aula:

1. frontmatter consumido pelo curso/harness;
2. resultado observável;
3. mecanismo, modelo ou decisão;
4. cenário e limite;
5. prática, artefato ou diagnóstico;
6. fonte e navegação;
7. auditoria pela rubrica `skills/teach/SKILL.md` quando disponível; fallback
   operacional em `checklists/didactic-rubric.md`.

Validar a cada 3–4 aulas ou módulo. Corrigir padrão antes de replicá-lo.

Saída: lotes verdes.

## Gate 6 — Avaliação e transferência

- Quiz: cenário, rationale, transferência e balanceamento A/B/C/D.
- Módulo: checkpoint ligado ao entregável intermediário.
- Capstone: reutiliza entregáveis e exige execução/decisão real quando prometida.
- Rubrica: critérios, pesos/níveis, falhas críticas e evidência aceitável.
- Preview: diagnóstico substitui certificação; não inventar score oficial.

Saída: avaliação alinhada à performance terminal.

## Gate 7 — Consumo e integração

Completar somente artefatos condicionais úteis. Integrar:

- `catalog.json` e `learning_journey`;
- `cursos/README.md` e MOCs relevantes;
- `AGENTS.md`/`CLAUDE.md` somente se nasce rota de agente;
- pontes nos dois lados quando a transição é bidirecional;
- `CHANGELOG.md` para mudança visível.

Nunca registrar `course-library-ops` na superfície do aluno.

Saída: curso descobrível sem responsabilidade duplicada.

## Gate 8 — Harness específico

Criar `dev/courses/<id>/manifest.yaml`. Usar regras declarativas para arquivos,
contagens, links e catálogo. Criar `checks.py` para risco específico:

- sequência/frontmatter e seções do perfil;
- rastreabilidade de fonte;
- cobertura de assets/rotas;
- maturidade/runtime;
- performance terminal;
- fronteira de IP;
- integração à jornada.

Preferir `dev/lib/*`. O harness acumula `ctx.errors`, não chama `sys.exit` e
não lê `docs/`.

```bash
python3 dev/validate.py --course <id>
```

Saída: gate capaz de falhar quando o invariante é violado.

## Gate 9 — Fechamento

1. Rodar `npm run validate`.
2. Verificar placeholders, conflitos, whitespace e paths absolutos.
3. Conferir contagens em todas as SoTs.
4. Atualizar gap, validation-report e deviations no bastidor.
5. Preencher `retrospective.md` no bastidor (template em
   `assets/course-templates/retrospective.md`) quando o fluxo for create,
   upgrade ou improve — captura o que o harness não pegou e candidatos a DNA.
6. Relatar artefatos, perfil, fontes, validações e limites não provados.
7. Opcional: `doctor.py --course <id>` para estado derivado `ready`.

Saída: `EXIT 0` e pacote reproduzível. Sem isso, estado é draft/blocked/failed,
nunca “pronto”.
