---
type: lesson
course: aiox-design
course_title: AIOX Design
lesson_id: repertorio-e-referencias
lesson_position: 3
title: "Repertório e referências antes da IA"
module: M0
sequence: M0.3
status: canonical
canonical_scope: cursos/AIOX-Design
reading_minutes: 22
tags: [curso/aiox-design, lesson, layer/curso]
---

# Repertório e referências antes da IA

[⌂ Curso](../README.md) · [↑ M0](../modulos/M0.md) · [← Anterior](02-design-system-greenfield-brownfield.md) · [Próxima →](04-tema-visual-vs-design-system.md)

## Resultado

Você monta um repertório curado e anota padrões/proibições **antes** de pedir UI à IA.

## Mapa visual

```mermaid
flowchart LR
  R["Referências"] --> N["Notas padrão/proibição"] --> P["Prompt restrito"] --> U["UI"]
```

## Quando usar — e quando não usar

**Use** antes de qualquer geração de UI.

**Não use** como desculpa para adiar o contrato: repertório sem DESIGN.md ainda vira moda.

## A mudança de pergunta

Sem repertório, o prompt é “faz uma tela moderna”. Com repertório, o prompt é “componha a partir **destas** referências e **destes** tokens — e não invente o resto”.

| Entrada | Efeito na IA |
|---------|----------------|
| Zero referência | UI genérica / AI-look |
| Moodboard vago | Mistura estilos sem critério |
| Pasta curada (5–15 peças) + notas | Consistência e direção |

## Processo mínimo de repertório

1. **Definir o contexto de uso** (quem olha, em que dispositivo, que tom).
2. **Coletar referências** (Pinterest, sites, apps, prints) — qualidade > quantidade.
3. **Anotar o que copiar** (ritmo, densidade, hierarquia) e o que **proibir**.
4. **Só então** pedir geração ou componente à IA.

## Caso rápido (live)

Nas aulas de Design do Advanced, o fluxo recomendado a quem está de primeira viagem era: pesquisar referências e cores → criar pastas de referência → **depois** gerar. Pedir “bonito” sem pasta de referência era o caminho mais rápido para o genérico.

## Âncora no acervo

Repertório alimenta o contrato (`DESIGN.md`) e o Brand Book. Marca estratégica: `squads/brand/`. Tradução visual: este curso e `ponte/brand-book-para-contrato.md`.

## Prática

Crie uma pasta `repertorio/` (no seu projeto ou em `notas/`) com **8 referências** e, para cada uma, uma linha: *ritmo / densidade / o que NÃO copiar*.

## Pergunte ao seu agente

```text
Vou descrever 8 referências visuais. Ajude a extrair padrões reutilizáveis (hierarquia, densidade, cor semântica) e 5 proibições. Não gere tela ainda. Não invente tokens que eu não aprovei.
```

## Evidência de conclusão

Pasta com 8 referências + notas de padrão/proibição. Você passou se consegue gerar um prompt de UI **sem** a palavra “moderno” genérica.

## Navegação

[⌂ Curso](../README.md) · [↑ M0](../modulos/M0.md) · [← Anterior](02-design-system-greenfield-brownfield.md) · [Próxima →](04-tema-visual-vs-design-system.md)
