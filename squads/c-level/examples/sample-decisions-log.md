# Advisory Board — Decisions Log

> Registro append-only de todas as decisoes do board.
> NAO editar entradas antigas. Apenas adicionar novas no topo.
> Para atualizacao de status/outcome, adicionar FOLLOW-UP referenciando a decisao original.

---

<!-- TEMPLATE PARA NOVA ENTRADA (copiar e preencher):

## [{YYYY-MM-DD}] {Titulo da Decisao}

- **Tipo**: go | no-go | go-com-condicoes | adiar
- **Sessao**: {link para session-record}
- **Advisors**: {IDs dos advisors que participaram}
- **Decisao**: {frase clara e acionavel}
- **Confianca**: {1-10}
- **Riscos aceitos**: {riscos explicitos que o board aceitou}
- **Condicoes** (se aplicavel): {condicoes que devem ser verdade}
- **Revisao**: {data para reavaliar}
- **Status**: pendente | em-execucao | concluido | revisado | revertido
- **Outcome** (preencher depois): {o que de fato aconteceu}

-->

## [2026-03-16] PRD Slides Creator Squad — GO-COM-CONDICOES (Simplificacao Drastica)

- **Tipo**: go-com-condicoes
- **Sessao**: `sessions/2026-03-16-prd-slides-creator/session-record.md`
- **Advisors**: ab-01, ab-02, ab-04, ab-06, ab-10
- **Decisao**: GO-COM-CONDICOES para versao DRASTICAMENTE simplificada do PRD-SLIDES-001. NAO implementar o PRD como esta (6 agents, 8 data files, pipeline 6 fases). Substituir por abordagem incremental: (1) Validar MCP + python-pptx no ambiente em 1-2 dias, (2) Se funcionar, criar 1 agent unico "slide-maker" que usa SOP-SLIDES-001 como contexto direto, (3) Testar com 3 briefings reais, (4) Adicionar segundo agent (qa-inspector) apenas se resultados justificarem. Preservar: taxonomia 11 tipos, constraints por modo, JSON schema OutlineItem, conceito PPTEval. Descartar: 6 agents separados, 8 data files YAML (duplicacao do SOP), template-curator, visual-scout, Fase 3 inteira, dados de mercado irrelevantes para ferramenta interna.
- **Confianca**: 8.5
- **Riscos aceitos**: Abordagem "1 agent primeiro" pode ser mais lenta se demanda se provar alta; qualidade limitada comparada a 6 agents especializados; validacao de MCP pode falhar
- **Condicoes**: MCP funciona no macOS e gera slides com qualidade >= 7/10; demanda real confirmada (CEO responde 3 perguntas de ab-10); uso >= 2x/semana nas primeiras 2 semanas; qualidade percebida >= 70% da manual
- **Revisao**: 4 semanas apos inicio da Fase 1, ou imediatamente se MCP falhar
- **Status**: pendente
- **Outcome**: (preencher depois)

---

## [2026-02-24] Pos-Call Diego/Bernardo — Posicao Comprometida, Acao Imediata

- **Tipo**: no-go (reafirmacao com urgencia)
- **Sessao**: `sessions/2026-02-24-reavaliacao-diego-monteiro-proposta3/post-call-deliberation.md`
- **Advisors**: ab-01, ab-02, ab-06, ab-09
- **Decisao**: POSICAO COMPROMETIDA — ACAO IMEDIATA REQUERIDA. Call executou 70% do roteiro mas falhou no fechamento: Bloco Bernardo ignorado (PIOR: delegou redacao ao Bernardo), take-it-or-leave-it abandonado, proximos passos delegados, sem deadline. Diego concordou verbalmente com tudo e imediatamente contra-propôs 50/50 no variavel. Diego trabalha sem contrato. Bernardo continua minimizando. Board reafirma NO-GO e exige: (1) mensagem a Diego pausando atividades HOJE, (2) advogado proprio AMANHA, (3) Bernardo NAO redige, (4) draft do contrato do advogado do CEO ate quarta, (5) deadline de 48h pra Diego, (6) se contra-propor, encerrar.
- **Confianca**: 9.5 (mais alta de todas as sessoes — comportamentos na call confirmaram TODAS as previsoes do board)
- **Riscos identificados**: Diego trabalhando sem contrato = sociedade de fato + risco CLT (R$200-400k); Bernardo redigindo = perda de controle; ausencia de deadline = posicao degrada; Diego interpreta espaco pra negociar
- **Condicoes de recuperacao**: Mensagem escrita hoje; advogado proprio amanha; Bernardo fora da redacao; contrato redigido pelo advogado do CEO; termos originais nao-negociaveis
- **Revisao**: Resposta de Diego ao contrato do advogado do CEO
- **Status**: pendente — urgencia CRITICA
- **Outcome**: (preencher depois)

