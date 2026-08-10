---
type: lesson
course: aiox-advanced-squads
course_title: AIOX Advanced Squads
lesson_id: copy
lesson_position: 19
title: "Copy — peças de alta conversão"
squad: copy
agents: 27
tasks: 86
workflows: 18
module: M4
sequence: M4.2
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
reading_minutes: 14
tags: [curso/aiox-advanced-squads, squad, copy, layer/curso, curso/squads, squad/copy]
maturity: partial
---

# Copy — peças de alta conversão

> Vault: [[squads/copy/README|copy]] · [[skills/copy/SKILL|copy]] · [[cursos/MOC-Squads]]

[← Conteúdo](18-conteudo.md) · [↑ M4](../modulos/M4-aquisicao-conteudo-vendas.md) · [⌂ Curso](../README.md) · [→ Sales](20-sales.md)

## Pré-requisito no AIOX Advanced

Antes de operar este squad, use `cursos/AIOX-Productizacao/` para decidir wedge, oferta e dor/ROI. Copy começa depois dessa decisão.

Mapa completo: `ponte/pre-requisitos-advanced.md`. Hub das trilhas: `cursos/README.md`.

## Onde está neste repositório

Este acervo é uma **biblioteca de distribuição**. O squad **não** roda “dentro” da pasta `cursos/`; você estuda aqui e **copia** o pacote para o seu projeto.

- pasta do squad: `squads/copy/`
- config: `squads/copy/config.yaml`
- agentes: `squads/copy/agents/`
- tasks: `squads/copy/tasks/`
- workflows: `squads/copy/workflows/`
- skill de entrada (opcional): `skills/copy/SKILL.md`
- inventário: `catalog.json` → squads

Para instalar no seu projeto:

```bash
cp -R squads/copy /caminho/do/seu-projeto/squads/
# se houver skill de entrada:
# cp -R skills/<nome> /caminho/do/seu-projeto/.claude/skills/
```

## Resultado

Saber **quando** chamar este squad, **como** ativá-lo, **que entrada** preparar e **que evidência** exigir. Snapshot atual no acervo: **27 agentes**, **86 tasks**, **18 workflows**.

## Quando usar — e quando não usar

**Use quando:** páginas, e-mails, VSL, scripts e frameworks de copywriters.

**Não use quando:** posicionamento de marca inteiro ou negociação comercial ao vivo. Se a missão for menor, prefira uma skill isolada; se for maior e multi-domínio, combine squads em sequência (mapa de decisão do curso).

## Prepare a entrada

- objetivo observável (o que muda no mundo real);
- estado atual e artefatos disponíveis;
- restrições (prazo, marca, stack, compliance, orçamento);
- formato de saída e critérios de aceite;
- o que **não** deve ser alterado;
- se haverá efeito externo (ClickUp, deploy, e-mail, banco): confirme autoridade antes.

## Como ativar

Orquestrador típico: **`copy-chief`** (`squads/copy/agents/copy-chief.md`).

```text
@copy-chief
# ou, se a skill de entrada estiver instalada:
# $ copy

*help
```

Agentes (amostra): `alex-hormozi`, `andre-chaperon`, `ben-settle`, `claude-hopkins`, `clayton-makepeace`, `copy-chief`, `copy-ops-worker`, `dan-kennedy` … (+2)

Tasks (amostra): `analyze-mental-conversation`, `apply-sugarman-triggers`, `audit-copy-hopkins`, `audit-landing-page`, `avatar-research`, `blend`, `briefing`, `create-book-funnel`

Workflows (amostra): `map-generated-quality-gates`, `map-generated-workflow-definition`, `wf-1-full-launch`, `wf-10-webinar-cold-weekly`, `wf-11-ghosted-recovery`, `wf-2-paid-traffic`, `wf-3-high-ticket`, `wf-4-organic-content`

Se o runtime não tiver o slash/`@` registrado, abra o `SKILL.md` ou o agent chief e peça explicitamente:

```text
Carregue o squad copy de squads/copy/.
Siga o config.yaml e o orquestrador copy-chief.
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
Use o squad copy (Copy).

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
Leia squads/copy/config.yaml e adote a persona de copy-chief.
```

## Evidência de conclusão

- artefato no formato pedido;
- critérios de aceite verificáveis (não “ficou bom”);
- premissas e limites declarados;
- próximo passo ou handoff para outro squad/skill, se couber.

## O que muda no AIOX Enterprise

Aqui, a qualidade da peça depende do contexto que você montar no briefing. No Enterprise, o Copy Squad lê primeiro oferta, marca, movimento e processo comercial do workspace. Sem o brief de campanha obrigatório, a produção fica bloqueada.

**O ganho prático:** a copy não começa de um prompt vazio nem avança com uma promessa sem base. A mesma verdade comercial acompanha anúncios, páginas, e-mails e handoffs, com um gate que protege a campanha da pressa.

## Limites neste acervo

Este repositório **não** é o monorepo de produção. Alguns fluxos esperam runtime AIOX, tools ou credenciais no **seu** projeto. Estude a anatomia aqui; execute com dependências resolvidas no destino. Não invente integrações que este pacote não oferece; confira dependências e maturidade no projeto de destino.

## Prática

Sua página de captura converte 1,8% com tráfego pago frio e a promessa atual — “o método completo” — não fala com dor nenhuma. A missão: reescrever a landing page com **um** ângulo dominante (dor de tempo, não de dinheiro), extraído de `avatar-research`, e só considerar a peça pronta depois de passá-la por `audit-landing-page`. Headline, lead e CTA devem derivar do mesmo ângulo, sem misturar promessas.

**Saída esperada:** uma landing page completa em markdown com o ângulo declarado no topo do documento, headline com 3 variações que atacam a mesma dor e o relatório do audit anexado, com score e pendências resolvidas.

**Erro comum neste squad:** misturar dois ângulos na mesma peça (“economize tempo E multiplique receita”) — ela fica média em tudo e não converte em nada. Detecte cedo: se headline e primeiro parágrafo não couberem na mesma frase de dor, o ângulo já se partiu.

> **Teste rápido**: leia só a headline e o CTA — se os dois apontam para a mesma promessa específica, o ângulo sobreviveu.
