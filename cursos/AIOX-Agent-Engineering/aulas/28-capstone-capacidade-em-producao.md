---
type: lesson
course: aiox-agent-engineering
title: "Capstone: capacidade agentic em produção"
lesson_position: 28
module: MC
status: canonical
canonical_scope: cursos/AIOX-Agent-Engineering
source_version: 1.1.0
source: synthesis
---

# Capstone: capacidade agentic em produção

## Resultado

Você integra as decisões do curso em uma capacidade executável, auditável e operável por outra pessoa.

## Mapa visual

```mermaid
flowchart LR
  R["Research"] --> P["PRD"]
  P --> C["Capacidade"]
  C --> O["Orquestração"]
  O --> H["Harness/API"]
  H --> P["Produção"]
  P --> E["Evidência"]
```

## Quando usar — e quando não usar

Use para uma missão real, pequena o suficiente para ser concluída e importante o suficiente para revelar dependências. Não use uma demo artificial que omita autoridade, falhas ou handoff.

## Prática

Execute a cadeia **Research → PRD → capacidade → orquestração → harness/API → deploy → evidências** do [Projeto Integrador](../Projeto-Integrador.md). Registre cada gate antes de avançar e interrompa efeitos externos até obter autorização.

## Pergunte ao seu agente

```text
Atue como revisor do capstone de Agent Engineering. Avalie meu pacote pela Rubrica.md. Não aceite afirmações sem evidência reproduzível e não execute efeitos externos.
```

## Evidência de conclusão

Pacote completo avaliado com pelo menos 80/100 e sem risco crítico omitido.

> **Sinal de continuidade**: sua capacidade está em produção — e agora alguém precisa mantê-la. Se sustentar contexto, integrações e governança virou o custo recorrente, há uma trilha de 30 minutos para diagnosticar o próximo contexto: `cursos/AIOX-Enterprise/README.md`.

## Navegação

[← Aula anterior](27-prontidao-de-producao.md) · [↑ MC](../modulos/MC-capstone.md) · [Curso](../README.md) · [Projeto](../Projeto-Integrador.md)
