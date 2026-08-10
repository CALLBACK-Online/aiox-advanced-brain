---
type: sources
course: aiox-fundamentals
status: canonical
canonical_scope: cursos/AIOX-Fundamentals
---

# Fontes técnicas

O curso usa o AIOX Core no commit `a68bd88f45e560f606e9bdc8a0f663570bdcef88`, pacote `@aiox-squads/core` 5.2.9.

A lista auditável de arquivos e hashes está em [sources/SOURCE-MANIFEST.yaml](sources/SOURCE-MANIFEST.yaml).

## Prioridade de fontes

Quando documentos do snapshot divergem:

1. `.aiox-core/constitution.md` e `AGENTS.md` governam princípios e autoridade.
2. A definição em `.aiox-core/development/agents/<id>.md` governa papel, comandos e limites do agent.
3. `package.json` e `bin/aiox.js` governam pacote, versão e CLI.
4. `README.md` e `docs/getting-started.md` orientam instalação e first-value.
5. Guias e fluxos explicam cenários, mas não criam comandos ausentes.

## Cobertura

| Tema | Fonte principal |
|---|---|
| identidade e CLI First | `README.md`, `AGENTS.md`, Constitution |
| instalação e doctor | `README.md`, Getting Started, Quick Start, `bin/aiox.js` |
| anatomia do core | Core Architecture, Source Tree, `core-config.yaml` |
| 12 agents | definições em `.aiox-core/development/agents/` |
| granularidade e squads | tasks, workflows, Squad Creator e Squads Guide |
| greenfield/brownfield | workflows correspondentes |
| ciclo da story | Story Development Cycle e definições SM/PO/Dev/QA/DevOps |
| qualidade e autoridade | Constitution, Git Workflow e definições dos agents |

## Limite epistemológico

O curso não transforma exemplos de documentação em garantia universal. Sintaxe de ativação e projeções variam por IDE; a instalação atual e a ajuda exposta pelo agent são a confirmação final.

Recursos do AIOX Pro ficaram fora do escopo. Nenhuma credencial, fonte integral ou path absoluto de máquina foi importado.
