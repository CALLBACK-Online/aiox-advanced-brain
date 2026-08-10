---
type: rubric
course: aiox-agent-engineering
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---

# Rubrica — capacidade agentic em produção

## 1. Decisão e research — 20

- 0: solução escolhida sem evidência.
- 10: há fontes, mas não há comparação ou anti-escopo.
- 20: prior art, trade-offs e decisão estão rastreáveis.

## 2. Arquitetura da capacidade — 20

- 0: prompt isolado.
- 10: unidade existe, mas contratos e estados são ambíguos.
- 20: entidade, responsabilidades, contratos e gates são coerentes.

## 3. Orquestração — 20

- 0: paralelismo ou múltiplos modelos sem justificativa.
- 10: execução funciona, mas dependências e limites não estão explícitos.
- 20: DAG, routing, concorrência, stop rules e baseline estão registrados.

## 4. Runtime e produção — 20

- 0: funciona apenas na sessão do autor.
- 10: harness existe, sem smoke, rollback ou observabilidade mínima.
- 20: execução reproduzível, deploy/bloqueio, smoke e rollback comprovados.

## 5. Evidência e handoff — 20

- 0: afirmação sem pacote de evidências.
- 10: evidências parciais ou dependentes do autor.
- 20: outra pessoa consegue reproduzir, auditar limites e continuar.

## Resultado

- 90–100: pronta para operação controlada.
- 80–89: aprovada com ajustes não críticos.
- 60–79: refazer os gates fracos.
- abaixo de 60: retornar à decisão e arquitetura.
