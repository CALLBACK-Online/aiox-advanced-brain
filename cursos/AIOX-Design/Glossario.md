---
type: glossary
course: aiox-design
status: canonical
canonical_scope: cursos/AIOX-Design
---

# Glossário — AIOX Design

| Termo | Definição de trabalho |
|-------|----------------------|
| **Atomic Design (Brad Frost)** | Taxonomia átomo → molécula → organismo → template → página; base da aula 10 |
| **Token** | Decisão visual registrada como valor reutilizável |
| **DESIGN.md** | Contrato visual lido pela IA antes de gerar UI |
| **Repertório** | Conjunto curado de referências + proibições |
| **Tema visual** | Aparência pontual de uma superfície/campanha |
| **Design system** | Decisões herdáveis (token, componente, regra) |
| **Top-down / bottom-up** | Rotas de construção do DS |
| **Drift** | UI fora do contrato sem atualização deliberada |
| **Storybook SoT** | Catálogo vivo como fonte da verdade |
| **Story** | Explicação viva de um componente/variante |
| **AI-look** | Estética genérica de modelo sem restrição |
| **AI-slop** | Estado extremo do AI-look: UI genérica descartável, sem decisão própria |
| **Base / override** | Núcleo compartilhado vs variação por produto |
| **Portão visual** | Critério que bloqueia “pronto” sem conformidade |
| **Craft / impeccable** | Polimento depois da conformidade |
| **Greenfield / brownfield (design)** | Sem UI em produção vs produto vivo com decisões visuais acumuladas |
| **Brownfield implícito** | Produto no ar sem DS declarado — o padrão vive espalhado nas telas; primeira ação é inventário |
| **Brownfield com DS** | Produto com DS existente — o problema é drift e governança, não recomeço |
| **UI kit** | Pacote de peças visuais prontas sem regra de uso — aparência sem contrato |
| **Biblioteca (de componentes)** | Código reutilizável de componentes; vira DS quando carrega tokens e regras |
| **Decision record** | Registro curto de uma decisão visual: alternativas comparadas, escolha e porquê |
| **Contrato de publicação** | O que o catálogo declara por componente: status, API pública, variantes, tokens, a11y e owner |
| **Estados de catálogo** | `experimental` / `canonical` / `deprecated` / `internal` — visão mínima do ciclo CANDIDATE→…→DEPRECATED do squad design-system |
| **RACI** | Matriz de autoridade: Responsável, Aprovador, Consultado, Informado |
| **Mini-RFC** | Proposta curta de mudança no DS: problema, proposta, evidência, owner, versão, migração, rollback |
| **Foundations** | Camada base compartilhada do DS multi-produto (= core); tema e extensão derivam dela |
| **Matriz de render** | Tabela estado × viewport/tema com a captura provada de cada célula |
| **Baseline (visual)** | Captura aprovada que serve de referência na comparação de regressão |
| **Waiver** | Exceção registrada a um portão: finding aceito temporariamente com dono e prazo |

[⌂ Curso](README.md)
