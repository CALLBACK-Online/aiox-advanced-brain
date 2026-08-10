---
type: agent-guide
course: aiox-design
status: canonical
canonical_scope: cursos/AIOX-Design
---

# AGENT-GUIDE — AIOX Design

## Algoritmo obrigatório

1. Classificar: dúvida de **critério visual** (este curso) vs **ativar squad** (Squads 13–15) vs **método SDC** (Advanced).
2. Abrir a aula pelo sintoma (tabela abaixo).
3. Exigir exercício/evidência; não declarar “pronto” sem artefato.
4. Citar paths `skills/` e `squads/` deste repo; declarar maturidade do catalog.
5. Não inventar CLI/runtime; este vault é biblioteca.

## Formato mínimo

```text
Aula: {path em cursos/AIOX-Design/aulas/}
Resultado esperado: {1 frase}
Exercício: {o da aula ou adaptação}
Ponte: {Squads / Advanced / skill}
Evidência: {o que a pessoa deve mostrar}
```

## Roteamento por intenção

| Intenção | Aula |
|----------|------|
| IA inventa cor/layout | `aulas/01-design-system-e-decisao.md`, `03-design-md-contrato.md` |
| Legado visual bagunçado | `aulas/02-design-system-greenfield-brownfield.md`, `05-tokens-componentes-anti-drift.md` |
| Como escrever DESIGN.md | `aulas/03-design-md-contrato.md` |
| Nomear componentes | `aulas/04-taxonomia-atomica.md` |
| Stack Tailwind/ShadCN | `aulas/06-stack-tailwind-shadcn-storybook.md` |
| Variantes / a11y | `aulas/07-storybook-variantes.md` |
| Review de PR de UI | `aulas/08-portao-qualidade-visual.md` |
| Qual squad/skill | `aulas/09-skill-vs-squad-design.md` |
| Fechar ciclo | `aulas/10-capstone-contrato-e-componente.md` |

## Falhas seguras

| Situação | Atitude |
|----------|---------|
| Pediu só Figma | Redirecionar: contrato + decisão; não simular curso de Figma |
| Quer “rodar design-ops agora” | Ponte Squads 15 + copiar pacote; maturidade study/partial |
| Quer polish | `impeccable` depois do portão (aula 08) |
| Sem produto | Usar cenário agenda da aula 10 |

[⌂ Curso](README.md)
