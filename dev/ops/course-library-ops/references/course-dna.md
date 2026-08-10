# DNA reverso dos cursos

## Atualizar a leitura

```bash
python3 dev/ops/course-library-ops/scripts/analyze_courses.py
python3 dev/ops/course-library-ops/scripts/analyze_courses.py \
  --course cursos/<Curso> --format json
```

O relatório dinâmico é a verdade do filesystem. A matriz registra o baseline
que originou esta skill e explica diferenças intencionais.

## Baseline observado

| Curso | Aulas | Perfil dominante | Assinatura |
|---|---:|---|---|
| Obsidian + IA | 8 | aplicado curto | uso/não uso, prática, evidência |
| Introdução à Arquitetura | 24 | fundacional | mapa visual, modelo mental, caso, prática |
| AIOX Fundamentals | 12 | técnico-operacional | objetivo, contexto, erro, recuperação, snapshot |
| AIOX Advanced | 28 | migração profunda | mapa, modelos, decisão/operação, portão, origem |
| Advanced Squads | 25 | catálogo/roteamento | fit, entrada, ativação, briefing, maturidade |
| Agent Engineering | 28 | migração profunda | mapa, origem curricular, operação e portão |
| AIOX Design | 20 | decisório/aplicado | mapa visual, caso, âncora, prática, evidência |
| Productização | 6 | decisório | mapa, casos, portão, registro epistemológico |
| Enterprise | 7 | preview protegido | cenário, mudança, limite e diagnóstico |

Não transformar o baseline em meta de tamanho. Promessa, dependências e
performance terminal determinam a quantidade de aulas.

## Pipeline comum real

```text
prior art + fontes
  → gap/brief aprovado
  → performance terminal + rubrica
  → outline e rastreabilidade
  → aulas em lotes
  → avaliações/capstone
  → README + agente + pontes
  → harness específico
  → catálogo/jornada
  → validação global + relatório
```

`docs/producao-cursos/` preserva decisões editoriais; `dev/courses/` preserva
a prova. Recriar apenas `cursos/` perde memória operacional.

## Invariantes

1. **Backward design:** estado depois e artefato terminal precedem assuntos.
2. **Uma progressão, vários perfis:** não há heading universal nos nove cursos.
3. **Evidência > consumo:** prática, portão, diagnóstico ou artefato fecha a unidade.
4. **Anti-escopo explícito:** fronteiras impedem duplicação entre trilhas.
5. **Rastreabilidade proporcional:** hash/commit para snapshot, `source_path`
   para migração e bibliografia para síntese pública.
6. **Síntese, não dump:** transcrições alimentam processos e casos sem cópia integral.
7. **Duplo consumo:** README atende pessoa; AGENT-GUIDE atende agente quando necessário.
8. **Autocontenção:** a unidade distribuída não depende do bastidor.
9. **Validação específica:** cada curso protege seu risco dominante.
10. **Desvio registrado:** exceção aparece com razão e mitigação.

## Variações legítimas

- `curriculum.yaml` só quando identidade machine-readable ou duração/ordem são
  fonte canônica.
- Glossário, mapa, templates, pontes e material de cohort só quando ajudam uma
  decisão ou evidência real.
- Preview pode usar diagnóstico em vez de quiz/capstone sem prometer formação.
- Migração pode preservar profundidade; curso novo não herda verbosidade.
- Wikilinks históricos podem permanecer; novos cursos preferem Markdown relativo.

## Anti-padrões encontrados

- Substituir termos em curso obsoleto sem reconstruir o modelo.
- Comprimir uma fonte e remover a performance terminal.
- Rebaixar execução real a bônus quando ela é a prova central.
- Misturar engenharia, oferta, design e catálogo de especialistas.
- Prometer aulas inexistentes no README.
- Usar inventário de features como pedagogia.
- Validar só links/contagens e ignorar o risco específico.
- Vazar brief, scripts ou relatório para a superfície do aluno.
