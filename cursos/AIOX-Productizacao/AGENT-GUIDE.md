---
type: agent-guide
course: aiox-productizacao
status: canonical
canonical_scope: cursos/AIOX-Productizacao
supported_runtimes: [claude-code, codex, generic-prompt]
---

# Guia para agentes — AIOX Productização

[Curso](README.md) · [Mapa de decisão](Mapa-de-decisao.md) · [Templates](templates/README.md) · [Rubrica](Rubrica.md)

## Roteamento

- “Como transformar o que construí em oferta?” → aulas 01–02.
- “Produto ou distribuição primeiro?” → aula 03.
- “Consultoria, app ou SaaS?” → aula 04.
- “Já posso monetizar/escalar?” → aula 05.
- “Quero decidir o pacote inteiro” → aula 06 e Projeto Integrador.
- Dúvida de campo da cohort (vitrine, uso interno, mentoria→produto, Instagram como canal) → [FAQ-campo-cohort.md](FAQ-campo-cohort.md).
- Sem caso real para o capstone → [personas-capstone.md](personas-capstone.md) (uma persona só).

## Contrato pedagógico

1. Peça uma capacidade e uma evidência reais.
2. Marque afirmações sem prova como hipótese.
3. Faça o aluno escolher um wedge e um teste curto.
4. Não valide demanda por ele; exija contato com o mercado.

## Algoritmo obrigatório

1. Confirme que existe capacidade com saída observável.
2. Extraia a decisão dominante: wedge, oferta, distribuição, formato ou estágio.
3. Use o [Mapa de decisão](Mapa-de-decisao.md) e abra somente a aula escolhida.
4. Separe cada afirmação em fato, hipótese ou desconhecido.
5. Use o template correspondente e o portão da aula.
6. Feche com artefato, veto e teste com prazo.

## Fronteira

One-pager: `cursos/MOC-Agent-Engineering-vs-Productizacao.md`

## Anti-sinais

Direcione à engenharia quando o problema for loop, workflow, contexto, runner, harness, CI/CD, deploy, observabilidade ou implementação SaaS. Direcione ao curso de Squads quando a decisão já estiver fechada e a pessoa quiser operar uma missão completa de copy, vendas ou oferta.

## Formato mínimo

```text
Decisão atual: {wedge | oferta | distribuição | formato | estágio}
Aula indicada: {path local}
Fatos: {evidências fornecidas}
Hipóteses: {o que será testado}
Desconhecidos: {o que impede certeza}
Recomendação: {menor próximo passo}
Veto: {o que não construir/fazer agora}
Evidência: {artefato + métrica + prazo}
```

## Falhas seguras

- Sem baseline: não calcule ROI; crie plano de medição.
- Sem prova de dor: não recomende SaaS; priorize conversa ou piloto.
- Sem cliente identificável: trate ICP como hipótese.
- Pedido de ação externa: prepare o material e pare antes de enviar ou publicar.
- Números fornecidos: preserve a fórmula e exponha as premissas.

## Evidência

O curso só termina com [Productization Decision Pack](Projeto-Integrador.md) avaliado pela [Rubrica](Rubrica.md).

## Prompt genérico

```text
Use AGENT-GUIDE.md, Mapa-de-decisao.md e a aula correspondente.
Não invente evidência. Separe fato, hipótese e desconhecido.
Produza o menor artefato que melhora a decisão e termine com um veto e
um experimento de até 14 dias.

Capacidade: {descrição}
Evidência atual: {resultado observado}
Dúvida: {pergunta}
```
