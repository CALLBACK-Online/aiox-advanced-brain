---
type: assessment
course: aiox-fundamentals
assessment_id: projeto-primeiro-ciclo-aiox
title: Primeiro ciclo AIOX com evidência
status: canonical
canonical_scope: cursos/AIOX-Fundamentals
---

# Projeto final — Primeiro ciclo AIOX com evidência

> Entrega: conduzir uma mudança pequena e reversível num projeto de prática.

## Missão

Escolha uma alteração que caiba em até 60 minutos de execução. Exemplos: corrigir texto com teste de link, exibir versão no rodapé, adicionar validação simples a um campo ou reparar um teste quebrado conhecido.

Não use produção, dados reais, push, deploy ou migração remota. O projeto avalia o ciclo local.

## Etapas

1. **Contexto:** monte o context pack da aula 2.1.
2. **Rota:** escolha os agents e a menor unidade de execução.
3. **Story:** escreva resultado, critérios, tarefas, file scope, fora do escopo e validação.
4. **Autoridade:** indique quem prepara, valida, implementa e revisa.
5. **Execução:** implemente somente se o projeto e o ambiente forem seus e a ação estiver autorizada.
6. **Gates:** execute checks proporcionais ao risco.
7. **Evidência:** relacione cada critério à respectiva prova.
8. **Handoff:** registre estado, limitações e próximo passo.

## Pacote de entrega

    01-contexto.md
    02-rota.md
    03-story.md
    04-evidencias.md
    05-handoff.md

Os nomes são sugestivos. Os cinco conteúdos podem viver numa única nota se permanecerem claramente separados.

## Definition of Done

- contexto contém fontes locais e hipóteses marcadas;
- rota respeita autoridade;
- story possui pelo menos três critérios verificáveis;
- alteração, se executada, permanece dentro do escopo;
- comandos e resultados foram registrados;
- falhas ou checks não executados aparecem explicitamente;
- handoff permite retomada sem a conversa original;
- nenhum segredo ou path absoluto de máquina aparece no pacote.

## Quando não executar

Pare na story e no plano de evidência se:

- o projeto não é seu;
- a mudança exige credencial ausente;
- há efeito externo não autorizado;
- a ação é destrutiva;
- o contexto não permite determinar o comportamento correto.

Uma parada segura bem documentada pode atender ao projeto melhor que uma mutação imprudente.

## Avaliação

Use a [rubrica](final-project-rubric.md). Aprovação: 14 de 20 pontos, sem nota zero em autoridade/segurança ou evidência.

## Próximo passo

Se você foi aprovado e consegue repetir o ciclo sem seguir a receita, avance para o [AIOX Advanced](../../AIOX%20Advanced/README.md). Se contexto, roteamento ou evidência ainda dependem de assistência, revise o módulo correspondente e execute outra mudança pequena antes de avançar.
