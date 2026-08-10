---
type: course-bridge
course: aiox-design
status: canonical
canonical_scope: cursos/AIOX-Design
tags: [ponte, brand, design]
---

# Ponte — Brand Book → contrato visual

[⌂ Curso](../README.md)

## Fronteira

| Camada | Dono | Entrega |
|--------|------|---------|
| Marca estratégica (posicionamento, voz, narrativa) | `squads/brand/` · aula Squads `13-brand.md` | Brand book / diretrizes de marca |
| Tradução visual para IA e código | **AIOX Design (este curso)** | Tokens, DESIGN.md, componentes, Storybook |
| Construir / governar biblioteca no tempo | `squads/design-system/` · `design-ops` | Registry, auditoria, a11y |

## Handoff mínimo (brand → Design)

```yaml
marca:
  princípios: []
  cores_semanticas: []      # primary, danger… não só hex solto
  tipografia: []
  o_que_nao_e_a_marca: []
  referencias_visuais: []   # links ou pastas de repertório
  restricoes: []            # ex.: sem gradiente neon
```

Se o YAML não fecha, volte ao brand squad ou complete repertório (Pinterest/referências) **antes** de pedir UI à IA.

## O que este curso faz com o handoff

1. Promove decisões a **tokens** e proibições no DESIGN.md.
2. Classifica componentes na taxonomia.
3. Materializa prova no Storybook (aulas 11–14 + capstone 20).
4. Define governança: quem altera token vs quem só compõe tela.

## O que **não** misturar

- Vender “design system” como SaaS sem Decision Pack → `cursos/AIOX-Productizacao/`.
- Orquestração/harness → Agent Engineering.
- Brand book sem tokens → ainda não é contrato legível por agente.

## Onde isso vive na trilha

Brand Book → tokens → Storybook percorre **M0–M3** e fecha no capstone executável (aula 20 + [Rubrica](../Rubrica.md)).
