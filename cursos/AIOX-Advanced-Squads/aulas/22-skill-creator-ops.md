---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: skill-creator-ops
lesson_position: 22
title: "Skill Creator Ops — ciclo de vida de skills"
squad: skill-creator-ops
agents: 3
tasks: 9
workflows: 1
module: M5
sequence: M5.1
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, skill-creator-ops, layer/curso, curso/squads, squad/skill-creator-ops]
maturity: partial
---

# Skill Creator Ops — ciclo de vida de skills

> Vault: [[squads/skill-creator-ops/README|skill-creator-ops]] · [[skills/skill-creator-ops/SKILL|skill-creator-ops]] · [[cursos/MOC-Squads]]

[← Hormozi](21-hormozi.md) · [↑ M5](../modulos/M5-metacapacidades.md) · [⌂ Curso](../README.md) · [→ Squad Creator](23-squad-creator.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `23-o-que-e-um-squad` no **AIOX Advanced**. Para skill como primitivo, use `cursos/AIOX-Agent-Engineering/aulas/02-taxonomia-da-capacidade.md`, `13-reuse-adapt-create.md` e `14-triagem-de-squad.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/skill-creator-ops/`
- config: `squads/skill-creator-ops/config.yaml`
- agentes: `squads/skill-creator-ops/agents/`
- tasks: `squads/skill-creator-ops/tasks/`
- workflows: `squads/skill-creator-ops/workflows/`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/skill-creator-ops /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **3 agentes**, **9 tasks**, **1 workflows**.

## Quando usar — e quando não usar

**Use quando:** criar, validar, testar, migrar e aposentar skills com padrão.

**Não use quando:** criar um squad multi-agente (use Squad Creator). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`skill-ops-chief`** (`squads/skill-creator-ops/agents/skill-ops-chief.md`).

```text
@skill-ops-chief
# ou, se a skill de entrada estiver instalada:
# $ skill-creator-ops

*help
```

Agentes (amostra): `skill-ops-chief`, `skill-tester`, `skill-validator`

Tasks (amostra): `audit-registry`, `init-skill`, `migrate-skill-to-47`, `package-skill`, `retire-skill`, `test-execution-pipeline`, `test-skill`, `validate-skill-prompt-quality`

Workflows (amostra): `skill-lifecycle`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad skill-creator-ops de squads/skill-creator-ops/.
Siga o config.yaml e o orquestrador skill-ops-chief.
Missão: <descreva>.
```

## Execução guiada

1. **Confirme o fit** com o mapa de decisão e o anti-escopo acima.
2. **Cole o briefing** (modelo abaixo) e peça confirmação de rota.
3. **Deixe o chief rotear** para o especialista/task; não pule o diagnóstico.
4. **Exija artefatos intermediários** (plano, hipótese, estrutura) antes do polimento.
5. **Aplique o gate** da missão (checklist, score, revisão ou smoke).
6. **Registre evidência**: briefing, decision-log, deliverable, validation.
7. **Só então** publique, envie ou grave em sistema externo — se autorizado.

## Briefing copiável

```text
Use o squad skill-creator-ops (Skill Creator Ops).

Objetivo: {mudança observável}
Estado atual: {o que existe hoje}
Entradas: {arquivos, dados, links, decisões}
Público: {quem usa a saída}
Restrições: {prazo, stack, marca, segurança}
Saída esperada: {artefato e formato}
Critérios de aceite:
1. {teste objetivo 1}
2. {teste objetivo 2}
3. {teste objetivo 3}
Fora de escopo: {o que não mexer}

Antes de executar: confirme rota, dependências ausentes e qualquer efeito externo.
Leia squads/skill-creator-ops/config.yaml e adote a persona de skill-ops-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Seu projeto acumulou 14 skills em `.claude/skills/` e ninguém sabe quais ainda funcionam. A missão: auditar o ciclo de vida do conjunto rodando `audit-registry` para levantar o inventário completo e depois `validate-skill` nas cinco mais usadas, registrando por skill um veredito: manter, migrar ou aposentar.

**Saída esperada:** um relatório de auditoria com inventário e status por skill (ativa, obsoleta, quebrada), resultado de validação com pendências objetivas e o veredito registrado skill a skill, com justificativa.

**Erro comum neste squad:** validar só o SKILL.md e nunca executar a skill — ela “passa” na leitura e quebra no primeiro uso real. Detecte cedo exigindo uma execução de teste registrada antes de marcar qualquer skill como ativa.

> **Teste rápido**: sorteie uma skill marcada como “ativa” no relatório — deve existir evidência de execução, não só frontmatter válido.
