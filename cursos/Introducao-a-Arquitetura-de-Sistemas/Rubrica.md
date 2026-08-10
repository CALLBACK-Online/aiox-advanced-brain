---
type: rubric
course: introducao-arquitetura-sistemas
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
---

# Rubrica — Arquitetura explicável

Pontue cada dimensão de 0 a 2.

| Dimensão | 0 | 1 | 2 |
|----------|---|---|---|
| Fronteira | sistema sem limite | componentes listados | dentro/fora e dependências explícitos |
| Fluxo | lista de caixas | caminho parcial | request, estado, assíncrono e conclusão rastreáveis |
| Dados | “tem banco” | entidades sem dono | fonte de verdade, ciclo e derivados claros |
| Comunicação | tudo vira API | mecanismos nomeados | síncrono/assíncrono escolhido por necessidade |
| Execução | etapas vagas | executor parcial | tasks, workers, pipeline e convergência definidos |
| Confiabilidade | só caminho feliz | alguns retries | timeouts, idempotência e falha degradada coerentes |
| Operação | “ter logs” | sinais genéricos | pergunta operacional ligada a log/métrica/trace/gate |
| Segurança | login como resposta total | identidade e acesso | autorização, secrets e isolamento no limite correto |
| Agentic | “colocar IA” | tools e prompt | autonomia, memória, gates e humano com autoridade claros |
| Trade-offs | tecnologia por moda | custo citado | alternativa, motivo e gatilho de revisão explícitos |

## Veredito

- **16–20:** pronto para revisão técnica e planejamento.
- **11–15:** arquitetura compreensível, mas ainda há riscos sem dono.
- **0–10:** volte ao mapa; mais componentes não corrigem fundamento ausente.

Nenhuma nota aprova efeitos externos. Deploy, banco, credenciais e dados reais continuam exigindo autorização e validação no projeto destino.
