---
type: project
course: aiox-agent-engineering
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
---

# Projeto Integrador — capacidade agentic em produção

## Cadeia obrigatória

```text
Research → PRD → capacidade → orquestração → harness/API → deploy → evidências
```

Cada seta é um gate: a saída anterior deve existir e ser validada antes da próxima etapa.

## Entrega

Escolha uma unidade real de processo e entregue:

1. **M0 — Arquitetura:** entidade, estados, pipeline, unidade por etapa e contratos.
2. **M1 — Research:** dossiê de decisão e prior art que termina em PRD executável.
3. **M2 — Capacidade:** squad mínimo — reutilizado, adaptado ou criado — executando uma unidade real de processo.
4. **M3 — Orquestração:** dependências, sequência/paralelismo, routing, fan-in e wall-clock medidos.
5. **M4 — Runtime:** runner, harness ou API com schema, logs e smoke reproduzível.
6. **M5 — Produção:** URL funcional, pipeline, readiness e rollback; ou bloqueio externo diagnosticado sem declaração falsa de deploy.
7. **Pacote de evidências:** decision log, comandos/execuções relevantes, resultados dos gates, limitações e handoff.

## Restrições

- Não execute efeitos externos sem autorização.
- Não use mais agentes do que a dependência exige.
- Não declare produção sem evidência de runtime e reversibilidade.
- Não invente URL, credencial, comando ou integração ausente no projeto destino.

## Aprovação

Use a [Rubrica](Rubrica.md). Mínimo: 80/100 e nenhuma omissão crítica de segurança, autoridade ou rollback.
