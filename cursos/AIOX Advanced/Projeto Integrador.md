---
type: course-project
course: aiox-advanced
status: canonical
track: essential
module: MC
timebox_minutes: 90
source_version: 1.0.0
canonical_scope: cursos/AIOX Advanced
tags: [curso/aiox-advanced, projeto]
---

# Projeto Integrador — do sinal ao sistema

Eu escolho um problema real e o transformo em um sistema operável. O projeto acompanha o curso inteiro; não é uma prova inventada no final.

## Definição de pronto

O sistema recebe uma entrada real, executa um processo explícito, produz uma saída útil, passa por gates e fica acessível para outra pessoa usar.

## Corrida de 90 minutos

Eu provo uma **fatia vertical mínima**, não tento terminar o produto inteiro. Antes do cronômetro, deixo repositório, acessos e ambiente prontos. Durante os 90 minutos, sigo este orçamento:

1. **0–15 min — Brief e PRD curto:** dor, usuário, outcome, fluxo, fora de escopo e métrica.
2. **15–25 min — 1 a 3 Stories:** cada uma com aceite testável; se o tempo apertar, mantenho apenas uma.
3. **25–65 min — Build:** implemento somente o que ficou `ready`.
4. **65–80 min — Quality Gate:** executo o gate e aplico correções curtas; não invento PASS.
5. **80–88 min — Deploy e smoke:** publico a fatia e provo o caminho feliz.
6. **88–90 min — ROI e retrospectiva:** fecho uma linha de valor e uma mudança para a próxima execução.

Quando o timer aperta, eu corto feature e acabamento. Não corto aceite crítico, Quality Gate ou smoke test.

## Gate 1 — sinal e resultado

Eu registro:

- dor ou oportunidade;
- usuário e contexto;
- baseline de tempo, custo ou qualidade;
- resultado mensurável;
- anti-escopo.

Evidência: artefato do [[modulos/Módulo 0 - Mindset e Princípios|Módulo 0]].

## Gate 2 — arquitetura operacional

Eu defino entidade, estados, agentes, autoridade, contexto e formato dos artefatos.

Evidências: saídas do [[modulos/Módulo 1 - Sistema AIOX|Módulo 1]], [[modulos/Módulo 2 - Setup e Contexto|Módulo 2]] e [[modulos/Módulo 5 - Arquitetura AIOX|Módulo 5]].

## Gate 3 — execução com qualidade

Eu escrevo um PRD curto, quebro o trabalho em uma a três Stories, executo o ciclo e registro o resultado do Quality Gate.

Evidências: [[47-ciclo-de-vida-do-story]], [[48-quality-gate-completo]] e [[20-determinismo-progressivo]].

## Gate 4 — entrega

Eu publico uma versão utilizável, provo o caminho feliz e documento rollback e limites conhecidos.

Evidências: [[71-vercel-deploy]], [[73-prontidao-de-producao]] e [[74-caso-integrado-end-to-end]].

## Gate 5 — valor

Eu comparo o resultado com a baseline e respondo:

- o que ficou mais rápido, barato ou confiável;
- o que ainda depende de mim;
- qual é o próximo gargalo;
- se o sistema merece virar serviço ou produto.

Eu fecho com uma linha explícita: **ROI = valor ou tempo economizado pela fatia − custo de construir e operar**, sempre mostrando a premissa usada.

## Entrega final

1. URL ou execução reproduzível.
2. Repositório ou pacote operacional.
3. Brief e PRD curto.
4. Uma a três Stories com aceite testável.
5. Diagrama do fluxo.
6. Evidências do Quality Gate, deploy e smoke test.
7. Before/after com métrica e uma linha de ROI.
8. Retrospectiva e decisão de próximo passo.

Eu avalio a entrega pela [[Rubrica]].

## Decisão de próximo passo

Depois da entrega, eu respondo com evidência:

1. consigo repetir esse ciclo sem reconstruir o processo do zero?
2. contexto, integrações e gates continuam fáceis de manter quando o número de projetos cresce?
3. meu próximo ganho depende de aprender o método ou de operar sobre uma base já integrada?

Se o limite ainda é competência, volto às aulas e aos squads. Se a entrega funciona, mas a manutenção da base virou o custo dominante, comparo o Advanced com o **AIOX Enterprise** em `JORNADA-AIOX.md` (raiz do repositório; Fundamentals, Advanced ou Enterprise?).

## Navegação

← [[modulos/Módulo C - Capstone|Capstone]] · ↑ [[cursos/AIOX Advanced/README|Curso]] · → [[Rubrica]]