---

## [2026-02-24] Reavaliacao Parceria Diego Monteiro (Monet) — Proposta 3

- **Tipo**: no-go
- **Sessao**: `sessions/2026-02-24-reavaliacao-diego-monteiro-proposta3/session-record.md`
- **Advisors**: ab-01, ab-02, ab-03, ab-06, ab-09
- **Decisao**: NO-GO para Proposta 3 (SCP, earn-out 50%, fusao em dezembro). Proposta reembala problemas da Proposta 2 com sofisticacao juridica. O "ativo Thiago" (audiencia, marca, lista 80k, distribuicao) e o ativo central nao precificado. Diego nao traz ativos unicos (tecnologia, base propria, capital). Alternativa oferecida: contrato de servicos R$15-20k/mes + bonus 5-10% incremental, zero equity, Monet encerrada, advogado proprio, fusao removida. Se Diego rejeitar, encerrar.
- **Confianca**: 9.0 (acima de 8.5 da sessao anterior — dados novos confirmaram e agravaram analise)
- **Riscos aceitos**: Diego pode se afastar permanentemente; custo de oportunidade se Diego genuinamente pudesse acelerar (board avalia como improvavel); Bernardo pode interpretar como desconfianca
- **Condicoes** (se contra-proposta apresentada): Diego aceitar TODOS os termos; Monet encerrada (nao suspensa); advogado independente do Thiago; baseline de receita documentado; board review em 90 dias
- **Revisao**: Imediatamente apos resposta de Diego, ou 90 dias se aceitar
- **Status**: em-execucao (call realizada 24/02 noite, ver post-call-deliberation.md)
- **Outcome**: CEO executou call com roteiro. 70% seguido, falha no fechamento (Bernardo, take-it-or-leave-it, deadline). Sessao pos-call convocada. Ver decisao acima.

---

## [2026-02-19] Parceria Diego Monteiro (Monet) — Furion & Hotplay

- **Tipo**: go-com-condicoes
- **Sessao**: `sessions/2026-02-19-parceria-diego-monteiro/session-record.md`
- **Advisors**: ab-02, ab-03, ab-05, ab-06, ab-09
- **Decisao**: NO-GO para Proposta 2 (50% cashflow, zero investimento). Apresentar contra-proposta com: 1 produto apenas, Monet suspensa, zero equity por 12 meses, fee de performance 10-15%, NDA/IP Assignment/Non-compete antes do dia 1, SPV isolado, milestones binarios 30/60/90 dias, termino unilateral em 90 dias. Se Diego rejeitar termos, confirma ausencia de skin in the game.
- **Confianca**: 8.5
- **Riscos aceitos**: Diego pode rejeitar e relacao terminar; custo de oportunidade de 3-6 meses; risco residual de absorção de processos
- **Condicoes**: Diego aceitar termos; Monet suspensa documentalmente; protecoes juridicas assinadas ANTES de acesso a informacao; milestones objetivos definidos
- **Revisao**: 30 dias apos apresentacao da contra-proposta a Diego
- **Status**: revisado (superada pela sessao 2026-02-24)
- **Outcome**: Diego apresentou Proposta 3 em reuniao com Bernardo Gribel. Proposta nao atendeu contra-proposta do board (Monet mantida, 50% mantido, fusao adicionada). Board reavaliou com confianca elevada (9.0) e emitiu NO-GO mais forte.
