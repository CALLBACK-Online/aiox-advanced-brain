---
type: agent-guide
course: aiox-advanced-squads
status: canonical
canonical_scope: cursos/AIOX-Advanced-Squads
supported_runtimes: [claude-code, codex, generic-prompt]
---

# Guia dos agentes para os squads

[⌂ Curso](README.md) · [Manifesto](agent-router.json) · [Mapa humano](Mapa-de-decisao.md) · [Execução](Guia-de-execucao.md)

## Contrato

Ao receber uma necessidade em linguagem natural, o agente deve identificar o squad adequado sem exigir que o usuário conheça o catálogo. O [manifesto](agent-router.json) contém 24 rotas com `signals`, `anti_signals`, `aliases`, skill opcional, agente de entrada, inputs, deliverable, evidence, limits e `generic_prompt`.

## Algoritmo obrigatório

1. Extrair verbo principal, objeto, estado atual e entrega desejada.
2. Ler `Mapa-de-decisao.md` como índice curto e obter uma ou duas rotas candidatas.
3. Consultar somente as candidatas em `agent-router.json`; não selecionar apenas por memória ou pelo nome do squad.
4. Comparar sinais e anti-sinais das rotas mais próximas.
5. Abrir a aula indicada e confirmar `Quando usar — e quando não usar`.
6. Se a ambiguidade mudar a entrega, fazer uma pergunta curta. Caso contrário, declarar a hipótese e avançar.
7. Verificar no projeto se existem o squad, a skill e o agente de entrada.
8. Pedir apenas os campos ausentes do briefing.
9. Informar maturidade e dependências antes de propor execução.
10. Usar somente sintaxe confirmada pelo runtime; caso contrário, usar o prompt genérico.
11. Exigir briefing, decision-log, deliverable e validation como evidência final.

## Formato mínimo da resposta

```text
Squad escolhido: {id}
Por quê: {sinais encontrados}
Não escolhi {vizinho}: {fronteira}
Maturidade: {study|partial} — {impacto}
Falta no briefing: {somente dados essenciais ausentes}
Ativação segura: {skill confirmada ou prompt genérico}
Evidência esperada: {artefato + gate}
```

## Runtime

### Codex

Forneça este guia e `agent-router.json` como contexto, ou instale `$aiox-squads`. Não assuma que `@agent`, `*comando` ou `/comando` são superfícies executáveis.

### Claude Code

Instale `$aiox-squads` no diretório de skills do projeto ou forneça este guia e `agent-router.json` como contexto. Só use `@agent`, `*comando` ou `/comando` depois de verificar seu registro.

### Outro agente

Use este prompt junto com esta pasta:

```text
Leia AGENT-GUIDE.md e agent-router.json. Para a missão abaixo, escolha uma das 24 rotas, confira o anti-escopo na aula indicada, explique a fronteira com o squad vizinho, peça apenas o briefing ausente e use o prompt genérico se o runtime não possuir uma integração confirmada.

Missão: {descreva a necessidade}
```

## Falhas seguras

- Squad ausente: orientar a cópia de `squads/<id>/`; não fingir ativação.
- Skill ausente: usar o prompt genérico e o agente de entrada existente.
- Agente de entrada ausente: reportar drift do acervo e não inventar substituto.
- Credencial ou escrita externa: parar antes do efeito e pedir autorização.
- Maturidade `study`: orientar e estudar a anatomia; não prometer execução autônoma.
- Maturidade `partial`: enumerar as dependências que precisam existir no destino.

## Exemplos de descoberta

- “Meu agente entra em loops e depende demais de mim.” → `agent-autonomy`.
- “Quero extrair regras do brownfield, não mapear toda a arquitetura.” → `domain-decoder`.
- “O processo já está validado e quero materializá-lo no ClickUp.” → `clickup-ops-squad`.
- “Quero criar tokens e componentes.” → `design-system`.
- “O design system já existe e preciso impedir drift.” → `design-ops`.

Esses casos e a cobertura 1:1 estão em `_tools/routing-evals.json` e são verificados por `npm run validate` (validador estrutural + `validate-agent-routing.mjs`). A prova opcional em sessões limpas dos runtimes é executada, na raiz do repositório, com `npm run smoke:routing:runtimes`.
