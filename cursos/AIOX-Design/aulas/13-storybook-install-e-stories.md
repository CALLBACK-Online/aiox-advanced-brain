---
type: lesson
course: aiox-design
course_title: AIOX Design
lesson_id: storybook-install-e-stories
lesson_position: 13
title: "Instalar Storybook e gerar stories vivas"
module: M3
sequence: M3.3
status: canonical
canonical_scope: cursos/AIOX-Design
reading_minutes: 26
tags: [curso/aiox-design, lesson, layer/curso]
---

# Instalar Storybook e gerar stories vivas

[⌂ Curso](../README.md) · [↑ M3](../modulos/M3.md) · [← Anterior](12-stack-tailwind-shadcn-storybook.md) · [Próxima →](14-storybook-variantes.md)

## Resultado

Você instala Storybook (ou documenta bloqueio real) e publica ao menos uma story de átomo.

## Mapa visual

```mermaid
flowchart LR
  App["App front"] --> SB["Storybook"] --> ST["Stories"] --> EV["Evidência local"]
```

## Quando usar — e quando não usar

**Use** quando o contrato mínimo já existe.

**Não use** para pular DESIGN.md.

## Resultado prático

Ao final você tem (ou documenta o bloqueio real de ambiente com evidência): Storybook **instalado** no repo de front e **pelo menos 1 story** de um átomo (Button ou equivalente).

## Sequência (conceito)

1. App front existente ou scaffold mínimo (Vite/Next + React, ou o stack do seu projeto).  
2. Adicionar Storybook compatível com a stack.  
3. Gerar/escrever story do átomo canônico.  
4. Rodar localmente e capturar evidência (URL local + print ou log).

Comandos exatos variam por stack — use a documentação da sua versão; o curso exige o **resultado**, não um vendor lock de CLI.

## Tema de casa das lives

Na T1 de Design System, o exercício de casa era **ter o Storybook com o design system materializado** — não um PDF de tokens. Esta aula restaura esse portão.

## Âncora no acervo

Aula 12 (stack). Skills/squads de design quando for operar em escala.

## Prática

1. Rode Storybook local **ou** registre bloqueio (Node ausente, monorepo, etc.) com passo que falta.  
2. Se rodou: 1 story de Button com default + disabled.

## Pergunte ao seu agente

```text
No meu repo (descrevo stack), planeje a instalação do Storybook em passos mínimos e a primeira story do Button alinhada ao DESIGN.md. Não invente tokens.
```

## Evidência de conclusão

Print/log de Storybook rodando **ou** bloqueio de ambiente documentado (não conta como Done do capstone, mas fecha a aula com honestidade).

## Navegação

[⌂ Curso](../README.md) · [↑ M3](../modulos/M3.md) · [← Anterior](12-stack-tailwind-shadcn-storybook.md) · [Próxima →](14-storybook-variantes.md)
