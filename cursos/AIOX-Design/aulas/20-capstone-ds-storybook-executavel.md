---
type: lesson
course: aiox-design
course_title: AIOX Design
lesson_id: capstone-ds-storybook-executavel
lesson_position: 20
title: "Capstone: materializar o DS no Storybook"
module: M5
sequence: M5.2
status: canonical
canonical_scope: cursos/AIOX-Design
reading_minutes: 35
seed: integração 01–09
tags: [curso/aiox-design, lesson, layer/curso]
---

# Capstone: materializar o DS no Storybook

[⌂ Curso](../README.md) · [↑ M5](../modulos/M5.md) · [← Anterior](19-skill-vs-squad-design.md) · → fim

[⌂ Curso](../README.md) · [↑ M3](../modulos/M3.md) · [← Anterior](19-skill-vs-squad-design.md) · → Capstone/fim

## Resultado

Você entrega um pacote mínimo: briefing, DESIGN.md utilizável, spec de 1 componente, matriz de variantes, rota operacional e autocrítica — sem inventar runtime.

## Mapa visual

```mermaid
flowchart LR
  B["Briefing"] --> D["DESIGN.md"]
  D --> C["Spec componente"]
  C --> V["Matriz variantes"]
  V --> R["Rota skill/squad"]
  R --> E["Evidência + limites"]
```

## Quando usar — e quando não usar

**Use** para fechar o curso ou para destravar UI de um projeto real em um ciclo curto.

**Não use** para prometer Storybook + Chromatic + 40 componentes no mesmo dia.

## Pacote de entrega

1. **Briefing** (5–10 linhas): usuário, tela/feature, restrições.
2. **DESIGN.md** (mínimo do curso, coerente).
3. **Spec do componente:** nome, camada taxonômica, props/variantes, REUSE/ADAPT/CREATE.
4. **Matriz de variantes** (mesmo se só documental).
5. **Rota operacional:** skill/squad + maturidade + o que copiar.
6. **Autocrítica:** o que falta para produção.

## Definition of Done (capstone)

- Contrato legível por agente
- Zero falha crítica da [Rubrica](../Rubrica.md)
- Anti-escopo de operação honesto
- Storybook rodando = **obrigatório** (local)


## Âncora no acervo

- Contrato: `skills/design-md/SKILL.md` (validar/manter DESIGN.md no projeto destino).
- Construir biblioteca: `squads/design-system/` · governar: `squads/design-ops/` · marca: `squads/brand/`.
- Craft pós-gate: `skills/impeccable/SKILL.md`.
- Hub deste curso: [README](../README.md) · operação com briefing: `cursos/AIOX-Advanced-Squads/aulas/14-design-system.md` e `15-design-ops.md` (paths monoespaçados; curso irmão).

## Prática

Execute o pacote acima no **seu** produto (ou no cenário: “app de agenda — tela de novo evento + Button primário e secondary”).

Salve em `notas/` (não sobrescreva aulas canônicas).


## Pergunte ao seu agente

```text
Vou colar meu pacote de capstone AIOX Design. Avalie pela rubrica do curso (contrato, taxonomia, variantes, portão vs craft, rota operacional, clareza). Nota por critério e falhas críticas. Não reescreva tudo — diga o menor patch para passar.
```

## Evidência de conclusão

Pacote completo em `notas/` + autoavaliação com nota estimada por critério da rubrica.


## Definition of Done (capstone v2)

1. DESIGN.md utilizável.  
2. Pelo menos 1 átomo e 1 molécula no catálogo.  
3. **Storybook local rodando** com stories das variantes mínimas.  
4. Um ciclo screenshot→correção documentado.  
5. Rota skill/squad + anti-escopo.  

**Bloqueio de ambiente** (sem Node/app): não é Done — registre o bloqueio e o próximo passo técnico. Chromatic/CI visual permanece opcional.

## Navegação

[⌂ Curso](../README.md) · [↑ M5](../modulos/M5.md) · [← Anterior](19-skill-vs-squad-design.md) · → fim

[⌂ Curso](../README.md) · [↑ M3](../modulos/M3.md) · [← Anterior](19-skill-vs-squad-design.md) · → Capstone/fim
