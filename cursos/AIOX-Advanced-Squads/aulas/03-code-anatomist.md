---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: code-anatomist
lesson_position: 3
title: "Code Anatomist — engenharia reversa completa"
squad: code-anatomist
agents: 12
tasks: 10
workflows: 3
module: M0
sequence: M0.3
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, code-anatomist, layer/curso, curso/squads, squad/code-anatomist]
maturity: partial
---

# Code Anatomist — engenharia reversa completa

> Vault: [[squads/code-anatomist/README|code-anatomist]] · [[skills/code-anatomist/SKILL|code-anatomist]] · [[cursos/MOC-Squads]]

[← Research](02-research.md) · [↑ M0](../modulos/M0-escolha-pesquisa-dominio.md) · [⌂ Curso](../README.md) · [→ Domain Decoder](04-domain-decoder.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, revise `31-brownfield-discovery` e `53-brownfield-enhancement` no **AIOX Advanced**. Para aprofundar engenharia reversa, use `cursos/AIOX-Agent-Engineering/aulas/10-code-anatomy-e-domain-decoder.md`.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/code-anatomist/`
- config: `squads/code-anatomist/config.yaml`
- agentes: `squads/code-anatomist/agents/`
- tasks: `squads/code-anatomist/tasks/`
- workflows: `squads/code-anatomist/workflows/`
- skill de entrada (opcional): `skills/code-anatomist/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/code-anatomist /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **12 agentes**, **10 tasks**, **3 workflows**.

## Quando usar — e quando não usar

**Use quando:** entender arquitetura, APIs, dados e infra de um codebase inteiro.

**Não use quando:** só extrair regras de domínio escondidas (use Domain Decoder). Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`decoder-chief`** (`squads/code-anatomist/agents/decoder-chief.md`).

```text
@decoder-chief
# ou, se a skill de entrada estiver instalada:
# $ code-anatomist

*help
```

Agentes (amostra): `barbara-von-halle`, `data-specialist`, `decoder-chief`, `eric-evans`, `gail-murphy`, `graham-witt`, `james-taylor`, `martin-fowler` … (+2)

Tasks (amostra): `adopt`, `audit`, `characterize-legacy`, `classify-rules`, `compare`, `express-rules`, `extract-rules`, `map-domain`

Workflows (amostra): `wf-extract-rules`, `wf-multi-compare`, `wf-standardize-rules`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad code-anatomist de squads/code-anatomist/.
Siga o config.yaml e o orquestrador decoder-chief.
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
Use o squad code-anatomist (Code Anatomist).

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
Leia squads/code-anatomist/config.yaml e adote a persona de decoder-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Pegue um repositório real que você **não** escreveu — um open-source que você usa ou um legado da empresa — e peça o mapa completo do sistema. Rode `characterize-legacy` para o diagnóstico inicial de saúde e depois `map-domain` para levantar módulos, fronteiras e fluxos de dados. O objetivo não é opinar sobre o código: é produzir um mapa que um dev novo usaria na primeira semana.

**Saída esperada:** dossiê de anatomia com (1) módulos e dependências entre eles enumerados, (2) pontos de entrada (APIs, jobs, CLIs) com caminho de arquivo para cada um, (3) riscos e áreas sem teste marcados explicitamente.

**Erro comum neste squad:** descrever a arquitetura *idealizada* — a que a documentação promete — em vez da real. Detecte cedo: peça o caminho de arquivo de três afirmações do mapa; se alguma não apontar para código existente, o mapa está sendo inventado.

> **Teste rápido**: abra dois arquivos citados no dossiê e confirme que fazem o que o mapa diz; um mapa que não sobrevive a essa amostragem não é anatomia, é ficção.
