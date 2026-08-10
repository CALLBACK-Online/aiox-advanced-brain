---
type: lesson
course: introducao-arquitetura-sistemas
lesson_id: monolito-modulos-microsservicos
lesson_position: 21
module: M7
sequence: M7.3
status: canonical
canonical_scope: cursos/Introducao-a-Arquitetura-de-Sistemas
difficulty: foundation
source_refs: [azure-architecture-styles, azure-microservices]
---

# Monólito, módulos, microsserviços e acoplamento

## Resultado

Você escolhe fronteiras pela mudança e pelo domínio, começando pela arquitetura operacionalmente mais simples que atende à necessidade.

## Mapa visual

```text
Monólito modular
┌──────────────────────────────┐
│ pedidos │ cobrança │ suporte │  um deploy, módulos explícitos
└──────────────────────────────┘

Microsserviços
[pedidos] ↔ API/eventos ↔ [cobrança] ↔ [suporte]
deploy e dados independentes, operação distribuída
```

## Modelo mental

**Monólito** é implantado como uma unidade. Pode ser organizado ou caótico. **Monólito modular** mantém fronteiras internas, contratos e ownership sem pagar desde cedo o custo da rede.

**Microsserviço** é uma capacidade de negócio autônoma, implantável de forma independente e dona de seus dados. Separar pastas ou criar endpoints não produz autonomia.

**Acoplamento** mede quanto uma parte depende de detalhes ou mudanças de outra. **Coesão** mede quanto responsabilidades que mudam juntas estão juntas. O objetivo é baixo acoplamento e alta coesão, independentemente do estilo.

## Quando usar — e quando não usar

Comece modular. Considere separar serviço quando existe fronteira de domínio estável, necessidade real de deploy/escala independente e maturidade para operar rede, consistência, tracing e versões.

Não escolha microsserviços por currículo ou tamanho de empresa imaginado. Não compartilhe banco e bibliotecas internas de forma que todo serviço precise mudar junto. Não confunda “monólito” com “ruim”: um monólito modular pode ser a arquitetura correta por anos.

## Caso rápido

Cobrança pode virar serviço quando possui equipe, regras, disponibilidade e ritmo de mudança próprios. Se pedidos precisa consultar cinco vezes o banco de cobrança para renderizar uma tela, as fronteiras estão acopladas e a rede só tornou o problema mais caro.

Anti-padrão: monólito distribuído — vários deploys, uma base compartilhada e mudanças coordenadas obrigatórias.

## Prática

Agrupe capacidades do seu sistema por coisas que mudam juntas. Desenhe primeiro módulos. Para cada candidato a serviço, prove: autonomia de dados, deploy, escala, owner e benefício maior que o custo operacional.

## Pergunte ao seu agente

```text
Revise estas fronteiras sem assumir microsserviços. Avalie coesão, acoplamento, ownership, dados, deploy, escala e maturidade operacional. Proponha monólito modular como baseline e só extraia serviço com evidência.
```

## Evidência de conclusão

Decisão arquitetural com alternativa simples, custo distribuído explícito e gatilhos mensuráveis para futura separação.

Fontes: [Azure — Architecture styles](https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/) e [Microservices](https://learn.microsoft.com/en-us/azure/architecture/microservices/).

[Anterior](20-multitenancy-isolamento-rls.md) · [Quiz M7](../avaliacoes/Quiz-M7-seguranca-e-fronteiras.md) · [Próxima: agentes](22-modelo-contexto-memoria-tool-skill.md)
