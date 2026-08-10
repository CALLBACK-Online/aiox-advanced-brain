---
type: template
template: context-brief
course: obsidian-ia
status: canonical
tags: [curso/obsidian-ia, segundo-cerebro, context-brief]
---

# Template canônico de Context Brief

Este arquivo pertence ao curso. Não o copie inteiro: o frontmatter acima identifica a fonte canônica. Crie uma nota em `notas/inbox/` — depois do primeiro uso descrito em `notas/README.md` — ou no vault pessoal indicado e copie somente o bloco abaixo.

## Template copiável

```markdown
---
type: context-brief
status: draft
created: YYYY-MM-DD
tags: [aiox, context-brief]
---

# Context Brief — {missão}

## Missão

**Transformação observável:** {o que precisa mudar}

**Destino:** {próximo curso/aula ou projeto não sensível; sem path absoluto}

## Contexto recuperado

- Fonte: `cursos/…/….md` — {qual decisão ou restrição esta fonte sustenta}
- Nota/MOC pessoal: {link ou nome} — {síntese necessária para executar}

Inclua somente contexto relevante. O agent da próxima etapa ou do projeto pode não ter acesso ao vault, então não dependa apenas dos links.

## Decisões e restrições

- Decisão já tomada: {…}
- Preservar: {…}
- Evitar: {…}
- Fora de escopo: {…}

## Mecanismo escolhido

- Tipo: {curso/aula | skill | squad | prompt genérico confirmado}
- Destino ou asset: `{id ou path relativo}`
- Maturidade: {não se aplica | portable | runtime-aiox | study | partial}
- Por que serve: {sinais objetivos}
- Por que não o vizinho: {fronteira}

## Handoff à próxima etapa

- Contexto transferido: {este briefing + anexos mínimos}
- Asset a copiar: {nenhum na rota de estudo; somente se necessário e com destino confirmado na rota operacional}
- Runtime disponível: {não se aplica | Codex | Claude Code | outro}
- Superfície de ativação confirmada: {não se aplica | skill | agent | comando | prompt genérico}
- Permissões ou credenciais necessárias: {nenhuma ou listar sem valores}

## Critérios de aceite

- [ ] {resultado observável 1}
- [ ] {resultado observável 2}

## Evidência esperada

- Artefato: {arquivo, relatório, teste ou outra saída verificável}
- Validação: {comando ou inspeção objetiva apropriada}

## Retorno ao segundo cérebro

- Resultado: {preencher depois da execução}
- Evidência obtida: {artefato + validação}
- Decisão final: {mantida, alterada ou descartada}
- Aprendizado reutilizável: {1–3 frases}
- Próximo passo: {uma ação}
```
